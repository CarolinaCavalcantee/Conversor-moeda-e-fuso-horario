from datetime import datetime
from zoneinfo import ZoneInfo  
import requests

def buscar_cotacoes():

    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        return None

def processar_fuso_horario(timestamp_api):
    try:
        data_utc = datetime.fromtimestamp(int(timestamp_api), ZoneInfo("UTC"))
        
        fuso_local = ZoneInfo("America/Maceio")
        data_local = data_utc.astimezone(fuso_local)
        
        return data_local.strftime("%d/%m/%Y às %H:%M:%S (%Z)")
    except Exception as e:
        return f"Não foi possível converter o fuso horário: {e}"

def calcular_conversao(valor, moeda_origem, moeda_destino, dados_api):

    if not dados_api:
        return None

    try:
        cotacao_usd = float(dados_api['USDBRL']['bid'])
        cotacao_eur = float(dados_api['EURBRL']['bid'])
        
        timestamp_servidor = dados_api['USDBRL']['timestamp']
        horario_convertido = processar_fuso_horario(timestamp_servidor)

        if moeda_origem == "USD":
            valor_em_brl = valor * cotacao_usd
        elif moeda_origem == "EUR":
            valor_em_brl = valor * cotacao_eur
        elif moeda_origem == "BRL":
            valor_em_brl = valor
        else:
            raise ValueError("Moeda de origem inválida.")

        if moeda_destino == "USD":
            valor_convertido = valor_em_brl / cotacao_usd
        elif moeda_destino == "EUR":
            valor_convertido = valor_em_brl / cotacao_eur
        elif moeda_destino == "BRL":
            valor_convertido = valor_em_brl
        else:
            raise ValueError("Moeda de destino inválida.")

        margem_inferior = valor_convertido * 0.97
        margem_superior = valor_convertido * 1.03

        return {
            "convertido": round(valor_convertido, 2),
            "minimo": round(margem_inferior, 2),
            "maximo": round(margem_superior, 2),
            "horario_local": horario_convertido
        }
    except KeyError as e:
        print(f"[Erro de Dados]: Chave não encontrada -> {e}")
        return None
    except ValueError as ve:
        print(f"[Erro]: {ve}")
        return None

def main():
    print("Conversão financeira e consulta de cotações em tempo real")

    try:
        valor_str = input("\nDigite o valor numérico que deseja converter: ").strip().replace(",", ".")
        valor_usuario = float(valor_str)
    except ValueError:
        print("\n[Erro]: Valor inválido inserido. Por favor, digite apenas números.")
        return
    print("\nEscolha a moeda de origem:")
    print("1 - BRL (Real)")
    print("2 - USD (Dólar)")
    print("3 - EUR (Euro)")
    
    op_origem = input("Digite o número da opção de origem: ").strip()
    mapa_moedas = {"1": "BRL", "2": "USD", "3": "EUR"}
    
    if op_origem not in mapa_moedas:
        print("\n[Erro]: Opção de origem inválida.")
        return
    moeda_origem = mapa_moedas[op_origem]

    print("\nEscolha a moeda de destino:")
    print("1 - BRL (Real)")
    print("2 - USD (Dólar)")
    print("3 - EUR (Euro)")
    
    op_destino = input("Digite o número da opção de destino: ").strip()
    
    if op_destino not in mapa_moedas:
        print("\n[Erro]: Opção de destino inválida.")
        return
    moeda_destino = mapa_moedas[op_destino]

    if moeda_origem == moeda_destino:
        return print("Por favor, escolha moedas diferentes para a conversão.")

    dados = buscar_cotacoes()

    if dados:
        resultado = calcular_conversao(valor_usuario, moeda_origem, moeda_destino, dados)
        
        if resultado:
            print(f" Resultado da conversão")
            print(f"Quantia inserida: {valor_usuario} {moeda_origem}")
            print(f"Valor convertido {moeda_destino}: {resultado['convertido']} {moeda_destino}")
            print(f"Margem de erro inferior: {resultado['minimo']} {moeda_destino}")
            print(f"Margem de erro superior: {resultado['maximo']} {moeda_destino}")
            print(f"Horário da cotação: {resultado['horario_local']}")

        else:
            print("\n[Erro]: Erro no processamento da conversão.")
    else:
        print("\n[Erro]: Não foi possível obter os dados da API.")

if __name__ == "__main__":
    main()
