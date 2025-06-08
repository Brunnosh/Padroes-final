#!/usr/bin/env python3
"""
TaskFlow - Script de Desenvolvimento Simplificado
Para uso quando há problemas com o script principal
"""

import os
import sys

def main():
    """Inicialização simplificada para desenvolvimento"""
    print("🚀 TaskFlow - Modo Desenvolvimento")
    print("=" * 40)
    
    try:
        # Verificação simples de dependências
        import flask
        import flask_sqlalchemy
        print("✅ Dependências OK")
        
        # Importar e executar aplicação
        from main import create_app
        app = create_app()
        
        print("\n✅ Aplicação carregada com sucesso!")
        print("📍 Acesse: http://localhost:5000")
        print("🔧 Modo: Desenvolvimento estável")
        print("=" * 40)
        print("💡 Para parar: Ctrl+C")
        print()
        
        # Executar com configurações estáveis
        app.run(
            debug=True,
            host='127.0.0.1',  # Localhost apenas
            port=5000,
            use_reloader=False,  # Sem auto-reload
            threaded=True
        )
        
    except ImportError as e:
        print(f"❌ Erro: {e}")
        print("💡 Execute: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code or 0)
    except KeyboardInterrupt:
        print("\n\n👋 Aplicação encerrada")
        sys.exit(0) 