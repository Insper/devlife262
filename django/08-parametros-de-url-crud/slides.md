---
marp: true
theme: default
paginate: true
size: 16:9
header: "Developer Life • Sistemas Web com Django"
footer: "Insper • 08. Parâmetros de URL — CRUD Completo (Check 7)"
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
# 08. Parâmetros de URL
### Completando o CRUD: Apagar e Editar Anotações

**Entrega vinculada:** Check 7 + Exercício *Parâmetros de URL*

---

## Capturando Parâmetros na Rota (`<tipo:nome>`)

Para apagar ou editar uma anotação específica, passamos seu `id` na URL:
Ex: `/anotacoes/15/apagar`

**Arquivo:** `notes/urls.py`
```python
urlpatterns = [
    path('', views.index, name='index'),
    path('anotacoes/<int:note_id>/apagar', views.delete_note, name='delete-note'),
    path('anotacoes/<int:note_id>', views.edit_note, name='edit-note'),
]
```

O Django converte `<int:note_id>` para inteiro e passa como argumento para a view:
```python
def delete_note(request, note_id): ...
```

---

## Apagando e Editando no Banco de Dados

<div class="cols">
<div>

### Apagar (`delete_note`)
```python
def delete_note(request, note_id):
    note = Note.objects.get(id=note_id)
    note.delete()
    return redirect('index')
```

</div>
<div>

### Editar (`edit_note`)
```python
def edit_note(request, note_id):
    note = Note.objects.get(id=note_id)
    if request.method == 'POST':
        note.title = request.POST.get('titulo')
        note.content = request.POST.get('detalhes')
        note.save()
        return redirect('index')
    return render(
        request,
        'notes/edit.html',
        {'note': note}
    )
```

</div>
</div>

---

## Hora da Prática: Exercício + Check 7

<div class="cols">
<div>

### Exercício no VS Code
**"Parâmetros de URL"**
- Rota `/hello/<str:nome>`
- `/hello/Ana` $\rightarrow$ `Olá Ana!`
- `/hello/Bernardo` $\rightarrow$ `Olá Bernardo!`

</div>
<div>

### Check 7 (no Get-it)
Em cada anotação da lista, adicione **2 links**:
1. **Apagar** (`/anotacoes/<id>/apagar`): remove do banco e redireciona para `index`.
2. **Editar** (`/anotacoes/<id>`): abre formulário preenchido com os dados da nota; ao salvar (POST), atualiza mantendo o mesmo `id` e redireciona para `index`.

</div>
</div>
