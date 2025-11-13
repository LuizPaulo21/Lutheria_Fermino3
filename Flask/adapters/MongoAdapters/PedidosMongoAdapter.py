import os, dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId #Para converter para ObjectId
from datetime import datetime # Para lidar com datas
from typing import Dict, Optional # Para anotações de tipo

dotenv.load_dotenv()

# Carregar as variáveis de ambiente do arquivo .env
login=os.getenv('user_MongoDB')
password=os.getenv('password_MongoDB')
uri = f"mongodb+srv://{login}:{password}@cluster0.25d5slc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

class PedidosMongoAdapter:
    def __init__(self, str = "LutheriaFermino2"):

        self.db_name = str # Nome dob banco de dados
        self.collection_name = "pedidos" # Nome da coleção de clientes

        # Cria um novo cliente MongoDB e se conecta com o servidor
        self.client = MongoClient(uri, server_api=ServerApi('1'))

    def create_pedido(self, pedido_data: Dict) -> Optional[Dict]:

        if not self.client:
            print("Erro de conexão com o banco de dados. Não é possível criar o pedido.")
            return None
        else:
            db = self.client[self.db_name]
            collection = db[self.collection_name]

        if not pedido_data:
            print("Dados do pedido não fornecidos para criação.")
            return None
        


        dados_para_inserir = pedido_data.copy() # Uma cópia dosdados para evitar mutações indesejadas

        # Converter id_cliente e id_produto para ObjectId se forem strings
        for id_field in ["id_cliente", "id_produto"]:
            if id_field in dados_para_inserir and isinstance(dados_para_inserir[id_field], str):
                try:
                    dados_para_inserir[id_field] = ObjectId(dados_para_inserir[id_field])
                except Exception as e:
                    print(f"Erro ao converter '{id_field}' ('{dados_para_inserir[id_field]}') para ObjectId: {e}. O campo será mantido como string ou removido se inválido.")
                    # Decida como tratar: remover, manter como string, ou falhar a operação
                    # Por simplicidade, vamos falhar se a conversão for crucial e falhar.
                    # return None

        # Tratar o campo 'data'
        # Se não fornecido, pode-se usar a data atual. Se fornecido como string, tentar converter.
        if "data" not in dados_para_inserir or not dados_para_inserir["data"]:
            dados_para_inserir["data"] = datetime.now() # Usar data atual em UTC
        elif isinstance(dados_para_inserir["data"], str):
            try:
                # Tentar converter se for uma string
                dados_para_inserir["data"] = datetime.fromisoformat(dados_para_inserir["data"].replace("Z", "+00:00"))
            except ValueError:
                print(f"Formato de data inválido para '{dados_para_inserir['data']}'. Usando data atual.")
                dados_para_inserir["data"] = datetime.now() 
        #Tenta inserir o pedido no MongoDB
        try:
            result = collection.insert_one(dados_para_inserir)
            print(f"Pedido inserido com ID: {result.inserted_id}")

            documento_criado = collection.find_one({"_id": result.inserted_id})
            return self._convert_document_to_strings(documento_criado) if documento_criado else None
        except Exception as e:
            print(f"Erro ao criar pedido no MongoDB: {e}")
            return None

#Função para buscar um pedido
    def get_pedido(self, pedido_id_str: str) -> Optional[Dict]:
        if not self.client:
            print("Erro de conexão com o banco de dados. Não é possível buscar o pedido.")
            return None

        db = self.client[self.db_name]
        collection = db[self.collection_name]

        try:
            idProcurado = ObjectId(pedido_id_str)
        except Exception as e:
            print(f"ID de pedido fornecido ('{pedido_id_str}') não é um ObjectId válido: {e}")
            return None

        documento = collection.find_one({"_id": idProcurado})
        #Retorna os dados no formato string
        if documento:
            return self._convert_document_to_strings(documento)
        else:
            print(f"Pedido com ID '{pedido_id_str}' não encontrado.")
            return None
        
