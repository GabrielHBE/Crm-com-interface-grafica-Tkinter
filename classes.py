class Clientes:

    def __init__(self, nome=None, telefone=None, cpf=None, endereco=None,valor=0.0, qntPedidos=0, cep=None, aniversario=None) -> None:
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.endereco = endereco
        self.valor = valor
        self.qntPedidos = qntPedidos
        self.cep = cep
        self.aniversario = aniversario

class Venda:

    def __init__(self, produto=None, qnt=0, consideracoes=None, dataPedido=None, dataEntrega=None, cliente=None, valor=0.0, frete=0.0) -> None:
        self.produto = produto
        self.qnt = qnt
        self.consideracoes = consideracoes
        self.dataPedido = dataPedido
        self.dataEntrega = dataEntrega
        self.cliente = cliente
        self.valor = valor
        self.frete = frete