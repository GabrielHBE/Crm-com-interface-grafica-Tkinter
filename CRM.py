from tkinter import *
from tkinter import ttk

from tkcalendar import *
from datetime import datetime
import babel.numbers

from dotenv import load_dotenv
import os

#Inicialização das classes
from classes import Clientes,Venda

#Aqui são as funções de conexão com o SQL
from conexao import *

janela = Tk()

#configura as abas
notebook = ttk.Notebook(janela)
estilo = ttk.Style()
estilo.configure('TNotebook.Tab', font=('Arial',10,'bold'))

#Variáveis globais

#Onde os clientes sao armazenados
lista_clientes = []
lista_vendas = []

#São as abas
abas = []
qntAbas=0

produto = []
quantidade_produtos=0
qntVendas=0
vendas=0

consideracao = None

ja_tem_consideracao = 0 

def IniciarValores():

    load_dotenv()

    try:

        connection = mysql.connector.connect(
            host = os.getenv("HOST"),
            database = os.getenv("DATABASE"),
            user = os.getenv("USER"),
            password = os.getenv("PASSWORD")
        )

        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM cliente")
            if cursor.with_rows: 
                # lendo dados
                result = cursor.fetchall()

                for dado in result:
                    nome, telefone, cpf, endereco, qntPedidos, valor, cep, aniversario = dado

                    if qntPedidos == None:
                        qntPedidos = 0.0

                    if valor == None:
                        valor = 0.0
 
                    lista_clientes.append(Clientes(nome, telefone, cpf, endereco, valor, qntPedidos, cep, aniversario))

            cursor.execute("SELECT * FROM vendas")
            if cursor.with_rows: 
                # lendo dados
                result = cursor.fetchall()

                for dado in result:
                    cliente, produto, qnt, consideracoes, datapedido, dataEntrega, valor, frete = dado

                    if qnt == None:
                        qnt = 0

                    if valor == None:
                        valor = 0.0

                    if frete == None:
                        frete = 0.0

                    produto = produto.split('/')

                    lista_vendas.append(Venda(produto,qnt,consideracoes,datapedido,dataEntrega,cliente,valor, frete))

    except:
        pass
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def FecharAba(frames):

    global notebook

    # Obtém o índice da aba atual
    current_tab = notebook.select()
    current_index = notebook.index(current_tab)
    
    # Remove a aba do Notebook
    notebook.forget(current_index)
    
    # Remove o frame da lista
    try:
        del frames[current_index]
    except:
        pass

#Função para cadastrar o cliente
def CadastrarCliente(aba):

    def submit():

        aniversario = ''

        texto_ja_tem = Label(aba,text='',font=('Arial',15))
        texto_ja_tem.place(x=200,y=50)

        ja_tem=0

        nome = entrada_nome.get().lower()
        if '\n' in nome:
            nome = nome.replace('\n','')
        telefone = entrada_numero.get()
        if '\n' in telefone:
            telefone = telefone.replace('\n','')
        cpf = entrada_cpf.get()
        if '\n' in cpf:
            cpf = cpf.replace('\n','')
        endereco = entrada_endereco.get().lower()
        if '\n' in endereco:
            endereco = endereco.replace('\n',' / ')
        cep = entrada_cep.get()
        if '\n' in cep:
            cep = cep.replace('\n','')
        data_aniversario = entrada_aniversario.get_date()

        data_aniversario = data_aniversario.split('/')

        aniversario = f'{data_aniversario[0]}/{data_aniversario[1]}'

        for i in lista_clientes:
            if i.nome == nome:
                ja_tem=1
                texto_ja_tem.config(text='Já tem um cliente com esse nome')
                
        if ja_tem!=1:
            mensagem_cadastrado = Label(aba,text=f'Cliente "{nome}" cadastrado',font=('Arial',15))
            mensagem_cadastrado.pack(anchor=W)

            lista_clientes.append(Clientes(nome=nome,telefone=telefone,cpf=cpf,endereco=endereco,cep=cep,aniversario=aniversario))
            texto_ja_tem.config(text='                                                                                  ')

            result = AdicionarCliente(nome,telefone,cpf,endereco,cep,aniversario)
            texto_erro =  Label(aba,text=result,font=('Arial',15))
            texto_erro.place(x=700,y=400)

        entrada_nome.delete(0,END)
        entrada_numero.delete(0,END)
        entrada_cpf.delete(0,END)
        entrada_endereco.delete(0,END)
        entrada_cep.delete(0,END)

    insira_o_nome = Label(aba,text='Informe o nome:',padx=10,pady=10,font=('Arial',15))
    entrada_nome = Entry(aba,font=('Arial',15),width=75)

    insira_o_numero= Label(aba,text='Informe o telefone:',padx=10,pady=10,font=('Arial',15))
    entrada_numero = Entry(aba,font=('Arial',15),width=75)

    insira_o_cpf= Label(aba,text='Informe o cpf:',padx=10,pady=10,font=('Arial',15))
    entrada_cpf = Entry(aba,font=('Arial',15),width=75)

    insira_o_endereco= Label(aba,text='Informe o endereco:',padx=10,pady=10,font=('Arial',15))
    entrada_endereco = Entry(aba,font=('Arial',15),width=75)

    insira_o_cep= Label(aba,text='Informe o CEP:',padx=10,pady=10,font=('Arial',15))
    entrada_cep = Entry(aba,font=('Arial',15),width=75)

    insira_o_aniversario= Label(aba,text='Informe a data de aniversário:',padx=10,pady=10,font=('Arial',15))
    entrada_aniversario = Calendar(aba, locale='pt_BR', date_pattern='dd/mm/yyyy')
            
    insira_o_nome.pack(anchor=W)
    entrada_nome.pack(anchor=W)
    insira_o_numero.pack(anchor=W)
    entrada_numero.pack(anchor=W)
    insira_o_cpf.pack(anchor=W)
    entrada_cpf.pack(anchor=W)
    insira_o_endereco.pack(anchor=W)
    entrada_endereco.pack(anchor=W)
    insira_o_cep.pack(anchor=W)
    entrada_cep.pack(anchor=W)
    insira_o_aniversario.pack(anchor=W)
    entrada_aniversario.pack(anchor=W)

    botao_cadastrar = Button(abas[qntAbas],text='Cadastrar',command= submit,font=('Arial',15))
    botao_cadastrar.pack(anchor=W,side=BOTTOM)

