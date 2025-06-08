# 🚀 Guia de Início Rápido - TaskFlow

## 🎯 Solução Rápida (se está com problemas)
```bash
source venv/bin/activate
python dev.py
```

## 🔍 Diagnóstico Automático
```bash
python diagnose.py  # Identifica e resolve problemas
```

## ⚡ Instalação e Execução em 3 Passos

### 1. Setup Automático
```bash
./setup.sh
```

### 2. Iniciar Aplicação
```bash
python dev.py  # Versão estável recomendada
```

### 3. Acessar
Abra: `http://localhost:5000`

---

## 🔧 Problemas Comuns

### ❌ "Aplicação para/reinicia instantaneamente"
**Causa**: Problemas de auto-reload do Flask ou ambiente virtual

**Soluções**:

**Opção 1 - Script estável:**
```bash
python dev.py  # Versão sem auto-reload
```

**Opção 2 - Setup completo:**
```bash
# 1. Criar ambiente virtual
python3 -m venv venv

# 2. Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# OU
.\venv\Scripts\activate   # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar versão estável
python dev.py
```

**Opção 3 - Automática:**
```bash
./setup.sh && python dev.py
```

### ❌ "Python/Flask não encontrado"
**Solução**:
```bash
# Use python3 em vez de python
python3 run.py

# Ou instale as dependências
pip install flask flask-sqlalchemy python-dotenv
```

### ❌ "Permission denied" nos scripts
**Solução**:
```bash
chmod +x setup.sh start.sh
```

### ❌ "Problemas de contraste/visibilidade"
**Solução**:
```bash
# Atualize a página após mudanças
Ctrl+F5 (Windows/Linux) ou Cmd+Shift+R (Mac)
```
**Para cards de estatísticas especificamente**:
```bash
# Force refresh completo para carregar novo CSS
Ctrl+Shift+F5 (Windows/Linux) ou Cmd+Shift+R (Mac)
```
**Detalhes**: Veja `ACESSIBILIDADE.md` para mais informações

### ❌ "Cards de estatísticas com texto claro"
**Causa**: Cache do navegador não carregou o CSS de contraste
**Solução**:
```bash
# Force refresh total
Ctrl+Shift+F5
```
**Resultado esperado**: Números brancos em fundos coloridos

---

## 📋 Comandos Essenciais

| Comando | Descrição |
|---------|-----------|
| `python diagnose.py` | **Diagnóstico automático** |
| `python dev.py` | **Execução estável (recomendado)** |
| `./setup.sh` | Configuração automática |
| `./start.sh` | Iniciar aplicação (padrão) |
| `python run.py` | Execução com verificações |
| `source venv/bin/activate` | Ativar ambiente virtual |
| `deactivate` | Desativar ambiente virtual |

---

## 🎮 Modos de Execução

### 🥇 Modo Estável (Recomendado)
```bash
python dev.py
```
- ✅ Sem auto-reload problemático
- ✅ Inicialização rápida  
- ✅ Ideal para desenvolvimento e testes

### 🔧 Modo Completo
```bash
python run.py
```
- ✅ Verificações completas de ambiente
- ✅ Detecção de problemas
- ⚠️ Pode ter problemas de auto-reload

### 🤖 Modo Automático
```bash
./start.sh
```
- ✅ Executa verificações e inicia
- ✅ Fácil de usar
- ⚠️ Depende do script funcionar

---

## 🎯 Verificação Manual

1. **Python instalado?**
   ```bash
   python3 --version
   ```

2. **Ambiente virtual ativo?**
   ```bash
   which python  # Deve mostrar caminho do venv
   ```

3. **Dependências instaladas?**
   ```bash
   pip list | grep -i flask
   ```

4. **Aplicação funcionando?**
   ```bash
   curl http://localhost:5000
   ```

---

## 💡 Dicas

- **Sempre use ambiente virtual** para evitar conflitos
- **Execute scripts com ./script.sh** não apenas `script.sh`
- **Use python3** em sistemas Linux/Mac
- **Acesse localhost:5000** após iniciar

---

## 🆘 Ainda com problemas?

### 🎯 Solução Direta (99% dos casos)
```bash
source venv/bin/activate
python dev.py
```

### 🔍 Diagnóstico Completo
1. Verifique se tem Python 3.8+: `python3 --version`
2. Ative o ambiente virtual: `source venv/bin/activate`
3. Instale dependências: `pip install -r requirements.txt`
4. Use o modo estável: `python dev.py`
5. Se não funcionar, verifique os logs de erro

### ⚡ Reset Completo
```bash
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python dev.py
``` 