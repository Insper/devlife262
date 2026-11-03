---
marp: true
theme: default
paginate: true
size: 16:9
header: "Developer Life • Sistemas Web com Django"
footer: "Insper • 09. Arquivos Estáticos (Check 8)"
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
# 09. Arquivos Estáticos
### Como o Django entrega imagens, arquivos CSS e JavaScript para o navegador

**Entrega vinculada:** Check 8

---

## O que são Arquivos Estáticos (e por que não ficam em `templates/`)?

<div class="cols">
<div>

### Templates (`templates/`)
- São **moldes dinâmicos**: o Django lê o arquivo e processa tags `{{ }}` e `{% %}` antes de responder.

### Estáticos (`static/`)
- São **arquivos prontos e fixos** (imagens `.png`, estilos `.css`, scripts `.js`).
- O app nativo `django.contrib.staticfiles` recolhe os arquivos `static/` de todos os apps e os disponibiliza para o navegador baixar.

</div>
<div>

```text
notes/
├── templates/
│   └── notes/
│       ├── base.html
│       └── index.html
└── static/
    └── notes/
        ├── img/
        │   └── logo-getit.png
        └── style/
            └── getit.css
```

</div>
</div>

---

## Como `{% load static %}` e `{% static %}` Funcionam?

Não colocamos caminhos fixos do computador no HTML. Pedimos para a tag `{% static %}` gerar a URL pública correta daquele arquivo:

**Arquivo:** `notes/templates/notes/base.html`
```html
{% load static %}                                              <!-- (1) Habilita a tag static neste arquivo -->
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Get-it</title>
    <link rel="stylesheet" href="{% static 'notes/style/getit.css' %}" /> <!-- (2) Gera /static/notes/style/getit.css -->
  </head>
  <body>
    <img src="{% static 'notes/img/logo-getit.png' %}" width="100" height="60" /> <!-- (3) Gera /static/notes/img/logo-getit.png -->
    {% block content %} {% endblock %}
  </body>
</html>
```

- **Atenção:** Se você usar `{% static %}` também no `index.html`, precisa colocar `{% load static %}` no topo do `index.html` também!

---

## Por Baixo dos Panos: O que Acontece no Navegador?

1. O navegador pede `GET /` para o Django.
2. O Django processa o `base.html`, transforma `{% static 'notes/style/getit.css' %}` em `href="/static/notes/style/getit.css"` e devolve o HTML.
3. O navegador lê o HTML e vê a tag `<link rel="stylesheet" href="/static/notes/style/getit.css">`.
4. O navegador faz **uma segunda requisição automática** `GET /static/notes/style/getit.css`.
5. O `django.contrib.staticfiles` localiza `notes/static/notes/style/getit.css` e entrega o CSS!

<div class="warn">
<strong>Dica importante:</strong> Quando você cria a pasta <code>static/</code> pela primeira vez, o <code>runserver</code> pode não enxergá-la até você parar o servidor (<code>Ctrl + C</code>) e rodar <code>python manage.py runserver</code> novamente!
</div>

---

## Hora da Prática: Check 8

1. Crie a pasta `notes/static/notes/style/` e um arquivo CSS (ex: `getit.css`).
2. Carregue esse CSS dentro do **`notes/templates/notes/base.html`** usando `{% load static %}` e `<link rel="stylesheet" href="{% static '...' %}">`.
3. Adicione uma regra CSS visível (ex: cor de fundo, fonte ou estilo dos cards) para comprovar que o estilo está sendo aplicado em todas as páginas!
