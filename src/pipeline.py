from crawler import get_year_urls, get_file_links
from download_files_sinc import download_file, create_folder
from extract_files import extrair_arquivos_zip



def main():

    pasta_destino = 'downloads'

    create_folder(pasta_destino)
    urls = get_year_urls()
    downloads_links = get_file_links(urls)

    for link in downloads_links:
        download_file(link, pasta_destino)

    extrair_arquivos_zip(pasta_destino, pasta_destino)

    


if __name__ == "__main__":
    main()
