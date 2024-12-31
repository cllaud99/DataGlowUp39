import logging
from typing import List
import requests
from bs4 import BeautifulSoup

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_year_urls(url: str) -> List[str]:
    """
    Função que extrai uma lista de URLs dinâmicas de um site específico,
    com base em links encontrados na página de indicadores educacionais.

    Realiza uma requisição GET ao site principal, faz o parsing do HTML
    e extrai os valores dos links que contêm a classe 'tab', criando URLs
    dinâmicas para cada link encontrado.

    Returns:
        List[str]: Lista de URLs dinâmicas extraídas da página.

    Raises:
        Exception: Se houver erro na requisição ou se a estrutura esperada
        da página for diferente.
    """
    # URL principal onde a lista de endpoints está

    # Realizando a requisição
    response = requests.get(url)

    # Verificando se a requisição foi bem sucedida
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        tabs = soup.find_all("div", class_="tab")

        year_urls = [
            url + f"/{tab.find('a')['data-id']}"
            for tab in tabs
            if tab.find("a") and not tab.find("a")["href"].endswith("sobre")
        ]
        
        filtered_urls = [url for url in year_urls if url.split("/")[-1].isdigit()]

        logger.info(f"Links encontrados: {filtered_urls}")

        return filtered_urls
    else:
        logger.error(f"Erro ao acessar a página: {response.status_code}")
        raise Exception(f"Erro ao acessar a página: {response.status_code}")


def get_file_links(urls: List[str]) -> List[str]:
    """
    Função que percorre uma lista de URLs e extrai todos os links
    que contenham arquivos com as extensões .zip, .xlsx, .xls ou .csv.

    Args:
        urls (List[str]): Lista de URLs para serem percorridas e analisadas.

    Returns:
        List[str]: Lista de URLs de arquivos encontrados com as extensões especificadas.

    Raises:
        Exception: Se houver erro ao acessar qualquer uma das URLs fornecidas.
    """
    file_links = []

    for url in urls:

        response = requests.get(url)

        if response.status_code == 200:
            # Parse do HTML
            soup = BeautifulSoup(response.content, "html.parser")

            # Encontrando todos os links na página
            links = soup.find_all("a", href=True)

            # Filtrando os links que terminam com as extensões desejadas
            for link in links:
                href = link["href"]
                if href.endswith(".zip"):
                    file_links.append(href)
        else:
            logger.error(f"Erro ao acessar a página: {url} (Status code: {response.status_code})")

    return file_links
