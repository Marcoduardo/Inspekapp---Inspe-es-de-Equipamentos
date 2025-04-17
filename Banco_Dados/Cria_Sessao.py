from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from Banco_Dados.models import Base

def obter_sessao():
    try:
        # Configuração centralizada do banco de dados
        db_config = {
            'tipo_banco': 'sqlite',
            'nome_banco': 'Banco_Dados//InspekApp.db'
        }

        # Criação da engine com timeout configurado (exemplo: 30 segundos)
        engine = create_engine(f"{db_config['tipo_banco']}:///{db_config['nome_banco']}", connect_args={'timeout': 30})
        
        # Criação das tabelas se não existirem
        Base.metadata.create_all(engine)

        # Criação da sessão usando o sessionmaker
        Session = sessionmaker(bind=engine)
        
        # Retornar uma nova instância da sessão
        return Session()

    except OperationalError as op_err:
        # Captura específica para OperationalError (SQLite database is locked)
        print(f"Erro de operação no banco de dados: {op_err}")
        return None
    except SQLAlchemyError as e:
        # Captura geral para outros erros SQLAlchemy
        print(f"Erro ao obter a sessão: {e}")
        return None
    
# Abre a Sessão
session = obter_sessao()
