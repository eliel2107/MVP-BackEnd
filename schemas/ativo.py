from pydantic import BaseModel
from typing import Optional, List
from schemas.manutencao import ManutencaoSchema


class AtivoSchema(BaseModel):
    """ Define como um novo ativo de TI a ser inserido deve ser representado.
    """
    nome: str 
    tipo: str 
    tag_patrimonio: str 
    status: Optional[str] 
    valor_aquisicao: float 


class AtivoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por tag.
    """
    tag_patrimonio: str


class AtivoBuscaFiltroSchema(BaseModel):
    """ Define a estrutura para a busca com filtros opcionais.
    """
    nome: Optional[str] = None
    tipo: Optional[str] = None
    status: Optional[str] = None


class ListagemAtivosSchema(BaseModel):
    """ Define como uma listagem de ativos será retornada.
    """
    ativos: List[AtivoSchema]


class AtivoViewSchema(BaseModel):
    """ Define como um ativo será retornado: ativo + registros de manutenção.
    """
    id: int 
    nome: str 
    tipo: str 
    tag_patrimonio: str 
    status: Optional[str] 
    valor_aquisicao: float 
    total_manutencoes: int 
    manutencoes: List[ManutencaoSchema]


class AtivoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    tag_patrimonio: str

class AtivoUpdateSchema(BaseModel):
    """ Define como os dados para atualização de um ativo serão representados.
        Todos os campos são opcionais.
    """
    nome: Optional[str] = None
    tipo: Optional[str] = None
    status: Optional[str] = None
    valor_aquisicao: Optional[float] = None

