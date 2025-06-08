#!/bin/bash

echo "🚀 TaskFlow - Setup Automatizado"
echo "=================================="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3."
    exit 1
fi

echo "✅ Python 3 encontrado"

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
else
    echo "✅ Ambiente virtual já existe"
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo "⬆️ Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt

echo ""
echo "🎉 Setup concluído com sucesso!"
echo ""
echo "Para executar a aplicação:"
echo "1. Ative o ambiente virtual: source venv/bin/activate"
echo "2. Execute: python3 main.py"
echo ""
echo "Ou use o script: ./start.sh" 