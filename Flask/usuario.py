import hashlib, os, dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#O usuário do sistema será o mesmo que o do banco de dados
# Carregar as variáveis de ambiente do arquivo .env

dotenv.load_dotenv()
login=os.getenv('user_MongoDB')
password=os.getenv('password_MongoDB')
uri = f"mongodb+srv://{login}:{password}@cluster0.25d5slc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Faz o hash da senha para evitar que a senha original seja exposta
hash = password + os.getenv('SECRETKEY')
hash = hashlib.sha1(hash.encode())
senha = hash.hexdigest()

db = "LutheriaFermino2" # Nome do banco de dados
collection = "usuarios" # Nome da coleção de clientes
# Cria um novo cliente MongoDB e se conecta com o servidor
client = MongoClient(uri, server_api=ServerApi('1'))

collection = client[db][collection]

resultado = collection.insert_one({
    "usuario": login,
    "senha": senha,
    "nivel_acesso": 1
})

if resultado:
    print("Usuário inserido com sucesso!")
else:
    print("Erro ao inserir o usuário.")