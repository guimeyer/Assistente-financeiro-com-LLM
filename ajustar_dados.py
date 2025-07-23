import pandas as pd

def ajustar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processa o DataFrame de transações financeiras:
    - Cria a coluna 'Tipo' (Receita ou Despesa) com base no sinal da coluna 'Valor'.
    - Remove colunas 'ID' e 'Arquivo', se existirem.
    - Converte a coluna 'Data' para datetime.
    - Cria colunas 'Ano' e 'Mês' com base na data.

    Parâmetros:
    - df (pd.DataFrame): DataFrame com colunas 'Data' e 'Valor'.

    Retorna:
    - df (pd.DataFrame): DataFrame limpo e enriquecido.
    """

    # 1. Criar coluna 'Tipo' com base no sinal do valor
    if 'Valor' not in df.columns:
        raise ValueError("O DataFrame precisa conter a coluna 'Valor'.")
    df['Tipo'] = df['Valor'].apply(lambda x: 'Receita' if x > 0 else 'Despesa')

    # 2. Remover colunas desnecessárias se existirem
    for col in ['ID', 'Arquivo']:
        if col in df.columns:
            df.drop(columns=col, inplace=True)

    # 3. Converter a coluna 'Data' para datetime
    if 'Data' not in df.columns:
        raise ValueError("O DataFrame precisa conter a coluna 'Data'.")
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')

    # 4. Remover linhas com data inválida
    df = df.dropna(subset=['Data'])

    # 5. Criar colunas de Ano e Mês
    df['Ano'] = df['Data'].dt.year
    df['Mês'] = df['Data'].dt.month

    return df





