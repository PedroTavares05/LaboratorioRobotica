import time
from Func import *

# Prepara e carrega a base de dados em JSON
inicializar_arquivos()
registros_emprestimos, equipamentos_cadastrados = carregar_dados()

while True:
    print("""
======================================
[1] Registar empréstimo
[2] Listar equipamentos em uso
[3] Buscar responsável ou equipamento
[4] Confirmar devolução
[5] Excluir registo
[0] Sair
======================================""")
    
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
        # A gravação já é feita nas funções, mas forçamos uma última vez por segurança
        salvar_dados(registros_emprestimos) 
        LimparTela()
        print("A sair do programa...")
        time.sleep(1)
        break
    else:
        print("ERRO: Opção inválida.")
    
    # Pausa e limpeza centralizadas para não sujar os if/elif
    if Entrada != "0":
        time.sleep(2.5)
        LimparTela()