#Função para atualizar um pedido
    def update_pedido(self, pedido_id_str: str, pedido_novos_dados: Dict) -> Optional[Dict]:
        if not self.client:
            print("Erro de conexão com o banco de dados. Não é possível atualizar o pedido.")
            return None

        if not pedido_novos_dados:
            print("Nenhum dado fornecido para atualização do pedido.")
            return None

        db = self.client[self.db_name]
        collection = db[self.collection_name]

        try:
            object_id_to_update = ObjectId(pedido_id_str)
        except Exception as e:
            print(f"ID de pedido fornecido ('{pedido_id_str}') não é válido para atualização: {e}")
            return None

        dados_para_atualizar = pedido_novos_dados.copy()
        if "_id" in dados_para_atualizar: # Não pode atualizar o ID do pedido
            del dados_para_atualizar["_id"]

        # Converter os outros IDs presentes
        for id_field in ["id_cliente", "id_produto"]:
            if id_field in dados_para_atualizar and isinstance(dados_para_atualizar[id_field], str):
                try:
                    dados_para_atualizar[id_field] = ObjectId(dados_para_atualizar[id_field])
                except Exception as e:
                    print(f"Erro ao converter '{id_field}' para atualização: {e}. O campo será mantido como string.")
                 

        # Se o campo data estiver em formato string, tentar converter
        if "data" in dados_para_atualizar and isinstance(dados_para_atualizar["data"], str):
            try:
                dados_para_atualizar["data"] = datetime.fromisoformat(dados_para_atualizar["data"].replace("Z", "+00:00"))
            except ValueError:
                print(f"Formato de data inválido para atualização: '{dados_para_atualizar['data']}'. O campo não será atualizado com este valor.")


        if not dados_para_atualizar: # Se após as manipulações não sobrar nada para atualizar
            print("Nenhum dado válido para atualização após o processamento.")
            return self.get_pedido(pedido_id_str) # Retorna o estado atual

        try:
            result = collection.update_one(
                {"_id": object_id_to_update}, #ID do pedido a ser atualizado
                {"$set": dados_para_atualizar} # Dados a serem atualizados
            )

            if result.matched_count == 0: #Se nada atualizado (dados iguais ou inexistentes)
                print(f"Pedido com ID '{pedido_id_str}' não encontrado para atualização.")
                return None
            
            print(f"Pedido com ID '{pedido_id_str}' verificado para atualização. Modificados: {result.modified_count}.")
            # Mesmo que modified_count seja 0 (dados iguais), devolve um documento.
            documento_atualizado = collection.find_one({"_id": object_id_to_update})
            return self._convert_document_to_strings(documento_atualizado) if documento_atualizado else None

        except Exception as e:
            print(f"Erro ao atualizar pedido com ID '{pedido_id_str}' no MongoDB: {e}")
            return None

#Função para deletar um pedido
    def delete_pedido(self, pedido_id_str: str) -> None: 
        if not self.client:
            print("Erro de conexão com o banco de dados. Não é possível deletar o pedido.")
            return

        db = self.client[self.db_name]
        collection = db[self.collection_name]

        try:
            object_id_to_delete = ObjectId(pedido_id_str)
        except Exception as e:
            print(f"ID de pedido fornecido ('{pedido_id_str}') não é um ObjectId válido para deleção: {e}")
            return

        try:
            result = collection.delete_one({"_id": object_id_to_delete})

            if result.deleted_count > 0:
                print(f"Pedido com ID '{pedido_id_str}' deletado com sucesso.")
            else:
                print(f"Nenhum pedido encontrado com ID '{pedido_id_str}' para deletar.")
        except Exception as e:
            print(f"Erro ao deletar pedido com ID '{pedido_id_str}' no MongoDB: {e}")

        if self.client:
            self.client.close()
            print("MongoDB connection for Pedidos closed.")