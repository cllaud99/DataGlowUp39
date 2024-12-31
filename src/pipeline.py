from extract.crawler import get_file_links, get_year_urls
from extract.download_files import create_folder, download_file
from extract.extract_files import extrair_arquivos_zip, limpar_pasta_por_criterio
from transform.transform_files import processar_arquivos_na_pasta
from transform.data_contract import DadosCenso
from load.db_operations import main_insert


def main():
    url = "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/percentual-de-docentes-com-pos-graduacao-stricto-sensu"

    pasta_destino = "downloads"

    create_folder(pasta_destino)
    urls = get_year_urls(url)
    downloads_links = get_file_links(urls)

    for link in downloads_links:
        download_file(link, pasta_destino)

    extrair_arquivos_zip(pasta_destino, pasta_destino)
    limpar_pasta_por_criterio(pasta_destino, "IES", ".xlsx")

    df_ies = processar_arquivos_na_pasta(pasta_destino, DadosCenso)

    main_insert(df_ies, 'perc_docentes_ies')

if __name__ == "__main__":
    main()