#Fução para remover o cadastro
def RemoverCadastro(aba,nome_cliente):
    
    confirmacao = Label(aba,font=('Arial',15))

    def remover(encontrado):

        posicao_cliente=0
        posicao_venda=0

        nome_pesquisa = entrada_nome.get().lower()
        if '\n' in nome_pesquisa:
            nome_pesquisa = nome_pesquisa.replace('\n','')

        for i in lista_clientes:
            if i.nome == nome_pesquisa:

                lista_clientes.pop(posicao_cliente)

                nome = i.nome
                entrada_nome.delete(0,END)
                
                erro = RemoverCLiente(nome)
                texto_erro = Label(aba,text=erro,font=('Arial',15))
                texto_erro.pack(side=BOTTOM,anchor=N)

                encontrado=1

                for j in lista_vendas:
                    if j.cliente == nome_pesquisa:

                        lista_vendas.pop(posicao_venda)

                    posicao_venda+=1

            else:
                encontrado=0
            
            posicao_cliente+=1
                
        if encontrado==1:
            confirmacao.config(text='Cliente removido')
        else:
            confirmacao.config(text='Cliente não encontrado')
                
        confirmacao.pack()

    encontrado=0

    if len(lista_clientes)!=0:

        texto_nome = Label(aba,text='Informe o nome do cliente que será removido o cadastro:',font=('Arial',15))
        entrada_nome = Entry(aba,width=75,font=('Arial',15))
        if nome_cliente !=None:
            entrada_nome.insert(0,nome_cliente)
        botao = Button(aba,text='Remover cadastro',command= lambda: remover(encontrado),font=('Arial',15))
        texto_nome.pack(anchor=W)
        entrada_nome.pack(anchor=W)
        botao.pack(anchor=W)
    
    else:
        sem_cliente = Label(aba,text='Nenhum cliente cdastrado até o momento',font=('Arial',15))
        sem_cliente.pack()

