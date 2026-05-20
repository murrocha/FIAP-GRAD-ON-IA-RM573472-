import csv
import random
from datetime import datetime, timedelta


NOME_ARQUIVO = "dados_sensores_farmtech.csv"   # nome do arquivo de saída
TOTAL_LEITURAS = 100                            # quantidade de registros
DATA_INICIO = datetime(2025, 1, 1, 6, 0, 0)    # data/hora da primeira leitura
INTERVALO_MINUTOS = 60                          # intervalo entre leituras (1h)

# FUNÇÃO PRINCIPAL

def gerar_dados():
    registros = []

    for i in range(TOTAL_LEITURAS):
        # Calcula a data/hora desta leitura
        data_hora = DATA_INICIO + timedelta(minutes=INTERVALO_MINUTOS * i)

        # Gera valores simulados com variação realista
        umidade      = round(random.uniform(20.0, 90.0), 2)   # % umidade
        fosforo_P    = round(random.uniform(5.0, 80.0), 2)    # mg/kg
        potassio_K   = round(random.uniform(50.0, 300.0), 2)  # mg/kg
        ph           = round(random.uniform(4.5, 8.5), 2)     # escala pH
        temperatura  = round(random.uniform(15.0, 40.0), 2)   # °C
        chuva_mm     = round(random.uniform(0.0, 30.0), 2)    # mm

        # Regra simples: irriga se umidade < 40% e não está chovendo muito
        irrigacao_ativa = 1 if (umidade < 40.0 and chuva_mm < 5.0) else 0

        registros.append({
            "data_hora"        : data_hora.strftime("%Y-%m-%d %H:%M:%S"),
            "umidade"          : umidade,
            "fosforo_P"        : fosforo_P,
            "potassio_K"       : potassio_K,
            "pH"               : ph,
            "temperatura"      : temperatura,
            "chuva_mm"         : chuva_mm,
            "irrigacao_ativa"  : irrigacao_ativa,
        })

    return registros


# SALVA O CSV

def formatar_numero(valor):
    """Converte float para string com vírgula decimal (padrão pt-BR / Oracle)."""
    if isinstance(valor, float):
        return str(valor).replace('.', ',')
    return str(valor)

def salvar_csv(registros):
    colunas = ["data_hora", "umidade", "fosforo_P", "potassio_K",
               "pH", "temperatura", "chuva_mm", "irrigacao_ativa"]

    with open(NOME_ARQUIVO, mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=colunas, delimiter=';')
        writer.writeheader()
        # Converte vírgula decimal em cada linha antes de gravar
        for registro in registros:
            linha = {k: formatar_numero(v) for k, v in registro.items()}
            writer.writerow(linha)

    print(f"Arquivo '{NOME_ARQUIVO}' criado com {len(registros)} registros!")
    print(f"Salvo na pasta onde este script está localizado.")
    print(f"Separador de colunas: ponto e vírgula (;)")
    print(f"Separador decimal: vírgula (,) — compatível com Oracle pt-BR")


# EXECUÇÃO

if __name__ == "__main__":
    dados = gerar_dados()
    salvar_csv(dados)

    # Mostra uma prévia dos primeiros 5 registros
    print("\n Prévia dos primeiros 5 registros:")
    print("-" * 75)
    colunas = list(dados[0].keys())
    print("  |  ".join(colunas))
    print("-" * 75)
    for linha in dados[:5]:
        print("  |  ".join(str(v) for v in linha.values()))
