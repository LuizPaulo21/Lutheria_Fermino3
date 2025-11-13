import os, dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId #Para converter para ObjectId

dotenv.load_dotenv()

# Carregar as variáveis de ambiente do arquivo .env
login=os.getenv('user_MongoDB')
password=os.getenv('password_MongoDB')
uri = f"mongodb+srv://{login}:{password}@cluster0.25d5slc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

class ProdutoMongoAdapter:
    def __init__(self, db_name: str):
        
        self.db_name = db_name # Nome dob banco de dados
        self.collection_name = "clientes" # Nome da coleção de clientes

        # Cria um novo cliente MongoDB e se conecta com o servidor
        self.client = MongoClient(uri, server_api=ServerApi('1'))


