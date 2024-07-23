import mysql.connector
from mysql.connector import Error

from dotenv import load_dotenv
import os

def AdicionarCliente(nome,telefone,cpf,endereco,cep,aniversario):

    try:

        load_dotenv()

        connection = mysql.connector.connect(
            host = os.getenv('HOST'),
            database = os.getenv('DATABASE'),
            user = os.getenv('USER'),
            password = os.getenv('PASSWORD')
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            # Inserindo dados
            inserir = "INSERT INTO cliente (nome, telefone, cpf, endereco, cep, aniversario) VALUES (%s, %s, %s, %s, %s, %s)"
            record = (nome, telefone, cpf, endereco, cep, aniversario)
            cursor.execute(inserir, record)
            connection.commit()

    except Error as e:
        return f'Erro:\n{e}\nVerifique os dados no MySql'
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def RemoverCLiente(nome):

    try:

        load_dotenv()

        connection = mysql.connector.connect(
            host = os.getenv('HOST'),
            database = os.getenv('DATABASE'),
            user = os.getenv('USER'),
            password = os.getenv('PASSWORD')
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            # Removendo dados
            deletar = "DELETE FROM cliente WHERE nome = %s"
            record = (nome,)
            cursor.execute(deletar, record)
            connection.commit()

            deletar = "DELETE FROM vendas WHERE cliente = %s"
            record = (nome,)
            cursor.execute(deletar, record)
            connection.commit()

    except Error as e:
        return f'Erro:\n{e}\nVerifique os dados no MySql'
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def AdicionarVenda(cliente,produto,qnt,consideracoes,dataPedido,dataEntrega,valor):

    produto = '/'.join(produto)

    try:

        load_dotenv()

        connection = mysql.connector.connect(
            host = os.getenv('HOST'),
            database = os.getenv('DATABASE'),
            user = os.getenv('USER'),
            password = os.getenv('PASSWORD')
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            # Inserindo dados
            inserir = "INSERT INTO vendas (cliente, produto, qnt, consideracoes, datapedido, dataentrega, valor) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            record = (cliente, produto, qnt, consideracoes, dataPedido, dataEntrega, valor)
            cursor.execute(inserir, record)
            connection.commit()

    except Error as e:
        return f'Erro:\n{e}\nVerifique os dados no MySql'
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def AtualizarQntPedidos(valor,qnt,nome):

    try:

        load_dotenv()

        connection = mysql.connector.connect(
            host = os.getenv('HOST'),
            database = os.getenv('DATABASE'),
            user = os.getenv('USER'),
            password = os.getenv('PASSWORD')
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            # Inserindo dados
            atualizar_qnt = "UPDATE cliente SET qnt_pedidos = %s WHERE nome = %s"
            record = (qnt,nome)
            cursor.execute(atualizar_qnt,record)
            connection.commit()
            atualizar_valor = "UPDATE cliente SET valor = %s WHERE nome = %s"
            record = (valor,nome)
            cursor.execute(atualizar_valor,record)
            connection.commit()

    except:
        pass
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def AlterarCliente(tipo,dadoNovo,nome):

    dadoNovo = str(dadoNovo)

    try:

        load_dotenv()

        connection = mysql.connector.connect(
            host = os.getenv('HOST'),
            database = os.getenv('DATABASE'),
            user = os.getenv('USER'),
            password = os.getenv('PASSWORD')
        )

        if connection.is_connected():
            cursor = connection.cursor()

            if tipo == 'Nome':
            
                # Alterando dados
                alterar= "UPDATE cliente SET nome = %s WHERE nome = %s"
                record = (dadoNovo, nome)
                cursor.execute(alterar, record)
                connection.commit()

            elif tipo == 'CPF':
               # Alterando dados
                alterar = "UPDATE cliente SET cpf = %s WHERE nome = %s"
                record = (dadoNovo, nome)
                cursor.execute(alterar, record)
                connection.commit()

            elif tipo == 'Telefone':
               # Alterando dados
                alterar = "UPDATE cliente SET telefone = %s WHERE nome = %s"
                record = (dadoNovo, nome)
                cursor.execute(alterar, record)
                connection.commit()

            elif tipo == 'Endereco':
               # Alterando dados
                alterar = "UPDATE cliente SET endereco = %s WHERE nome = %s"
                record = (dadoNovo, nome)
                cursor.execute(alterar, record)
                connection.commit()

    except Error as e:
        return f'Erro:\n{e}\nVerifique os dados no MySql'
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
