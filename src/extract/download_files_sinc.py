import os
import requests
from typing import Optional, List

def create_folder(pasta: str) -> None:
    """
    Cria uma pasta no projeto.
    
    Args:
        pasta (str): Pasta a ser criada.
        
    Returns:
        None
    """
    if not os.path.exists(pasta):
        os.makedirs(pasta)
        print(f"Pasta '{pasta}' criada com sucesso.")
    else:
        print(f"A pasta '{pasta}' já existe.")


def download_file(url: str, pasta_destino: str) -> None:
    """
    Baixa um arquivo de uma URL para a pasta de destino fornecida.
    
    Args:
        url (str): A URL do arquivo a ser baixado.
        pasta_destino (str): O caminho da pasta onde o arquivo será salvo.
        
    Returns:
        None
    """

    # Obtém o nome do arquivo a partir da URL
    nome_arquivo = os.path.basename(url)

    # Caminho completo para salvar o arquivo
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

    try:
        # Baixa o arquivo
        resposta = requests.get(url)
        resposta.raise_for_status()  # Levanta um erro para respostas de status 4xx/5xx

        # Salva o arquivo no caminho especificado
        with open(caminho_arquivo, 'wb') as file:
            file.write(resposta.content)
        print(f"Arquivo '{nome_arquivo}' baixado com sucesso para '{pasta_destino}'.")
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o arquivo: {e}")


if __name__ == "__main__":

    url = [
        "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/nivel-socioeconomico/2021",
        "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/nivel-socioeconomico/2019",
        "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/nivel-socioeconomico/2015",
        "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/nivel-socioeconomico/2011-2013"
    ]
    download_file(url,"downloads")