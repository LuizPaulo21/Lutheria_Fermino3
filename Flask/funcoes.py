from flask import Blueprint, render_template, request, session, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import hashlib, os, dotenv
from flask import current_app
import pandas as pd
from lifetimes.utils import summary_data_from_transaction_data
from lifetimes import BetaGeoFitter
import datetime
import os, dotenv
import bson.json_util
from bson.objectid import ObjectId


# Carregar as variáveis de ambiente do arquivo .env
login=os.getenv('user_MongoDB')
password=os.getenv('password_MongoDB')
uri = f"mongodb+srv://{login}:{password}@cluster0.25d5slc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

dotenv.load_dotenv()

bp = Blueprint("funcoes", __name__, url_prefix="/")

dotenv.load_dotenv()
login=os.getenv('user_MongoDB')
password=os.getenv('password_MongoDB')
uri = f"mongodb+srv://{login}:{password}@cluster0.25d5slc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

@bp.route('/login', methods=['POST'])
def login():

    # Aqui é verificado se o método da requisição é POST e se os compos necessários foram preenchidos. 
    # Em seguida, os valores dos campos são armazenados em variáveis.
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        usuario = request.form.get('username')
        senha = request.form.get('password')

    # Faz o hash da senha para evitar que a senha original seja exposta
    hash = senha + os.getenv('SECRETKEY')
    hash = hashlib.sha1(hash.encode())
    senha = hash.hexdigest()

    # Cria uma conexão ao MongoDB
    db = "LutheriaFermino2" # Nome do banco de dados
    collection = "usuarios" # Nome da coleção de clientes
    # Cria um novo cliente MongoDB e se conecta com o servidor
    client = MongoClient(uri, server_api=ServerApi('1'))
    collection = client[db][collection]

    # Busca um registro e retorna o resultado
    usuario = collection.find_one({
        "usuario": usuario,
        "senha": senha
    })

    #Convertendo o id do usuario para string
    if usuario:
        usuario['_id'] = str(usuario['_id'])

    # Verificando se existe o usuario no banco de dados
    if usuario:
        # Dados da sessão
        session['loggedin'] = True
        session['id']= usuario['_id']
        session['username']=usuario['usuario']

        # Redireciona ao inicio do sistema
        return render_template("inicio.html")
    else:
        msg = "Usuario ou senha incorretos!"

    return render_template('inicio.html', msg=msg)

#Função para salvar o cliente no banco de dados
@bp.route('/create_cliente', methods=['POST'])
def create_cliente():
    # Verifica se o método da requisição é POST e se os campos necessários foram preenchidos
    if request.method == 'POST':

        ejuridica = bool(request.form.get('tipoPessoaJuridica'))

        nome_completo = request.form.get('nomeCompleto')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        cnpj = request.form.get('cnpj')
        razao_social = request.form.get('razaoSocial')
        nome_fantasia = request.form.get('nomeFantasia')
        endereco = request.form.get('logradouro')
        cep = request.form.get('cep')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')

        cliente_data = {
                "nome": nome_completo,
                "cpf": cpf,
                "cnpj": cnpj,
                "razaoSocial": razao_social,
                "nomeFantasia": nome_fantasia,
                "email": email,
                "cnpj": cnpj,
                "endereco": endereco,
                "cep": cep,
                "bairro": bairro,  
                "cidade": cidade,
                "estado": estado, 
                "tipoPessoaJuridica": ejuridica
            }

        # Validação mínima na rota (o Caso de Uso fará a validação completa)
        if ejuridica:
            msg = "Nome e E-mail são campos obrigatórios."
            return render_template('cadastro_cliente.html', msg=msg)
        else:
            # Acessa o Caso de Uso
            use_case_key = 'use_case'
            if use_case_key not in current_app.extensions:
                msg = "Erro crítico: Configuração de casos de uso não encontrada."
                return render_template('cadastro_cliente.html', msg=msg)

            create_cliente_uc = current_app.extensions['use_case'].get('create_cliente')

            if not create_cliente_uc:
                msg = "Erro: Serviço de criação de cliente indisponível."
                return render_template('cadastro_cliente.html', msg=msg)
            
            try:
                novo_cliente = create_cliente_uc.execute(cliente_data)
                if novo_cliente:
                    msg = f"Cliente '{novo_cliente.get('nome', 'N/A')}' cadastrado com sucesso!"
                else:
                    msg = "Erro ao cadastrar cliente. Verifique os dados ou os logs do servidor."
            except ValueError as ve: # Captura erros de validação do Caso de Uso
                msg = f"Erro de validação: {ve}"
            except Exception as e:
                current_app.logger.error(f"Exceção em create_cliente (POST): {e}", exc_info=True)
                msg = "Ocorreu um erro inesperado ao processar sua solicitação."
    
    # Para o método GET (exibir o formulário) ou após o POST (para mostrar a msg)
    return render_template('cadastro_cliente.html', msg=msg)

