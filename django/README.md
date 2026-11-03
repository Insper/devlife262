# Aulas de Django — Slides (Marp)

Coleção enxuta de slides em formato **Marp** cobrindo todos os **14 subtópicos** de Sistemas Web (Django 6.X) da disciplina **Developer Life (Insper)**.

## Índice dos Módulos

1. [01. Introdução à Web e ao Django](01-introducao-web-django/slides.md)
2. [02. Configuração, Venv e Estrutura do Projeto (Check 1)](02-configuracao-venv-estrutura/slides.md)
3. [03. Modelagem Inicial, Migrações e Django Admin (Check 2)](03-modelagem-migracoes-admin/slides.md)
4. [04. URLs e Views (Check 3)](04-urls-e-views/slides.md)
5. [05. Models, Views e URLs — QuerySets (Check 4)](05-models-views-urls-querysets/slides.md)
6. [06. Templates HTML e Herança de Layout (Check 5)](06-templates-html-base/slides.md)
7. [07. Formulários e o Método POST (Check 6)](07-formularios-metodo-post/slides.md)
8. [08. Parâmetros de URL — CRUD Completo (Check 7)](08-parametros-de-url-crud/slides.md)
9. [09. Arquivos Estáticos (Check 8)](09-arquivos-estaticos/slides.md)
10. [10. Autenticação de Usuários (Check 9)](10-autenticacao-usuarios/slides.md)
11. [11. Relacionamentos Entre Modelos — ForeignKey (Check 10)](11-relacionamentos-foreignkey/slides.md)
12. [12. Desafio: Muitos-para-Muitos — Tags](12-desafio-many-to-many-tags/slides.md)
13. [13. Deploy no Render com PostgreSQL](13-deploy-render-postgresql/slides.md)
14. [14. Django REST Framework e React](14-django-rest-react/slides.md)

## Como Visualizar ou Exportar

- **No VS Code:** Instale a extensão **Marp for VS Code** (`marp-team.marp-vscode`) e abra o preview do arquivo `slides.md`.
- **Via Linha de Comando (`marp-cli`):**
  ```bash
  npx @marp-team/marp-cli@latest 01-introducao-web-django/slides.md --html
  npx @marp-team/marp-cli@latest 01-introducao-web-django/slides.md --pdf --allow-local-files
  ```
