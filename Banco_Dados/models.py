from sqlalchemy import Column, Integer, LargeBinary, String, Date, DateTime,ForeignKey, Boolean, Float, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum as PythonEnum
from datetime import datetime

Base = declarative_base()

class Setores(Base):
    __tablename__ = 'setores'

    id = Column(Integer, primary_key=True)
    nome_setor = Column(String(1000))
    centro_custo = Column(String(255))
    data_geracao = Column(String(255))  # Se quiser armazenar como string formatada
    usuario_geracao = Column(String(255))  # Se quiser armazenar como string formatada
    
    def __init__(self, **kwargs):
        # Garante que a data está no formato correto ao criar novo log
        if 'data_geracao' in kwargs:
            if isinstance(kwargs['data_geracao'], datetime):
                kwargs['data_geracao'] = kwargs['data_geracao'].strftime('%d-%m-%Y %H:%M:%S')
        super().__init__(**kwargs)

class ChecklistItem(Base):
    __tablename__ = 'checklist_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255))  # Descrição do item do checklist
    checked = Column(Boolean, default=False)  # Indica se o item foi verificado
    registro_id = Column(Integer, ForeignKey('registros.id'))  # Chave estrangeira para o registro

    # Relacionamento com a tabela Registro
    registro = relationship("Registro", back_populates="checklist_items")

class LocalizacaoUsuario(Base):
    __tablename__ = 'localizacoes_usuarios'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    registro_id = Column(Integer, ForeignKey('registros.id'), nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    data_registro = Column(DateTime, default=datetime.now)
    usuario = Column(String(255))
    metadados = Column(JSON, name='metadata')  # Renomeado para 'metadados' mas mantém 'metadata' no banco
    
    registro = relationship('Registro', back_populates='localizacoes')

class Equipamento(Base):  # De Equipamentos para Equipamento
    __tablename__ = 'equipamentos'

    id = Column(Integer, primary_key=True)
    tag_equipamento = Column(String(255))
    localizacao = Column(String(255))
    tipo = Column(String(255))
    classe = Column(String(255), default="N/A")
    fabricante = Column(String(255))
    modelo = Column(String(255))
    numero_serie = Column(String(255))
    data_fabricacao = Column(Date)
    peso = Column(String(10), default="N/A")
    teste_hidrostatico_n2 = Column(Date)
    teste_hidrostatico_n3 = Column(Date)
    data_validade = Column(Date)
    status = Column(String(50))
    codigo_barras = Column(String(50))
    patrimonio = Column(String(100))
    criticidade = Column(Integer)    
    foto = Column(String(255))  # caminho da imagem
    observacoes = Column(Text)

    data_ultima_manutencao = Column(Date)
    data_proxima_manutencao = Column(Date)

    data_ultima_inspecao = Column(Date)
    data_proxima_inspecao = Column(Date)

    usuario_geracao = Column(String(255), nullable=False)
    usuario_atualizacao = Column(String(255))

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos atualizados
    inspecoes = relationship("Registro", back_populates="equipamento")
    manutencoes = relationship("Manutencao", back_populates="equipamento")

    def __init__(self, tag_equipamento, localizacao, tipo, classe, fabricante, modelo, numero_serie,
                 data_fabricacao, peso, teste_hidrostatico_n2, criticidade, teste_hidrostatico_n3, data_validade,
                 status, usuario_geracao, codigo_barras=None, patrimonio=None, foto=None,
                 observacoes=None, usuario_atualizacao=None):
        self.tag_equipamento = tag_equipamento
        self.localizacao = localizacao
        self.tipo = tipo
        self.classe = classe
        self.fabricante = fabricante
        self.criticidade = criticidade
        self.modelo = modelo
        self.numero_serie = numero_serie
        self.data_fabricacao = data_fabricacao
        self.peso = peso
        self.teste_hidrostatico_n2 = teste_hidrostatico_n2
        self.teste_hidrostatico_n3 = teste_hidrostatico_n3
        self.data_validade = data_validade
        self.status = status
        self.usuario_geracao = usuario_geracao
        self.usuario_atualizacao = usuario_atualizacao
        self.codigo_barras = codigo_barras
        self.patrimonio = patrimonio
        self.foto = foto
        self.observacoes = observacoes

class FotoRegistro(Base):
    __tablename__ = 'foto_registro'  # Nome corrigido da tabela

    id = Column(Integer, primary_key=True, autoincrement=True)
    registro_id = Column(Integer, ForeignKey('registros.id'), nullable=False)  # Chave estrangeira para o registro
    caminho = Column(String(255), nullable=False)  # Caminho do arquivo da foto

    # Relacionamento com a tabela Registro
    registro = relationship('Registro', back_populates='fotos')

class Registro(Base):
    __tablename__ = 'registros'

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_inspecao = Column(String(255))
    equipamento_id = Column(Integer, ForeignKey('equipamentos.id'))
    responsavel_id = Column(Integer, ForeignKey('usuarios.id'))  # Alterado para FK
    tipo = Column(String(255))
    classe = Column(String(255))
    localizacao = Column(String(255))  # Localização do equipamento
    status_equipamento = Column(String(255))
    criticidade_inspecao = Column(String(255))    
    responsavel = Column(String(255))
    data_registro = Column(Date)
    data_inspecao = Column(Date)
    data_validade_inspecao = Column(Date)
    data_encerramento_inspecao = Column(Date)    
    observacoes = Column(String)
    motivo_acao = Column(String)
    status_inspecao = Column(String)
    usuario_geracao = Column(String(255), nullable=False)

    # Relacionamentos atualizados
    equipamento = relationship("Equipamento", back_populates="inspecoes")
    checklist_items = relationship('ChecklistItem', back_populates='registro')
    fotos = relationship('FotoRegistro', back_populates='registro')
    manutencoes = relationship("Manutencao", back_populates="inspecao")
    localizacoes = relationship('LocalizacaoUsuario', back_populates='registro')

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    primeiro_nome = Column(String(255), nullable=False)
    nome_meio = Column(String(255), nullable=False)
    sobrenome = Column(String(255), nullable=False)    
    nome = Column(String(255), nullable=False)
    matricula = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    setor = Column(String(255), nullable=False)
    usuario = Column(String(255), nullable=False, unique=True)
    senha = Column(LargeBinary, nullable=False)
    nivel_acesso = Column(String(255), nullable=False)
    pergunta_seguranca = Column(String(255))
    resposta_seguranca = Column(String(255))
    tentativas_login = Column(Integer, default=0)
    precisa_redefinir_senha = Column(Boolean, default=False)
    usuario_geracao = Column(String(255), nullable=False)
    foto_perfil = Column(String(255))

    # Relacionamentos atualizados
    manutencoes_responsavel = relationship("Manutencao", back_populates="responsavel")
    status = relationship('StatusUsuario', back_populates='usuario', uselist=False, cascade="all, delete-orphan")

    def define_usuario_precisa_alterar_senha(self, value=True):
        self.precisa_redefinir_senha = value

class StatusUsuario(Base):
    __tablename__ = 'status_usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(10), default="Acesso Liberado")
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuario", back_populates="status")


class AnexoManutencao(Base):
    __tablename__ = 'anexo_manutencao'

    id = Column(Integer, primary_key=True, autoincrement=True)
    manutencao_id = Column(Integer, ForeignKey('manutencoes.id'), nullable=False)
    caminho = Column(String(255), nullable=False)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(50))
    tamanho = Column(Integer)
    data_upload = Column(DateTime, default=func.now())

    # Relacionamento com a tabela Manutencao
    manutencao = relationship('Manutencao', back_populates='anexos')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'caminho': self.caminho,
            'data_upload': self.data_upload.strftime('%Y-%m-%d %H:%M') if self.data_upload else None
        }
    
