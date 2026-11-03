---
marp: true
theme: default
paginate: true
size: 16:9
header: "Developer Life • Sistemas Web com Django"
footer: "Insper • 04. URLs e Views (Check 3)"
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
# 04. URLs e Views
### Mapeando rotas para funções que respondem HTML

**Entrega vinculada:** Check 3 + Exercício *Mapeando rotas*

---

## Onde estamos no Fluxo do Django?

![w:760 center](../assets/urlpattern.jpg)

1. O caminho da URL chega em **`getit/urls.py`**.
2. É repassado para **`notes/urls.py`**.
3. Chama a função correspondente em **`notes/views.py`**.

---

## Roteamento Principal (`getit/urls.py`)

O Django percorre `urlpatterns` **em ordem** e para na primeira correspondência:

**Arquivo:** `getit/urls.py`
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('notes.urls')),
]
```

<div class="warn">
<strong>Cuidado com a ordem!</strong> Como <code>''</code> casa com qualquer prefixo, se vier antes de <code>'admin/'</code>, o Django Admin deixará de funcionar!
</div>

---

## Rotas do App e Primeira View

<div class="cols">
<div>

**Arquivo:** `notes/urls.py` *(criar arquivo)*
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```
> Passamos `views.index` **sem parênteses** (referência para a função).

</div>
<div>

**Arquivo:** `notes/views.py`
```python
from django.http import HttpResponse

def index(request):
    return HttpResponse(
        "Olá mundo! Este é o app notes."
    )
```
> Toda view recebe `request` e devolve um `HttpResponse`.

</div>
</div>

---

## Retornando HTML na View

Podemos devolver código HTML diretamente dentro de `HttpResponse`:

**Arquivo:** `notes/views.py`
```python
from django.http import HttpResponse

def index(request):
    html = """
    <h1>Olá mundo!</h1>
    <p>Este é o app notes de <em>DevLife do Insper</em>.</p>
    """
    return HttpResponse(html)
```

---

## Hora da Prática: Exercício + Check 3

<div class="cols">
<div>

### Exercício no VS Code
**"Mapeando rotas"**
Configurar rotas para exibir:
- `/comida` $\rightarrow$ `baião de dois`
- `/filme` $\rightarrow$ `Estrelas Além do Tempo`
- `/livro` $\rightarrow$ `O Design do Dia a Dia`

</div>
<div>

### Check 3 (no projeto Get-it)
Ao acessar **`http://localhost:8000/creditos/`**, o navegador deve renderizar:

```html
<h1>Créditos</h1>

<p>Sistema web desenvolvido por SEU_NOME</p>
```

</div>
</div>
