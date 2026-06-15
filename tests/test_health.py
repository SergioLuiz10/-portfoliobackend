from fastapi.testclient import TestClient#de teste que o próprio FastAPI 
from app.main import app #importa a aplicação FastAPI do arquivo main.py

#cria um cliente frontende fake pra testar a api entrando na pasta app 
client = TestClient(app) 


#testa o endpoint de saúde (health) pra garantir que a API tá respondendo direitinho q ta na main 
def test_endpoint_de_saude():
    response = client.get("/health") #faz uma requisição GET pro endpoint /health
    assert response.status_code == 200 #verifica se o status code da resposta é 200 (OK)
    assert response.json() == {"message": "Bem-vindo à API de Perguntas e Respostas do Sérgio!"} #verifica se o conteúdo da resposta é {"status": "ok"}
