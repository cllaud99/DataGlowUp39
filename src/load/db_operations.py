import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_environment_variables():
    """Carrega as variáveis de ambiente do arquivo .env."""
    load_dotenv()
    
    required_vars = [
        'POSTGRES_USER', 'POSTGRES_PASSWORD', 
        'POSTGRES_DB', 'POSTGRES_PORT', 'POSTGRES_HOST'
    ]
    
    for var in required_vars:
        if not os.getenv(var):
            logger.error(f"A variável de ambiente {var} não foi encontrada.")
            raise ValueError(f"A variável de ambiente {var} não foi encontrada.")
    
    logger.info("Variáveis de ambiente carregadas com sucesso.")
    return {
        'POSTGRES_USER': os.getenv('POSTGRES_USER'),
        'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'POSTGRES_DB': os.getenv('POSTGRES_DB'),
        'POSTGRES_PORT': os.getenv('POSTGRES_PORT'),
        'POSTGRES_HOST': os.getenv('POSTGRES_HOST')
    }

def create_postgres_engine(config):
    """Cria a conexão com o banco de dados PostgreSQL usando SQLAlchemy."""
    db_url = f"postgresql://{config['POSTGRES_USER']}:{config['POSTGRES_PASSWORD']}@" \
             f"{config['POSTGRES_HOST']}:{config['POSTGRES_PORT']}/{config['POSTGRES_DB']}"
    
    try:
        engine = create_engine(db_url)
        logger.info("Conexão com o PostgreSQL estabelecida com sucesso.")
        return engine
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        raise

def insert_dataframe_to_postgres(df, table_name, engine):
    """Insere os dados do DataFrame na tabela do PostgreSQL."""
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logger.info(f"Dados inseridos na tabela {table_name} com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao inserir dados na tabela {table_name}: {e}")
        raise

def main_insert(df, table_name):
    """Função principal que carrega as variáveis de ambiente, 
    cria a conexão e insere os dados."""
    try:
        # Carregar variáveis de ambiente
        config = load_environment_variables()

        # Criar a conexão com o banco de dados
        engine = create_postgres_engine(config)

        # Inserir o DataFrame na tabela
        insert_dataframe_to_postgres(df, table_name, engine)
    except Exception as e:
        logger.error(f"Erro no processo: {e}")


def truncate_table(table_name, engine):
    """Executa um TRUNCATE na tabela especificada."""
    try:
        with engine.connect() as connection:
            connection.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"))
        logger.info(f"Tabela {table_name} truncada com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao truncar a tabela {table_name}: {e}")
        raise

# Exemplo de uso
if __name__ == "__main__":
    # Exemplo de DataFrame
    data = {
        'coluna1': [1, 2, 3],
        'coluna2': ['A', 'B', 'C']
    }
    df = pd.DataFrame(data)

    # Inserir dados na tabela 'exemplo_tabela'
    main_insert(df, 'exemplo_tabela')
