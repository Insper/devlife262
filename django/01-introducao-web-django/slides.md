---
marp: true
theme: default
paginate: true
size: 16:9
header: "Developer Life • Sistemas Web com Django"
footer: "Insper • 01. Introdução à Web e ao Django"
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
# 01. Introdução à Web e ao Django
### Como a internet funciona e o que acontece dentro do servidor

**Projeto da Trilha:** Sistema de Anotações **Get-it**
Django 6.X • Python

---

## O que muda: Biblioteca vs. Framework

<div class="cols">
<div>

### Biblioteca (ex: Pygame)
- **Você** cria o loop principal (`while True`).
- **O seu programa chama** as funções da biblioteca na ordem que você quiser.
- Você controla todo o fluxo.

</div>
<div>

### Framework (ex: Django)
- O loop de esperar requisições de rede **já vem pronto**.
- Você escreve funções e classes em arquivos específicos (`views.py`, `models.py`).
- **O Django chama as suas funções** quando chega uma requisição (*Inversão de Controle*).

</div>
</div>

<div class="box">
<strong>Por que isso importa?</strong> Você não vai dar <code>python meu_programa.py</code> para rodar uma função isolada. O servidor Django fica rodando e aciona seu código automaticamente a cada acesso do navegador!
</div>

---

## Como um Computador Encontra Outro na Rede?

Para o navegador conversar com o nosso servidor Django, ele precisa de **2 endereços**:

```text
192.168.0.1 : 8000
└────┬────┘   └─┬┘
 Endereço IP   Porta
```

1. **Endereço IP (`192.168.0.1` ou `localhost`):** Identifica **qual computador** na rede queremos acessar (`localhost` = a sua própria máquina).
2. **Porta (`8000`):** Um computador roda vários programas usando a internet ao mesmo tempo (Spotify, navegador, VS Code). A porta identifica **qual programa específico** naquele computador deve receber a mensagem.

---

## Anatomia de uma URL: O que cada parte faz?

Quando você digita um endereço no navegador, ele é desmontado em **4 partes**:

```text
http://192.168.32.18:8000/imagens/logotipo.png
└─┬┘   └─────┬─────┘ └─┬┘└─────────┬─────────┘
 (1)        (2)       (3)         (4)
```

| Parte | Valor no exemplo | O que acontece nos bastidores? |
| :--- | :--- | :--- |
| **(1) Protocolo** | `http` | Define a língua (regras) usada na conversa entre navegador e servidor. |
| **(2) Endereço** | `192.168.32.18` | Usado na rede para chegar até a máquina do servidor (nomes como `insper.edu.br` são traduzidos para IP pelo **DNS**). |
| **(3) Porta** | `8000` | Entrega o pacote para o processo do Django que está escutando nessa porta. |
| **(4) Caminho** | `/imagens/logotipo.png` | **Entregue ao Django** para ele decidir qual página ou arquivo devolver! |

---

## Por Baixo dos Panos: Carregando uma Página Web

<div class="cols">
<div>

O carregamento de uma página não é uma única mensagem — é uma **conversa em etapas**:

1. Você digita a URL no navegador.
2. O navegador envia uma **Requisição (*Request*)** pedindo o caminho.
3. O Django processa e devolve uma **Resposta (*Response*)** com o texto HTML.
4. O navegador lê o HTML. Ao encontrar `<img src="...">` ou `<link href=".css">`, ele faz **novas requisições automáticas** para buscar cada imagem e estilo!

</div>
<div>

![w:460](../assets/client-server.jpg)

</div>
</div>

---

## O Mapa Completo: O que Acontece Dentro do Django?

![w:840 center](../assets/django-flow.png)

---

## Passo a Passo da Requisição no Servidor (1 a 6)

Quando o navegador pede `http://localhost:8000/caminho/escolhido`:

1. **Chegada:** A requisição entra na porta `8000` e é entregue ao Django.
2. **Roteamento (`urls.py`):** O Django olha apenas o caminho (`/caminho/escolhido`) e procura na lista de rotas qual função deve ser chamada.
3. **Execução da Lógica (`views.py`):** A função escolhida (chamada de *view*) é executada, recebendo todos os dados do pedido no parâmetro `request`.
4. **Banco de Dados (`models.py`):** Se precisar ler ou salvar dados, a *view* conversa com o banco de dados através das classes de modelo.
5. **Construção do HTML (`templates/`):** A *view* injeta os dados do banco em um molde HTML (*template*) usando um dicionário de contexto.
6. **Resposta:** O HTML final pronto é empacotado em um `HttpResponse` e enviado de volta ao navegador do usuário.

---

## Resumo Rápido: Quem faz o quê no Django?

| Arquivo / Pasta | Papel na Arquitetura MVT | Pergunta que ele responde |
| :--- | :--- | :--- |
| **`urls.py`** | Roteador de endereços | *"Qual função devo chamar para este caminho da URL?"* |
| **`views.py`** | Maestro / Controlador da lógica | *"Quais dados preciso buscar ou salvar e qual resposta devolver?"* |
| **`models.py`** | Representação das tabelas do banco | *"Qual é o formato dos dados guardados no banco de dados?"* |
| **`templates/`** | Molde visual da página | *"Como exibir esses dados em formato HTML para o usuário?"* |
