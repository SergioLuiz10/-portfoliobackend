from app.rag.retriever import buscar_chunks_parecidos


#pergunta q falhou no teste de avaliação
#jogar ela no banco pra ver quais chunks voltaram
#pergunta = "Onde o Sérgio estuda e quando se forma?"


#pega os chunks parecidos com a pergunta q falhou no teste de avaliação
#chunks = buscar_chunks_parecidos(pergunta)


# printa os chunks que vieram do banco, pra ver se tem algum q é parecido com a resposta certa  
#for i, chunk in enumerate(chunks):
#    print(f"\n--- CHUNK {i} ---")
    #mostra o texto do chunk q veio do banco
#    print(chunk.page_content) 

#pergunta q falhou no teste de avaliação
#jogar ela no banco pra ver quais chunks voltaram
#pergunta = "Qual foi a experiência anterior do Sérgio?"


pergunta2 = "Qual foi a experiência anterior do Sérgio?"

#pega os chunks parecidos com a pergunta q falhou no teste de avaliação
chunks2 = buscar_chunks_parecidos(pergunta2)


# printa os chunks que vieram do banco, pra ver se tem algum q é parecido com a resposta certa  
for i, chunk in enumerate(chunks2):
    print(f"\n--- CHUNK {i} ---")
    #mostra o texto do chunk q veio do banco
    print(chunk.page_content)