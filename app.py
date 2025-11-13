from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import random
import json
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Simulação de um banco de dados
# Adicione a chave 'foto' com o caminho da imagem de cada veículo
veiculos = {
    'compactos': [
        {'id': 1, 'nome': 'Fiat Mobi', 'opcionais': ['Ar condicionado', 'Vidros elétricos'], 'valor': 80.00, 'foto': 'mobi.jpg'},
        {'id': 2, 'nome': 'Renault Kwid', 'opcionais': ['Ar condicionado'], 'valor': 75.00, 'foto': 'kwid.jpg'},
    ],
    'suvs': [
        {'id': 3, 'nome': 'Jeep Renegade', 'opcionais': ['Ar condicionado', 'Multimídia', 'Direção elétrica'], 'valor': 150.00, 'foto': 'renegade.jpg'},
        {'id': 4, 'nome': 'Nissan Kicks', 'opcionais': ['Ar condicionado', 'Direção elétrica'], 'valor': 140.00, 'foto': 'kicks.jpg'},
    ],
    'esportivos': [
        {'id': 5, 'nome': 'Ford Mustang', 'opcionais': ['Motor V8', 'Câmbio automático', 'Bancos de couro'], 'valor': 350.00, 'foto': 'mustang.jpg'},
        {'id': 6, 'nome': 'Chevrolet Camaro', 'opcionais': ['Motor V8', 'Teto solar', 'Bancos esportivos'], 'valor': 340.00, 'foto': 'camaro.jpg'},
    ]
}

# Instrumentação mínima: armazenar eventos em memória e em arquivo (JSON lines)
EVENTS_LOG = os.path.join(os.path.dirname(__file__), 'events.log')
events_store = []  # lista em memória (apenas para debug/consulta rápida)
DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

# -----------------------------
# AI helper (FAQ/assistente) – abordagem leve baseada em regras/recuperação
# Tipo: Assistente de FAQ com recomendações simples por atributos.
# Não usa chamadas externas; tudo offline.

AI_KB = [
    {
        'tags': ['preço', 'preco', 'valor', 'custo', 'taxa', 'tarifa', 'desconto'],
        'answer': (
            'Nossas tarifas variam por categoria, disponibilidade e período. '
            'No checkout você vê o preço diário final. Dica: reservas antecipadas '
            'e períodos maiores costumam ter melhor custo-benefício.'
        )
    },
    {
        'tags': ['seguro', 'proteção', 'cobertura', 'franquia'],
        'answer': (
            'Oferecemos opções de proteção com diferentes franquias. '
            'Você pode escolher a cobertura no checkout. Para viagens longas, '
            'recomendamos proteção ampliada.'
        )
    },
    {
        'tags': ['documento', 'habilitação', 'cnh', 'idade'],
        'answer': (
            'É necessário CNH válida e ter mais de 21 anos (ou 18 com taxa jovem, quando aplicável). '
            'Leve um cartão válido no momento da retirada.'
        )
    },
    {
        'tags': ['quilometragem', 'km', 'km livre', 'limite'],
        'answer': (
            'A maioria dos planos possui quilometragem livre. Quando houver limite, '
            'o valor por km excedente estará indicado no checkout.'
        )
    },
    {
        'tags': ['combustível', 'gasolina', 'tanque', 'diesel', 'etanol'],
        'answer': (
            'Política de combustível: devolução com o mesmo nível. '
            'Podemos oferecer pré-pagamento de tanque em algumas localidades.'
        )
    },
    {
        'tags': ['retirada', 'devolução', 'entrega', 'retirar', 'devolver', 'horário'],
        'answer': (
            'Retiradas e devoluções seguem o horário da loja selecionada. '
            'Chegue com alguns minutos de antecedência e traga seus documentos.'
        )
    },
]

def _simple_intent_answer(text: str) -> str:
    """Retorna uma resposta com base em palavras‑chave simples."""
    t = (text or '').lower()
    best = None
    score_best = 0
    for item in AI_KB:
        score = sum(1 for tag in item['tags'] if tag in t)
        if score > score_best:
            score_best = score
            best = item
    if best and score_best > 0:
        return best['answer']
    # fallback
    return (
        'Posso ajudar com preços, proteção/seguro, documentos, quilometragem, combustível '
        'e prazos de retirada/devolução. Você também pode perguntar recomendações de carros.'
    )

