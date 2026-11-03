---
marp: true
theme: default
paginate: true
size: 16:9
header: "Developer Life • Sistemas Web com Django"
footer: "Insper • 07. Formulários e o Método POST (Check 6)"
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
# 07. Formulários e o Método POST
### Como os dados digitados pelo usuário viajam até o Banco de Dados

**Entrega vinculada:** Check 6

---

## Verbos HTTP: Qual a Diferença entre `GET` e `POST`?

Toda requisição HTTP carrega um **verbo** que indica a intenção do navegador:

| Situação | Verbo HTTP | O que acontece? |
| :--- | :---: | :--- |
| Você digita `http://localhost:8000/` na barra de endereço ou clica em um link `<a>` | **`GET`** | O navegador está **pedindo para ler** uma página. Nenhuma anotação nova é criada. |
| Você preenche o formulário e clica no botão `<input type="submit">` | **`POST`** | O navegador está **enviando dados** no pacote da requisição para **criar/modificar** algo no servidor. |

---

## Anatomia do `<form>`: O que cada atributo faz?

**Arquivo:** `notes/templates/notes/index.html`
```html
<form method="post" action="/">                         <!-- (1) Verbo e destino -->
  {% csrf_token %}                                      <!-- (2) Crachá de segurança -->
  <label for="titulo">Título</label>
  <input id="titulo" type="text" name="titulo" />       <!-- (3) Chave "titulo" -->

  <label for="detalhes">Detalhes</label>
  <textarea id="detalhes" name="detalhes"></textarea>   <!-- (4) Chave "detalhes" -->

  <input type="submit" value="Criar" />                 <!-- (5) Dispara o envio -->
</form>
```

- **(1) `method="post" action="/"`:** Envia uma requisição `POST` para a rota `/`.
- **(2) `{% csrf_token %}`:** Gera um `<input type="hidden">` com uma chave secreta que prova ao Django que o formulário veio do nosso próprio site (evita o erro **403 Forbidden**).
- **(3) e (4) `id` vs. `name`:** O `id` serve apenas para o `<label for="...">` no HTML; já o **`name` é fundamental**, pois vira a chave do dicionário `request.POST` no Python!

---

## A Ponte Entre o HTML e a View (`name` $\leftrightarrow$ `request.POST`)

Veja como os nomes nos dois arquivos precisam coincidir:

<div class="cols">
<div>

**No HTML (`index.html`):**
```html
<input
  type="text"
  name="titulo"
/>

<textarea
  name="detalhes">
</textarea>
```

</div>
<div>

**Na View (`notes/views.py`):**
```python
def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')

        Note.objects.create(
            title=title,
            content=content
        )
```

</div>
</div>

- Se o usuário digitar *"Miojo"* no input `name="titulo"`, então `request.POST.get('titulo')` retornará `"Miojo"`.
- Se você errar o nome da chave (ex: `request.POST.get('title')`), ele retornará `None`!

---

## O Problema do F5 e o Padrão Post/Redirect/Get (PRG)

<div class="cols">
<div>

### O que acontece SEM `redirect`?
1. Usuário envia `POST /` criando uma nota.
2. Se a view responder direto com `render(...)`, a última ação registrada no navegador continua sendo `POST /`.
3. Se o usuário apertar **F5 (Recarregar)**, o navegador repete o `POST /` e **cria a mesma anotação duplicada várias vezes**!

</div>
<div>

### A Solução COM `redirect('index')`:
```python
from django.shortcuts import render, redirect
from .models import Note

def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        Note.objects.create(
            title=title, content=content
        )
        return redirect('index')  # Status 302!
    else:
        all_notes = Note.objects.order_by('-created_at')
        return render(
            request,
            'notes/index.html',
            {'notes': all_notes}
        )
```

</div>
</div>

---

## Como o `redirect('index')` sabe para onde ir?

O argumento `'index'` dentro de `redirect('index')` **não** é o nome da função em `views.py` — é o atributo **`name='index'`** definido lá no `notes/urls.py`!

```python
# Em notes/urls.py:
path('', views.index, name='index')
#                     └─────┬─────┘
#                           │ (conecta aqui!)
# Em notes/views.py:        ▼
return redirect('index')
```

### Passo a passo do Redirect:
1. A view salva a nota no banco e devolve um código HTTP **302 (Redirecionamento)** apontando para `/`.
2. O navegador recebe o 302 e faz automaticamente uma **nova requisição `GET /`**.
3. Agora, se o usuário der F5, ele apenas repete o `GET /` (sem duplicar nada!).

---

## Hora da Prática: Check 6

1. Adicione o `<form method="post">` com `{% csrf_token %}` em `notes/templates/notes/index.html`.
2. Em `notes/views.py`, verifique `if request.method == 'POST':`.
3. Extraia `titulo` e `detalhes` de `request.POST`, salve a nova `Note` no banco e retorne `redirect('index')`.
4. Teste criar uma anotação e apertar F5 para confirmar que ela não duplica!
