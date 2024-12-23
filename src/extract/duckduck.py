import duckdb

# Caminho do arquivo CSV
caminho_arquivo = 'downloads/extraidos/Microdados_EOL_Matricula_Atividades_Complementares.csv'

# Conectar ao DuckDB
con = duckdb.connect()

# Ler o CSV, forçando todas as colunas a serem tratadas como VARCHAR automaticamente
query = f"""
SELECT *
FROM read_csv('downloads/extraidos/*.csv', header=True,  all_varchar = 1, ignore_errors=True, union_by_name=True);
"""

duckdb.sql(query).show()

duckdb.sql(query).write_parquet("test.parquet") 