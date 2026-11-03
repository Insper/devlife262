---
marp: true
theme: default
paginate: true
size: 16:9
header: "Developer Life • Sistemas Web com Django"
footer: "Insper • 13. Deploy no Render com PostgreSQL"
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
# 13. Deploy da Aplicação
### Do `localhost` (SQLite) para a Nuvem (Render + PostgreSQL)

---

## Desenvolvimento Local vs. Produção na Nuvem

<div class="cols">
<div>

### Local (`localhost:8000`)
- Roda apenas na sua máquina
- Banco em arquivo local (**SQLite**)
- `python manage.py runserver`

</div>
<div>

### Produção (Render)
- Servidor público disponível 24/7
- Banco relacional robusto (**PostgreSQL**)
- Servidor WSGI de produção (**Gunicorn** + **WhiteNoise**)

</div>
</div>

![w:640 center](../assets/deploy_v2.png)

---

## Variáveis de Ambiente e Segurança

<div class="cols">
<div>

**Nunca** suba senhas ou chaves secretas direto no código do GitHub!

Configuramos no painel do Render (`Environment Variables`):
- `DATABASE_URL` (conexão PostgreSQL)
- `SECRET_KEY`
- `DEBUG = False`
- `PYTHON_VERSION`

</div>
<div>

![w:460](../assets/render-variaveis-ambiente.png)

</div>
</div>

---

## Passo a Passo Resumido de Publicação

1. **Criar instância PostgreSQL no Render** e copiar a *Internal Database URL*.
2. **Preparar o projeto Django:**
   - `dj-database-url`, `psycopg2-binary`, `gunicorn`, `whitenoise` no `requirements.txt`
   - Script `build.sh` executando `pip install`, `collectstatic` e `migrate`
3. **Criar Web Service no Render** conectado ao repositório GitHub:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn getit.wsgi:application`

<div class="box">
<strong>Alternativa para testes rápidos locais:</strong> Use o <strong>Ngrok</strong> (<code>ngrok http 8000</code>) adicionando o domínio gerado em <code>ALLOWED_HOSTS</code> e <code>CSRF_TRUSTED_ORIGINS</code>.
</div>
