import os, dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId #Para converter para ObjectId

dotenv.load_dotenv()

# Carregar as variáveis de ambiente do arquivo .env
login=os.getenv('user_MongoDB')
password=os.getenv('password_MongoDB')
uri = f"mongodb+srv://{login}:{password}@cluster0.25d5slc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

class GrupoMongoAdapter:
    def __init__(self, str = "LutheriaFermino2"):

        self.db_name = str # Nome dob banco de dados
        self.collection_name = "grupo" # Nome da coleção de grupos

        # Cria um novo cliente MongoDB e se conecta com o servidor
        self.client = MongoClient(uri, server_api=ServerApi('1'))

    def get_grupo(self, id):
        # Busca o grupo pelo ID
        grupo = self.collection_name.find_one({"_id": ObjectId(id)})

        return grupo
    
    def create_grupo(self, grupo):
        #Insere um grupo no banco de dados
        grupo = self.collection_name.insert_one(grupo)
        return grupo
    
    def delete_grupo(self, id):
        #Deleta um grupo do banco de dados
        grupo = self.collection_name.delete_one({"_id": ObjectId(id)})
        return grupo
        
    def update_grupo(self, id, grupo):
        #Atualiza um grupo no banco de dados
        grupo = self.collection_name.update_one({"_id": ObjectId(id)}, {"$set": grupo})
        return grupo