#Função para cadastra a venda
def CadastrarVenda(aba,cliente_ja_colocado):
    
    global vendas,quantidade_produtos

    vendas=0

    agora = datetime.now()

    dataPedido = agora.strftime("%d/%m/%Y")

    def cadastrar():

        global produto, quantidade_produtos,vendas,consideracao

        cliente_encontrado=0

        texto_cliente_nao_encontrado = Label(aba,text='',font=('Arial',15))
        texto_cliente_nao_encontrado .place(x=200,y=40)

        dataEntrega = calendario.get_date()
        frete = entrada_frete.get()
        nome = entrada_do_cliente.get().lower()
        if '\n' in nome:
            nome = nome.replace('\n','')
        valor = entrada_valor.get()

        if '\n' in valor:
            valor = valor.replace('\n','')

        if '\n' in frete:
            frete = frete.replace('\n','')

        if ' ' in frete:
            frete = frete.replace(' ','')

        if ' ' in valor:
            valor = valor.replace(' ','')

        if 'R$' in valor:
            valor = valor.replace('R$','')

        if ',' in valor:
            valor = valor.replace(',','.')

        if 'R$' in frete:
            frete = frete.replace('R$','')

        if ',' in frete:
            frete = frete.replace(',','.')

        try:
            frete = float(frete)
        except:
            pass

        try:
            valor = float(valor)
        except:
            pass

        for n in lista_clientes:
            if n.nome == nome:
                cliente_encontrado=1

                texto_cliente_nao_encontrado.config(text='                                                                                  ')

                vendas+=1

                if consideracao != None:
                    c = consideracao.get()
                    if '\n' in c:
                        c = c.replace('\n','')

                else:
                    c = ''

                texto_venda_realizada.config(text=f'Venda realizada X{vendas}')

                lista_vendas.append(Venda(produto, quantidade_produtos, c, dataPedido, dataEntrega, nome, valor,frete))
            
                for i in lista_clientes:
                    if i.nome == nome:
                        i.valor+=valor
                        i.qntPedidos+=1

                        AtualizarQntPedidos(i.valor,i.qntPedidos,i.nome)

                result = AdicionarVenda(nome,produto,quantidade_produtos,c,dataPedido,dataEntrega,valor)
                texto_erro = Label(aba,text=result,font=('Arial',15)        )

                #deletando os itens para adicionar mais
                entrada_de_produtos.delete(0,END)
                entrada_do_cliente.delete(0,END)
                entrada_quantidade_de_produtos.delete(0,END)
                entrada_quantidade_de_produtos.insert(0,0)
                entrada_valor.delete(0,END)
                entrada_valor.insert(0,0)
                entrada_frete.delete(0,END)
                entrada_frete.insert(0,0)
                texto_produtos_adicionados.config(text='')
                produto = []

        if cliente_encontrado==0:
            texto_cliente_nao_encontrado.config(text='Cliente não encontrado')          

        quantidade_produtos=0
                
    def adicionarproduto():

        global quantidade_produtos
        global produto

        nome = entrada_de_produtos.get()
        if '\n' in nome:
            nome = nome.replace('\n','')
        qnt = int(entrada_quantidade_de_produtos.get())
    
        produto.append(f'Produto: {nome}, Quantidade: {qnt}')

        conteudo = '\n'.join(produto)
        texto_produtos_adicionados.config(text=conteudo)
        entrada_de_produtos.delete(0,END)
        entrada_quantidade_de_produtos.delete(0,END)
        
        try:
            quantidade_produtos+=qnt
        except:
            pass

    def consideracoes():

        global consideracao, ja_tem_consideracao

        if ja_tem_consideracao==0:

            texto_consideracoes = Label(aba,text='Informe a consideração: ',font=('Arial',15))
            consideracao = Entry(aba,font=('Arial',15),width=75)

            texto_consideracoes.pack(anchor=W)
            consideracao.pack(anchor=W)

            ja_tem_consideracao=1

    texto_entrada_do_cliente = Label(aba,text='Informe o cliente:',font=('Arial',15))
    entrada_do_cliente = Entry(aba,font=('Arial',15),width=75)

    if cliente_ja_colocado != None:
        entrada_do_cliente.insert(0,cliente_ja_colocado)

    texto_entrada_de_produtos = Label(aba,text='Inforne os produtos:',font=('Arial',15))
    entrada_de_produtos = Entry(aba,font=('Arial',15),width=75)

    texto_produtos_adicionados = Label(aba,text='',font=('Arial',15))
    texto_produtos_adicionados.pack(side=RIGHT,anchor=N)

    texto_entrada_quantidade_de_produtos = Label(aba,text='Informe a quantidade desse produto:',font=('Arial',15))
    entrada_quantidade_de_produtos = Entry(aba,font=('Arial',15),width=75)
    entrada_quantidade_de_produtos.insert(0,0)

    botao_adicionar_produto = Button(aba,text='Adiconar Produto',command= adicionarproduto,font=('Arial',15))

    texto_valor = Label(aba,text='Informe o valor total da venda:',font=('Arial',15))
    entrada_valor = Entry(aba,font=('Arial',15),width=75)
    entrada_valor.insert(0,0)

    texto_frete = Label(aba,text='Informe o valor total do frete:',font=('Arial',15))
    entrada_frete = Entry(aba,font=('Arial',15),width=75)
    entrada_frete.insert(0,0)

    texto_pedir_data = Label(aba,text='Informe a data de entrega do pedido',font=('Arial',15))
    calendario = Calendar(aba, locale='pt_BR', date_pattern='dd/mm/yyyy')

    botao_consideracoes = Button(aba,text='Clique aqui caso o pedido tenha considerações a fazer',command=consideracoes,font=('Arial',15))

    botao_adicionar_venda = Button(aba,text='Adicionar venda',command= cadastrar,font=('Arial',15))

    #Adicionar na tela
    texto_entrada_do_cliente.pack(anchor=W)
    entrada_do_cliente.pack(anchor=W)

    texto_entrada_de_produtos.pack(anchor=W)
    entrada_de_produtos.pack(anchor=W)

    texto_entrada_quantidade_de_produtos.pack(anchor=W)
    entrada_quantidade_de_produtos.pack(anchor=W)

    botao_adicionar_produto.pack(anchor=W)

    texto_valor.pack(anchor=W)
    entrada_valor.pack(anchor=W)

    texto_frete.pack(anchor=W)
    entrada_frete.pack(anchor=W)

    texto_pedir_data.pack(anchor=W)
    calendario.pack(anchor=W)

    botao_consideracoes.pack(anchor=W)

    texto_venda_realizada = Label(aba,text=f'Venda realizada X{vendas}',font=('Arial',15))
    texto_venda_realizada.pack(anchor=W,side=BOTTOM)

    botao_adicionar_venda.pack(anchor=W,side=BOTTOM)