# Database Model
class Manutencao(Base):
    __tablename__ = 'manutencoes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(String(50), unique=True)
    equipamento_id = Column(Integer, ForeignKey('equipamentos.id'))
    inspecao_id = Column(Integer, ForeignKey('registros.id'))
    tipo_manutencao = Column(String(50))  # Preventiva/Corretiva
    prioridade = Column(String(20))
    status = Column(String(20), default='Aberto')
    responsavel_id = Column(Integer, ForeignKey('usuarios.id'))
    data_abertura = Column(DateTime, default=datetime.now)
    data_limite = Column(DateTime)
    data_conclusao = Column(DateTime)
    descricao = Column(Text)
    comentarios = Column(JSON)  # {usuario: string, comentario: string, data: datetime}
    historico = Column(JSON)  # Registro de alterações
    usuario_geracao = Column(String(255))

    # Relacionamentos atualizados
    equipamento = relationship("Equipamento", back_populates="manutencoes")
    inspecao = relationship("Registro", back_populates="manutencoes")
    responsavel = relationship("Usuario", back_populates="manutencoes_responsavel")
    anexos = relationship('AnexoManutencao', back_populates='manutencao')

class EntradaLog(Base):
    __tablename__ = 'entradas_log'

    id = Column(Integer, primary_key=True)
    mensagem = Column(String(1000))
    usuario = Column(String(255))
    nivel_acesso = Column(String(255))
    tipo_log = Column(String(255))
    data_geracao = Column(String(255))  # Se quiser armazenar como string formatada

    def __init__(self, **kwargs):
        # Garante que a data está no formato correto ao criar novo log
        if 'data_geracao' in kwargs:
            if isinstance(kwargs['data_geracao'], datetime):
                kwargs['data_geracao'] = kwargs['data_geracao'].strftime('%d-%m-%Y %H:%M:%S')
        super().__init__(**kwargs)

class Nivel_Acesso(PythonEnum):
    ADMIN = "Administrador"
    USER = "Operador"
    USERC = "Somente Leitura"


class ChecklistTipo(Base):
    __tablename__ = 'checklists_tipos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_item = Column(String(255), nullable=False)  # Descrição do item do checklist
    ordem = Column(Integer)  # Ordem de exibição dos itens
    obrigatorio = Column(Boolean, default=True)  # Se o item é obrigatório
    tipo_id = Column(Integer, ForeignKey('tipos_equipamentos.id'), nullable=False)

    # Relacionamento com a tabela TiposEquipamentos
    tipo_equipamento = relationship('TiposEquipamentos', back_populates='checklists')
    
class TiposEquipamentos(Base):
    __tablename__ = 'tipos_equipamentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False, unique=True)  # Nome do tipo de equipamento
    descricao = Column(String)  # Descrição detalhada
    validade_inspecao = Column(Integer)  
    status = Column(Boolean, default=True)  # Ativo/Inativo
    usuario_geracao = Column(String(255), nullable=False)  # Usuário que criou o tipo
    data_geracao = Column(DateTime, default=datetime.now)  # Data de criação

    # Relacionamentos
    checklists = relationship('ChecklistTipo', back_populates='tipo_equipamento', 
                            cascade="all, delete-orphan", order_by="ChecklistTipo.ordem")
