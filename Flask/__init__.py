import os
import dotenv
from flask import Flask
from Flask.repositories import clienteRepository
from Flask.repositories import produtoRepository
from Flask.repositories import pedidoRepository
from Flask.repositories import grupoRepository
from Flask.adapters.MongoAdapters.ClienteMongoAdapter import ClienteMongoAdapter
from Flask.adapters.MongoAdapters.ProdutoMongoAdapter import ProdutoMongoAdapter
from Flask.adapters.MongoAdapters.PedidosMongoAdapter import PedidosMongoAdapter
from Flask.adapters.MongoAdapters.GrupoMongoAdapter import GrupoMongoAdapter
from Flask.usecases.Cliente.CreateClienteUseCase import CreateClienteUseCase
from Flask.usecases.Cliente.DeleteClienteUserCase import DeleteClienteUserCase
from Flask.usecases.Cliente.UpdateClienteUseCase import UpdateClienteUseCase
from Flask.usecases.Cliente.GetClienteUseCase import GetClienteUseCase
from Flask.usecases.Pedidos.CreatePedidoUseCase import CreatePedidoUseCase
from Flask.usecases.Pedidos.DeletePedidoUseCase import DeletePedidoUserCase
from Flask.usecases.Pedidos.UpdatePedidoUseCase import UpdatePedidoUseCase
from Flask.usecases.Pedidos.GetPedidoUseCase import GetPedidoUseCase
from Flask.usecases.Produtos.CreateProdutoUseCase import CreateProdutoUseCase
from Flask.usecases.Produtos.DeleteProdutoUseCase import DeleteProdutoUseCase
from Flask.usecases.Produtos.UpdateProdutoUseCase import UpdateProdutoUseCase
from Flask.usecases.Produtos.GetProdutoUseCase import GetProdutoUseCase
from Flask.usecases.Grupo.CreateGrupoUseCase import CreateGrupoUseCase
from Flask.usecases.Grupo.DeleteGrupoUseCase import DeleteGrupoUseCase
from Flask.usecases.Grupo.UpdateGrupoUseCase import UpdateGrupoUseCase
from Flask.usecases.Grupo.GetGrupoUseCase import GetGrupoUseCase
from. import funcoes
from. import routes

dotenv.load_dotenv()
login=os.getenv('user_MongoDB')
password=os.getenv('password_MongoDB')
uri = f"mongodb+srv://{login}:{password}@cluster0.25d5slc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
db_nome = "LutheriaFermino2" # Nome do banco de dados