lista_nome_clientes = []
lista_de_botoes = []

# Função para mostrar cliente
def MostrarCliente(aba, nome):

    barra_de_pesquisa.insert(0,'Informe o nome do cliente')

    nome = nome.lower()

    global lista_nome_clientes,lista_de_botoes

    lista_nome_clientes.clear()
    lista_de_botoes.clear()

    def PedidoEntregue(posicao):
        pass
        
    def exibir(nome_cliente):

        global lista_nome_clientes,lista_de_botoes

        for j in lista_de_botoes:
            j.destroy()

        compras_do_cliente = []
        lista_botoes_pedidos_entregues = []

        compra1 = StringVar()
        compra2 = StringVar()

        for i in lista_vendas:
            if i.cliente == nome_cliente:
                compras_do_cliente.append(i)
                if i.entregue == False or i.entregue == None:
                    botao_entregue = Button(aba,text='Pedido entregue',command=PedidoEntregue)
                    lista_botoes_pedidos_entregues.append(botao_entregue)
                else:
                    lista_botoes_pedidos_entregues.append('')


        compras_do_cliente = sorted(compras_do_cliente, key=lambda data: data.dataPedido)

        compras_do_cliente = compras_do_cliente[::-1]

        def atualizarVlores(val):
            index = int(val)
            
            try:
                
                compra1.set(compras_do_cliente[index])

            except:

                compra1.set('')

            try:
                
                compra2.set(compras_do_cliente[index+1])

            except:

                compra2.set('')

        # Mostra os dados pessoais

        for j in lista_clientes:
            if j.nome == nome_cliente:

                botao_fazer_venda = Button(aba, text='Clique aqui para \nrealizar uma venda', font=('Arial', 15), command=lambda: nova_Aba(tipo='CadastrarVenda', cliente=nome_cliente))
                botao_fazer_venda.pack(anchor=W)
                botao_excluir_conta = Button(aba, text='Clique aqui para \nExcluir o cliente', font=('Arial', 15), command=lambda: nova_Aba(tipo='RemoverCadastro', cliente=nome_cliente))
                botao_excluir_conta.place(x=200,y=43)
                botao_excluir_conta = Button(aba, text='Clique aqui para \nAlterar o cadastro', font=('Arial', 15), command=lambda: nova_Aba(tipo='AlterarCadastro', cliente=nome_cliente))
                botao_excluir_conta.place(x=385,y=42)

                texto_informacoes_pessoais = Label(aba, text='Informações pessoais:', font=('Arial', 15, 'bold'))
                texto_informacoes_pessoais.pack(anchor=W)

                texto_dados_pessoais = Label(aba, text=j, font=('Arial', 15))
                texto_dados_pessoais.pack(anchor=W)

        texto_informacoes_de_compras = Label(aba, text='Compras realizadas:', font=('Arial', 15, 'bold'))
        texto_informacoes_de_compras.pack(anchor=W)

        try:       
            compra1.set(compras_do_cliente[0])

        except:

            compra1.set('')

        try:

            compra2.set(compras_do_cliente[1])

        except:

            compra2.set('')

        texto_compra1 = Label(aba,textvariable=compra1,font=('Arial',15))
        texto_compra1.pack(side=LEFT,anchor=N,padx=50,pady=20)

        texto_compra2 = Label(aba,textvariable=compra2,font=('Arial',15))
        texto_compra2.pack(side=LEFT,anchor=N,padx=50,pady=20)

        scale = Scale(aba, from_=0, to=len(compras_do_cliente)-1, orient=HORIZONTAL, command=atualizarVlores,length=600)
        scale.place(x=500,y=700)

        if len(compras_do_cliente)==0:
            scale.destroy()
            sem_compras = Label(aba,text='Cliente não fez compras',font=('Arial',15))
            sem_compras.pack(anchor=W)


    for i in lista_clientes:
        if nome in i.nome:
            lista_nome_clientes.append(i)


    if len(lista_nome_clientes) ==0:
        texto_sem_cliente = Label(aba,text='Nenhum cliente com esse nome!',font=('Arial',15))
        texto_sem_cliente.pack()

    for i in lista_nome_clientes:

        botao = Button(aba, text=f'Nome: {i.nome} / CPF: {i.cpf} / Telefone: {i.telefone} / CEP: {i.cep}', command=lambda nome=i.nome: exibir(nome),font=('Arial',15))
        botao.pack(pady=5)
        lista_de_botoes.append(botao)

    if len(lista_nome_clientes)==1:
        exibir(lista_nome_clientes[0].nome)


