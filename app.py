from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote

from model import Session
from sqlalchemy.exc import IntegrityError

from model import Ativo, Manutencao 
from logger import logger

from schemas import (
    AtivoSchema, AtivoUpdateSchema, AtivoBuscaSchema, AtivoBuscaFiltroSchema,
    AtivoViewSchema, ListagemAtivosSchema, AtivoDelSchema, 
    ManutencaoSchema, ManutencaoBuscaSchema, ManutencaoUpdateSchema, ManutencaoDelSchema,
    ErrorSchema, apresenta_ativo, apresenta_ativos
)
from flask_cors import CORS

# Imports necessários para o comando init-db
from model import engine
from model.base import Base


info = Info(title="API de Gestão de Ativos de TI", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, resources={r"/*": {"origins": ["null", "*"]}})

# --- COMANDO CLI PARA INICIALIZAR O BANCO DE DADOS ---
@app.cli.command("init-db")
def init_db_command():
    """Cria as tabelas e popula com dados iniciais."""
    print("Iniciando a criação das tabelas no banco de dados...")
    Base.metadata.create_all(engine)
    print("Tabelas 'ativo' e 'manutencao' criadas com sucesso.")

    # Inicia uma sessão com o banco para adicionar os dados
    with Session() as db:
        # Verifica se a tabela de ativos já tem algum dado
        if not db.query(Ativo).first():
            print("Populando o banco de dados com dados de exemplo...")

            # Criando ativos de exemplo
            ativo1 = Ativo(
                nome="Notebook Dell Vostro",
                tag_patrimonio="NTK-001",
                tipo="Eletrônico",
                status="Em uso",
                valor_aquisicao=4500.00
            )
            ativo2 = Ativo(
                nome="Monitor LG UltraWide 29'",
                tag_patrimonio="MON-005",
                tipo="Eletrônico",
                status="Disponível",
                valor_aquisicao=1200.50
            )
            ativo3 = Ativo(
                nome="Cadeira de Escritório Ergonômica",
                tag_patrimonio="CAD-012",
                tipo="Mobiliário",
                status="Em manutenção",
                valor_aquisicao=800.00
            )

            # Adicionando manutenções de exemplo
            manutencao1 = Manutencao(descricao="Troca de pasta térmica e limpeza interna.")
            ativo1.adiciona_manutencao(manutencao1)
            
            manutencao2 = Manutencao(descricao="Reparo no pistão de gás.")
            ativo3.adiciona_manutencao(manutencao2)

            # Adiciona os novos ativos na sessão e commita no banco
            db.add_all([ativo1, ativo2, ativo3])
            db.commit()
            print("Banco de dados populado com sucesso!")
        else:
            print("O banco de dados já contém dados. Nenhuma ação foi tomada.")


# --- DEFINIÇÃO DAS TAGS PARA O SWAGGER ---
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
ativo_tag = Tag(name="Ativo", description="Adição, visualização, atualização e remoção de ativos de TI da base de dados")
manutencao_tag = Tag(name="Manutenção", description="Adição, visualização, atualização e remoção de registros de manutenção")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')


# --- ROTAS DE ATIVO ---

