import textwrap

def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [7]\tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += (f"Deposito de R$ {valor: .2f}\n")
    else:
        print("Operacao falhou! Valor invalido de deposito.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saque = numero_saques >= limite_saques

    if not excedeu_saque:
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        if not excedeu_saldo and not excedeu_limite:
            saldo -= valor
            extrato += (f"Saque de R$: {valor: .2f}\n")
            numero_saques += 1
        else:
            if excedeu_saldo:
                print("Nao foi possivel efetuar a operacao! Valor informado maior que saldo atual.")
            else:
                print("Nao foi possivel efetuar a operacao! Valor informado excedeu o limite máximo de saque.")

    else:
        print("Limite de saques diarios esgotados! Volte amanha.")
    return saldo, extrato, numero_saques

def mostrar_extrato(saldo,/,*,extrato):
    print(f"{'EXTRATO'.center(30, "=")}\n")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"O saldo atual é: R$ {saldo: .2f}\n")
    print(f"{''.center(30, "=")}")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF do usuário. (somente números) \n")
    usuario = procurar_usuario(usuarios, cpf)

    if usuario:
        print("CPF informado já cadastrado no banco de dados. ")
        return
    
    nome = input("Informe o nome completo. \n")
    data_nascimento = input("Informe a data de nascimento. (dd-mm-aaaa)\n")   
    endereco = input("Informe o endereço. (logradouro, nro - bairro - cidade/sigla estado) \n")     
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Usuario cadstrado com sucesso !! ")

def procurar_usuario (usuarios, cpf):
    usuario = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuario[0] if usuario else False

""" def mostrar_usuarios_cadastrados(usuarios):
    [print(usuario) for usuario in usuarios] """

def criar_conta(contas, usuarios, agencia):
    cpf = input("Informe o CPF do cliente. \n")
    usuario = procurar_usuario(usuarios, cpf)
    if usuario:
        numero_conta = len(contas) + 1
        contas.append({"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario})
        print("Conta criada com sucesso!! ")
        return
    print("Usuário não existe. Processo de criação de conta encerrado !!")
    
def listar_contas(contas):
    for conta in contas:
        print(f"""
        Agência: {conta["agencia"]}
        Numero da conta: {conta["numero_conta"]}
        Titular: {conta["usuario"]["nome"]}
        {"".center(30, "=")}
        """)

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0

    usuarios = []
    contas = []

    while True:

        opcao = menu()

        if opcao == "1":
            valor = float(input("Qual valor será depositado? \n"))
            saldo, extrato = depositar(saldo, valor, extrato)
        elif opcao == "2":
            valor = float(input("Digite o quanto voce quer sacar.\n"))
            saldo, extrato, numero_saques = sacar(
                saldo = saldo, 
                valor = valor, 
                extrato = extrato, 
                limite = limite,
                numero_saques = numero_saques, 
                limite_saques = LIMITE_SAQUES)
        elif opcao == "3":
            mostrar_extrato(saldo, extrato = extrato)
        elif opcao == "4":
            criar_conta(contas, usuarios, AGENCIA)
        elif opcao == "5":
            listar_contas(contas)
        elif opcao == "6":
            criar_usuario(usuarios)
        elif opcao == "7":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
main()