def VerClientes(aba):

    mostrar_ordenado =Label(aba,text=f'',font=('Arial',15))
    texto_titulo_mostrar = Label(aba,text='Os 10 melhores clientes são: \n',font=('Arial',15,'bold'))

    def selecionar():

        clientes = []

        conteudo = ''

        qnt = 0

        opcao = entrada_selecao.get()

        if opcao == 'Quantidade de compras':

            ordenados = sorted(lista_clientes, key=lambda clientes: clientes.qntPedidos)
            ordenados.reverse()

            for i in ordenados:
                clientes.append(f'{qnt+1}- Cliente: {i.nome}. Quantidade pedido: {i.qntPedidos}')
                conteudo = '\n'.join(clientes)
                if qnt==10:
                    break
                qnt+=1

            mostrar_ordenado.config(text=conteudo)

        elif opcao == 'Valor':

            ordenados = sorted(lista_clientes, key=lambda clientes: clientes.valor)
            ordenados.reverse()

            for i in ordenados:
                clientes.append(f'{qnt+1}- Cliente: {i.nome}. Valor total: {i.valor}')
                conteudo = '\n'.join(clientes)
                if qnt==10:
                    break
                qnt+=1

            mostrar_ordenado.config(text=conteudo)

    if len(lista_clientes)!=0:

        opcoes = ['Quantidade de compras','Valor']

        texto_selecionar = Label(aba,text='Informe o tipo de ordenação',font=('Arial',15))
        texto_selecionar.pack()

        entrada_selecao = ttk.Combobox(aba,values=opcoes,font=('Arial',15))
        entrada_selecao.pack()

        botao_selecao = Button(aba,text='Selecionar',font=('Arial',15),command= selecionar)
        botao_selecao.pack()

        texto_titulo_mostrar = Label(aba,text='Os 10 melhores clientes são: \n',font=('Arial',15,'bold'))
        texto_titulo_mostrar.pack(anchor=W)

        mostrar_ordenado.pack(anchor=W)
    
    else:
        texto_sem_venda = Label(aba,text='Nenhuma venda cadastrada até o momento!',font=('Arial',15))
        texto_sem_venda.pack(anchor=CENTER)

def VerReceita(aba):
    
    valor_total = 0

    for i in lista_vendas:
        valor_total +=i.valor

    texto_valor_total = Label(aba,text=f'O valor total vendido é: R${valor_total} com {len(lista_vendas)} vendas',font=('Arial',15))
    texto_valor_total.pack(anchor=W)

