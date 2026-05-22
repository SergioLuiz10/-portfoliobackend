# Projetos — Sérgio Nunes

## Crom.IA — Plataforma de IA para Cromatografia Analítica

O Crom.IA é a principal plataforma de IA desenvolvida pelo
Sérgio na MG3. É um produto voltado para o setor de
cromatografia analítica, que abrange técnicas laboratoriais
como HPLC (cromatografia líquida de alta eficiência) e GC
(cromatografia gasosa). O objetivo do Crom.IA é apoiar
profissionais dessa área com inteligência artificial.

A arquitetura do Crom.IA é multi-agente. Existe um agente
Orquestrador que recebe a demanda do usuário e direciona para
agentes especializados, cada um com uma função: um agente de
Troubleshooting (resolução de problemas técnicos), um agente
de Estudo Guiado (apoio ao aprendizado) e um agente de
Gestão. Essa orquestração entre agentes é feita com n8n.

O Crom.IA tem um pipeline de RAG construído em FastAPI,
usando LangChain para a orquestração, PGVector como banco
vetorial e modelos da OpenAI para embeddings e geração de
texto. Isso permite que a plataforma responda perguntas
baseadas em documentos técnicos de cromatografia.

A plataforma também tem um serviço standalone de análise de
imagem chamado image_service, que usa o GPT-4o Vision para
interpretar imagens — por exemplo, gráficos e cromatogramas
enviados pelos usuários.

A infraestrutura do Crom.IA usa Edge Functions no Supabase,
protegidas por autenticação via header secreto, e o deploy é
feito com Docker no EasyPanel, rodando em uma VPS da
Hostinger.

No Crom.IA, o Sérgio é o responsável técnico pelo
desenvolvimento: ele projetou a arquitetura multi-agente,
construiu o pipeline RAG, implementou o serviço de visão
computacional e configurou toda a infraestrutura de deploy.

## FreelancerOS — Sistema Open Source para Freelancers

O FreelancerOS é um projeto open source desenvolvido pelo
Sérgio. É um sistema voltado para organização do trabalho de
freelancers, ajudando a gerenciar clientes, projetos e
tarefas.

A stack do FreelancerOS combina FastAPI no backend, n8n para
automações e integração com o ClickUp como ferramenta de
gestão de tarefas. O projeto demonstra a capacidade do Sérgio
de integrar sistemas diferentes e de construir software
pensado para ser usado e mantido pela comunidade.

Por ser open source, o FreelancerOS também mostra o interesse
do Sérgio em compartilhar conhecimento e contribuir
publicamente com código.

## Automação Comercial MG3

A Automação Comercial é um projeto interno desenvolvido pelo
Sérgio na MG3 para automatizar processos da área comercial da
empresa.

A solução integra Microsoft Forms (para captura de dados),
Microsoft Power Automate (para orquestração do fluxo) e o
Omie (sistema de gestão empresarial / ERP). Com essa
automação, dados capturados em formulários passam a alimentar
automaticamente o sistema de gestão, reduzindo trabalho
manual e erros.

Esse projeto mostra a habilidade do Sérgio de aplicar
automação a processos reais de negócio, usando ferramentas
low-code integradas a sistemas corporativos.

## Bots de WhatsApp

O Sérgio desenvolveu bots de atendimento para WhatsApp,
voltados para automação de comunicação e atendimento ao
cliente.

A stack desses bots usa Java com o framework Spring Boot no
backend, a EvolutionAPI para integração com o WhatsApp e o
Chatwoot como plataforma de atendimento. Esse projeto mostra
que o Sérgio também tem experiência com Java e Spring Boot,
além do ecossistema Python, e que sabe trabalhar com
integração de canais de mensageria.

## Ask Sérgio — Este Próprio Assistente

O Ask Sérgio é o assistente de IA com quem você está
conversando agora. É um projeto pessoal do Sérgio: um chat
com RAG, embedado no portfólio dele, criado para responder
perguntas de recrutadores sobre a experiência, os projetos e
a stack do Sérgio.

A stack do Ask Sérgio é FastAPI no backend, LangChain para a
orquestração do RAG, PostgreSQL com PGVector como banco
vetorial e modelos da OpenAI para embeddings e geração de
respostas. É mais um exemplo prático de IA generativa
aplicada construída pelo Sérgio.