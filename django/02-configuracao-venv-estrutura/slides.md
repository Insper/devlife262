---
marp: true
theme: default
paginate: true
size: 16:9
header: "Developer Life • Sistemas Web com Django"
footer: "Insper • 02. Configuração, Venv e Estrutura (Check 1)"
style: |
  section {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 24px;
  }
  h1 { color: #092e20; }
  h2 { color: #0c4b33; border-bottom: 2px solid #44b78b; padding-bottom: 6px; }
  code { background: #f0f4f2; color: #0c4b33; padding: 2px 6px; border-radius: 4px; }
  pre code { background: transparent; color: inherit; }
  .cols { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; align-items: center; }
  .box { background: #f4fbf7; border-left: 5px solid #44b78b; padding: 12px 16px; border-radius: 6px; margin-top: 10px; }
  .warn { background: #fff8e6; border-left: 5px solid #f59e0b; padding: 12px 16px; border-radius: 6px; margin-top: 10px; }
  table { font-size: 21px; width: 100%; }
---

<!-- _class: lead -->
# 02. Configuração, Venv e Estrutura
### O que cada comando cria e como os arquivos se conectam

**Entrega vinculada:** Check 1

---

## O que é o `venv` e por que usamos?

<div class="cols">
<div>

### O que acontece sem `venv`?
- Todos os pacotes (`pygame`, `django`) vão para a mesma pasta global do computador.
- Se um projeto antigo exigir Django 4 e um novo exigir Django 6, um quebra o outro.

### O que o `venv` faz nos bastidores?
- Cria uma pasta `.venv` dentro do projeto com uma **cópia isolada do Python e do `pip`**.
- Tudo que instalamos com o `venv` ativo fica restrito apenas a este projeto!

</div>
<div>

![w:460](../assets/python_venv.jpg)

</div>
</div>

---

## Anatomia dos Comandos do `venv`

<div class="cols">
<div>

**macOS / Linux:**
```bash
python3 -m venv .venv --prompt .   # (1)
. .venv/bin/activate               # (2)
pip install -r requirements.txt    # (3)
```

**Windows (PowerShell):**
```powershell
python3 -m venv .venv --prompt .   # (1)
. .venv\Scripts\Activate.ps1       # (2)
pip install -r requirements.txt    # (3)
```

</div>
<div>

### O que cada linha faz?
1. **`-m venv .venv`:** Cria a pasta `.venv` com o Python isolado.
2. **`activate`:** Faz o seu terminal passar a usar o Python de dentro da `.venv` (precisa rodar sempre que abrir um terminal novo!).
3. **`pip install -r requirements.txt`:** Lê a lista de pacotes do arquivo `requirements.txt` e instala todos de uma vez.

</div>
</div>

---

## Gerando o Projeto: O que `startproject` faz?

```bash
django-admin startproject getit .
```

- **`django-admin`:** Ferramenta instalada pelo pacote Django para criar estruturas iniciais (*boilerplate*).
- **`startproject getit`:** Cria o pacote principal de configuração chamado `getit`.
- **O ponto `.` no final:** Diz *"crie os arquivos diretamente na pasta atual"*. (Sem o `.`, ele criaria `pasta-atual/getit/getit/settings.py`).

```text
pasta-do-projeto/
├── .venv/               # Ambiente virtual isolado
├── manage.py            # Controle remoto do nosso projeto Django
└── getit/               # Pacote de configuração do projeto
    ├── __init__.py      # Indica ao Python que a pasta getit é um módulo importável
    ├── settings.py      # Painel de controle: apps instalados, banco de dados, idioma
    ├── urls.py          # Porta de entrada de todas as rotas da aplicação
    └── wsgi.py / asgi.py# Conector usado no deploy em servidores de produção
```

---

## O que acontece quando rodamos `runserver`? (Check 1)

<div class="cols">
<div>

```bash
python manage.py runserver
```

### Nos bastidores:
1. O `manage.py` lê as configurações em `getit/settings.py`.
2. Inicia um servidor web local escutando na porta **`8000`**.
3. Fica monitorando seus arquivos `.py`: sempre que você salva uma alteração, ele **reinicia sozinho**!

<div class="box">
<strong>Check 1:</strong> Acesse <code>http://localhost:8000</code> e mostre a página do foguete funcionando!
</div>

</div>
<div>

![w:440](../assets/django-page.png)

</div>
</div>

---

## Projeto vs. App: Qual a diferença?

<div class="cols">
<div>

- **Projeto (`getit`):** É a casca do sistema inteiro (configurações globais, conexão com banco, lista de rotas raiz).
- **App (`notes`):** É um módulo focado em uma funcionalidade específica (no nosso caso, cuidar das anotações).

```bash
python manage.py startapp notes
```
> Cria a pasta `notes/` com `models.py`, `views.py`, `admin.py` e `apps.py`.

</div>
<div>

![w:440](../assets/projeto_app.jpg)

</div>
</div>

---

## Conectando o App ao Projeto (`settings.py`)

Criar a pasta `notes/` com `startapp` **não** conecta o app automaticamente ao projeto. Precisamos avisar o Django no `getit/settings.py`:

```python
# Arquivo: getit/settings.py
INSTALLED_APPS = [
    'notes.apps.NotesConfig',    # (1) Conecta a classe NotesConfig criada em notes/apps.py
    'django.contrib.admin',      # (2) App nativo da interface de administração
    'django.contrib.auth',       # (3) App nativo de usuários, senhas e login
    'django.contrib.staticfiles',# (4) App nativo para servir CSS e imagens
    ...
]
```

<div class="warn">
<strong>O que acontece se esquecer este passo?</strong><br>
Quando você criar modelos ou templates dentro de <code>notes/</code>, o Django vai ignorá-los completamente (gerando erros como <code>TemplateDoesNotExist</code> ou não criando tabelas no banco)!
</div>