def AlterarCadastro(aba,cliente=None):

    def selecionar():

        def mudar():

            nome = entrada_alterar.get().lower()
            if '\n' in nome:
                nome = nome.replace('\n','')
            novo_valor = entrada_novo_valor.get()
            if '\n' in novo_valor:
                novo_valor = novo_valor.replace('\n','')

            for posicao in lista_clientes:
                if posicao.nome == nome:

                    nome = posicao.nome

                    if tipo == 'Nome':
                        novo_valor =novo_valor.lower()
                        posicao.nome = novo_valor
                    elif tipo == 'CPF':
                        posicao.cpf = novo_valor
                    elif tipo == 'Telefone':
                        posicao.telefone = novo_valor
                    elif tipo == 'Endereço':
                        novo_valor =novo_valor.lower()
                        posicao.endereco = novo_valor


                    confirmacao = Label(aba,text=f'O {tipo} do cliente {nome} foi alterado',font=('Arial',15))
                    confirmacao.pack(anchor=W)
                
                    result = AlterarCliente(tipo,novo_valor, nome)
                    texto_result = Label(aba,text=result,font=('Arial',15))
                    texto_result.pack(anchor=W)
                    

        tipo = selecionar_opcoes.get()

        if tipo == 'Nome':
            texto_informe = Label(aba,text='Informe o novo nome: ',font=('Arial',15))
            texto_informe.pack(anchor=W)
            entrada_novo_valor = Entry(aba,font=('Arial',15))
            entrada_novo_valor.pack(anchor=W)
            botao_alterar = Button(aba,text='Alterar',font=('Arial',15),command= mudar)
            botao_alterar.pack(anchor=W)
                
        elif tipo == 'CPF':
            texto_informe = Label(aba,text='Informe o novo CPF: ',font=('Arial',15))
            texto_informe.pack(anchor=W)
            entrada_novo_valor = Entry(aba,font=('Arial',15))
            entrada_novo_valor.pack(anchor=W)
            botao_alterar = Button(aba,text='Alterar',font=('Arial',15),command= mudar)
            botao_alterar.pack(anchor=W)

        elif tipo == 'Telefone':
            texto_informe = Label(aba,text='Informe o novo Telefone: ',font=('Arial',15))
            texto_informe.pack(anchor=W)
            entrada_novo_valor = Entry(aba,font=('Arial',15))
            entrada_novo_valor.pack(anchor=W)
            botao_alterar = Button(aba,text='Alterar',font=('Arial',15),command= mudar)
            botao_alterar.pack(anchor=W)

        elif tipo == 'Endereço':
            texto_informe = Label(aba,text='Informe o novo Telefone: ',font=('Arial',15))
            texto_informe.pack(anchor=W)
            entrada_novo_valor = Entry(aba,font=('Arial',15))
            entrada_novo_valor.pack(anchor=W)
            botao_alterar = Button(aba,text='Alterar',font=('Arial',15),command= mudar)
            botao_alterar.pack(anchor=W)
                
    if len(lista_clientes)!=0:

        titulo_alterar = Label(aba,text='Informe o nome do cliente que será alterado o cadastro: ',font=('Arial',15))
        titulo_alterar.pack(anchor=W)

        entrada_alterar = Entry(aba,font=('Arial',15))
        entrada_alterar.pack(anchor=W)

        if cliente!=None:
            entrada_alterar.insert(0,cliente)

        opcoes = ['Nome','CPF','Telefone','Endereço']

        selecionar_opcoes = ttk.Combobox(aba,values=opcoes,font=('Arial',15))
        selecionar_opcoes.pack(anchor=W)

        botao_selecionar_opcoes = Button(aba,text='Selecionar',font=('Arial',15),command=selecionar)
        botao_selecionar_opcoes.pack(anchor=W)

    else:
        sem_cliente = Label(aba,text='Nenhum cliente cadastrado até o momento',font=('Arial',15))
        sem_cliente.pack()

mes = ''

