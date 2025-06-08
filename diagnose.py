#!/usr/bin/env python3
"""
TaskFlow - Script de Diagnóstico
Identifica e resolve problemas comuns de configuração
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python():
    """Verifica a versão do Python"""
    print("🐍 Verificando Python...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} muito antigo")
        print("💡 Instale Python 3.8+")
        return False

def check_venv():
    """Verifica o ambiente virtual"""
    print("\n📦 Verificando ambiente virtual...")
    
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Ambiente virtual não encontrado")
        print("💡 Execute: python3 -m venv venv")
        return False
    
    # Verificar se está ativo
    in_venv = (
        hasattr(sys, 'real_prefix') or 
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
        os.environ.get('VIRTUAL_ENV') is not None
    )
    
    if in_venv:
        print("✅ Ambiente virtual ativo")
        return True
    else:
        print("⚠️ Ambiente virtual existe mas não está ativo")
        print("💡 Execute: source venv/bin/activate")
        return False

def check_dependencies():
    """Verifica as dependências"""
    print("\n📚 Verificando dependências...")
    
    required = ["flask", "flask_sqlalchemy", "werkzeug", "python_dotenv"]
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n💡 Dependências faltando: {', '.join(missing)}")
        print("💡 Execute: pip install -r requirements.txt")
        return False
    
    return True

def check_files():
    """Verifica arquivos essenciais"""
    print("\n📁 Verificando arquivos...")
    
    essential_files = [
        "main.py", "run.py", "dev.py", "requirements.txt",
        "domain/entities.py", "application/use_cases.py",
        "infrastructure/database.py", "presentation/controllers.py"
    ]
    
    missing = []
    for file_path in essential_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing.append(file_path)
    
    if missing:
        print(f"\n💡 Arquivos faltando: {', '.join(missing)}")
        return False
    
    return True

def check_port():
    """Verifica se a porta 5000 está livre"""
    print("\n🌐 Verificando porta 5000...")
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 5000))
        sock.close()
        
        if result == 0:
            print("⚠️ Porta 5000 está ocupada")
            print("💡 Pare outras aplicações ou use outra porta")
            return False
        else:
            print("✅ Porta 5000 livre")
            return True
    except Exception:
        print("⚠️ Não foi possível verificar a porta")
        return True

def suggest_solution():
    """Sugere a melhor solução baseada nos problemas encontrados"""
    print("\n" + "="*50)
    print("🎯 DIAGNÓSTICO COMPLETO")
    print("="*50)
    
    # Verificar tudo
    python_ok = check_python()
    venv_ok = check_venv()
    deps_ok = check_dependencies()
    files_ok = check_files()
    port_ok = check_port()
    
    print("\n" + "="*50)
    print("💡 SOLUÇÕES RECOMENDADAS")
    print("="*50)
    
    if not python_ok:
        print("🔴 CRÍTICO: Atualize o Python para 3.8+")
        return
    
    if not files_ok:
        print("🔴 CRÍTICO: Arquivos essenciais faltando")
        print("💡 Baixe novamente o projeto ou verifique se está no diretório correto")
        return
    
    if not venv_ok:
        print("🟡 SETUP: Configure o ambiente virtual")
        print("💡 Execute:")
        print("   python3 -m venv venv")
        print("   source venv/bin/activate")
        print("   pip install -r requirements.txt")
        print("   python dev.py")
        return
    
    if not deps_ok:
        print("🟡 DEPENDÊNCIAS: Instale as dependências")
        print("💡 Execute:")
        print("   pip install -r requirements.txt")
        print("   python dev.py")
        return
    
    if not port_ok:
        print("🟡 PORTA: Conflito na porta 5000")
        print("💡 Execute em outra porta:")
        print("   python dev.py")
        return
    
    # Tudo OK
    print("🟢 TUDO OK: Sistema pronto para uso!")
    print("💡 Execute:")
    print("   python dev.py")
    print("\n✨ Se ainda houver problemas de reinicialização,")
    print("   use sempre 'python dev.py' em vez de 'python run.py'")

def main():
    """Função principal"""
    print("🔍 TaskFlow - Diagnóstico do Sistema")
    print("="*50)
    
    suggest_solution()
    
    print("\n" + "="*50)
    print("🚀 Pronto para começar!")
    print("="*50)

if __name__ == "__main__":
    main() 