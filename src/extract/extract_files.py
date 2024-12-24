import os
import zipfile


def extrair_arquivos_zip(pasta_zipada, pasta_destino):
    """
    Obtém todos os arquivos .zip de uma pasta, transforma em lista e extrai para o destino especificado.

    Args:
        pasta_zipada (str): Caminho da pasta onde os arquivos .zip estão localizados.
        pasta_destino (str): Caminho para a pasta onde os arquivos extraídos serão salvos.

    Returns:
        None
    """

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    for arquivo in os.listdir(pasta_zipada):
        if arquivo.endswith(".zip"):
            caminho_zip = os.path.join(pasta_zipada, arquivo)
            try:
                with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
                    for file in zip_ref.namelist():
                        caminho_arquivo_destino = os.path.join(
                            pasta_destino, os.path.basename(file)
                        )
                        if not file.endswith("/"):
                            zip_ref.extract(file, pasta_destino)
                            os.rename(
                                os.path.join(pasta_destino, file),
                                caminho_arquivo_destino,
                            )
                print(f"Arquivo {arquivo} extraído com sucesso para {pasta_destino}.")
            except zipfile.BadZipFile:
                print(f"O arquivo {arquivo} não é um arquivo .zip válido.")


if __name__ == "__main__":
    pasta_zipada = "downloads"
    pasta_destino = "downloads/extraidos"
    extrair_arquivos_zip(pasta_zipada, pasta_destino)