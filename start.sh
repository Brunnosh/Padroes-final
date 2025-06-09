#!/bin/bash

echo "🚀 Iniciando TaskFlow..."

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "💡 Execute primeiro: ./setup.sh"
    exit 1
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Verificar se as dependências estão instaladas
if ! python -c "import flask" 2>/dev/null; then
    echo "❌ Dependências não instaladas!"
    echo "💡 Execute: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Dependências verificadas"

# Executar aplicação
echo "🌟 Iniciando aplicação..."
python3 main.py 