# CONFIGURAÇÃO do Flask
# Centralizar configurações em uma classe evita valores espalhados pelo código.
# Em produção, os valores sensíveis devem vir de variáveis de ambiente:
#   import os
#   SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
import secrets


class Config:
    # SECRET_KEY é usada pelo Flask para:
    #   - Assinar cookies de sessão (session[])
    #   - Proteger mensagens flash (flash())
    #   - Qualquer dado que precise de assinatura criptográfica
    # secrets.token_hex(32) gera 64 caracteres hexadecimais aleatórios.
    # ATENÇÃO: em produção, use uma chave fixa e guarde em variável de ambiente!
    SECRET_KEY = secrets.token_hex(32)

    # Exemplo de configuração para banco de dados SQLite:
    # SQLALCHEMY_DATABASE_URI = "sqlite:///tarefas.db"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False  # desativa aviso desnecessário
