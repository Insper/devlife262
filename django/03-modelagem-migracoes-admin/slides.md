---
marp: true
theme: default
paginate: true
size: 16:9
header: "Developer Life • Sistemas Web com Django"
footer: "Insper • 03. Modelagem Inicial, Migrações e Admin (Check 2)"
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
# 03. Modelagem Inicial, Migrações e Admin
### Como classes Python viram tabelas no Banco de Dados

**Entrega vinculada:** Check 2 + Exercício *Criando alguns modelos*

---

## Onde estamos na Arquitetura do Django?

<div class="cols">
<div>

Nesta etapa vamos construir a base de persistência:
- Escrevemos uma classe em **`notes/models.py`**.
- O **ORM do Django** traduz essa classe Python para uma **tabela SQL** no arquivo `db.sqlite3`.

![w:440](../assets/tabela.png)

</div>
<div>

![w:460](../assets/django-flow.png)

</div>
</div>

---

## Anatomia do Modelo `Note` (`notes/models.py`)

```python
from django.db import models

class Note(models.Model):                             # (1) Herda de models.Model
    title = models.CharField(max_length=200)          # (2) Coluna de texto curto
    content = models.TextField()                      # (3) Coluna de texto longo
    created_at = models.DateTimeField(auto_now_add=True) # (4) Data e hora automática
```

### O que está acontecendo em cada linha?
- **(1) `models.Model`:** Avisa ao Django que `Note` não é uma classe comum — ela deve ser salva no banco de dados e ganha uma coluna **`id`** numérica automática!
- **(2) `CharField(max_length=200)`:** Cria uma coluna `VARCHAR(200)` para textos curtos (título).
- **(3) `TextField()`:** Cria uma coluna sem limite curto de caracteres para o corpo da anotação.
- **(4) `DateTimeField(auto_now_add=True)`:** Preenche sozinho com a data/hora exata do momento em que a anotação é criada pela primeira vez.

---

## Comparando Tipos e Parâmetros de Campos

| Dúvida comum | Opção A | Opção B | Qual usar no Get-it? |
| :--- | :--- | :--- | :--- |
| **Texto curto vs. longo** | `CharField(max_length=N)` | `TextField()` | `CharField` no `title` e `TextField` no `content`. |
| **Data vs. Data e Hora** | `DateField` (só dia/mês/ano) | `DateTimeField` (dia + horário) | `DateTimeField` para saber o horário exato de criação. |
| **`auto_now_add` vs. `auto_now`** | `auto_now_add=True` (fixa na **criação**) | `auto_now=True` (atualiza em **toda edição**) | `auto_now_add=True` para o campo `created_at`. |

---

## Por que precisamos de Migrações? (`makemigrations` vs `migrate`)

Salvar o arquivo `notes/models.py` **ainda não toca no banco de dados**! O processo ocorre em 2 passos:

```bash
python manage.py makemigrations   # Passo 1: Gera o código da mudança
python manage.py migrate          # Passo 2: Executa a mudança no banco
```

### O que acontece por baixo dos panos?
1. **`makemigrations`:** O Django compara o seu `models.py` atual com o histórico anterior e cria um arquivo `notes/migrations/0001_initial.py` (como uma "planta arquitetônica" da tabela).
2. **`migrate`:** O Django lê os arquivos da pasta `migrations/` que ainda não foram rodados e cria de fato a tabela `notes_note` dentro do arquivo `db.sqlite3`.

<div class="warn">
<strong>Erro clássico:</strong> <code>OperationalError: no such table: notes_note</code> $\rightarrow$ Significa que você criou ou alterou o modelo, mas esqueceu de rodar <code>makemigrations</code> e <code>migrate</code>!
</div>

---

## Explorando o Banco com o Django Admin

O Django já traz um site administrativo pronto para testarmos o banco sem precisar criar telas antes:

<div class="cols">
<div>

**1. Criar conta de administrador:**
```bash
python manage.py createsuperuser
```

**2. Liberar o modelo `Note` no Admin:**
Arquivo: **`notes/admin.py`**
```python
from django.contrib import admin
from .models import Note

admin.site.register(Note)
```

</div>
<div>

### O que `admin.site.register(Note)` faz?
- Diz ao Django Admin para inspecionar os campos de `Note` (`title`, `content`) e **gerar automaticamente** telas de listagem, criação, edição e remoção em `http://localhost:8000/admin/`!

</div>
</div>

---

## Como o Método `__str__` Muda o Nome no Admin?

<div class="cols">
<div>

Para exibir qualquer objeto na tela, o Django chama `str(note)`. Por padrão, isso retorna `Note object (1)`.

Sobrescrevendo `__str__` em **`notes/models.py`**:
```python
class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.id}. {self.title}"
```
*(Alterar métodos como `__str__` não muda colunas da tabela, então não precisa de nova migração!)*

</div>
<div>

**Antes (`Note object (x)`):**
![w:380](../assets/django-admin.png)

**Depois (`ID. TITULO`):**
![w:380](../assets/admin-com-nomes.png)

</div>
</div>

---

## Hora da Prática: Exercício + Check 2

<div class="cols">
<div>

### Exercício no VS Code: `Produto`
Em `produtos/models.py`:
- `nome`: `CharField(max_length=100)`
- `descricao`: `TextField(blank=True)` *(permite deixar em branco)*
- `preco`: `DecimalField(max_digits=7, decimal_places=2)`
- `foto`: `ImageField(upload_to='uploads/imgs/')`
- `ultima_modificacao`: `DateTimeField(auto_now=True)`

</div>
<div>

### Checklist do Check 2
1. App `notes` criado e em `INSTALLED_APPS`
2. Classe `Note` (`title`, `content`, `created_at`)
3. `makemigrations` + `migrate` executados
4. Superusuário criado (`createsuperuser`)
5. `admin.site.register(Note)` em `notes/admin.py`
6. 5 anotações cadastradas pelo `/admin/`
7. Método `__str__` retornando `f"{self.id}. {self.title}"`

</div>
</div>
