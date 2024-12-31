import pandas as pd
from pydantic import BaseModel, ValidationError
from typing import Type
import os
import logging

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,  # Nível de log, pode ser ajustado para DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Para exibir os logs no console
)

def le_xlsx_ies(arquivo: str) -> pd.DataFrame:
    """
    Lê um arquivo Excel (.xlsx) e retorna um DataFrame contendo os dados da planilha, 
    após a remoção das linhas com valores ausentes na coluna "CO_IES".

    A função ignora as primeiras 9 linhas do arquivo ao ler os dados, com base na 
    suposição de que essas linhas não contêm informações relevantes. Além disso, 
    filtra as linhas onde a coluna "CO_IES" está ausente.

    Args:
        arquivo (str): O caminho para o arquivo Excel a ser lido.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados do arquivo, com as linhas 
        sem valor na coluna "CO_IES" removidas.
    """
    try:
        df = pd.read_excel(arquivo, skiprows=9)
        df = df.dropna(subset=["CO_IES"])
        
        # Transformando os cabeçalhos para minúsculo
        df.columns = df.columns.str.lower()
        
        logging.info(f"Arquivo {arquivo} lido com sucesso.")
        return df
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo {arquivo}: {e}")
        raise

def validar_dataframe(df: pd.DataFrame, model: Type[BaseModel]):
    """
    Valida cada linha de um DataFrame de acordo com as regras definidas no modelo Pydantic.

    Para cada linha do DataFrame, tenta-se criar uma instância do modelo Pydantic especificado.
    Caso a linha seja válida, a instância é criada e a linha é considerada válida. Caso contrário,
    uma exceção de validação é capturada e a linha é considerada inválida.
    """
    for index, row in df.iterrows():
        try:
            # Tenta criar uma instância do modelo a partir da linha do DataFrame
            dados = model(**row.to_dict())
        except ValidationError as e:
            logging.error(f"Linha {index} inválida: {e}")

def processar_arquivos_na_pasta(pasta: str, model: Type[BaseModel]) -> pd.DataFrame:
    """
    Processa todos os arquivos Excel (.xlsx) em uma pasta, validando seus dados com um modelo Pydantic.
    Retorna um DataFrame concatenado contendo os dados válidos de todos os arquivos.

    Args:
        pasta (str): Caminho para a pasta contendo os arquivos .xlsx.
        model (Type[BaseModel]): Classe do modelo Pydantic usada para validação.

    Returns:
        pd.DataFrame: DataFrame concatenado com os dados válidos de todos os arquivos.
    """
    dataframes_validos = []
    
    for arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, arquivo)
        
        if arquivo.endswith(".xlsx"):
            logging.info(f"Processando arquivo: {arquivo}")
            try:
                df = le_xlsx_ies(caminho_arquivo)
                validar_dataframe(df, model)
                dataframes_validos.append(df) 
            except Exception as e:
                logging.error(f"Erro ao processar o arquivo {arquivo}: {e}")
    
    if dataframes_validos:
        logging.info("Processamento completo. Concatenando os DataFrames válidos.")
        return pd.concat(dataframes_validos, ignore_index=True)
    else:
        logging.warning("Nenhum arquivo válido foi processado.")
        return pd.DataFrame() 

if __name__ == "__main__":
    pasta = 'downloads'
    # df_final = processar_arquivos_na_pasta(pasta, DadosCenso)
    # logging.info(df_final.head(10))  # Exemplo de como imprimir um log com o DataFrame resultante
