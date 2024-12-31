import os
import zipfile
import py7zr
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extrair_arquivos_zip(pasta_zipada, pasta_destino):
    """
    Extrai arquivos compactados no formato 7z ou zip de uma pasta de origem para uma pasta de destino.

    Args:
        pasta_zipada (str): Caminho da pasta contendo os arquivos compactados.
        pasta_destino (str): Caminho da pasta onde os arquivos extraídos serão salvos.

    Raises:
        Exception: Se ocorrer um erro durante a extração dos arquivos.
    """

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    for arquivo in os.listdir(pasta_zipada):
        if arquivo.endswith(".zip") or arquivo.endswith(".7z"):
            caminho_zip = os.path.join(pasta_zipada, arquivo)
            try:
                # Tenta extrair com py7zr para 7z
                with py7zr.SevenZipFile(caminho_zip, mode="r") as z:
                    z.extractall(path=pasta_destino)
                logger.info(f"Arquivo {arquivo} extraído com sucesso para {pasta_destino}.")
            except Exception:
                try:
                    # Se der erro, tenta com zipfile para .zip
                    with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                        zip_ref.extractall(pasta_destino)
                    logger.info(f"Arquivo {arquivo} extraído com sucesso para {pasta_destino}.")
                except Exception as e:
                    logger.error(f"Erro ao extrair {arquivo}: {e}")
            finally:
                # Exclui o arquivo compactado após a extração
                os.remove(caminho_zip)
                logger.info(f"Arquivo {arquivo} excluído com sucesso.")


def limpar_pasta_por_criterio(pasta: str, contem: str, extensao: str) -> None:
    """
    Remove arquivos de uma pasta que não contenham uma string específica ou não tenham a extensão especificada.

    Args:
        pasta (str): Caminho da pasta a ser analisada.
        contem (str): String que deve estar contida no nome do arquivo.
        extensao (str): Extensão dos arquivos que devem ser mantidos (com ponto, por exemplo, ".txt").
    """
    if not os.path.isdir(pasta):
        raise ValueError(f"O caminho '{pasta}' não é uma pasta válida.")
    
    for arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho_arquivo):
            if contem not in arquivo or not arquivo.endswith(extensao):
                os.remove(caminho_arquivo)
                logger.info(f"Removido: {arquivo}")


if __name__ == "__main__":
    pasta_zipada = "downloads"
    pasta_destino = "downloads/extraidos"
    extrair_arquivos_zip(pasta_zipada, pasta_destino)
