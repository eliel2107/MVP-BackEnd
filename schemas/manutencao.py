from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ManutencaoSchema(BaseModel):
    """ Define como um novo registro de manutenção a ser inserido deve ser representado.
    """
    ativo_id: int
    descricao: str


class ManutencaoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca, que será
        feita com base no ID da manutenção.
    """
    id: int


class ManutencaoUpdateSchema(BaseModel):
    """ Define como os dados para atualização de uma manutenção serão representados.
    """
    descricao: str

class ManutencaoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção de manutenção.
    """
    message: str
    id: int

