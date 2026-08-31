import pandas as pnd
from datetime import datetime, timedelta
import os

caminhoCSV = "./csvs/dados.csv"

# Verifica se o arquivo existe antes de tentar ler para evitar erros na inicialização
if not os.path.exists(caminhoCSV):
    print("Arquivo CSV não encontrado. Execute o script de coleta primeiro.")
    exit()

DataFrame = pnd.read_csv(caminhoCSV, sep=";")

def TratarTimeStamp():
    DataFrame['TimeStamp'] = pnd.to_datetime(DataFrame['TimeStamp'])

    DataFrame['Ano'] = DataFrame['TimeStamp'].dt.year
    DataFrame['Mes'] = DataFrame['TimeStamp'].dt.month
    DataFrame['Dia'] = DataFrame['TimeStamp'].dt.day
    DataFrame['Hora'] = DataFrame['TimeStamp'].dt.hour

def CalcularDados():
    # 1. Média de uso da RAM (Última hora)
    filtro_ram = DataFrame['TimeStamp'] > datetime.now() - timedelta(hours=1)
    
    if not DataFrame['UsoRAM'][filtro_ram].empty:
        mediaRam = DataFrame['UsoRAM'][filtro_ram].mean()
        print(f"Média de RAM na última hora: {mediaRam:.1f}%")
    else:
        print("Sem medidas de RAM na última hora.")

    # 2. Pico da CPU (Últimas 2 horas)
    filtro_cpu = DataFrame['TimeStamp'] > datetime.now() - timedelta(hours=2)

    if not DataFrame['UsoCPU'][filtro_cpu].empty:
        picoCPU = DataFrame['UsoCPU'][filtro_cpu].max()
        tempoPico = DataFrame['TimeStamp'][DataFrame['UsoCPU'] == picoCPU]
        print(f"Pico da CPU: {picoCPU}% registrado em {tempoPico.iloc[0]}")
    else:
         print("Sem medidas de CPU nas últimas 2 horas.")

    # 3. Média do uso do Disco (Últimos 12 minutos)
    tempo = 12
    filtro_disco = DataFrame['TimeStamp'] > datetime.now() - timedelta(minutes=tempo)
    valorDiscoIntervaloTempo = DataFrame['UsoDisco'][filtro_disco]
    
    if not valorDiscoIntervaloTempo.empty:
        mediaDisco = valorDiscoIntervaloTempo.mean()  
        print(f"Média do disco nos últimos {tempo} minutos: {mediaDisco:.1f}%")
    else:
        print(f"Sem medidas de disco nos últimos {tempo} minutos.")

TratarTimeStamp()
CalcularDados()