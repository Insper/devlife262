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
# 08. Parâmetros de URL
### Como passar o `id` na URL para Editar e Apagar registros

**Entrega vinculada:** Check 7 + Exercício *Parâmetros de URL*

---

## O Problema: Como Apagar ou Editar uma Nota Específica?

Já temos o **C** (*Create*) e o **R** (*Read*) do CRUD. Faltam o **U** (*Update*) e o **D** (*Delete*).
- Se temos 10 anotações na tela e clicamos em "Apagar" na anotação de `id = 15`, como o servidor sabe que queremos apagar a nota `15` e não a `3`?
- **Solução:** Colocamos o `id` da anotação dentro do próprio caminho da URL!
  - Ex: `/anotacoes/15/apagar`
  - Ex: `/anotacoes/15`

---

## Como o Django Extrai Variáveis da URL?

Usamos a sintaxe **`<tipo:nome_da_variavel>`** no `notes/urls.py`:

```python
# Em notes/urls.py:
urlpatterns = [
    path('', views.index, name='index'),
    path('anotacoes/<int:note_id>/apagar', views.delete_note, name='delete-note'),
    path('anotacoes/<int:note_id>', views.edit_note, name='edit-note'),
]
```

### O que acontece quando o usuário acessa `/anotacoes/15/apagar`?
1. O Django vê que `15` está na posição de `<int:note_id>`.
2. Ele converte a string `"15"` para o inteiro `15`.
3. Ele chama a sua função passando `note_id=15` como segundo argumento:
   ```python
   views.delete_note(request, note_id=15)
   ```

<div class="warn">
<strong>Atenção:</strong> O nome depois dos dois pontos (<code>note_id</code>) no <code>urls.py</code> <strong>precisa ser idêntico</strong> ao nome do parâmetro na função do <code>views.py</code>!
</div>

---

## Passo a Passo da Exclusão (`delete_note`)

<div class="cols">
<div>

**1. Link no Template (`index.html`):**
```html
{% for note in notes %}
  <li>
    <strong>{{ note.title }}</strong>:
    {{ note.content }}
    <a href="/anotacoes/{{ note.id }}/apagar">
      Apagar
    </a>
    <a href="/anotacoes/{{ note.id }}">
      Editar
    </a>
  </li>
{% endfor %}
```

</div>
<div>

**2. Função na View (`notes/views.py`):**
```python
def delete_note(request, note_id):
    # (1) Busca no banco a nota com esse id
    note = Note.objects.get(id=note_id)

    # (2) Remove a linha da tabela no banco
    note.delete()

    # (3) Volta para a página principal
    return redirect('index')
```

</div>
</div>

---

## Passo a Passo da Edição (`edit_note`): `GET` vs. `POST`

A rota `/anotacoes/<int:note_id>` faz **duas coisas** dependendo do método HTTP:

<div class="cols">
<div>

**Na View (`notes/views.py`):**
```python
def edit_note(request, note_id):
    note = Note.objects.get(id=note_id)

    if request.method == 'POST':
        # Atualiza os atributos do objeto existente
        note.title = request.POST.get('titulo')
        note.content = request.POST.get('detalhes')
        note.save() # Salva mantendo o mesmo ID!
        return redirect('index')

    # Se for GET, mostra o formulário preenchido:
    return render(
        request, 'notes/edit.html', {'note': note}
    )
```

</div>
<div>

**No Template (`notes/templates/notes/edit.html`):**
```html
{% extends "notes/base.html" %}
{% block content %}
<form method="post">
  {% csrf_token %}
  <input
    type="text"
    name="titulo"
    value="{{ note.title }}"
  />
  <textarea name="detalhes">{{ note.content }}</textarea>
  <button type="submit">Salvar</button>
</form>
{% endblock %}
```
> Note o `value="{{ note.title }}"` preenchendo o campo com o valor atual!

</div>
</div>

---

## Hora da Prática: Exercício + Check 7

<div class="cols">
<div>

### Exercício no VS Code
**"Parâmetros de URL"**
- Rota `hello/<str:nome>`
- `/hello/Ana` $\rightarrow$ `Olá Ana!`
- `/hello/Bernardo` $\rightarrow$ `Olá Bernardo!`

</div>
<div>

### Check 7 (no Get-it)
1. Adicione os links de **Apagar** (`/anotacoes/<id>/apagar`) e **Editar** (`/anotacoes/<id>`) em cada anotação no `index.html`.
2. Implemente a exclusão com `.delete()` e redirecionamento para `index`.
3. Implemente a edição carregando os dados atuais no formulário e salvando no mesmo objeto (`note.save()`), mantendo o mesmo `id`.

</div>
</div>
