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
# 10. Autenticação de Usuários
### Login, Logout e Controle de Acesso com `django.contrib.auth`

**Entrega vinculada:** Check 9

---

## Rotas Nativas de Autenticação e Redirecionamento

O app `django.contrib.auth` já traz models, views e urls prontos!

<div class="cols">
<div>

**1. `getit/urls.py`**
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'accounts/',
        include('django.contrib.auth.urls')
    ),
    path('', include('notes.urls')),
]
```

</div>
<div>

**2. `getit/settings.py`**
```python
# Para onde ir após login/logout:
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
```

</div>
</div>

---

## Criando o Template de Login

Por padrão, a view de login procura por **`notes/templates/registration/login.html`**:

```html
{% extends "notes/base.html" %}

{% block content %}
  {% if form.errors %}
    <p>Usuário ou senha incorretos. Tente novamente.</p>
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

---

## Usuário Logado, Logout via POST e `@login_required`

<div class="cols">
<div>

**No `base.html` (Usuário + Botão Sair):**
```html
{% if user.is_authenticated %}
  <p>
    {{ user.first_name }} {{ user.last_name }}
  </p>
  <form action="{% url 'logout' %}" method="post">
    {% csrf_token %}
    <button type="submit">Sair</button>
  </form>
{% endif %}
```

</div>
<div>

**Protegendo a View (`notes/views.py`):**
```python
from django.contrib.auth.decorators import (
    login_required
)

@login_required
def index(request):
    ...
```
> Se não estiver logado, `@login_required` redireciona para `/accounts/login/` automaticamente!

</div>
</div>

---

## Hora da Prática: Check 9

1. Página de login funcionando em **`/accounts/login/`**.
2. Mostrar **nome e sobrenome** (`first_name` e `last_name`) do usuário logado em todas as páginas via `base.html` *(cadastre nome e sobrenome no Django Admin)*.
3. Botão de **logout via formulário POST** para `accounts/logout/` redirecionando para a tela de login.
4. Forçar autenticação na página principal com **`@login_required`**.
