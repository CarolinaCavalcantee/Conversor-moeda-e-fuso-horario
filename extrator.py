{
  "name": "Alerta do Dólar",
  "nodes": [
    {
      "id": "a1b2c3d4-0001-4000-8000-000000000001",
      "name": "Agendamento",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.2,
      "position": [0, 0],
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "minutes",
              "minutesInterval": 30
            }
          ]
        }
      }
    },
    {
      "id": "a1b2c3d4-0002-4000-8000-000000000002",
      "name": "Buscar cotação",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [220, 0],
      "parameters": {
        "method": "GET",
        "url": "https://economia.awesomeapi.com.br/json/last/USD-BRL",
        "options": {}
      }
    },
    {
      "id": "a1b2c3d4-0003-4000-8000-000000000003",
      "name": "Dólar abaixo do limite?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2.2,
      "position": [440, 0],
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "loose"
          },
          "conditions": [
            {
              "id": "a1b2c3d4-0013-4000-8000-000000000013",
              "leftValue": "={{ parseFloat($json.USDBRL.bid) }}",
              "rightValue": 5,
              "operator": {
                "type": "number",
                "operation": "lt"
              }
            }
          ],
          "combinator": "and"
        },
        "options": {}
      }
    },
    {
      "id": "a1b2c3d4-0004-4000-8000-000000000004",
      "name": "Avisar no Telegram",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1.2,
      "position": [660, -80],
      "parameters": {
        "chatId": "COLOQUE_SEU_CHAT_ID_AQUI",
        "text": "=💱 Alerta! O dólar está em R$ {{ $json.USDBRL.bid }}, abaixo do seu limite.\nHorário da cotação: {{ $json.USDBRL.create_date }}",
        "additionalFields": {}
      }
    }
  ],
  "connections": {
    "Agendamento": {
      "main": [
        [
          {
            "node": "Buscar cotação",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Buscar cotação": {
      "main": [
        [
          {
            "node": "Dólar abaixo do limite?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Dólar abaixo do limite?": {
      "main": [
        [
          {
            "node": "Avisar no Telegram",
            "type": "main",
            "index": 0
          }
        ],
        []
      ]
    }
  },
  "pinData": {},
  "settings": {
    "executionOrder": "v1"
  }
}
