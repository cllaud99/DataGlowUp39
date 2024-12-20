import os
import pandas as pd
from typing import List, Type
from pydantic import ValidationError

from models import Escola, Turma  # Importa os modelos criados

def validar_arquivos_csv(pasta: str):
    # Mapear modelos para nomes de arquivos esperados
    modelos = {
        "escola.csv": Escola,
        "turma.csv": Turma,
    }
    
    arquivos_csv = [f for f in os.listdir(pasta) if f.endswith('.csv')]
    resultados = []

    for arquivo in arquivos_csv:
        caminho_arquivo = os.path.join(pasta, arquivo)
        
        if arquivo not in modelos:
            resultados.append((arquivo, "Modelo não encontrado"))
            continue
        
        modelo: Type = modelos[arquivo]
        try:
            # Ler o CSV
            df = pd.read_csv(caminho_arquivo)
            # Validar linha por linha
            for _, linha in df.iterrows():
                dados = linha.to_dict()
                modelo(**dados)  # Valida com o Pydantic
            resultados.append((arquivo, "Validação bem-sucedida"))
        except ValidationError as e:
            resultados.append((arquivo, f"Erro de validação: {e}"))
        except Exception as e:
            resultados.append((arquivo, f"Erro ao processar: {e}"))
    
    return resultados


if __name__ == "__main__":
    pasta = "downloads/extraidos"
    resultados = validar_arquivos_csv(pasta)