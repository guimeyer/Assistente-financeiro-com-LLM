import os
import pandas as pd
from ofxparse import OfxParser

def ler_extratos_ofx(caminho_origem: str, nome_csv='finance.csv')-> pd.DataFrame:
    """
    Esta função lê um ou mais arquivos .ofx, transforma os dados em DataFrame e salva como CSV.

    Parâmetros:
    - caminho_origem (str): Caminho para um arquivo .ofx ou uma pasta com vários arquivos .ofx.
    - nome_csv (str): Nome do arquivo CSV de saída. Padrão: 'finance.csv'.

    Retorna:
    - df (DataFrame): DataFrame com todas as transações consolidadas.
    """

    df = pd.DataFrame()

    # Verifica se é um único arquivo ou uma pasta
    if os.path.isfile(caminho_origem) and caminho_origem.endswith('.ofx'):
        arquivos_ofx = [caminho_origem]
    elif os.path.isdir(caminho_origem):
        arquivos_ofx = [
            os.path.join(caminho_origem, f)
            for f in os.listdir(caminho_origem)
            if f.endswith('.ofx')
        ]
    else:
        raise ValueError("Forneça um arquivo .ofx válido ou uma pasta contendo arquivos .ofx")

    # Processa cada arquivo .ofx
    for caminho in arquivos_ofx:
        with open(caminho, encoding='ISO-8859-1') as ofx_file:
            ofx = OfxParser.parse(ofx_file)

        transactions_data = []

        for account in ofx.accounts:
            for transaction in account.statement.transactions:
                transactions_data.append({
                    'Data': transaction.date.date(),
                    'Valor': float(transaction.amount),
                    'Descrição': transaction.memo,
                    'ID': transaction.id,
                    'Arquivo': os.path.basename(caminho)
                })

        df_temp = pd.DataFrame(transactions_data)
        df = pd.concat([df, df_temp], ignore_index=True)

    # Salva em CSV
    df.to_csv(nome_csv, index=False, encoding='utf-8')
    print(f"Arquivo {nome_csv} criado com sucesso!")

    return df
