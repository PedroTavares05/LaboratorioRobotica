from Func import *

# As listas de composição continuam aqui em cima se assim o exigires
lista_kit_arduino = ["Placa Arduino Uno R3", "Cabo USB", "Protoboard 400 furos"]
lista_multimetro = ["Multímetro Digital", "Pontas de prova", "Bateria 9V"]
lista_ferro_solda = ["Ferro de solda 40W", "Suporte metálico", "Tubo de estanho"]
lista_osciloscopio = ["Osciloscópio Digital", "Cabo AC", "Pontas de prova"]

equipamentos_cadastrados = [
    {"id_equipamento": 1, "nome": "Kit Arduino", "itens_inclusos": lista_kit_arduino},
    {"id_equipamento": 2, "nome": "Multímetro Digital", "itens_inclusos": lista_multimetro},
    {"id_equipamento": 3, "nome": "Kit Ferro de Solda", "itens_inclusos": lista_ferro_solda},
    {"id_equipamento": 4, "nome": "Osciloscópio Digital", "itens_inclusos": lista_osciloscopio}
]

registros_emprestimos = [
    {
        "id_registro": 1,
        "aluno": "João Silva",           
        "id_equipamento": 1, 
        "equipamento": "Kit Arduino",  
        "quantidade": 1,                   
        "status": "Pendente"             
    },
    {
        "id_registro": 2,
        "aluno": "Maria Souza",
        "id_equipamento": 2,
        "equipamento": "Multímetro Digital",
        "quantidade": 1,
        "status": "Devolvido"            
    }
]

while True:
    print("""
[1] Registar empréstimo
[2] Listar equipamentos em uso
[3] Buscar responsável ou equipamento
[4] Confirmar devolução
[5] Excluir registo
[0] Sair""")
    
    Entrada = input("\nEscolhe uma opção: ").strip()
    
    if Entrada == "1":
        cadastrar_emprestimo(registros_emprestimos, equipamentos_cadastrados)
    elif Entrada == "2":
        listar_pendentes(registros_emprestimos)
    elif Entrada == "3":
        buscar_emprestimo(registros_emprestimos)
    elif Entrada == "4":
        confirmar_devolucao(registros_emprestimos, equipamentos_cadastrados)
    elif Entrada == "5":
        excluir_emprestimo(registros_emprestimos)
    elif Entrada == "0":
        salvar_dados(registros_emprestimos)
        break
    else:
        print("ERRO: Opção inválida.")