#Função de busca de clientes para o JS
@bp.route('/cliente', methods=['GET'])
def cliente():
# Pega o termo de busca da query string
    termo_busca = request.args.get('termo', '')

    db_name = "LutheriaFermino2"
    collection_name = "clientes"
    
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client[db_name]
        collection = db[collection_name]

        # Prepara a query para buscar clientes cujo 'nome_completo' contenha o termo_busca (case-insensitive)
        # Se o termo_busca estiver vazio, pode retornar uma lista vazia ou os primeiros N clientes,
        # dependendo do comportamento desejado. Aqui, retornaremos correspondências.
        if termo_busca:
            # Usando regex para busca "contém" e 'i' para case-insensitive
            query = {"nome": {"$regex": termo_busca, "$options": "i"}}
            resultados_cursor = collection.find(query).limit(10) 
        else:
            # Se nenhum termo for fornecido, retorna uma lista vazia
            resultados_cursor = [] 

        clientes_lista = []
        for cliente in resultados_cursor:
            # É importante converter ObjectId para string para ser serializável em JSON
            cliente['_id'] = str(cliente['_id']) 
            clientes_lista.append(cliente)
        
        client.close() # Fechar a conexão
        return jsonify(clientes_lista)

    except Exception as e:
        print(f"Erro ao buscar clientes: {e}")

#Função de busca de clientes para o JS
@bp.route('/produto', methods=['GET'])
def produto():
# Pega o termo de busca da query string
    termo_busca = request.args.get('termo', '')

    db_name = "LutheriaFermino2"
    collection_name = "produtos"
    
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client[db_name]
        collection = db[collection_name]

        # Prepara a query para buscar produtos cujo 'nome' contenha o termo_busca (case-insensitive)
        # Se o termo_busca estiver vazio, pode retornar uma lista vazia ou os primeiros N produtos,
        if termo_busca:
            # Usando regex para busca "contém" e 'i' para case-insensitive
            query = {"nome": {"$regex": termo_busca, "$options": "i"}}
            resultados_cursor = collection.find(query).limit(10) 
        else:
            # Se nenhum termo for fornecido, retorna uma lista vazia
            resultados_cursor = [] 

        produtos_lista = []
        for produto in resultados_cursor:
            # É importante converter ObjectId para string para ser serializável em JSON
            produto['_id'] = str(produto['_id']) 
            produtos_lista.append(produto)
        
        client.close() # Fechar a conexão
        return jsonify(produtos_lista)

    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        return jsonify({"error": "Erro ao buscar produtos."})


#Função para salvar o pedido no banco de dados
@bp.route('/create_pedido', methods=['POST'])
def create_pedido():
    
        if request.is_json:
            dados_recebidos = request.get_json()
            print("Dados recebidos (JSON):", dados_recebidos)
        else:
            dados_recebidos = request.form.to_dict() # .to_dict() para melhor visualização
            print("Dados recebidos (Form):", dados_recebidos)
  

        create_pedido_uc = current_app.extensions['use_case'].get('create_pedido')

        # Acessa o Caso de Uso
        use_case_key = 'use_case'
        if use_case_key not in current_app.extensions:
             msg = "Erro crítico: Casos de uso não encontrado."
             return render_template('cadastro_pedido.html', msg=msg)
        else:
             if not create_pedido_uc:
                 msg = "Erro: Serviço de criação de pedido indisponível."
                 return render_template('cadastro_pedido.html', msg=msg)
             try:
                 novo_pedido = create_pedido_uc.execute(dados_recebidos)
                 if novo_pedido:
                     msg = f"Pedido '{novo_pedido.get('id', 'N/A')}' cadastrado com sucesso!"
                     return render_template('cadastro_pedido.html', msg=msg)
                 else:
                     msg = "Erro ao cadastrar pedido. Verifique os dados ou os logs do servidor."
                     return render_template('cadastro_pedido.html', msg=msg)
             except ValueError as ve:
                 msg = f"Erro de validação: {ve}"
                 return render_template('cadastro_pedido.html', msg=msg)
             