@app.post('/ativo', tags=[ativo_tag],
          responses={"200": AtivoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_ativo(body: AtivoSchema):
    """Adiciona um novo Ativo de TI à base de dados.

    A validação dos dados de entrada é feita automaticamente pela biblioteca
    com base no schema 'AtivoSchema' fornecido como type hint.
    """
    with Session() as db:
        try:
            ativo = Ativo(
                tag_patrimonio=body.tag_patrimonio,
                nome=body.nome,
                tipo=body.tipo,
                status=body.status,
                valor_aquisicao=body.valor_aquisicao
            )
            db.add(ativo)
            db.commit()
            db.refresh(ativo) 
            logger.debug(f"Adicionado ativo com tag: '{ativo.tag_patrimonio}'")
            return apresenta_ativo(ativo), 200
        except IntegrityError:
            db.rollback() 
            error_msg = "Ativo com a mesma tag de patrimônio já salvo na base."
            logger.warning(f"Erro ao adicionar ativo '{body.nome}': {error_msg}")
            return {"message": error_msg}, 409
        except Exception as e:
            db.rollback() 
            error_msg = "Não foi possível salvar novo ativo."
            logger.warning(f"Erro ao adicionar ativo '{body.nome}': {error_msg} - {e}")
            return {"message": error_msg}, 400

@app.get('/ativos', tags=[ativo_tag],
         responses={"200": ListagemAtivosSchema, "404": ErrorSchema})
def get_ativos(query: AtivoBuscaFiltroSchema):
    """Faz a busca por todos os Ativos de TI, permitindo filtragem opcional.
    
    Os filtros são passados como query params e validados pelo schema 'AtivoBuscaFiltroSchema'.
    """
    logger.debug(f"Coletando ativos com base nos filtros: {query}")
    
    with Session() as db:
        db_query = db.query(Ativo)
        
        # Filtro de nome continua com busca parcial (ilike)
        if query.nome:
            search = f"%{query.nome}%"
            db_query = db_query.filter(Ativo.nome.ilike(search))
        
        # CORREÇÃO: Filtro de tipo agora usa comparação exata (==)
        if query.tipo:
            db_query = db_query.filter(Ativo.tipo == query.tipo)
            
        # CORREÇÃO: Filtro de status agora usa comparação exata (==)
        if query.status:
            db_query = db_query.filter(Ativo.status == query.status)

        ativos = db_query.order_by(Ativo.data_insercao.desc()).all()
        
        if not ativos:
            return {"ativos": []}, 200
        else:
            logger.debug(f"{len(ativos)} ativos encontrados")
            return apresenta_ativos(ativos), 200

@app.get('/ativo', tags=[ativo_tag],
         responses={"200": AtivoViewSchema, "404": ErrorSchema})
def get_ativo(query: AtivoBuscaSchema):
    """Faz a busca por um Ativo a partir da sua tag de patrimônio."""
    tag_patrimonio = query.tag_patrimonio
    
    logger.debug(f"Coletando dados sobre o ativo #{tag_patrimonio}")
    with Session() as db:
        ativo = db.query(Ativo).filter(Ativo.tag_patrimonio == tag_patrimonio).first()
        if not ativo:
            error_msg = "Ativo não encontrado na base."
            logger.warning(f"Erro ao buscar ativo '{tag_patrimonio}': {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(f"Ativo encontrado: '{ativo.nome}'")
            return apresenta_ativo(ativo), 200

@app.put('/ativo', tags=[ativo_tag],
         responses={"200": AtivoViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_ativo(query: AtivoBuscaSchema, body: AtivoUpdateSchema):
    """Atualiza as informações de um Ativo de TI a partir da tag de patrimônio."""
    tag_patrimonio = query.tag_patrimonio
    
    logger.debug(f"Atualizando dados do ativo #{tag_patrimonio}")
    with Session() as db:
        ativo = db.query(Ativo).filter(Ativo.tag_patrimonio == tag_patrimonio).first()
        if not ativo:
            error_msg = "Ativo não encontrado na base."
            logger.warning(f"Erro ao atualizar ativo '{tag_patrimonio}', {error_msg}")
            return {"message": error_msg}, 404
        
        # Usa os dados do body para atualizar. a validação já foi feita.
        if body.nome: ativo.nome = body.nome
        if body.tipo: ativo.tipo = body.tipo
        if body.status: ativo.status = body.status
        if body.valor_aquisicao is not None: ativo.valor_aquisicao = body.valor_aquisicao
        
        db.commit()
        db.refresh(ativo)
        logger.debug(f"Ativo atualizado: '{ativo.tag_patrimonio}'")
        return apresenta_ativo(ativo), 200

@app.delete('/ativo', tags=[ativo_tag],
            responses={"200": AtivoDelSchema, "404": ErrorSchema})
def del_ativo(query: AtivoBuscaSchema):
    """Deleta um Ativo a partir da tag de patrimônio informada."""
    tag_patrimonio = query.tag_patrimonio
    
    logger.debug(f"Deletando dados sobre o ativo #{tag_patrimonio}")
    with Session() as db:
        count = db.query(Ativo).filter(Ativo.tag_patrimonio == tag_patrimonio).delete()
        db.commit()
        if count:
            logger.debug(f"Deletado ativo #{tag_patrimonio}")
            return {"message": "Ativo removido", "tag_patrimonio": tag_patrimonio}, 200
        else:
            error_msg = "Ativo não encontrado na base."
            logger.warning(f"Erro ao deletar ativo '{tag_patrimonio}': {error_msg}")
            return {"message": error_msg}, 404

# --- ROTAS DE MANUTENÇÃO ---

@app.post('/manutencao', tags=[manutencao_tag],
          responses={"200": AtivoViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def add_manutencao(body: ManutencaoSchema):
    """Adiciona um novo registro de manutenção a um ativo cadastrado na base."""
    ativo_id = body.ativo_id
    logger.debug(f"Adicionando manutenção ao ativo de ID #{ativo_id}")
    with Session() as db:
        ativo = db.query(Ativo).filter(Ativo.id == ativo_id).first()
        if not ativo:
            error_msg = "Ativo não encontrado na base."
            logger.warning(f"Erro ao adicionar manutenção ao ativo '{ativo_id}': {error_msg}")
            return {"message": error_msg}, 404
        
        manutencao = Manutencao(descricao=body.descricao)
        ativo.adiciona_manutencao(manutencao)
        db.commit()
        db.refresh(ativo)
        logger.debug(f"Adicionada manutenção ao ativo #{ativo_id}")
        return apresenta_ativo(ativo), 200

@app.delete('/manutencao', tags=[manutencao_tag],
            responses={"200": ManutencaoDelSchema, "404": ErrorSchema})
def del_manutencao(query: ManutencaoBuscaSchema):
    """Deleta uma manutenção a partir do seu id."""
    manutencao_id = query.id
    
    logger.debug(f"Deletando manutenção #{manutencao_id}")
    with Session() as db:
        count = db.query(Manutencao).filter(Manutencao.id == manutencao_id).delete()
        db.commit()
        if count:
            logger.debug(f"Deletada manutenção #{manutencao_id}")
            return {"message": "Manutenção removida", "id": int(manutencao_id)}, 200
        else:
            error_msg = "Manutenção não encontrada na base."
            logger.warning(f"Erro ao deletar manutenção '{manutencao_id}': {error_msg}")
            return {"message": error_msg}, 404

@app.put('/manutencao', tags=[manutencao_tag],
         responses={"200": AtivoViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_manutencao(query: ManutencaoBuscaSchema, body: ManutencaoUpdateSchema):
    """Atualiza a descrição de uma manutenção."""
    manutencao_id = query.id
    
    logger.debug(f"Atualizando manutenção #{manutencao_id}")
    with Session() as db:
        manutencao = db.query(Manutencao).filter(Manutencao.id == manutencao_id).first()
        if not manutencao:
            error_msg = "Manutenção não encontrada na base."
            logger.warning(f"Erro ao atualizar manutenção '{manutencao_id}': {error_msg}")
            return {"message": error_msg}, 404
        
        manutencao.descricao = body.descricao
        db.commit()
        db.refresh(manutencao.ativo)
        logger.debug(f"Atualizada manutenção #{manutencao_id}")
        return apresenta_ativo(manutencao.ativo), 200