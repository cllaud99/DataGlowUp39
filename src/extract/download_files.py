import os
from typing import List, Optional
import time
import shutil
import logging

import requests

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_folder(pasta: str) -> None:
    """
    Cria uma pasta no projeto. Caso já exista, a pasta será excluída e recriada.

    Args:
        pasta (str): Caminho da pasta a ser criada.

    Returns:
        None
    """
    try:
        if os.path.exists(pasta):
            shutil.rmtree(pasta)
            logger.info(f"Pasta '{pasta}' excluída com sucesso.")
        
        os.makedirs(pasta)
        logger.info(f"Pasta '{pasta}' criada com sucesso.")
    
    except Exception as e:
        logger.error(f"Erro ao manipular a pasta '{pasta}': {e}")


def download_file(url: str, pasta_destino: str, max_retries: int = 2) -> None:
    """
    Baixa um arquivo de uma URL para a pasta de destino fornecida, com tentativas de retry.
    Verifica se o arquivo já existe na pasta antes de tentar o download.

    Args:
        url (str): A URL do arquivo a ser baixado.
        pasta_destino (str): O caminho da pasta onde o arquivo será salvo.
        max_retries (int): Número máximo de tentativas de retry em caso de falha.

    Returns:
        None
    """
    # Obtém o nome do arquivo a partir da URL
    nome_arquivo = os.path.basename(url)

    # Caminho completo para salvar o arquivo
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

    # Verifica se o arquivo já existe na pasta de destino
    if os.path.exists(caminho_arquivo):
        logger.info(f"O arquivo '{nome_arquivo}' já existe na pasta '{pasta_destino}'.")
        return  # Retorna sem fazer o download

    tentativa = 0
    while tentativa <= max_retries:
        try:
            # Tenta baixar o arquivo
            resposta = requests.get(url, timeout=10)
            resposta.raise_for_status()  # Levanta erro para status 4xx/5xx
            
            # Salva o arquivo no caminho especificado
            with open(caminho_arquivo, "wb") as file:
                file.write(resposta.content)
            logger.info(f"Arquivo '{nome_arquivo}' baixado com sucesso para '{pasta_destino}'.")
            return  # Sai da função se o download for bem-sucedido

        except requests.exceptions.RequestException as e:
            tentativa += 1
            logger.warning(f"Tentativa {tentativa} de {max_retries + 1}: erro ao baixar o arquivo. {e}")
            if tentativa > max_retries:
                logger.error("Número máximo de tentativas atingido. Download falhou.")
                break
            time.sleep(2)  # Espera 2 segundos antes de tentar novamente


if __name__ == "__main__":

    url = [
        "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/nivel-socioeconomico/2021",
        "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/nivel-socioeconomico/2019",
        "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/nivel-socioeconomico/2015",
        "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/nivel-socioeconomico/2011-2013",
    ]
    download_file(url, "downloads")
