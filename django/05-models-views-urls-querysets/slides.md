---
marp: true
theme: default
paginate: true
size: 16:9
header: "Developer Life • Sistemas Web com Django"
footer: "Insper • 05. Models, Views e URLs — QuerySets (Check 4)"
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
# 05. Models, Views e URLs
### Consultando o banco de dados na View com QuerySets

**Entrega vinculada:** Check 4

---

## Juntando Models e Views (`Note.objects`)

Toda classe de modelo ganha o atributo **`objects`** para consultar o banco:

**Arquivo:** `notes/views.py`
```python
from django.http import HttpResponse
from .models import Note

def index(request):
    all_notes = Note.objects.all()  # Retorna um QuerySet (lista de objetos Note)
    items_html = ""
    for note in all_notes:
        items_html += f"<li>{note.title}</li>"

    return HttpResponse(f"<h1>Get-it</h1><ul>{items_html}</ul>")
```

---

## Principais Métodos de `QuerySet`

| Método | O que faz? | Exemplo |
| :--- | :--- | :--- |
| **`.all()`** | Retorna todos os registros da tabela | `Note.objects.all()` |
| **`.filter(...)`** | Mantém apenas os que atendem ao critério | `Note.objects.filter(title="Lembrete")` |
| **`.exclude(...)`** | Remove os que atendem ao critério | `Note.objects.exclude(id=1)` |
| **`.order_by(...)`** | Ordena pela coluna (`-` para decrescente) | `Note.objects.order_by('-created_at')` |
| **`.reverse()`** | Inverte a ordem de um QuerySet ordenado | `qs.reverse()` |
| **`.distinct()`** | Elimina linhas duplicadas no resultado | `Note.objects.distinct()` |

---

## Hora da Prática: Check 4

Na página principal (`http://localhost:8000/`):

1. Substitua o "Olá mundo" pela listagem das anotações salvas no banco.
2. Exiba uma lista não ordenada (`<ul>`) com o `title` de cada anotação em um `<li>`.
3. **Importante:** As anotações devem aparecer em **ordem decrescente de criação** (mais recentes primeiro):
   ```python
   Note.objects.order_by('-created_at')
   ```

<div class="box">
<strong>Próximo passo:</strong> Montar strings HTML dentro do Python dá trabalho e não tem autocomplete. Vamos resolver isso com <strong>Templates</strong>!
</div>
