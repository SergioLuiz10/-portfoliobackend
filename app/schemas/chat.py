from pydantic import BaseModel 



#Recebe da api (mensagem do recrutador e a linguagem escolhida)
class EntradaDoChat(BaseModel):
    message: str
    language: str 