def _recommend_by_attributes(context: dict) -> list:
    """Gera recomendações simples por atributos: prioriza alta margem e mesma categoria.
    context pode conter: categoria, orcamento, finalidade ('viagem', 'cidade', 'familia')."""
    categoria = context.get('categoria')
    orcamento = context.get('orcamento')  # valor diário máximo
    finalidade = context.get('finalidade')

    # achatar veículos com categoria
    catalogo = []
    for cat, lista in veiculos.items():
        for v in lista:
            item = dict(v)
            item['_categoria'] = cat
            item['_is_high'] = item.get('valor', 0) >= 150
            catalogo.append(item)

    def score(v):
        s = 0
        # mesma categoria desejada
        if categoria and v['_categoria'] == categoria:
            s += 3
        # alta margem (propósito de negócio)
        if v['_is_high']:
            s += 2
        # orçamento
        if orcamento is not None:
            if v.get('valor') <= orcamento:
                s += 2
            else:
                s -= 2
        # finalidade
        if finalidade:
            if finalidade in ('familia', 'viagem') and v['_categoria'] in ('suvs',):
                s += 2
            if finalidade in ('cidade',) and v['_categoria'] in ('compactos',):
                s += 2
            if finalidade in ('experiência', 'experiencia', 'luxo') and v['_categoria'] in ('esportivos',):
                s += 2
        # preço menor ajuda levemente se dentro do orçamento
        s += max(0, 200 - v.get('valor', 0)) / 200.0
        return s

    ranked = sorted(catalogo, key=score, reverse=True)
    return ranked[:3]


