from download_files import listar_links_zip_rar, baixar_arquivos
from extract_file import extrair_arquivos_zip


def main():

    pasta_destino = "downloads"
    pasta_extraida = "downloads/extraidos"

    url = 'http://dados.prefeitura.sp.gov.br/it/dataset/microdados-matriculas'
    links = listar_links_zip_rar(url)

    baixar_arquivos(links, pasta_destino=pasta_destino)

    links = listar_links_zip_rar(url)
    baixar_arquivos(links)

    extrair_arquivos_zip(pasta_destino, pasta_extraida)


if __name__ == "__main__":
    main()