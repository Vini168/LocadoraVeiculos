import json
import math

# Events copied from user's message
events = [
  {
    "event_type": "convert",
    "is_high_margin": False,
    "payload": {
      "event_type": "convert",
      "margin": 30,
      "price": 150,
      "reservation_id": 12,
      "timestamp": "2025-11-05T23:20:09.234581Z",
      "variant": "B",
      "veiculo_id": 3
    },
    "remote_addr": None,
    "timestamp": "2025-11-05T23:20:09.234581Z",
    "variant": "B",
    "veiculo_id": 3
  },
  {
    "event_type": "click",
    "is_high_margin": True,
    "payload": {
      "event_type": "click",
      "is_high_margin": True,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T23:20:08.926469Z",
      "variant": "B",
      "veiculo_id": 3
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T23:20:08.926469Z",
    "variant": "B",
    "veiculo_id": 3
  },
  {
    "event_type": "view",
    "is_high_margin": True,
    "payload": {
      "event_type": "view",
      "is_high_margin": True,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T23:20:07.348953Z",
      "variant": "B",
      "veiculo_id": 3
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T23:20:07.348953Z",
    "variant": "B",
    "veiculo_id": 3
  },
  {
    "event_type": "view",
    "is_high_margin": False,
    "payload": {
      "event_type": "view",
      "is_high_margin": False,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T23:11:02.353751Z",
      "variant": "B",
      "veiculo_id": 1
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T23:11:02.353751Z",
    "variant": "B",
    "veiculo_id": 1
  },
  {
    "event_type": "convert",
    "is_high_margin": False,
    "payload": {
      "event_type": "convert",
      "margin": 70,
      "price": 350,
      "reservation_id": 11,
      "timestamp": "2025-11-05T23:10:59.612690Z",
      "variant": "B",
      "veiculo_id": 5
    },
    "remote_addr": None,
    "timestamp": "2025-11-05T23:10:59.612690Z",
    "variant": "B",
    "veiculo_id": 5
  },
  {
    "event_type": "click",
    "is_high_margin": True,
    "payload": {
      "event_type": "click",
      "is_high_margin": True,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T23:10:59.296443Z",
      "variant": "B",
      "veiculo_id": 5
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T23:10:59.296443Z",
    "variant": "B",
    "veiculo_id": 5
  },
  {
    "event_type": "view",
    "is_high_margin": True,
    "payload": {
      "event_type": "view",
      "is_high_margin": True,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T23:10:54.532621Z",
      "variant": "B",
      "veiculo_id": 5
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T23:10:54.532621Z",
    "variant": "B",
    "veiculo_id": 5
  },
  {
    "event_type": "view",
    "is_high_margin": True,
    "payload": {
      "event_type": "view",
      "is_high_margin": True,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T23:08:43.374507Z",
      "variant": "B",
      "veiculo_id": 3
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T23:08:43.374507Z",
    "variant": "B",
    "veiculo_id": 3
  },
  {
    "event_type": "view",
    "is_high_margin": True,
    "payload": {
      "event_type": "view",
      "is_high_margin": True,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T23:06:30.410171Z",
      "variant": "B",
      "veiculo_id": 3
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T23:06:30.410171Z",
    "variant": "B",
    "veiculo_id": 3
  },
  {
    "event_type": "view",
    "is_high_margin": False,
    "payload": {
      "event_type": "view",
      "is_high_margin": False,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T23:06:13.396257Z",
      "variant": "B",
      "veiculo_id": 2
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T23:06:13.396257Z",
    "variant": "B",
    "veiculo_id": 2
  },
  {
    "event_type": "view",
    "is_high_margin": True,
    "payload": {
      "event_type": "view",
      "is_high_margin": True,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T23:06:00.848535Z",
      "variant": "B",
      "veiculo_id": 5
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T23:06:00.848535Z",
    "variant": "B",
    "veiculo_id": 5
  },
  {
    "event_type": "view",
    "is_high_margin": True,
    "payload": {
      "event_type": "view",
      "is_high_margin": True,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T22:52:15.064536Z",
      "variant": "B",
      "veiculo_id": 5
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T22:52:15.064536Z",
    "variant": "B",
    "veiculo_id": 5
  },
  {
    "event_type": "convert",
    "is_high_margin": False,
    "payload": {
      "event_type": "convert",
      "margin": 16,
      "price": 80,
      "reservation_id": 10,
      "timestamp": "2025-11-05T22:52:11.948370Z",
      "variant": "B",
      "veiculo_id": 1
    },
    "remote_addr": None,
    "timestamp": "2025-11-05T22:52:11.948370Z",
    "variant": "B",
    "veiculo_id": 1
  },
  {
    "event_type": "click",
    "is_high_margin": False,
    "payload": {
      "event_type": "click",
      "is_high_margin": False,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T22:52:11.633478Z",
      "variant": "B",
      "veiculo_id": 1
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T22:52:11.633478Z",
    "variant": "B",
    "veiculo_id": 1
  },
  {
    "event_type": "view",
    "is_high_margin": False,
    "payload": {
      "event_type": "view",
      "is_high_margin": False,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T22:52:07.298481Z",
      "variant": "B",
      "veiculo_id": 1
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T22:52:07.298481Z",
    "variant": "B",
    "veiculo_id": 1
  },
  {
    "event_type": "convert",
    "is_high_margin": False,
    "payload": {
      "event_type": "convert",
      "margin": 30,
      "price": 150,
      "reservation_id": 9,
      "timestamp": "2025-11-05T22:52:04.397719Z",
      "variant": "B",
      "veiculo_id": 3
    },
    "remote_addr": None,
    "timestamp": "2025-11-05T22:52:04.397719Z",
    "variant": "B",
    "veiculo_id": 3
  },
  {
    "event_type": "click",
    "is_high_margin": True,
    "payload": {
      "event_type": "click",
      "is_high_margin": True,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T22:52:04.079393Z",
      "variant": "B",
      "veiculo_id": 3
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T22:52:04.079393Z",
    "variant": "B",
    "veiculo_id": 3
  },
  {
    "event_type": "view",
    "is_high_margin": True,
    "payload": {
      "event_type": "view",
      "is_high_margin": True,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T22:52:03.001297Z",
      "variant": "B",
      "veiculo_id": 3
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T22:52:03.001297Z",
    "variant": "B",
    "veiculo_id": 3
  },
  {
    "event_type": "convert",
    "is_high_margin": False,
    "payload": {
      "event_type": "convert",
      "margin": 70,
      "price": 350,
      "reservation_id": 8,
      "timestamp": "2025-11-05T22:51:58.651069Z",
      "variant": "B",
      "veiculo_id": 5
    },
    "remote_addr": None,
    "timestamp": "2025-11-05T22:51:58.651069Z",
    "variant": "B",
    "veiculo_id": 5
  },
  {
    "event_type": "click",
    "is_high_margin": True,
    "payload": {
      "event_type": "click",
      "is_high_margin": True,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T22:51:58.332842Z",
      "variant": "B",
      "veiculo_id": 5
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T22:51:58.332842Z",
    "variant": "B",
    "veiculo_id": 5
  },
  {
    "event_type": "view",
    "is_high_margin": True,
    "payload": {
      "event_type": "view",
      "is_high_margin": True,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T22:51:33.818396Z",
      "variant": "B",
      "veiculo_id": 5
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T22:51:33.818396Z",
    "variant": "B",
    "veiculo_id": 5
  },
  {
    "event_type": "view",
    "is_high_margin": True,
    "payload": {
      "event_type": "view",
      "is_high_margin": True,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T22:14:35.773549Z",
      "variant": "B",
      "veiculo_id": 3
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T22:14:35.773549Z",
    "variant": "B",
    "veiculo_id": 3
  },
  {
    "event_type": "view",
    "is_high_margin": False,
    "payload": {
      "event_type": "view",
      "is_high_margin": False,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T22:14:28.478891Z",
      "variant": "B",
      "veiculo_id": 2
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T22:14:28.478891Z",
    "variant": "B",
    "veiculo_id": 2
  },
  {
    "event_type": "convert",
    "is_high_margin": False,
    "payload": {
      "event_type": "convert",
      "margin": 16,
      "price": 80,
      "reservation_id": 7,
      "timestamp": "2025-11-05T22:14:25.042234Z",
      "variant": "B",
      "veiculo_id": 1
    },
    "remote_addr": None,
    "timestamp": "2025-11-05T22:14:25.042234Z",
    "variant": "B",
    "veiculo_id": 1
  },
  {
    "event_type": "click",
    "is_high_margin": False,
    "payload": {
      "event_type": "click",
      "is_high_margin": False,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T22:14:24.699646Z",
      "variant": "B",
      "veiculo_id": 1
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T22:14:24.699646Z",
    "variant": "B",
    "veiculo_id": 1
  },
  {
    "event_type": "view",
    "is_high_margin": False,
    "payload": {
      "event_type": "view",
      "is_high_margin": False,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T22:14:23.116701Z",
      "variant": "B",
      "veiculo_id": 1
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T22:14:23.116701Z",
    "variant": "B",
    "veiculo_id": 1
  },
  {
    "event_type": "convert",
    "is_high_margin": False,
    "payload": {
      "event_type": "convert",
      "margin": 68,
      "price": 340,
      "reservation_id": 6,
      "timestamp": "2025-11-05T22:14:18.506007Z",
      "variant": "B",
      "veiculo_id": 6
    },
    "remote_addr": None,
    "timestamp": "2025-11-05T22:14:18.506007Z",
    "variant": "B",
    "veiculo_id": 6
  },
  {
    "event_type": "click",
    "is_high_margin": True,
    "payload": {
      "event_type": "click",
      "is_high_margin": True,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T22:14:18.243342Z",
      "variant": "B",
      "veiculo_id": 6
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T22:14:18.243342Z",
    "variant": "B",
    "veiculo_id": 6
  },
  {
    "event_type": "convert",
    "is_high_margin": False,
    "payload": {
      "event_type": "convert",
      "margin": 68,
      "price": 340,
      "reservation_id": 5,
      "timestamp": "2025-11-05T22:14:17.899414Z",
      "variant": "B",
      "veiculo_id": 6
    },
    "remote_addr": None,
    "timestamp": "2025-11-05T22:14:17.899414Z",
    "variant": "B",
    "veiculo_id": 6
  },
  {
    "event_type": "click",
    "is_high_margin": True,
      "payload": {
      "event_type": "click",
      "is_high_margin": True,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T22:14:17.582898Z",
      "variant": "B",
      "veiculo_id": 6
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T22:14:17.582898Z",
    "variant": "B",
    "veiculo_id": 6
  },
  {
    "event_type": "view",
    "is_high_margin": True,
    "payload": {
      "event_type": "view",
      "is_high_margin": True,
      "remote_addr": "127.0.0.1",
      "timestamp": "2025-11-05T22:14:07.688243Z",
      "variant": "B",
      "veiculo_id": 6
    },
    "remote_addr": "127.0.0.1",
    "timestamp": "2025-11-05T22:14:07.688243Z",
    "variant": "B",
    "veiculo_id": 6
  },
  {
    "event_type": "convert",
    "is_high_margin": False,
    "payload": {
      "event_type": "convert",
      "margin": 16,
      "price": 80,
      "reservation_id": 4,
      "timestamp": "2025-11-05T22:09:25.629697Z",
      "variant": "B",
      "veiculo_id": 1
    },
    "remote_addr": None,
    "timestamp": "2025-11-05T22:09:25.629697Z",
    "variant": "B",
    "veiculo_id": 1
  },
  {
    "event_type": "click",
The file continues but is large... (truncated)