def VendasNoMes(aba):

    global mes

    compra1 = StringVar()
    compra2 = StringVar()
    vendas_nesse_mes = []

    def mostrar():

        compra1.set('')
        compra2.set('')

        vendas_nesse_mes.clear()

        def atualizarValores(val):
            index = int(val)
            
            try:

                conteudo = '\n'.join(vendas_nesse_mes[index].produto)

                texto_cliente = f'Cliente: {vendas_nesse_mes[index].cliente}\n' +\
                                f'Valor total do pedido: {vendas_nesse_mes[index].valor}\n' +\
                                f'Quantidade total pedido: {vendas_nesse_mes[index].qnt}\n'+\
                                f'Data do pedido: {vendas_nesse_mes[index].dataPedido}\n'+\
                                f'Data de entrega do pedido: {vendas_nesse_mes[index].dataEntrega}\n'+\
                                f'Considerações: {vendas_nesse_mes[index].consideracoes}\n'+\
                                f'Produtos comprados: \n{conteudo}'
                
                compra1.set(texto_cliente)

            except:

                compra1.set('')

            try:

                conteudo = '\n'.join(vendas_nesse_mes[index+1].produto)

                texto_cliente = f'Cliente: {vendas_nesse_mes[index+1].cliente}\n' +\
                                f'Valor total do pedido: {vendas_nesse_mes[index+1].valor}\n' +\
                                f'Quantidade total pedido: {vendas_nesse_mes[index+1].qnt}\n'+\
                                f'Data do pedido: {vendas_nesse_mes[index+1].dataPedido}\n'+\
                                f'Data de entrega do pedido: {vendas_nesse_mes[index+1].dataEntrega}\n'+\
                                f'Considerações: {vendas_nesse_mes[index+1].consideracoes}\n'+\
                                f'Produtos comprados: \n{conteudo}'
                
                compra2.set(texto_cliente)

            except:

                compra2.set('')


        match entrada_mes.get():

            case 'Janeiro':
                mes = '1'

            case 'Fevereiro':
                mes = '2'

            case 'Março':
                mes = '3'

            case 'Abril':
                mes = '4'

            case 'Maio':
                mes = '5'

            case 'Junho':
                mes = '6'

            case 'Julho':
                mes = '7'

            case 'Agosto':
                mes = '8'

            case 'Setembro':
                mes = '9'

            case 'Outubro':
                mes = '10'

            case 'Novembro':
                mes = '11'

            case 'Dezembro':
                mes = '12'

        for i in lista_vendas:

            pedido = i.dataPedido.split('/')

            if mes in pedido[1]:
                vendas_nesse_mes.append(i)

        if len(vendas_nesse_mes) !=0:

            texto_sem_cliente.config(text='')

            try:

                conteudo = '\n'.join(vendas_nesse_mes[0].produto)

                texto_cliente = f'Cliente: {vendas_nesse_mes[0].cliente}\n' +\
                                f'Valor total do pedido: {vendas_nesse_mes[0].valor}\n' +\
                                f'Quantidade total pedido: {vendas_nesse_mes[0].qnt}\n'+\
                                f'Data do pedido: {vendas_nesse_mes[0].dataPedido}\n'+\
                                f'Data de entrega do pedido: {vendas_nesse_mes[0].dataEntrega}\n'+\
                                f'Considerações: {vendas_nesse_mes[0].consideracoes}\n'+\
                                f'Produtos comprados: \n{conteudo}'
                    
                compra1.set(texto_cliente)

            except:

                compra1.set('')

            try:

                conteudo = '\n'.join(vendas_nesse_mes[1].produto)

                texto_cliente = f'Cliente: {vendas_nesse_mes[1].cliente}\n' +\
                                f'Valor total do pedido: {vendas_nesse_mes[1].valor}\n' +\
                                f'Quantidade total pedido: {vendas_nesse_mes[1].qnt}\n'+\
                                f'Data do pedido: {vendas_nesse_mes[+1].dataPedido}\n'+\
                                f'Data de entrega do pedido: {vendas_nesse_mes[1].dataEntrega}\n'+\
                                f'Considerações: {vendas_nesse_mes[1].consideracoes}\n'+\
                                f'Produtos comprados: \n{conteudo}'
                    
                compra2.set(texto_cliente)

            except:

                compra2.set('')

            scale = Scale(aba, from_=0, to=len(vendas_nesse_mes)-1, orient=HORIZONTAL, command=atualizarValores,length=600)
            scale.place(x=500,y=700)

        else:
            texto_sem_cliente.config(text='Nenhuma venda realizada nesse mês!')

    opcoes = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    
    texto_selecionar_mes = Label(aba,text='Informe o mês:',font=('Arial',15))
    texto_selecionar_mes.pack(anchor=W,padx=10,pady=10)

    entrada_mes = ttk.Combobox(aba,values=opcoes,font=('Arial',15))
    entrada_mes.pack(anchor=W,padx=10,pady=10)

    botao_escolher = Button(aba,text='Selecionar',font=('Arial',15),command=mostrar)
    botao_escolher.pack(anchor=W,padx=10,pady=10)

    texto_informacoes_de_compras = Label(aba, text='Compras realizadas:',font=('Arial',15))
    texto_informacoes_de_compras.pack(anchor=W)

    texto_sem_cliente = Label(aba,text='',font=('Arial',15))
    texto_sem_cliente.pack(anchor=W)

    texto_compra1 = Label(aba,textvariable=compra1,font=('Arial',15))
    texto_compra1.pack(side=LEFT,anchor=N,padx=80,pady=20)

    texto_compra2 = Label(aba,textvariable=compra2,font=('Arial',15))
    texto_compra2.pack(side=LEFT,anchor=N,padx=80,pady=20)


def MostrarTodosClientes(aba):

    def mudar(val):

        index = int(val)

        for i in range(len(lista[index-1])):
            lista[index-1][i].pack_forget()

        for i in lista[index]:
            i.pack(pady=5)

    botoes = []

    lista_ordenada = sorted(lista_clientes,key=lambda clientes: clientes.nome)

    for i in lista_ordenada:

        botao = Button(aba, text=f'Nome: {i.nome} / CPF: {i.cpf} / Telefone: {i.telefone} / CEP: {i.cep}', command=lambda nome=i.nome: nova_Aba(tipo='Pesquisar',cliente=nome),font=('Arial',15))
        botoes.append(botao)

    lista = [botoes[i:i + 12] for i in range(0,len(botoes),12)]

    for i in lista[0]:
        i.pack(pady=5)

    scale = Scale(aba,from_=0,to=len(lista)-1,orient=HORIZONTAL,command=mudar,length=600)
    scale.place(x=500,y=700)
    

