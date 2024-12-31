from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal
from datetime import datetime

class DadosCenso(BaseModel):

    @model_validator(mode='before')
    def transformar_para_minusculo(cls, values):
        """
        Converte todos os campos para minúsculo para garantir consistência com o banco de dados PostgreSQL.
        """
        return {k.lower(): v for k, v in values.items()}

    @model_validator(mode='before')
    def validar_sg_ies(cls, values):
        """
        Valida o campo SG_IES. Se o valor não for uma string, 
        o campo será definido como None.
        """
        sg_ies = values.get('sg_ies')
        if sg_ies is not None and not isinstance(sg_ies, str):
            values['sg_ies'] = None
        return values
    
    @model_validator(mode='before')
    def transformar_categoria_administrativa(cls, values):
        """
        Altera o termo 'Privada com fins lucrativos' para apenas 'Privada' em no_categoria_administrativa
        """
        categoria = values.get('no_categoria_administrativa')
        if categoria == 'Privada com fins lucrativos':
            values['no_categoria_administrativa'] = 'Privada'
        return values

    nu_ano_censo: int = Field(
        ..., 
        description="Ano do censo.",
        ge=2010, 
        le=datetime.now().year
    )
    co_ies: int = Field(..., description="Código da Instituição de Ensino Superior.", ge=1)
    no_ies: str = Field(..., description="Nome da Instituição de Ensino Superior.", max_length=255)
    sg_ies: Optional[str] = Field(None, description="Sigla da Instituição de Ensino Superior.")
    no_categoria_administrativa: Literal[
        'Pública Federal', 
        'Pública Estadual', 
        'Privada sem fins lucrativos', 
        'Pública Municipal', 
        'Privada com fins lucrativos',
        'Privada'
    ] = Field(..., description="Categoria administrativa da instituição.")
    no_organizacao_academica: str = Field(..., description="Organização acadêmica da instituição.", max_length=255)
    no_regiao: str = Field(..., description="Nome da região onde a instituição está localizada.", max_length=50)
    no_uf: Literal[
        'Mato Grosso', 'Distrito Federal', 'Sergipe', 'Amazonas', 'Piauí',
        'Minas Gerais', 'São Paulo', 'Paraná', 'Pernambuco', 'Rio Grande do Sul',
        'Rio de Janeiro', 'Bahia', 'Ceará', 'Alagoas', 'Pará', 'Santa Catarina',
        'Goiás', 'Rio Grande do Norte', 'Espírito Santo', 'Paraíba',
        'Mato Grosso do Sul', 'Rondônia', 'Tocantins', 'Maranhão', 'Acre', 
        'Roraima', 'Amapá'
    ] = Field(..., description="Unidade Federativa (UF) onde a instituição está localizada.")
    percentual_total: float = Field(..., description="Percentual total de algo especificado no censo.", ge=0.0, le=100.0)
    percentual_mestrado: float = Field(..., description="Percentual de mestres na instituição.", ge=0.0, le=100.0)
    percentual_doutorado: float = Field(..., description="Percentual de doutores na instituição.", ge=0.0, le=100.0)
