## What this is

"Ask Sérgio" — a FastAPI RAG backend that answers recruiters' questions about Sérgio, grounded only in the Markdown files in `data/`. Frontend is a separate Next.js app on Vercel; this backend deploys to Railway.

The codebase (identifiers, comments, log event names, commit-facing docs) is written in **Portuguese**. Keep new code consistent with that style (e.g. `buscar_chunks_parecidos`, `registrar_evento`, `objeto_config_env`).

## Commands

```bash
docker-compose up -d                 # local Postgres + pgvector on port 5433
pip install -r requirements.txt
python -m app.rag.ingest             # load data/*.md → chunk → embed → pgvector (rerun after editing data/)
uvicorn app.main:app --reload        # API on http://localhost:8000

pytest -m "not eval"                 # unit tests (what CI runs); no DB/OpenAI needed
pytest tests/test_chat.py::test_chat_endpoint   # single test
pytest tests/eval/ -v -s             # RAG quality eval — needs real DB (ingested) + real OpenAI key; -s shows ✅/❌

ruff check .                         # lint (CI gate)
bandit -r app/                       # security scan (CI gate)
```

## Architecture

Request flow for `POST /chat` (`app/routers/chat.py`):
`buscar_chunks_parecidos` (`rag/retriever.py`, PGVector similarity search) → `registrar_evento("chat_recebido", ...)` → `gerar_resposta_streaming` (`rag/gerador.py`, a generator over `ChatOpenAI.stream`) → `StreamingResponse(text/plain)`. The generator logs a `chat_gerado` event with token usage *after* the stream finishes (`stream_usage=True` makes the last chunk carry `usage_metadata`). The system prompt (`INSTRUCOES_DO_SISTEMA`) enforces third-person answers using only retrieved context; the response language comes from the request's `language` field.

Ingestion (`rag/ingest.py:rodar_ingestao`, exposed via `POST /ingest` and runnable as a module): `loader` reads `data/*.md` → `chunker` splits first by Markdown headers (`#`→`titulo`, `##`→`secao` metadata, headers kept in text) then by `RecursiveCharacterTextSplitter` → deletes and recreates the PGVector collection `documentos_picados_sergio` → `add_documents` (PGVector embeds via `rag/embedder.py`). Each ingest is a full replace.

Key cross-cutting details:
- **Config is instantiated at import time** (`app/config.py: objeto_config_env`), and `embedder.py`/`gerador.py` build their OpenAI clients at import time too. Importing `app.main` (including in tests) therefore requires `OPENAI_API_KEY`, `DATABASE_URL`, `EMBEDDING_MODEL`, `LLM_MODEL`, `ADMIN_TOKEN` to be set (via `.env` or env vars — CI sets fake values). A validator rewrites `postgres://` URLs to `postgresql+psycopg://` for Railway.
- `POST /ingest` is guarded by a `tokenAdmin` header compared against `ADMIN_TOKEN` (`routers/ingest.py`).
- Observability (`app/observability.py`): `registrar_evento(**dados)` prints one JSON line to stdout per event. It also increments an **in-memory, per-process** counter in `metricas`, which `GET /metrics` returns — it resets on restart.
- CORS origins are hardcoded in `app/main.py`.

## Testing conventions

- Unit tests use `monkeypatch.setattr("app.routers.chat.<fn>", fake)` — patch the name **where it's imported** (the router module), not in `app.rag.*`.
- Eval tests (`tests/eval/`) are marked `@pytest.mark.eval` (marker declared in `pytest.ini`) and excluded from CI. They use `CASOS_AVALIACAO` from `tests/eval/dataset.py` and an LLM-as-judge returning `SIM`/`NAO`. They print scores but do not assert on them.

## CI/CD

- `ci.yml` (every push/PR, Python 3.11): `ruff check .` → `bandit -r app/` → `pytest -v -m "not eval"`.
- `cd.yml`: runs after CI succeeds on `main`; deploys with `railway up` and curls `/health` on the production URL. The `Dockerfile` binds uvicorn to Railway's `$PORT`.


## Regras
- Nunca commitar nem dar push na main (push na main faz deploy).
- Trabalhar sempre numa branch; ao terminar, avisar para eu revisar.