import os, dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId #Para converter o ID do cliente para ObjectId

dotenv.load_dotenv()

# Carregar as variáveis de ambiente do arquivo .env
login=os.getenv('user_MongoDB')
password=os.getenv('password_MongoDB')
uri = f"mongodb+srv://{login}:{password}@cluster0.25d5slc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

class ClienteMongoAdapter:
    def __init__(self, db_name: str):

        self.db_name = db_name # Nome dob banco de dados
        self.collection_name = "clientes" # Nome da coleção de clientes

        # Cria um novo cliente MongoDB e se conecta com o servidor
        self.client = MongoClient(uri, server_api=ServerApi('1'))


        
  #Função para buscar um cliente pelo ID      
    def get_cliente(self, id: str) -> dict:
         
        if not self.client:
            print("Erro de conexão com o banco de dados.")
            return None
        else:
            db = self.client[self.db_name]
            collection = db[self.collection_name]

            #Buscando o cliente pelo ID, convertendo para ObjectId
            id_cliente = ObjectId(id)
            documento = collection.find_one({"_id": id_cliente})

            if documento:
                # Se o documento existe, iterar e salvar os dados em um novo dicionário
                # e converter os valores para string
                if documento:
                    novo_documento = {}
                    for key, dado in documento.items():
                        novo_documento[key] = str(dado)
                    return novo_documento

                return documento
            else:
                    print(f"Cliente com ID '{id}' não encontrado.")


    def create_cliente(self, cliente: dict) -> dict:
        if not self.client:
            print("Erro de conexão com o banco de dados. Não é possível criar o cliente.")
            return None

        if not cliente: # checa se os dados estão presentes
            print("Dados do cliente não fornecidos para criação.")
            return None

        db = self.client[self.db_name]
        collection = db[self.collection_name]

        # Não precisa converter o objeto de dicionário para mongo, pois o MongoDB aceita dicionários diretamente.
        # O id será gerado pelo mongodb automaticamente.

        resultado = collection.insert_one(cliente)
        print(f"Cliente inserido com ID: {resultado.inserted_id}")

        # Buscar o documento recém-inserido para retorná-lo completo
        documento_criado = collection.find_one({"_id": resultado.inserted_id})

        if documento_criado:
            novo_documento = {}
            for key, dado in documento_criado.items():
                novo_documento[key] = str(dado) # Convertendo os valores para string
            return novo_documento
        else:
            print(f"Erro ao buscar o cliente recém-criado com ID: {resultado.inserted_id}")
            return None


    def update_cliente(self, id: int, cliente: dict) -> dict:
            
            if not self.client: # checa se a conexão está ativa
                print("Erro de conexão com o banco de dados. Não é possível atualizar o cliente.")

            if not cliente: # checa se os dados estão presentes
                print("Nenhum dado fornecido para atualização.")
            
            db = self.client[self.db_name]
            collection = db[self.collection_name]

            try:
                idObjetoaAtualizar = ObjectId(cliente["_id"]) # Converte o ID do cliente para ObjectId
            except Exception as e:
                print(f"ID fornecido ('{idObjetoaAtualizar}') não existe: {e}")

            #Verifica se existe um campo _id nos dados e o remove para evitar conflitos
            if "_id" in cliente:
                del cliente["_id"]


            result = collection.update_one(
                {"_id": idObjetoaAtualizar},
                {"$set": cliente}
            )

            # Verifica o resultado da atualização foi igual a 0
            if result.matched_count == 0:
                print(f"Cliente com ID '{idObjetoaAtualizar}' não encontrado para atualização.")
                return None
            
            # Verifica o resultado da atualização foi igual a 1 e se algum dado foi modificado. Como não foi modificado, 
            # retorna o cliente
            elif result.modified_count == 0 and result.matched_count == 1:
                print(f"Cliente com ID '{idObjetoaAtualizar}' encontrado, mas os dados fornecidos são iguais.")
                return self.get_cliente(idObjetoaAtualizar) # Reutiliza o get_cliente
            #Se o resultado de modificação for maior que 0, então o cliente foi atualizado
            elif result.modified_count > 0:
                print(f"Cliente com ID '{idObjetoaAtualizar}' atualizado com sucesso.")
                # Buscar e retornar o documento atualizado
                return self.get_cliente(idObjetoaAtualizar) # chama o get_cliente para retornar o documento atualizado

    # Função para deletar um cliente
    def delete_cliente(self, id: int) -> None:

        if not self.client:
            print("Erro de conexão com o banco de dados. Não é possível deletar o cliente.")
            return

        db = self.client[self.db_name]
        collection = db[self.collection_name]

        idObjetoaSerDeletado = ObjectId(id)


        resultado = collection.delete_one({"_id": idObjetoaSerDeletado})

        if resultado.deleted_count > 0:
            print(f"Cliente com ID '{id}' deletado com sucesso.")
        else:
            print(f"Nenhum cliente encontrado com ID '{id}' para deletar.")
