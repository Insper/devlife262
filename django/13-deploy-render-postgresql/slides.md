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
# 13. Deploy da Aplicação
### O que muda para tirar o projeto do `localhost` e colocar na Internet

---

## Por que o `localhost` e o `SQLite` não bastam em Produção?

<div class="cols">
<div>

### No seu Computador (Desenvolvimento)
- Quando você fecha o notebook, o site sai do ar.
- O **SQLite** é apenas um arquivo (`db.sqlite3`): em servidores de nuvem gratuitos (como o Render), arquivos locais são **apagados** toda vez que o servidor reinicia!

### Na Nuvem (Produção no Render)
- Um servidor Linux roda o código Django 24h por dia.
- Um segundo servidor dedicado roda o banco **PostgreSQL**, garantindo que os dados nunca sejam perdidos.

</div>
<div>

![w:480](../assets/deploy_v2.png)

</div>
</div>

---

## O Papel de Cada Nova Biblioteca no Deploy

No `requirements.txt` de produção, adicionamos 4 pacotes essenciais:

| Biblioteca | Por que precisamos dela em produção? |
| :--- | :--- |
| **`gunicorn`** | O `runserver` é lento e inseguro para muitos usuários. O **Gunicorn** é o servidor de produção real que executa o Django via `getit.wsgi`. |
| **`psycopg2-binary`** | Driver que permite ao Python/Django conversar com um banco de dados **PostgreSQL**. |
| **`dj-database-url`** | Lê a URL de conexão do PostgreSQL a partir de uma variável de ambiente e configura o `DATABASES` no `settings.py`. |
| **`whitenoise`** | Em produção (`DEBUG=False`), o Django para de servir arquivos estáticos sozinho. O **WhiteNoise** empacota e serve os arquivos CSS e imagens com alta performance. |

---

## Variáveis de Ambiente: Protegendo Credenciais

<div class="cols">
<div>

Se você deixar a senha do banco de dados ou a `SECRET_KEY` escrita direto no `settings.py` e der `git push`, qualquer pessoa na internet terá acesso ao seu banco!

**Como funciona com Variáveis de Ambiente (`os.environ`):**
- No código Python, lemos: `os.environ.get('DATABASE_URL')`.
- Os valores reais ficam guardados em segredo apenas no painel do **Render**!

</div>
<div>

![w:460](../assets/render-variaveis-ambiente.png)

</div>
</div>

---

## O que o Script de Build Faz no Deploy?

Toda vez que você faz `git push` para o GitHub, o Render baixa seu código novo e roda automaticamente:

1. **`pip install -r requirements.txt`** $\rightarrow$ Instala o Django e todas as bibliotecas no servidor.
2. **`python manage.py collectstatic --no-input`** $\rightarrow$ Reúne todos os CSS e imagens na pasta central para o WhiteNoise servir.
3. **`python manage.py migrate`** $\rightarrow$ Aplica qualquer migração nova diretamente nas tabelas do **PostgreSQL**!
4. **`gunicorn getit.wsgi:application`** $\rightarrow$ Inicia o servidor em produção para receber os usuários.
