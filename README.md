# MetaInvestimento

![GitHub](https://img.shields.io/github/license/seu-usuario/seu-repositorio)
![GitHub last commit](https://img.shields.io/github/last-commit/seu-usuario/seu-repositorio)
![GitHub issues](https://img.shields.io/github/issues-raw/seu-usuario/seu-repositorio)

## Descrição

O projeto **MetaInvestimento** é uma aplicação Python que permite aos usuários calcular metas de investimento diárias em diferentes moedas com base em uma banca inicial e uma porcentagem de lucro desejada por dia. A aplicação fornece uma visão geral das metas de investimento diárias, incluindo o lucro esperado, o valor da banca ao longo do tempo e informações sobre limites de perda.

## Recursos Principais:

- Cálculo de metas de investimento diárias em moedas como Real (BRL), Dólar (USD), Euro (EUR) e Rúpia Indiana (INR).
- egistro e armazenamento de resultados em um banco de dados SQLite.
- Conversão automática de valores para diferentes moedas com base nas taxas de câmbio mais recentes.
- Interface de linha de comando (CLI) interativa para interagir com o programa.
- Visualização de resultados em formato legível, incluindo símbolos de moeda.
- Instruções de Uso:

Escolha a moeda base (BRL, USD, EUR ou INR).
Insira sua banca inicial e a porcentagem de lucro desejada por dia.
O programa calculará e exibirá as metas de investimento diárias, incluindo o lucro esperado, banca ao longo do tempo e limites de perda.
O resultado projetado em diferentes moedas também é apresentado para uma compreensão abrangente dos ganhos potenciais em várias moedas.
Dependências:

## Requisitos

- Python 3.x
- Biblioteca 

- Bibliotecas Python: requests, sqlite3, calendar, datetime, locale
- Notas: Biblioteca `requests` (pode ser instalada via `pip install requests`)

## Uso

1. Clone este repositório:

   ```bash
   git clone https://github.com/roninunes-projects/MetaInvestimento.git

   # Navegue até o diretório do projeto:
   cd seu-repositorio
   # Execute o programa:
   python main_invest.py
    # Siga as instruções no terminal para inserir a moeda base, banca inicial e porcentagem de lucro por dia.
    # Exemplo de Saída:
   
    RESULTADO PROJETADO PARA 30 DIAS em EUR
    ----------------------------------------
    €: 17.449,40
    $ (USD): 20.085,11
    R$ (BRL): 106.738,80
    ₹ (INR): 1.545.384,62
    ----------------------------------------
