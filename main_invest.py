import sqlite3
import calendar
import requests
from datetime import datetime
import locale

# Pegar o mês e o ano atual
ano_atual = datetime.now().year
mes_atual = datetime.now().month

# Calcula o número de dias do mês atual
dias = calendar.monthrange(ano_atual, mes_atual)[1]

class MetaInvestimento:
    def __init__(self, banca_inicial, percent_lucro, dias):
        self.banca_inicial = banca_inicial
        self.percent_lucro = percent_lucro
        self.dias = dias
        self.conectar_bd()

    def conectar_bd(self):
        self.conn = sqlite3.connect('metas_investimento.db')
        self.cursor = self.conn.cursor()

        # Criar tabela se não existir
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS metas (
            dia INTEGER,
            banca_dia REAL,
            lucro_dia REAL,
            banca_final REAL,
            stop_loss REAL,
            entrada REAL,
            g1 REAL,
            g2 REAL,
            g3 REAL,
            g4 REAL
        )
        """)

    def inserir_dados(self, resultados):
        self.cursor.executemany("""
        INSERT INTO metas (dia, banca_dia, lucro_dia, banca_final, stop_loss, entrada, g1, g2, g3, g4)
        VALUES (:dia, :banca_dia, :lucro_dia, :banca_final, :stop_loss, :entrada, :g1, :g2, :g3, :g4)
        """, resultados)
        self.conn.commit()

    def calcular(self):
        banca = self.banca_inicial
        resultados = []

        for dia in range(1, self.dias + 1):
            lucro_dia = banca * self.percent_lucro
            banca_final = banca + lucro_dia
            stop_loss = banca * 0.88
            entrada = int(round(banca * 0.03))
            g1 = int(round(entrada * 3))
            g2 = int(round(entrada * 7.5))
            g3 = int(round(entrada * 15.5))
            g4 = int(round(entrada * 31))

            resultados.append({
                "dia": dia,
                "banca_dia": banca,
                "lucro_dia": lucro_dia,
                "banca_final": banca_final,
                "stop_loss": stop_loss,
                "entrada": entrada,
                "g1": g1,
                "g2": g2,
                "g3": g3,
                "g4": g4
            })

            banca = banca_final

        self.inserir_dados(resultados)
        return resultados

    def exibir(self):
        resultados = self.calcular()
        for resultado in resultados:
            print(f"Dia {resultado['dia']} - Banca do Dia: R${resultado['banca_dia']:.2f} - "
                f"Lucro do Dia: R${resultado['lucro_dia']:.2f} - Banca Final: R${resultado['banca_final']:.2f} - "
                f"Stop Loss: R${resultado['stop_loss']:.2f} - Entrada: R${resultado['entrada']:.2f} - "
                f"G1: R${resultado['g1']:.2f} - G2: R${resultado['g2']:.2f} - "
                f"G3: R${resultado['g3']:.2f} - G4: R${resultado['g4']:.2f}")

class ConversorMoeda:
    def __init__(self, moeda_base):
        self.base_url = f"https://open.er-api.com/v6/latest/{moeda_base}"  

    def obter_taxa_cambio(self):
        response = requests.get(self.base_url)
        if response.status_code != 200:
            raise ValueError("Não foi possível obter as taxas de câmbio.")
        
        dados = response.json()
        return dados["rates"]

    def converter_para_moedas(self, valor_moeda):
        taxas = self.obter_taxa_cambio()
        conversoes = {}
        for moeda, taxa in taxas.items():
            conversao = valor_moeda / taxa
            conversoes[moeda] = conversao
        return conversoes

# Mapeamento de símbolos de moeda
moeda_simbolos = {
    "BRL": "R$",
    "USD": "$",
    "EUR": "€",
    "INR": "₹"
}

# Solicitar a moeda base do usuário
moedas_disponiveis = ["BRL", "USD", "EUR", "INR"]
print("Selecione a moeda base:")
for i, moeda in enumerate(moedas_disponiveis, 1):
    print(f"{i}. {moeda}")

# Coletar seleção de moeda do usuário
while True:
    try:
        selecao = int(input("Digite o número correspondente à moeda: "))
        if selecao in range(1, 5):
            break
        else:
            print("Por favor, digite um número válido.")
    except ValueError:
        print("Por favor, digite um número válido.")

moeda_base = moedas_disponiveis[selecao - 1]

# Solicitar a banca inicial ao usuário
while True:
    banca_inicial_input = input(f"Banca Inicial (exemplo: 64 para {moeda_simbolos[moeda_base]}64): ")
    if banca_inicial_input.isdigit():
        banca_inicial = int(banca_inicial_input)
        break
    else:
        print("Por favor, digite um valor numérico válido.")

# Solicitar a porcentagem de lucro por dia ao usuário
while True:
    percent_lucro_input = input("Porcentagem de Lucro por Dia (exemplo: 10 para 10%): ")
    if percent_lucro_input.isdigit():
        percent_lucro = int(percent_lucro_input) / 100
        break
    else:
        print("Por favor, digite um valor numérico válido.")

investimento = MetaInvestimento(banca_inicial, percent_lucro, dias)
investimento.exibir()

# Mostra um resumo motivacional
print("\nRESUMO MOTIVACIONAL")
print("-" * 40)
print(f"Banca Inicial: {moeda_simbolos[moeda_base]} {banca_inicial:.2f}")
print(f"Porcentagem de Lucro por Dia: {percent_lucro*100}%")
print("-" * 40)

# Calcule o resumo em diferentes moedas
conversor = ConversorMoeda(moeda_base)
valor_final = investimento.calcular()[-1]['banca_final']

print(f"\nRESULTADO PROJETADO PARA {dias} DIAS em {moeda_base}")
print("-" * 40)

# Calcular o valor equivalente em BRL
valor_brl_final = valor_final / conversor.obter_taxa_cambio()[moeda_base]

# Formate o resultado na moeda base selecionada pelo usuário
locale.setlocale(locale.LC_ALL, '')
valor_formatado = locale.currency(valor_brl_final, grouping=True)
print(f"{moeda_base}: {valor_formatado}")

# Converta o valor para outras moedas e exiba apenas as moedas válidas
for moeda, simbolo in moeda_simbolos.items():
    if moeda != moeda_base:
        taxa_cambio = conversor.obter_taxa_cambio()[moeda]
        if taxa_cambio is not None:
            valor_convertido = valor_brl_final * taxa_cambio
            valor_formatado = locale.currency(valor_convertido, grouping=True)
            print(f"{simbolo}: {valor_formatado}")

print("-" * 40)
