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
# 12. Desafio: Relacionamento Muitos-para-Muitos
### Implementando um sistema de Tags com `ManyToManyField`

---

## 1:N (`ForeignKey`) vs. N:N (`ManyToManyField`)

<div class="cols">
<div>

### Autor $\leftrightarrow$ Anotação (1:N)
- Uma anotação tem **1** autor.
- Um autor tem **N** anotações.
- Usa `models.ForeignKey`.

</div>
<div>

### Tag $\leftrightarrow$ Anotação (N:N)
- Uma anotação pode ter **várias** tags.
- Uma mesma tag pode estar em **várias** anotações.
- Usa `models.ManyToManyField`.

</div>
</div>

---

## Modelando `Tag` e Associando Anotações

<div class="cols">
<div>

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
    owner = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(Tag)
```

</div>
<div>

**Adicionando e Filtrando na View:**
```python
# Associando uma tag a uma nota:
tag_obj, _ = Tag.objects.get_or_create(
    name=nome_tag.strip()
)
note.tags.add(tag_obj)

# Filtrando notas do usuário por tag:
Note.objects.filter(
    owner=request.user,
    tags__id=tag_id
)
```

</div>
</div>

---

## Requisitos do Desafio

1. **Formulário único:** Campo de texto no próprio formulário de criação de anotações onde as tags são digitadas separadas por `,` ou `;`.
2. **Exibição:** Mostrar as tags associadas em cada anotação na tela principal.
3. **Filtro por Tag:** Ao clicar em uma tag, abrir uma página listando todas as anotações **do usuário logado** que possuem aquela tag.
