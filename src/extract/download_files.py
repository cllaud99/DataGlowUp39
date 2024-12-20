import requests
from bs4 import BeautifulSoup
import os

def listar_links_zip_rar(url):
    """
    Extrai links .zip e .rar de uma página web.

    Esta função faz uma requisição HTTP à URL fornecida e busca por todos os links de ancoragem (tags <a>)
    que terminam com '.zip' ou '.rar'.

    Args:
        url (str): URL da página da qual os links serão extraídos.

    Returns:
        list: Lista de links encontrados que terminam com '.zip' ou '.rar'.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Levanta exceções para códigos de status HTTP de erro
    except requests.RequestException as e:
        print(f"Erro ao acessar a URL {url}: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith(('.zip', '.rar')):  # Verifica se o link termina com .zip ou .rar
            links.append(href)
    
    return links

def baixar_arquivos(links, pasta_destino="downloads"):
    """
    Faz o download dos arquivos a partir dos links fornecidos e os salva na pasta especificada.

    A função verifica se a pasta de destino existe e a cria, caso necessário. Em seguida, faz o download
    de cada arquivo e o salva com o nome original do arquivo na pasta de destino.

    Args:
        links (list): Lista de URLs para os arquivos a serem baixados.
        pasta_destino (str, opcional): Diretório onde os arquivos serão salvos. O padrão é "downloads".

    Returns:
        None
    """
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    for link in links:
        arquivo = link.split('/')[-1]
        caminho_arquivo = os.path.join(pasta_destino, arquivo)
        
        print(f"Baixando {arquivo}...")
        resposta = requests.get(link)
        
        with open(caminho_arquivo, 'wb') as f:
            f.write(resposta.content)
        print(f"{arquivo} salvo em {caminho_arquivo}")


if __name__ == "__main__":
    # Exemplo de uso
    url = 'http://dados.prefeitura.sp.gov.br/it/dataset/microdados-matriculas'
    links = listar_links_zip_rar(url)
    baixar_arquivos(links)
