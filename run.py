# PONTO DE ENTRADA da aplicação
# Este arquivo é o que você executa no terminal: python run.py
from app import create_app

# Chama a fábrica de aplicação definida em app/__init__.py
app = create_app()

if __name__ == "__main__":
    # debug=True ativa:
    #   - Recarregamento automático ao salvar arquivos (hot reload)
    #   - Página de erro detalhada no navegador
    # NUNCA use debug=True em produção!
    app.run(debug=True)
