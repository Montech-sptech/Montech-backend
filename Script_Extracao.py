import pandas as pnd
from datetime import datetime
import os
import psutil
import socket

def coletarMetricas():
    # 1. Identificação do Servidor 
    hostname_atual = socket.gethostname()
    

    uso_ram = psutil.virtual_memory().percent
    uso_cpu = psutil.cpu_percent(interval=1)
    uso_disco = psutil.disk_usage('/').percent
    timestamp_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    resultados = {
        "TimeStamp": [timestamp_atual],
        "Hostname": [hostname_atual],
        "UsoRAM": [uso_ram],
        "UsoCPU": [uso_cpu],
        "UsoDisco": [uso_disco]
    }

    # Criação do DataFrame
    df_Novo = pnd.DataFrame(resultados)

    # 4. Carga 
    caminhoCSV = "./csvs/dados.csv"
    
    # Cria a pasta automaticamente caso ela não exista
    os.makedirs(os.path.dirname(caminhoCSV), exist_ok=True)
    arquivoExiste = os.path.exists(caminhoCSV)

    # Exportação usando o Pandas em modo append
    df_Novo.to_csv(
        caminhoCSV,
        sep=';',
        mode='a',
        index=False,
        header=not arquivoExiste,
        encoding='utf-8'
    )

    print(f"[{timestamp_atual}] Coleta salva com sucesso | Servidor: {hostname_atual}")

if __name__ == "__main__":
    coletarMetricas()