import json
from math import sqrt

# Paste the events data from the user here
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
... (continued) ...
]