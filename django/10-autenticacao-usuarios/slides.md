---
marp: true
theme: default
paginate: true
size: 16:9
header: "Developer Life • Sistemas Web com Django"
footer: "Insper • 10. Autenticação de Usuários (Check 9)"
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
# 10. Autenticação de Usuários
### Como funcionam Login, Sessão, Logout e `@login_required`

**Entrega vinculada:** Check 9

---

## O que o `django.contrib.auth` já faz por nós?

Autenticação segura é complexa (criptografia de senha, cookies de sessão, proteção contra ataques). Por isso o Django já traz o app **`django.contrib.auth`** instalado:

```python
# Em getit/urls.py:
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # <-- Ativa as rotas de auth!
    path('', include('notes.urls')),
]
```

### O que essa única linha `include("django.contrib.auth.urls")` cria?
- `/accounts/login/` (view pronta de login com nome `name='login'`)
- `/accounts/logout/` (view pronta de logout com nome `name='logout'`)
- **O que falta fazermos?** Apenas criar o template HTML da tela de login e configurar para onde redirecionar!

---

## Como Funciona o Template `registration/login.html`?

A view nativa de login procura automaticamente pelo arquivo **`notes/templates/registration/login.html`** e envia no contexto um objeto **`form`**:

```html
{% extends "notes/base.html" %}
{% block content %}
  {% if form.errors %}
    <p>Usuário ou senha incorretos. Por favor, tente novamente.</p>
  {% endif %}

  <form method="post" action="{% url 'login' %}">
    {% csrf_token %}
    <div>{{ form.username.label_tag }} {{ form.username }}</div>
    <div>{{ form.password.label_tag }} {{ form.password }}</div>
    <input type="submit" value="login" />
    <input type="hidden" name="next" value="{{ next }}" />
  </form>
{% endblock %}
```

- **`{{ form.username }}` e `{{ form.password }}`:** O próprio Django gera as tags `<input>` de usuário e senha!
- **Para onde o login redireciona?** Por padrão, ele tenta ir para `/accounts/profile/` (que não existe e dá 404). Para ir para a home (`/`), adicione no **`getit/settings.py`**:
  ```python
  LOGIN_REDIRECT_URL = '/'
  ```

---

## Mostrando o Usuário Logado e Fazendo Logout (`base.html`)

Em qualquer template do Django, a variável **`user`** já está disponível automaticamente!

<div class="cols">
<div>

**No `notes/templates/notes/base.html`:**
```html
<body>
  {% if user.is_authenticated %}
    <p>
      Olá, {{ user.first_name }} {{ user.last_name }}!
    </p>
    <form action="{% url 'logout' %}" method="post">
      {% csrf_token %}
      <button type="submit">Sair</button>
    </form>
  {% endif %}

  {% block content %} {% endblock %}
</body>
```

</div>
<div>

### O que acontece aqui?
- **`user.is_authenticated`:** É `True` se houver um usuário logado na sessão atual.
- **Por que o Logout é um `<form method="post">`?** No Django moderno, deslogar via link `GET` é bloqueado por segurança. O botão envia um `POST` com `{% csrf_token %}` para a rota `logout`.
- **No `getit/settings.py`:**
  ```python
  LOGOUT_REDIRECT_URL = '/accounts/login/'
  ```

</div>
</div>

---

## Protegendo Views com `@login_required`

Como impedir que alguém sem login veja a página principal?

```python
# Arquivo: notes/views.py
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    # Este código só roda se o usuário estiver autenticado!
    ...
```

### O que o decorator `@login_required` faz nos bastidores?
1. Antes de executar a sua função `index`, ele checa se `request.user.is_authenticated` é verdadeiro.
2. Se **não** estiver logado, ele nem entra na função: **redireciona automaticamente** o navegador para `/accounts/login/?next=/`.
3. Se estiver logado, executa a função `index` normalmente!

---

## Hora da Prática: Check 9

1. Inclua `path("accounts/", include("django.contrib.auth.urls"))` em `getit/urls.py` e crie `notes/templates/registration/login.html`.
2. No Django Admin (`/admin/`), edite seu usuário e preencha **First name** e **Last name**.
3. No `base.html`, exiba o nome e sobrenome do usuário logado e, ao lado, o formulário POST de logout apontando para `accounts/logout/` (redirecionando para o login com `LOGOUT_REDIRECT_URL`).
4. Proteja a view `index` com `@login_required`.
