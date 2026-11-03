---
marp: true
theme: default
paginate: true
size: 16:9
header: "Developer Life • Sistemas Web com Django"
footer: "Insper • 12. Desafio: Muitos-para-Muitos (Tags)"
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
# 12. Desafio: Relacionamento Muitos-para-Muitos
### Como funciona o `ManyToManyField` para criar um sistema de Tags

---

## Por que `ForeignKey` não serve para Tags?

<div class="cols">
<div>

### Relacionamento 1 para N (`ForeignKey`)
- Uma anotação tem **apenas 1** dono (`owner`).
- Basta uma coluna `owner_id` na tabela `Note`.

</div>
<div>

### Relacionamento N para N (`ManyToManyField`)
- Uma anotação pode ter **várias** tags (`#urgente`, `#faculdade`).
- E a mesma tag `#urgente` pode estar em **várias** anotações diferentes!
- Nos bastidores, o Django cria automaticamente uma **3ª tabela intermediária** ligando IDs de `Note` e IDs de `Tag`.

</div>
</div>

---

## Modelando `Tag` e `ManyToManyField`

**Arquivo:** `notes/models.py`
```python
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)   # <-- Relação Muitos-para-Muitos!
```

---

## Como Salvar, Exibir e Filtrar Tags na Prática?

<div class="cols">
<div>

**1. Salvando tags digitadas no POST (`views.py`):**
```python
note = Note.objects.create(
    title=title, content=content, owner=request.user
)
# Ex: tags_str = "urgente, insper"
for raw_tag in tags_str.split(','):
    tag_name = raw_tag.strip()
    if tag_name:
        # Busca a tag existente ou cria se for nova:
        tag_obj, _ = Tag.objects.get_or_create(
            name=tag_name
        )
        # Adiciona na tabela intermediária:
        note.tags.add(tag_obj)
```

</div>
<div>

**2. Exibindo no Template (`index.html`):**
```html
{% for tag in note.tags.all %}
  <a href="/tags/{{ tag.id }}">{{ tag.name }}</a>
{% endfor %}
```

**3. Filtrando anotações por Tag (`views.py`):**
```python
def notes_by_tag(request, tag_id):
    notes = Note.objects.filter(
        owner=request.user,
        tags__id=tag_id
    ).order_by('-created_at')
    ...
```

</div>
</div>

---

## Requisitos Completos do Desafio

1. **No formulário de criação de anotações:** Adicionar um campo de texto onde o usuário digita tags separadas por `,` ou `;`.
2. **Na listagem de anotações:** Exibir todas as tags associadas a cada anotação.
3. **Página de filtro por tag:** Ao clicar em uma tag, abrir uma rota mostrando apenas as anotações **do usuário logado** que possuem aquela tag.