def create_app(test_config=None):
    
    #Cria variável global Flask. __name__ é o nome do modulo python atual.
    #O segundo parametro, indica que os arquivos de configuração estão na pasta instance, que fica fora do pacote atual.
    app = Flask(__name__, instance_relative_config=True)

    #Define alguns parametros que o APP terá
    app.config.from_mapping(
        SECRET_KEY='dev',
        )

    if test_config is None:
        #Sobrescreve as configurações padrão por aquelas presentes no arquivo na pasta instance. Pode ser usado para definir uma SECRET_KEY verdadeira.
        app.config.from_pyfile('config.py', silent=True)
    else:
        #Configurações de teste podem ser passadas, para diferir dos valores de desenvolvimento.
        app.config.from_mapping(test_config)

    try:
        #Para ter certeza que o diretório de instance exista
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #Registra o blueprint criado (arquivo com rotas)
    app.register_blueprint(routes.bp)

    #Registra o blueprint criado (arquivo com funcoes)
    app.register_blueprint(funcoes.bp)

    #Inicializando os adaptadores para clientes
    try:
        # ClienteMongoAdapter que implementa a interface clienteRepository
        cliente_repository_instance: clienteRepository = ClienteMongoAdapter(db_nome)
        create_use_case_instance = CreateClienteUseCase(cliente_repository=cliente_repository_instance)
        delete_use_case_instance = DeleteClienteUserCase(cliente_repository=cliente_repository_instance)
        update_use_case_instance = UpdateClienteUseCase(cliente_repository=cliente_repository_instance)
        get_use_case_instance = GetClienteUseCase(cliente_repository=cliente_repository_instance)
        print("ClienteMongoAdapter instanciado com sucesso.")
    except ConnectionError as e: 
        print(f"CRÍTICO: Falha ao conectar ao MongoDB na inicialização do adapter: {e}")
        cliente_repository_instance = None
    except Exception as e:
        print(f"CRÍTICO: Erro inesperado ao instanciar ClienteMongoAdapter: {e}")
        cliente_repository_instance = None

        #Inicializando os adaptadores para produtos
    try:
        # ProdutoMongoAdapter que implementa a interface produtoRepository
        produto_repository_instance: produtoRepository = ProdutoMongoAdapter(db_nome)
        create_produto_use_case_instance = CreateProdutoUseCase(produto_repository=produto_repository_instance)
        delete_produto_use_case_instance = DeleteProdutoUseCase(produto_repository=produto_repository_instance)
        update_produto_use_case_instance = UpdateProdutoUseCase(produto_repository=produto_repository_instance)
        get_produto_use_case_instance = GetProdutoUseCase(produto_repository=produto_repository_instance)
        print("ProdutoMongoAdapter instanciado com sucesso.")
    except ConnectionError as e: 
        print(f"CRÍTICO: Falha ao conectar ao MongoDB na inicialização do adapter: {e}")
        produto_repository_instance = None
    except Exception as e:
        print(f"CRÍTICO: Erro inesperado ao instanciar ClienteMongoAdapter: {e}")
        produto_repository_instance = None
    
    #Inicializando os adaptadores para pedidos
    try:
        # ClienteMongoAdapter que implementa a interface pedidoRepository
        pedido_repository_instance: pedidoRepository = PedidosMongoAdapter()
        create_pedido_use_case_instance = CreatePedidoUseCase(pedido_repository=pedido_repository_instance)
        delete_pedido_use_case_instance = DeletePedidoUserCase(pedido_repository=pedido_repository_instance)
        update_pedido_use_case_instance = UpdatePedidoUseCase(pedido_repository=pedido_repository_instance)
        get_pedido_use_case_instance = GetPedidoUseCase(pedido_repository=pedido_repository_instance)
        print("PedidoMongoAdapter instanciado com sucesso.")
    except ConnectionError as e: 
        print(f"CRÍTICO: Falha ao conectar ao MongoDB na inicialização do adapter: {e}")
        pedido_repository_instance = None
    except Exception as e:
        print(f"CRÍTICO: Erro inesperado ao instanciar ClienteMongoAdapter: {e}")
        pedido_repository_instance = None

    #Inicializando os adaptadores para grupos de produtos
    try:
        # ClienteMongoAdapter que implementa a interface grupoProdutoRepository
        grupo_produto_repository_instance: grupoRepository = GrupoMongoAdapter()
        create_grupo_use_case_instance = CreateGrupoUseCase(grupo_repository=grupo_produto_repository_instance)
        delete_grupo_use_case_instance = DeleteGrupoUseCase(grupo_repository=grupo_produto_repository_instance)
        update_grupo_use_case_instance = UpdateGrupoUseCase(grupo_repository=grupo_produto_repository_instance)
        get_grupo_use_case_instance = GetGrupoUseCase(grupo_repository=grupo_produto_repository_instance)
        print("GrupoProdutoMongoAdapter instanciado com sucesso.")
    except ConnectionError as e:
        print(f"CRÍTICO: Falha ao conectar ao MongoDB na inicialização do adapter: {e}")
        grupo_produto_repository_instance = None
    except Exception as e:
        print(f"CRÍTICO: Erro inesperado ao instanciar ClienteMongoAdapter: {e}")
        grupo_produto_repository_instance = None

    #Inicializando váriáveis para evitar erro de unbound
    delete_produto_use_case_instance = None
    update_produto_use_case_instance = None
    get_produto_use_case_instance = None
    create_produto_use_case_instance = None
    

    with app.app_context():
        app.extensions['use_case'] = {}
        #Grupo de casos de uso para clientes
        app.extensions['use_case']['create_cliente'] = create_use_case_instance
        app.extensions['use_case']['delete_cliente'] = delete_use_case_instance
        app.extensions['use_case']['update_cliente'] = update_use_case_instance
        app.extensions['use_case']['get_cliente'] = get_use_case_instance

        #Grupo de casos de uso para pedidos
        app.extensions['use_case']['create_pedido'] = create_pedido_use_case_instance
        app.extensions['use_case']['delete_pedido'] = delete_pedido_use_case_instance
        app.extensions['use_case']['update_pedido'] = update_pedido_use_case_instance
        app.extensions['use_case']['get_pedido'] = get_pedido_use_case_instance

        #Grupo de casos de uso para produtos
        app.extensions['use_case']['create_produto'] = create_produto_use_case_instance
        app.extensions['use_case']['delete_produto'] = delete_produto_use_case_instance
        app.extensions['use_case']['update_produto'] = update_produto_use_case_instance
        app.extensions['use_case']['get_produto'] = get_produto_use_case_instance

        #Grupo de casos de uso para grupos de produtos
        app.extensions['use_case']['create_grupo'] = create_grupo_use_case_instance
        app.extensions['use_case']['delete_grupo'] = delete_grupo_use_case_instance
        app.extensions['use_case']['update_grupo'] = update_grupo_use_case_instance
        app.extensions['use_case']['get_grupo'] = get_grupo_use_case_instance

    return app
