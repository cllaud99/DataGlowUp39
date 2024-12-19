import requests
from bs4 import BeautifulSoup
import os

def listar_links_zip_municipio(url):
    """
    Extrai links .zip contendo a palavra 'municipio' de uma página web.

    Esta função faz uma requisição HTTP à URL fornecida e busca por todos os links de ancoragem (tags <a>)
    que terminam com '.zip' e contêm a palavra 'municipio'.

    Args:
        url (str): URL da página da qual os links serão extraídos.

    Returns:
        list: Lista de links encontrados que atendem aos critérios (.zip e 'municipio').
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links_municipio = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.zip') and 'municipio' in href.lower():
            links_municipio.append(href)
    
    return links_municipio


def listar_links_ano_incremental(ano_inicial):
    """
    Obtém links .zip contendo 'municipio' para múltiplos anos consecutivos.

    A função começa no ano especificado e tenta acessar a URL do ano atual. Ela continua até que
    uma resposta diferente de 200 seja recebida, indicando que o ano não tem dados disponíveis.

    Args:
        ano_inicial (int): Ano inicial para busca dos links.

    Returns:
        list: Lista de links encontrados para os anos com dados disponíveis.
    """
    base_url = "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/remuneracao-media-dos-docentes/"
    links_municipio = []
    ano_atual = ano_inicial
    
    while True:
        url = f"{base_url}{ano_atual}"
        response = requests.get(url)
        
        if response.status_code != 200:
            break
        
        links_municipio.extend(listar_links_zip_municipio(url))
        ano_atual += 1
    
    return links_municipio

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
    ano_inicial = 2014
    links = listar_links_ano_incremental(ano_inicial)
    baixar_arquivos(links)
