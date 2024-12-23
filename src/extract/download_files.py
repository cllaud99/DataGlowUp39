import requests
from bs4 import BeautifulSoup
import os
import aiohttp
import asyncio

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

async def baixar_arquivo(session, link, pasta_destino):
    """
    Faz o download de um único arquivo de forma assíncrona.

    Args:
        session (aiohttp.ClientSession): Sessão HTTP assíncrona.
        link (str): URL do arquivo a ser baixado.
        pasta_destino (str): Diretório onde o arquivo será salvo.

    Returns:
        None
    """
    arquivo = link.split('/')[-1]
    caminho_arquivo = os.path.join(pasta_destino, arquivo)

    print(f"Baixando {arquivo}...")
    try:
        async with session.get(link) as resposta:
            if resposta.status == 200:
                with open(caminho_arquivo, 'wb') as f:
                    f.write(await resposta.read())
                print(f"{arquivo} salvo em {caminho_arquivo}")
            else:
                print(f"Erro ao baixar {arquivo}: Código HTTP {resposta.status}")
    except Exception as e:
        print(f"Erro ao baixar {arquivo}: {e}")

async def baixar_arquivos(links, pasta_destino="downloads"):
    """
    Faz o download de múltiplos arquivos de forma assíncrona e os salva na pasta especificada.

    Args:
        links (list): Lista de URLs para os arquivos a serem baixados.
        pasta_destino (str, opcional): Diretório onde os arquivos serão salvos. O padrão é "downloads".

    Returns:
        None
    """
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    async with aiohttp.ClientSession() as session:
        tarefas = [baixar_arquivo(session, link, pasta_destino) for link in links]
        await asyncio.gather(*tarefas)

def main_download():
    """
    Função principal para listar links e baixar arquivos.
    """
    url = 'http://dados.prefeitura.sp.gov.br/it/dataset/microdados-matriculas'
    links = listar_links_zip_rar(url)
    if links:
        asyncio.run(baixar_arquivos(links))
    else:
        print("Nenhum link válido encontrado para download.")

if __name__ == "__main__":
    main_download()
