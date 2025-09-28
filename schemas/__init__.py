from typing import List
from model.ativo import Ativo
from schemas.manutencao import (
    ManutencaoSchema, 
    ManutencaoBuscaSchema, 
    ManutencaoUpdateSchema,
    ManutencaoDelSchema
)
from schemas.ativo import (
    AtivoSchema, 
    AtivoUpdateSchema, 
    AtivoBuscaSchema, 
    AtivoViewSchema,
    ListagemAtivosSchema, 
    AtivoDelSchema,
    AtivoBuscaFiltroSchema
)
from schemas.error import ErrorSchema

def apresenta_ativo(ativo: Ativo):
    """ Retorna uma representação do ativo seguindo o schema definido em
        AtivoViewSchema.
    """
    return {
        "id": ativo.id,
        "nome": ativo.nome,
        "tipo": ativo.tipo,
        "tag_patrimonio": ativo.tag_patrimonio,
        "status": ativo.status,
        "valor_aquisicao": ativo.valor_aquisicao,
        "total_manutencoes": len(ativo.manutencoes),
        "manutencoes": [
            {
                "id": m.id,
                "descricao": m.descricao, 
                "data_manutencao": m.data_manutencao.strftime('%Y-%m-%d %H:%M:%S')
            } for m in ativo.manutencoes
        ]
    }

def apresenta_ativos(ativos: List[Ativo]):
    """ Retorna uma representação dos ativos seguindo o schema definido em
        AtivoViewSchema.
    """
    result = []
    for ativo in ativos:
        result.append(apresenta_ativo(ativo))

    return {"ativos": result}

