---
marp: true
theme: default
paginate: true
size: 16:9
header: "Developer Life • Sistemas Web com Django"
footer: "Insper • 06. Templates HTML e Herança (Check 5)"
style: |
  section {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 26px;
  }
  h1 { color: #092e20; }
  h2 { color: #0c4b33; border-bottom: 2px solid #44b78b; padding-bottom: 6px; }
  code { background: #f0f4f2; color: #0c4b33; padding: 2px 6px; border-radius: 4px; }
  pre code { background: transparent; color: inherit; }
  .cols { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; align-items: center; }
  .box { background: #f4fbf7; border-left: 5px solid #44b78b; padding: 14px 18px; border-radius: 6px; margin-top: 12px; }
  .warn { background: #fff8e6; border-left: 5px solid #f59e0b; padding: 14px 18px; border-radius: 6px; margin-top: 12px; }
---

<!-- _class: lead -->
# 06. Templates HTML e Herança
### Separando a camada de visualização com páginas dinâmicas

**Entrega vinculada:** Check 5

---

## Por que usar Templates?

<div class="cols">
<div>

### String HTML na View
- Sem *syntax highlighting* de HTML
- Sem *autocomplete* no editor
- Mistura lógica Python com estrutura visual

</div>
<div>

### Templates Django (`.html`)
- Arquivo HTML separado e organizado
- Recebe dados dinâmicos da view via **Dicionário de Contexto**
- Suporta variáveis e laços de repetição

</div>
</div>

---

## Elementos de um Template Django (DTL)

- **Variáveis:** `{{ note.title }}` $\rightarrow$ substituído pelo valor no contexto.
- **Tags de lógica:** `{% for note in notes %} ... {% empty %} ... {% endfor %}`
- **Filtros:** `{{ texto|lower }}` $\rightarrow$ transforma o valor da variável.
- **Comentários:** `{# Comentário ignorado no HTML final #}`

```html
<ul>
  {% for note in notes %}
    <li>{{ note.title }}</li>
  {% empty %}
    <li>Nenhuma anotação por enquanto.</li>
  {% endfor %}
</ul>
```

---

## Herança de Templates (`base.html` e `index.html`)

Evita repetir `<head>`, menu e rodapé em todas as páginas (Consistência / CRAP):

<div class="cols">
<div>

**`notes/templates/notes/base.html`**
```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Get-it</title>
  </head>
  <body>
    {% block content %} {% endblock %}
  </body>
</html>
```

</div>
<div>

**`notes/templates/notes/index.html`**
```html
{% extends "notes/base.html" %}

{% block content %}
<h1>Get-it</h1>
<ul>
  {% for note in notes %}
  <li>
    <strong>{{ note.title }}</strong>:
    {{ note.content }}
  </li>
  {% empty %}
  <li>Nenhuma anotação por enquanto.</li>
  {% endfor %}
</ul>
{% endblock %}
```

</div>
</div>

---

## Renderizando o Template na View (Check 5)

A função `render()` junta `request` + arquivo de template + **dicionário de contexto**:

**Arquivo:** `notes/views.py`
```python
from django.shortcuts import render
from .models import Note

def index(request):
    all_notes = Note.objects.order_by('-created_at')
    return render(request, 'notes/index.html', {'notes': all_notes})
```

<div class="box">
<strong>Check 5:</strong> Usar templates separados (<code>base.html</code> e <code>index.html</code>) mostrando <strong>título e conteúdo</strong> de cada anotação ordenada por data!
</div>