#Função para buscar dados de ML
#@bp.route('/mldata', methods=['GET'])
def mldata():

            db_name = "LutheriaFermino2"
            collection_name = "pedidos"
            # Cria um novo cliente MongoDB e se conecta com o servidor
            client = MongoClient(uri, server_api=ServerApi('1'))

            db = client[db_name]
            collection = db[collection_name] 

            #busca os pedidos no banco de dados
            try:
                cursor = collection.find({})
                documentos = list(cursor)
                retorno = bson.json_util.dumps(documentos)
                
                #monta um dataframe com os dados retornados e filtra as colunas necessárias
                pedidos_df = pd.read_json(retorno)
                pedidos_filtrados_df = pedidos_df[['id_cliente', 'datapedido',]]
                
                #Convertendo os dados do tipo object para os necessário para as funções do lifetimes
                pedidos_filtrados_df['datapedido'] = pd.to_datetime(pedidos_filtrados_df['datapedido'], format="%d-%m-%Y")
                pedidos_filtrados_df['id_cliente'] = pedidos_filtrados_df['id_cliente'].astype(str)

                #previsão de pedidos
                rfm_df = summary_data_from_transaction_data(
                transactions= pedidos_filtrados_df,
                customer_id_col='id_cliente',
                datetime_col='datapedido',
                freq='D'
                )

                #Usando o beta geo fitter
                bgf = BetaGeoFitter(penalizer_coef=0.01) # campo utilizado para impedir overfitting dos dados
                # treinando o modelo
                bgf.fit(rfm_df['frequency'], rfm_df['recency'], rfm_df['T'])
                print("Modelo BG/NBD treinado com sucesso!")

                #Aqui vamos prever quantos pedidos o cliente fará nos próximos 30 dias
                t = 30  # Dias
                rfm_df['pedidos_prox_30_dias'] = bgf.conditional_expected_number_of_purchases_up_to_time(
                    t, 
                    rfm_df['frequency'], 
                    rfm_df['recency'], 
                    rfm_df['T']
                )

                # --- Seleção e Retorno dos Top 5 Clientes ---
                
                # Seleciona as colunas relevantes e ordena pela previsão
                # Se houver menos de 5 clientes válidos, ele retornará todos que existem.
                top_5_predicoes = rfm_df.sort_values(
                    by='pedidos_prox_30_dias', 
                    ascending=False
                ).head(5)

                # O índice é o cliente_id. Para retorná-lo no JSON como uma coluna chamada 'cliente_id',
                # precisamos resetar o índice e renomear a coluna resultante (que será 'index')
                top_5_predicoes = top_5_predicoes.reset_index()
                top_5_predicoes.rename(columns={'index': 'id_cliente'}, inplace=True)


                print(f"\nPedidos Previstos nos Próximos {t} Dias (Top 5):")
                # Exibe as colunas desejadas para o log
                print(top_5_predicoes[['id_cliente', 'pedidos_prox_30_dias', 'frequency', 'recency', 'T']])
            
                #Chamando a função para obter o nome do cliente
                top_5_predicoes_lista = top_5_predicoes['id_cliente'].tolist() #convertendo para lista
                top_5_predicoes['nome_cliente'] = get_client_name(top_5_predicoes_lista)

                # Retorna apenas os Top 5 Clientes em formato JSON (lista de objetos),
                # garantindo que o ID do cliente esteja explícito na chave 'cliente_id'.
                lista_clientes_30_dias = top_5_predicoes.to_dict(orient='records')
                return lista_clientes_30_dias
                            
            except Exception as e:
                print(f"Erro ao buscar pedidos no MongoDB: {e}")
                return []


def get_client_name(client_id):
    """Função auxiliar para obter o nome do cliente pelo ID."""

    db_name = "LutheriaFermino2"
    collection_name = "clientes"
    
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client[db_name]
        collection = db[collection_name]

        cliente_resultado = []
        print("IDs de clientes para busca de nome:", client_id)

        for current_cliente_id in client_id: #para cada um dos itens da lista de id

            try:
                bson_id = ObjectId(current_cliente_id) #converter o id em objectId
                cliente_doc = collection.find_one({"_id": bson_id}) #buscar no banco
                if cliente_doc:
                    cliente_resultado.append(cliente_doc['nome']) # se existe, adiciona o nome na lista
                else:
                    cliente_resultado.append('Cliente não encontrado') # se não existe, adiciona a mensagem
            except Exception as e:
                print(f"Erro ao converter ou buscar cliente com ID {current_cliente_id}: {e}") #log de erro
                cliente_resultado.append('Erro ao buscar cliente')

        return cliente_resultado

    except Exception as e:
        print(f"Erro ao buscar cliente: {e}")
        return "Erro ao buscar cliente"