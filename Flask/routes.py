from flask import Blueprint, render_template

bp = Blueprint("routes", __name__, url_prefix="/")

#Rota da página login
@bp.route('/')
@bp.route('/index')
def hello():
    return render_template("login.html")

#Rota da página inicial
@bp.route('/inicio.html')
def inicio():
    return render_template("inicio.html")

################################
# Seção de páginas de cadastro #
################################

#Rota para a pagina de cadastro de cliente
@bp.route('/cadastro_cliente.html')
def cadastro_cliente():
    return render_template("cadastro_cliente.html")

#Rota para alterar cliente
@bp.route('/alterar_cliente.html')
def alterar_cliente():
    return render_template("alterar_cliente.html")

#Rota para excluir cliente
@bp.route('/excluir_cliente.html')
def excluir_cliente():
    return render_template("excluir_cliente.html")

#Rota para Cadastro de pedidos
@bp.route('/cadastro_pedido.html')
def cadastro_pedido():
    return render_template("cadastro_pedido.html")

#Rota para alterar pedido
@bp.route('/alterar_pedido.html')
def alterar_pedido():
    return render_template("alterar_pedido.html")

#Rota para excluir pedido
@bp.route('/excluir_pedido.html')
def excluir_pedido():
    return render_template("excluir_pedido.html")

#Rota para Cadastro de produtos
@bp.route('/cadastro_produto.html')
def cadastro_produto():
    return render_template("cadastro_produto.html")

#Produtos não podem ser alterados para manter a integridade do sistema

#Rota para Cadastro de Grupos de produtos
@bp.route('/cadastro_grupo.html')   
def cadastro_grupo_produto():
    return render_template("cadastro_grupo.html")

#Rota para alterar grupo/fornecedores
@bp.route('/alterar_grupo.html')
def alterar_grupo_produto():
    return render_template("alterar_grupo.html")

#Fornecedores não podem ser alterados para manter a integridade do sistema


