from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

class Manutencao(Base):
    __tablename__ = 'manutencao'

    id = Column(Integer, primary_key=True)
    descricao = Column(String(4000))
    data_manutencao = Column(DateTime, default=datetime.now())
    
    # Chave estrangeira para o ativo
    ativo_id = Column(Integer, ForeignKey('ativo.id'), nullable=False)
    
    # Relação com o ativo
    ativo = relationship("Ativo", back_populates="manutencoes")
    
    def __init__(self, descricao:str, data_manutencao:Union[DateTime, None] = None):
       
        self.descricao = descricao
        if data_manutencao:
            self.data_manutencao = data_manutencao
