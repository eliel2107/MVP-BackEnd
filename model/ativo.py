from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

class Ativo(Base):
    __tablename__ = 'ativo'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140), nullable=False)
    tipo = Column(String(50), nullable=False)
    tag_patrimonio = Column(String(50), unique=True, nullable=False)
    status = Column(String(50))
    valor_aquisicao = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

    # Relação com a tabela de manutenções
    manutencoes = relationship("Manutencao", back_populates="ativo", cascade="all, delete-orphan")

    def __init__(self, nome:str, tipo:str, tag_patrimonio:str, status:str, valor_aquisicao:float,
                 data_insercao:Union[DateTime, None] = None):

        self.nome = nome
        self.tipo = tipo
        self.tag_patrimonio = tag_patrimonio
        self.status = status
        self.valor_aquisicao = valor_aquisicao
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_manutencao(self, manutencao):
        """ Adiciona um novo registro de manutenção ao Ativo
        """
        self.manutencoes.append(manutencao)
