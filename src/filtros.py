import pandas as pd
from typing import Union, List, Optional

def filter_data(
    df: pd.DataFrame,
    mes: Union[int, str],
    selected_categories: List[str],
    tipos: Optional[List[str]] = None  # filtro agora é opcional
) -> pd.DataFrame:
    """
    Filtra o DataFrame por mês (número ou nome), categorias e opcionalmente por tipo (Receita/Despesa).

    Parâmetros:
    - df (pd.DataFrame): DataFrame com as colunas 'Mês', 'Categoria' e 'Tipo'.
    - mes (int ou str): Mês como número (1 a 12) ou nome (ex: 'Julho').
    - selected_categories (List[str]): Categorias selecionadas.
    - tipos (List[str], opcional): Lista com 'Receita', 'Despesa' ou ambos. Se None, não filtra por tipo.

    Retorna:
    - df_filtered (pd.DataFrame): DataFrame filtrado.
    """

    meses_dict = {
        'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
        'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
        'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
    }

    if isinstance(mes, str):
        mes = mes.strip().lower()
        if mes not in meses_dict:
            raise ValueError(f"Nome de mês inválido: '{mes}'")
        mes = meses_dict[mes]

    df_filtered = df[df['Mês'] == mes]

    if selected_categories and 'Categoria' in df.columns:
        df_filtered = df_filtered[df_filtered['Categoria'].isin(selected_categories)]

    # Aplica filtro por tipo apenas se fornecido
    if tipos and 'Tipo' in df.columns:
        df_filtered = df_filtered[df_filtered['Tipo'].isin(tipos)]

    return df_filtered
