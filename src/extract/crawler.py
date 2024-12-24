import requests
from bs4 import BeautifulSoup
from typing import List

def get_year_urls() -> List[str]:
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
    url = "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/nivel-socioeconomico"
    
    # Realizando a requisição
    response = requests.get(url)

    # Verificando se a requisição foi bem sucedida
    if response.status_code == 200:
        # Parse do HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontrando todos os links que contêm a classe 'tab' e extraindo os valores 'data-id'
        tabs = soup.find_all('div', class_='tab')
        
        # Criando as URLs dinâmicas com base nos valores 'data-id'
        base_url = "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/nivel-socioeconomico"
        year_urls = [base_url + f"/{tab.find('a')['data-id']}" for tab in tabs if tab.find('a')]

        return year_urls
    else:
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
        # Realizando a requisição para cada URL
        response = requests.get(url)
        
        if response.status_code == 200:
            # Parse do HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Encontrando todos os links na página
            links = soup.find_all('a', href=True)
            
            # Filtrando os links que terminam com as extensões desejadas
            for link in links:
                href = link['href']
                if href.endswith(('.zip', '.xlsx', '.xls', '.csv')):
                    file_links.append(href)
        else:
            print(f"Erro ao acessar a página: {url} (Status code: {response.status_code})")

    return file_links


if __name__ == "__main__":
    try:
        # Obtém as URLs dinâmicas
        urls = get_year_urls()
        
        # Obtém os links dos arquivos desejados
        downloads_links = get_file_links(urls)
        
        # Exibe os links encontrados
        print("Links encontrados:")
        for link in downloads_links:
            print(link)
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
