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
# 09. Arquivos Estáticos
### Servindo CSS, Imagens e JavaScript no Django

**Entrega vinculada:** Check 8

---

## Onde Ficam os Arquivos Estáticos?

O app `django.contrib.staticfiles` reúne imagens, CSS e scripts de cada app.

<div class="cols">
<div>

Estrutura de pastas dentro do app `notes`:
```text
notes/
└── static/
    └── notes/
        ├── img/
        │   └── logo-getit.png
        └── style/
            └── getit.css
```

</div>
<div>

![w:220 center](../assets/logo-getit.png)

<div class="warn">
Se o arquivo não carregar após criar a pasta <code>static</code> pela primeira vez, pare o <code>runserver</code> (Ctrl+C) e inicie novamente.
</div>

</div>
</div>

---

## Carregando Estáticos nos Templates (`{% static %}`)

1. Adicione `{% load static %}` no topo do template.
2. Use `{% static 'caminho/do/arquivo' %}` nos atributos `href` ou `src`.

**Arquivo:** `notes/templates/notes/base.html`
```html
{% load static %}
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Get-it</title>
    <link rel="stylesheet" href="{% static 'notes/style/getit.css' %}" />
  </head>
  <body>
    <img src="{% static 'notes/img/logo-getit.png' %}" width="100" height="60" />
    {% block content %} {% endblock %}
  </body>
</html>
```

---

## Hora da Prática: Check 8

1. Crie um arquivo CSS em `notes/static/notes/...`.
2. Carregue esse arquivo CSS no **`base.html`** usando `{% load static %}` e `{% static ... %}` para que funcione em todas as páginas.
3. Aplique um estilo visível (ex: cor de fundo ou fonte) para validar o carregamento.
