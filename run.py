#!/usr/bin/env python3
"""
TaskFlow - Sistema de Gerenciamento de Tarefas
Script de inicialização simplificado
"""

import os
import sys

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário. Versão atual:", sys.version.split()[0])
        return False
    print(f"✅ Python {sys.version.split()[0]} encontrado")
    return True

def check_virtual_env():
    """Verifica se está executando em um ambiente virtual"""
    # Verificação mais robusta para ambiente virtual
    in_venv = (
        hasattr(sys, 'real_prefix') or 
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
        os.environ.get('VIRTUAL_ENV') is not None
    )
    
    if not in_venv:
        print("⚠️  ATENÇÃO: Recomendamos executar em um ambiente virtual")
        print("   Para criar: python3 -m venv venv")
        print("   Para ativar (Linux/Mac): source venv/bin/activate")
        print("   Para ativar (Windows): .\\venv\\Scripts\\activate")
        print()
        print("💡 Ou use os scripts automáticos: ./setup.sh e ./start.sh")
        print()
        
        # Em modo não-interativo, continuar automaticamente
        if os.getenv('FLASK_ENV') == 'production' or '--auto' in sys.argv:
            print("🔄 Continuando automaticamente...")
            return True
            
        try:
            response = input("Deseja continuar mesmo assim? (s/N): ").lower()
            if response not in ['s', 'sim', 'y', 'yes']:
                print("👋 Configuração cancelada. Use: source venv/bin/activate")
                return False
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Configuração cancelada.")
            return False
    else:
        print("✅ Ambiente virtual ativo")
    
    return True

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    required_packages = [
        'flask',
        'flask_sqlalchemy',
        'werkzeug'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} encontrado")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} não encontrado")
    
    if missing_packages:
        print("\n🔧 Dependências faltando!")
        print("Execute: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Função principal para inicializar a aplicação"""
    print("🚀 Iniciando TaskFlow...")
    print("=" * 50)
    
    # Verificar versão do Python
    if not check_python_version():
        return
    
    # Verificar ambiente virtual
    if not check_virtual_env():
        return
    
    # Verificar dependências
    if not check_dependencies():
        return
    
    # Importar e executar aplicação
    try:
        print("\n🔄 Carregando aplicação...")
        from main import create_app
        app = create_app()
        
        print("🌟 TaskFlow iniciado com sucesso!")
        print("📍 Acesse: http://localhost:5000")
        print("🔧 Modo Debug: Ativado")
        print("=" * 50)
        print("💡 Pressione Ctrl+C para parar a aplicação")
        print()
        
        # Configurações para evitar loops de reinicialização
        app.run(
            debug=True, 
            host='0.0.0.0', 
            port=5000, 
            use_reloader=False,  # Desabilita auto-reload para estabilidade
            threaded=True
        )
        
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("💡 Verifique se todas as dependências estão instaladas")
        print("💡 Execute: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
        print("💡 Verifique o log de erros acima para mais detalhes")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Aplicação encerrada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("💡 Contate o suporte técnico se o problema persistir") 