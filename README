# Conversor e extrator de cotações financeiras

Projeto pessoal desenvolvido em Python com foco no entendimento e aprendizado da automação de processos, do consumo de APIs REST e da manipulação de fusos horários.

Esta aplicação foi criada para facilitar a conversão rápida de moedas em tempo real (BRL, USD e EUR). 
O diferencial técnico deste projeto é a integração direta com a AwesomeAPI e a auditoria temporal, pois o sistema captura o carimbo de data/hora (timestamp) da cotação e aplica uma conversão precisa de fuso horário, garantindo que o utilizador saiba exatamente quão recente é a atualização dos dados do mercado financeiro. Além disso, o software aplica uma margem de segurança de mais ou menos 3%, simulando cenários de volatilidade de câmbio.

## Principais funcionalidades
* Consumo de API REST: Requisições HTTP em tempo real utilizando a biblioteca requests para buscar cotações atualizadas.
* Gestão de fusos horários (Timezones): Conversão automática do horário universal (UTC) para o fuso local (America/Maceio), garantindo rastreabilidade exata dos dados.
* Margem de Variação: Projeção automática de margem de erro de mais ou menos 3% sobre o valor convertido.
* Robustez e tratamento de erros: Validação de entradas de dados, aceitando tanto pontos quanto vírgulas e prevenindo falhas por exceções de rede ou chaves inválidas.

## Tecnologias utilizadas
* Python 3.x
* requests (comunicação HTTP com a API)
* zoneinfo (manipulação nativa moderna de fusos horários)
* datetime (gestão e formatação de timestamps)

## Como executar o projeto
Siga os passos abaixo para testar o projeto no seu terminal (Linux / WSL):

1. Crie e ative um ambiente virtual (venv):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
