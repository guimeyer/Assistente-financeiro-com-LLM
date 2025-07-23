from src.leitura_ofx import ler_extratos_ofx
from src.categorizacao import categorizar_transacoes
from src.processamento import ajustar_dados
from src.dashboard import run_dashboard

def main():
    df = ler_extratos_ofx("extratos")
    categorias = ["Alimentação", "Cartão de crédito", "Carro", "Lazer", "Moradia", "Trabalho", "Saúde"]
    df = categorizar_transacoes(df, categorias)
    df = ajustar_dados(df)
    run_dashboard(df)

if __name__ == "__main__":
    main()
