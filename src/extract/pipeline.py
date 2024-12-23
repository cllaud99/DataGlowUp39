from download_files import main_download
from extract_file import extrair_arquivos_zip


def main():

    pasta_destino = "downloads"
    pasta_extraida = "downloads/extraidos"

    main_download()

    extrair_arquivos_zip(pasta_destino, pasta_extraida)


if __name__ == "__main__":
    main()