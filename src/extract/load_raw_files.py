import os
from dotenv import load_dotenv
import psycopg2

# Carregar variáveis do .env
load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")  # Default para localhost

# Sua query aqui
query = f"""
SELECT *
FROM read_csv('downloads/extraidos/Microdados_EOL_Matricula_Atividades_Complementares.csv', header=True,  all_varchar = 1);
"""

# Conectar ao banco PostgreSQL e executar a query
try:
    connection = psycopg2.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB
    )

    cursor = connection.cursor()
    cursor.execute(query)

    # Obter os resultados
    records = cursor.fetchall()
    for row in records:
        print(row)

except Exception as error:
    print(f"Erro ao conectar ao banco de dados: {error}")

finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'connection' in locals() and connection:
        connection.close()