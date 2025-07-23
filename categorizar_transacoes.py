import os
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

def categorizar_transacoes(
    df: pd.DataFrame,
    categorias: list[str] = [
    "Alimentação",
    "Cartão de crédito",
    "Carro",
    "Lazer",
    "Moradia",
    "Trabalho",
    "Saúde"
],
    model: str = "llama-3.1-8b-instant"
) -> pd.DataFrame:
    """
    Esta função categoriza transações financeiras com base nas descrições, usando LLM.

    Parâmetros:
    - df (pd.DataFrame): DataFrame contendo uma coluna 'Descrição'.
    - categorias (list[str]): Lista de categorias possíveis.
    - model (str): Nome do modelo a ser utilizado pela Groq. Padrão: 'llama-3.1-8b-instant'.

    Retorna:
    - df (pd.DataFrame): DataFrame com nova coluna 'Categoria'.
    """

    # Carrega variáveis de ambiente (incluindo GROQ_API_KEY)
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError("A chave GROQ_API_KEY não foi encontrada no arquivo .env")

    # Instancia o modelo da Groq
    chat = ChatGroq(model=model, api_key=groq_api_key)

    # Cria o prompt dinâmico com as categorias fornecidas
    categorias_str = "\n- " + "\n- ".join(categorias)
    template = f"""'
    Você é um analista de dados encarregado de categorizar transações financeiras de uma pessoa física.
    Seu trabalho é escolher a categoria mais apropriada para cada lançamento financeiro que eu fornecer.

    As possíveis categorias são:{categorias_str}

    Analise o seguinte lançamento e responda apenas com uma das categorias listadas:
    {{text}}
    """

    # Monta o prompt template e encadeia com o LLM
    prompt = PromptTemplate.from_template(template=template)
    chain = prompt | chat

    # Gera a lista de categorias previstas
    categorias_previstas = []
    for descricao in df["Descrição"].values:
        resposta = chain.invoke({"text": descricao})
        categoria = resposta.content.strip()
        categorias_previstas.append(categoria)

    # Adiciona ao DataFrame
    df["Categoria"] = categorias_previstas
    return df
