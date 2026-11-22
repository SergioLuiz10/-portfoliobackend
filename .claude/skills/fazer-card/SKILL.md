---
name: fazer-card
description: Use quando eu passar um card/demanda de tarefa para implementar. Transforma o card num pedido estruturado, planeja, espera minha aprovação, implementa na branch atual e chama o QA.
---

# Fazer card

Recebo um card (texto da demanda). Siga as etapas na ordem. Seja econômico: leia só o necessário.

## 1. Entender
Reescreva o card em até 5 linhas:
- **Objetivo:** uma frase
- **Dados:** informações concretas do card
- **Não fazer:** limites (sempre incluir: não dar push, não fazer deploy)
- **Pronto quando:** critério para saber que terminou

Se faltar "Pronto quando" ou algum dado essencial, PERGUNTE antes de continuar.

## 2. Conferir a branch
Rode `git branch --show-current`. Se for `main` ou `master`, PARE e me avise. Não trabalhe na main.

## 3. Planejar e esperar
Use o CLAUDE.md/AGENTS.md como mapa. Leia só os arquivos necessários (busque com grep antes de abrir arquivos inteiros).
Responda com:
- Arquivos que vai alterar + por quê (1 linha cada)
- Riscos ou dúvidas (se houver)

PARE e espere eu aprovar. Não altere nada antes da aprovação.

## 4. Implementar
Faça só o que foi aprovado. Se precisar mexer em algo fora do plano, pergunte antes.
Faça commit nesta branch com mensagem no padrão `feat:` / `fix:` / `chore:`.

## 5. Revisar
Chame o subagente `qa`. Se a mudança mexeu em tela/UI e existir o subagente `frontend`, chame ele também.
Se o QA reprovar, corrija e chame o QA de novo (máximo 2 tentativas, depois me avise).

## 6. Responder
Resumo curto:
- **O que mudou:** 3 linhas no máximo
- **Commit:** hash + mensagem
- **QA:** PASSOU / FALHOU
- **Pendências:** o que eu preciso fazer (ex.: push, deploy, rodar algo)