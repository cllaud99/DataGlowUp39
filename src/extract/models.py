from pydantic import BaseModel, Field
from typing import Optional, Type
import os
import pandas as pd
from pydantic import ValidationError


class Escola(BaseModel):
    ano_letivo: int = Field(..., alias="AN_LETIVO", description="Ano Letivo")
    cd_unidade_educacao: int = Field(..., alias="CD_UNIDADE_EDUCACAO", description="Código da escola")
    nome_distrito: str = Field(..., alias="NOME_DISTRITO", description="Nome do distrito a qual a escola pertence")
    cd_setor: int = Field(..., alias="CD_SETOR", description="Código do Setor a qual a escola pertence")
    tipo_escola: str = Field(..., alias="TIPO_ESCOLA", description="Tipo da escola")
    nome_escola: str = Field(..., alias="NOME_ESCOLA", description="Nome da escola")
    dre: str = Field(..., alias="DRE", description="Nome da Diretoria Regional de Ensino (DRE)")
    cd_inep_escola: Optional[int] = Field(None, alias="CD_INEP_ESCOLA", description="Código INEP da escola")
    situacao_escola: str = Field(..., alias="SITUACAO_ESCOLA", description="Situação de funcionamento da escola")


class Turma(BaseModel):
    cd_turma: int = Field(..., alias="CD_TURMA", description="Código da Turma")
    cd_turno: int = Field(..., alias="CD_TURNO", description="Código do Turno")
    desc_turno: str = Field(..., alias="DESC_TURNO", description="Descritivo do Turno")
    cd_serie: int = Field(..., alias="CD_SERIE", description="Código da Série")
    desc_serie: str = Field(..., alias="DESC_SERIE", description="Descritivo da Série")
    modalidade: str = Field(..., alias="MODALIDADE", description="Modalidade/Etapa de ensino da turma")
    modalidade_segmento: str = Field(..., alias="MODALIDADE_SEGMENTO", description="Modalidade/Etapa/Ciclo/Segmento")
    turma_escol: str = Field(..., alias="TURMA_ESCOL", description="Turma de Escolarização")
    nome_turma: str = Field(..., alias="NOME_TURMA", description="Nome da turma")
    hora_in_turma: Optional[int] = Field(None, alias="HORA_IN_TURMA", description="Horário início da turma")
    hora_fim_turma: Optional[int] = Field(None, alias="HORA_FIM_TURMA", description="Horário fim da turma")
    desc_periodicidade_turma: str = Field(..., alias="DESC_PERIODICIDADE_TURMA", description="Periodicidade da turma")
    cd_etapa_ensino: int = Field(..., alias="CD_ETAPA_ENSINO", description="Código da etapa de ensino")
    desc_etapa_ensino: str = Field(..., alias="DESC_ETAPA_ENSINO", description="Descritivo da etapa de ensino")


class Aluno(BaseModel):
    cd_aluno_sme: int = Field(..., alias="CD_ALUNO_SME", description="Código SME do aluno")
    cd_inep_aluno: Optional[int] = Field(None, alias="CD_INEP_ALUNO", description="Código INEP do aluno")
    ano_nasc_aluno: int = Field(..., alias="ANO_NASC_ALUNO", description="Ano de nascimento do aluno")
    mes_nasc_aluno: int = Field(..., alias="MÊS_NASC_ALUNO", description="Mês de nascimento do aluno")
    idade_aluno_ano_civil: int = Field(..., alias="IDADE_ALUNO_ANO_CIVIL", description="Idade no ano civil")
    idade_aluno_31_03: int = Field(..., alias="IDADE_ALUNO_31_03", description="Idade em 31 de março")
    cd_sexo: str = Field(..., alias="CD_SEXO", description="Código do sexo do aluno")
    cd_raca_cor: Optional[int] = Field(None, alias="CD_RACA_COR", description="Código da raça/cor do aluno")


class Microdados(BaseModel):
    escola: Escola
    turma: Turma
    aluno: Aluno

def validate_csv_folder(folder_path: str, model: Type[BaseModel]):
    """
    Valida todos os arquivos CSV em uma pasta usando um modelo Pydantic.

    :param folder_path: Caminho para a pasta contendo os arquivos CSV.
    :param model: Classe Pydantic para validação.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"A pasta '{folder_path}' não existe.")

    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    if not csv_files:
        print("Nenhum arquivo CSV encontrado na pasta.")
        return

    for csv_file in csv_files:
        csv_path = os.path.join(folder_path, csv_file)
        print(f"Validando: {csv_file}")

        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            print(f"Erro ao ler o arquivo {csv_file}: {e}")
            continue

        for index, row in df.iterrows():
            try:
                record = model(**row.to_dict())
            except ValidationError as e:
                print(f"Erro de validação na linha {index + 1} do arquivo {csv_file}: {e}")

if __name__ == "__main__":
    folder = "./downloads/extraidos"  # Substitua pelo caminho da pasta desejada
    validate_csv_folder(folder_path=folder, model=Microdados)