#Função para chamar as respectivas funções
def nova_Aba(tipo,cliente=None):

    global qntAbas

    frame = ttk.Frame(notebook, width=400, height=280)

    abas.append(frame)

    close_button = ttk.Button(abas[qntAbas], text='Fechar Aba Atual', command=lambda: FecharAba(frame))
    close_button.pack(pady=10)

    if tipo == 'CadastrarCliente':
        notebook.add(abas[qntAbas],text=f'Cadastrar cliente')
        CadastrarCliente(abas[qntAbas])
    
    elif tipo == 'RemoverCadastro':
        notebook.add(abas[qntAbas],text=f'Remover cliente')
        RemoverCadastro(abas[qntAbas],cliente)
    
    elif tipo == 'CadastrarVenda':
        notebook.add(abas[qntAbas],text=f'Cadastrar Venda')
        CadastrarVenda(abas[qntAbas],cliente)

    elif tipo == 'AlterarCadastro':
        notebook.add(abas[qntAbas],text=f'Alterar Cadastro')
        AlterarCadastro(abas[qntAbas],cliente)

    elif tipo == 'Pesquisar':

        if cliente == None:
            nome_cliente = barra_de_pesquisa.get()
        else:
            nome_cliente = cliente
        barra_de_pesquisa.delete(0,END)
        notebook.add(abas[qntAbas],text=f'{nome_cliente}')
        MostrarCliente(abas[qntAbas],nome_cliente)
        
    elif tipo == 'VerClientes':
        notebook.add(abas[qntAbas],text=f'Ver principais clientes')
        VerClientes(abas[qntAbas])

    elif tipo =='VerReceita':
        notebook.add(abas[qntAbas],text=f'Ver receita')
        VerReceita(abas[qntAbas])

    elif tipo == 'VendasMes':
        notebook.add(abas[qntAbas],text=f'Vendas no mês')
        VendasNoMes(abas[qntAbas])

    elif tipo == 'Aniversario':
        notebook.add(abas[qntAbas],text=f'Aniversário')
        texto_aniversario = Label(abas[qntAbas],text=f'Hoje é aniversário de: \n{cliente}',font=('Arial',15))
        texto_aniversario.pack()

    elif tipo == 'VerTodosClientes':
        notebook.add(abas[qntAbas],text='Clientes Cadastrados')
        MostrarTodosClientes(abas[qntAbas])

    notebook.place(x=350,y=100,width=1557,height=900)
    qntAbas+=1

def Aniversario():

    clientes = []

    agora = datetime.now()

    data_aniversario = agora.strftime("%d/%m")
    
    for i in lista_clientes:
        if i.aniversario == data_aniversario:
            clientes.append(f'{i.nome} com o telefone {i.telefone}')

    retornar = '\n'.join(clientes)

    return retornar

#Main
IniciarValores()

cliente = Aniversario()

janela.geometry('1920x1080')
janela.config(bg='gray')
janela.title('projeto')

abainicial = ttk.Frame(notebook, width=400, height=280)
notebook.place(x=350,y=100,width=1557,height=900)
notebook.add(abainicial)

barra_de_pesquisa = Entry(janela,width=50,font=('Arial',15))
barra_de_pesquisa.insert(0,'Informe o nome do cliente')
barra_de_pesquisa.place(x=500,y=5)

botao_barra_de_pesquisa = Button(janela,text='Pesquisar',command= lambda: nova_Aba('Pesquisar'))
botao_barra_de_pesquisa.place(x=1070,y=6)

botao_cadasrar_Ciente = Button(janela,text='Cadastrar cliente',font=('Arial',15),command= lambda: nova_Aba('CadastrarCliente'))
botao_cadasrar_Ciente.place(x=10,y=150)

botao_ver_clientes_que_mais_compraram = Button(janela,text='Ver clientes que mais compraram',font=('Arial',15),command= lambda: nova_Aba('VerClientes'))
botao_ver_clientes_que_mais_compraram.place(x=10,y=200)

botao_alterar_cadastro_de_cliente = Button(janela,text='Alterar cadastro',font=('Arial',15),command= lambda: nova_Aba('AlterarCadastro'))
botao_alterar_cadastro_de_cliente.place(x=10,y=250)

botao_ver_receita = Button(janela,text='Ver receita',font=('Arial',15),command= lambda: nova_Aba('VerReceita'))
botao_ver_receita.place(x=10,y=300)

botao_remover_cadastro_de_cliente = Button(janela,text='Remover cadastro',font=('Arial',15),command= lambda: nova_Aba('RemoverCadastro'))
botao_remover_cadastro_de_cliente.place(x=10,y=350)

botao_cadastro_de_vendas = Button(janela,text='Cadastrar venda',font=('Arial',15),command= lambda: nova_Aba('CadastrarVenda'))
botao_cadastro_de_vendas.place(x=10,y=400)

botao_cadastro_de_vendas = Button(janela,text='Ver vendas feitas no mês',font=('Arial',15),command= lambda: nova_Aba('VendasMes'))
botao_cadastro_de_vendas.place(x=10,y=450)

botao_ver_todos_clientes = Button(janela,text='Ver todos os clientes',font=('Arial',15),command= lambda: nova_Aba('VerTodosClientes'))
botao_ver_todos_clientes.place(x=10,y=500)

if cliente != '':
    nova_Aba('Aniversario',cliente)

janela.mainloop()
