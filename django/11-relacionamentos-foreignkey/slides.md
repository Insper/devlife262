---
marp: true
theme: default
paginate: true
size: 16:9
header: "Developer Life • Sistemas Web com Django"
footer: "Insper • 11. Relacionamentos Entre Modelos (Check 10)"
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
# 11. Relacionamentos Entre Modelos
### Chaves Estrangeiras (`ForeignKey`) e Dados por Usuário

**Entrega vinculada:** Check 10

---

## Chave Estrangeira (Relacionamento 1 para N)

<div class="cols">
<div>

- Um usuário pode ter **várias** anotações.
- Cada anotação pertence a **um único** usuário (autor/dono).
- No banco relacional, uma coluna guarda o **`id`** da linha correspondente na tabela de usuários.

</div>
<div>

![w:480](../assets/tabela-relacionamento.png)

</div>
</div>

---

## Adicionando `ForeignKey` e Migrando

**Arquivo:** `notes/models.py`
```python
class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)
```

- **`on_delete=models.CASCADE`:** Se o usuário for apagado, suas anotações também são removidas.
- Ao rodar `python manage.py makemigrations`, escolha a opção **`1`** e informe **`1`** (ID do usuário padrão para as anotações já existentes no banco), depois rode `migrate`.

---

## Salvando o Dono e Filtrando por Usuário

**Arquivo:** `notes/views.py`
```python
@login_required
def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        Note.objects.create(title=title, content=content, owner=request.user)
        return redirect('index')

    # Filtra primeiro pelo usuário logado e depois ordena!
    user_notes = Note.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'notes/index.html', {'notes': user_notes})
```

<div class="box">
<strong>Por que <code>.filter().order_by()</code>?</strong> Filtrar antes reduz drasticamente a quantidade de registros que precisam ser comparados na ordenação!
</div>

---

## Hora da Prática: Check 10

1. Adicione o campo `owner` (`ForeignKey` para `"auth.User"`) em `Note`.
2. Crie e aplique as migrações definindo um usuário padrão para notas antigas.
3. No POST da view, salve `request.user` como `owner` da nova anotação.
4. Na listagem principal, mostre **apenas** as anotações criadas por `request.user`.
5. Teste com 2 usuários diferentes!