def _get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Inicializa o banco SQLite com tabelas básicas: events e reservations."""
    conn = _get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event_type TEXT,
            veiculo_id INTEGER,
            variant TEXT,
            is_high_margin INTEGER,
            remote_addr TEXT,
            payload TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            veiculo_id INTEGER,
            variant TEXT,
            price REAL,
            margin REAL,
            meta TEXT
        )
    ''')
    conn.commit()
    conn.close()

def _record_event(event: dict):
    """Registra um evento no store em memória e no arquivo `events.log` como JSON lines."""
    event.setdefault('timestamp', datetime.utcnow().isoformat() + 'Z')
    events_store.append(event)
    try:
        with open(EVENTS_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event, ensure_ascii=False) + '\n')
    except Exception:
        # não falhar o app por erro de log
        pass
    # também persiste no SQLite
    try:
        conn = _get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO events (timestamp, event_type, veiculo_id, variant, is_high_margin, remote_addr, payload) VALUES (?,?,?,?,?,?,?)',
            (
                event.get('timestamp'),
                event.get('event_type'),
                event.get('veiculo_id'),
                event.get('variant'),
                1 if event.get('is_high_margin') else 0,
                event.get('remote_addr'),
                json.dumps(event, ensure_ascii=False)
            )
        )
        conn.commit()
        conn.close()
    except Exception:
        # não deixar isso quebrar o fluxo principal
        pass

# (O resto do seu código Flask permanece o mesmo)
@app.route('/')
def index():
    # ...
    # Se você quiser fotos nas categorias, adicione-as aqui também.
    # Exemplo: categorias = {'compactos': {'foto': 'categoria_compactos.jpg'}, 'suvs': {'foto': 'categoria_suvs.jpg'}}
    # e depois ajuste o template index.html para usar isso.
    # Por enquanto, vamos manter a simplicidade e focar nas fotos dos veículos.
    categorias = veiculos.keys()
    return render_template('index.html', categorias=categorias)

@app.route('/categoria/<categoria_nome>')
def ver_categoria(categoria_nome):
    if categoria_nome in veiculos:
        lista_veiculos = veiculos[categoria_nome]
        return render_template('categoria.html', categoria=categoria_nome, veiculos=lista_veiculos)
    else:
        return "Categoria não encontrada", 404

def _assign_variant():
    """Atribui (e retorna) a variante A ou B baseada em cookie ou sorteio 50/50."""
    variant = request.cookies.get('ab_variant')
    if variant in ('A', 'B'):
        return variant
    # atribuição aleatória 50/50
    return 'B' if random.random() < 0.5 else 'A'


@app.route('/checkout/<int:veiculo_id>')
def checkout(veiculo_id):
    veiculo_selecionado = None
    for categoria in veiculos.values():
        for veiculo in categoria:
            if veiculo['id'] == veiculo_id:
                veiculo_selecionado = veiculo
                break
        if veiculo_selecionado:
            break

    if not veiculo_selecionado:
        return "Veículo não encontrado", 404

    # determinar variante A/B e indicar se o veículo é de alta margem
    variant = _assign_variant()
    # heurística simples: veículos com valor diário >= 150 considerados high-margin
    is_high_margin = veiculo_selecionado.get('valor', 0) >= 150

    resp = make_response(render_template('checkout.html', veiculo=veiculo_selecionado, variant=variant, is_high_margin=is_high_margin))
    # setar cookie apenas se ainda não existir (persistir atribuição)
    if not request.cookies.get('ab_variant'):
        resp.set_cookie('ab_variant', variant, max_age=60*60*24*30)  # 30 dias
    return resp



@app.route('/event', methods=['POST'])
def event():
    """Endpoint para receber eventos de instrumentação (view, click, convert).

    Exemplo payload JSON:
    {"event_type": "view", "veiculo_id": 5, "variant": "B", "is_high_margin": true}
    """
    payload = request.get_json(silent=True)
    if not payload or 'event_type' not in payload:
        return jsonify({'error': 'invalid payload'}), 400
    # enrich
    try:
        payload['remote_addr'] = request.remote_addr
    except Exception:
        pass
    _record_event(payload)
    return jsonify({'status': 'ok'})


@app.route('/reserve', methods=['POST'])
def reserve():
    """Simula a conclusão de uma reserva (conversão). Recebe JSON com veiculo_id e variant.
    Registra evento de tipo 'convert' e retorna JSON. (Uso via fetch no front-end.)
    """
    payload = request.get_json(silent=True) or {}
    veiculo_id = payload.get('veiculo_id')
    variant = payload.get('variant') or request.cookies.get('ab_variant')
    # buscar preço do veículo se disponível
    price = None
    margin = None
    for categoria in veiculos.values():
        for v in categoria:
            if v.get('id') == veiculo_id:
                price = v.get('valor')
                # placeholder: margem estimada 20% do preço (substituir por cálculo real)
                margin = round(price * 0.20, 2) if price is not None else None
                break
        if price is not None:
            break

    # inserir reserva no DB
    reservation_id = None
    try:
        conn = _get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO reservations (timestamp, veiculo_id, variant, price, margin, meta) VALUES (?,?,?,?,?,?)',
                    (datetime.utcnow().isoformat() + 'Z', veiculo_id, variant, price, margin, json.dumps(payload, ensure_ascii=False)))
        reservation_id = cur.lastrowid
        conn.commit()
        conn.close()
    except Exception:
        pass

    event = {
        'event_type': 'convert',
        'veiculo_id': veiculo_id,
        'variant': variant,
        'reservation_id': reservation_id,
        'price': price,
        'margin': margin
    }
    _record_event(event)
    return jsonify({'status': 'reserved', 'reservation_id': reservation_id})


@app.route('/events', methods=['GET'])
def events():
    """Rota de debug: retorna eventos do DB (parâmetro opcional ?limit=)."""
    limit = int(request.args.get('limit', 200))
    try:
        conn = _get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT timestamp, event_type, veiculo_id, variant, is_high_margin, remote_addr, payload FROM events ORDER BY id DESC LIMIT ?', (limit,))
        rows = cur.fetchall()
        result = []
        for r in rows:
            try:
                payload = json.loads(r['payload'])
            except Exception:
                payload = None
            result.append({
                'timestamp': r['timestamp'],
                'event_type': r['event_type'],
                'veiculo_id': r['veiculo_id'],
                'variant': r['variant'],
                'is_high_margin': bool(r['is_high_margin']),
                'remote_addr': r['remote_addr'],
                'payload': payload
            })
        conn.close()
        return jsonify(result)
    except Exception:
        # fallback para memória
        return jsonify(list(events_store[-limit:]))


@app.route('/dashboard-summary', methods=['GET'])
def dashboard_summary():
    """Retorna um resumo por variante: views, clicks, converts e taxa de conversão."""
    try:
        conn = _get_db_connection()
        cur = conn.cursor()
        # total por variant e event_type
        cur.execute("SELECT variant, event_type, COUNT(*) as cnt FROM events GROUP BY variant, event_type")
        rows = cur.fetchall()
        summary = {}
        for r in rows:
            variant = r['variant'] or 'unknown'
            event_type = r['event_type']
            cnt = r['cnt']
            summary.setdefault(variant, {})
            summary[variant][event_type] = cnt

        # calcular taxas simples
        for variant, metrics in summary.items():
            views = metrics.get('view', 0)
            converts = metrics.get('convert', 0)
            metrics['conversion_rate'] = (converts / views) if views > 0 else None

        conn.close()
        return jsonify(summary)
    except Exception:
        return jsonify({'error': 'db error'}), 500


@app.route('/ai/ask', methods=['POST'])
def ai_ask():
    """Assistente de IA (FAQ + recomendações simples).
    Payload esperado (JSON): {"question": str, "context": {"categoria": str, "orcamento": float, "finalidade": str}}
    Retorna: {"answer": str, "recommendations": [ {veiculo}, ... ] }
    """
    payload = request.get_json(silent=True) or {}
    question = payload.get('question', '')
    context = payload.get('context') or {}

    # resposta de FAQ
    answer = _simple_intent_answer(question)

    # recomendações (opcional, quando contexto disponível)
    recs = []
    try:
        recs = _recommend_by_attributes(context)
    except Exception:
        recs = []

    # registrar evento de uso do assistente (para métricas)
    _record_event({
        'event_type': 'ai_ask',
        'payload': {'question': question, 'context': context},
        'remote_addr': request.remote_addr
    })

    return jsonify({
        'answer': answer,
        'recommendations': recs
    })

if __name__ == '__main__':
    # inicializar DB (cria tabelas se necessário)
    try:
        init_db()
    except Exception:
        pass
    app.run(debug=True)