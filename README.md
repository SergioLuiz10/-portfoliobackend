# Ask Sérgio — Backend
![CI](https://github.com/SergioLuiz10/-portfoliobackend/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/SergioLuiz10/-portfoliobackend/actions/workflows/cd.yml/badge.svg)

API que responde perguntas sobre mim para recrutadores. O usuário digita uma pergunta no frontend e recebe uma resposta gerada por um LLM, mas fundamentada apenas nas informações que eu mesmo escrevi nos arquivos de dados.

A ideia é simples: em vez de um portfólio estático, o recrutador conversa com uma IA que conhece meu perfil, experiências e projetos, e responde no idioma em que a pergunta foi feita.

---

## Como funciona

O projeto usa uma arquitetura RAG (Retrieval-Augmented Generation). O fluxo é:

1. Os arquivos `.md` da pasta `data/` são carregados, picados em chunks e armazenados como vetores no PostgreSQL via pgvector — isso é feito uma vez pelo endpoint `/ingest`.
2. Quando uma pergunta chega no `/chat`, ela é transformada em vetor, os chunks mais parecidos são recuperados do banco e enviados junto com a pergunta pro modelo da OpenAI.
3. A resposta é devolvida em streaming — o frontend vai recebendo o texto conforme ele é gerado.

```
data/*.md  →  loader  →  chunker  →  pgvector
                                         ↓
pergunta do usuário  →  embedder  →  retriever  →  LLM  →  resposta (stream)
```

---

## Stack

- **FastAPI** — framework da API
- **LangChain** — orquestração do pipeline RAG
- **OpenAI** — embeddings (`text-embedding-3-small`) e geração de texto (`gpt-4o-mini`)
- **PostgreSQL + pgvector** — banco vetorial
- **Docker** — ambiente local do banco e deploy da aplicação

---

## Estrutura do projeto

```
app/
├── main.py          # criação do app FastAPI e registro dos routers
├── config.py        # leitura do .env via pydantic-settings
├── database.py      # conexão com o pgvector
├── routers/
│   ├── chat.py      # POST /chat
│   └── ingest.py    # POST /ingest
├── rag/
│   ├── loader.py    # lê os .md da pasta data/
│   ├── chunker.py   # pica os documentos em chunks
│   ├── embedder.py  # ferramenta de embeddings da OpenAI
│   ├── retriever.py # busca os chunks mais parecidos no banco
│   ├── gerador.py   # monta o prompt e gera a resposta em streaming
│   └── ingest.py    # orquestra o pipeline de ingestão
data/
├── 01-perfil.md
├── 02-experiencia.md
├── 03-projetos.md
├── 04-stack.md
└── 05-faq.md
```

---

## Rodando localmente

### Pré-requisitos

- Python 3.11+
- Docker e Docker Compose
- Uma chave de API da OpenAI

### 1. Suba o banco

```bash
docker-compose up -d
```

Isso sobe um PostgreSQL com pgvector na porta `5433`.

### 2. Configure o ambiente

Crie um `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/asksergio
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4o-mini
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=asksergio
```

### 3. Instale as dependências

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Rode a ingestão

```bash
python -m app.rag.ingest
```

Isso carrega os arquivos `.md`, pica em chunks e popula o banco. Precisa ser feito ao menos uma vez antes de usar o `/chat`. Rode de novo sempre que atualizar os dados.

### 5. Suba a API

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

---

## Endpoints

### `POST /ingest`

Reprocessa todos os arquivos da pasta `data/`, limpa a coleção anterior e repopula o banco.

```json
// response
{ "quantidade_de_documentos_picados": 42 }
```

### `POST /chat`

Recebe uma pergunta e o idioma desejado para a resposta. Retorna um stream de texto.

```json
// request
{
  "message": "Quais tecnologias o Sérgio usa no trabalho?",
  "language": "português"
}
```

A resposta é devolvida como `text/plain` em streaming — leia chunk a chunk no frontend.

---

## Deploy

O backend está configurado para deploy no **Railway**. O `Dockerfile` usa a variável `$PORT` injetada pelo Railway na hora de subir o uvicorn.

O frontend em Next.js fica no **Vercel** e as origens permitidas no CORS já estão configuradas em `app/main.py`.

---

## Dados

Os arquivos em `data/` são documentos Markdown que eu escrevi manualmente descrevendo meu perfil profissional. São a única fonte de verdade da IA — ela não usa conhecimento externo, só o que está nesses arquivos.
