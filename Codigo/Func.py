import json
import os

ARQUIVO_REGISTROS = "registros.json"
ARQUIVO_CATALOGO = "catalogo.json"

def LimparTela():
    os.system('cls' if os.name == 'nt' else 'clear')

def inicializar_arquivos():
    """Cria os ficheiros JSON com dados padrão se eles não existirem."""
    if not os.path.exists(ARQUIVO_CATALOGO):
        catalogo_padrao = [
            {"id_equipamento": 1, "nome": "Kit Arduino", "itens_inclusos": ["Placa Arduino Uno R3", "Cabo USB", "Protoboard 400 furos"]},
            {"id_equipamento": 2, "nome": "Multímetro Digital", "itens_inclusos": ["Multímetro Digital", "Pontas de prova", "Bateria 9V"]},
            {"id_equipamento": 3, "nome": "Kit Ferro de Solda", "itens_inclusos": ["Ferro de solda 40W", "Suporte metálico", "Tubo de estanho"]},
            {"id_equipamento": 4, "nome": "Osciloscópio Digital", "itens_inclusos": ["Osciloscópio Digital", "Cabo AC", "Pontas de prova"]}
        ]
        with open(ARQUIVO_CATALOGO, "w", encoding="utf-8") as f:
            json.dump(catalogo_padrao, f, indent=4, ensure_ascii=False)

    if not os.path.exists(ARQUIVO_REGISTROS):
        registros_padrao = [] # Inicia vazio ou com os testes que quiseres
        with open(ARQUIVO_REGISTROS, "w", encoding="utf-8") as f:
            json.dump(registros_padrao, f, indent=4, ensure_ascii=False)

def carregar_dados():
    with open(ARQUIVO_CATALOGO, "r", encoding="utf-8") as f:
        catalogo = json.load(f)
    with open(ARQUIVO_REGISTROS, "r", encoding="utf-8") as f:
        registros = json.load(f)
    return registros, catalogo

def salvar_dados(registros):
    try:
        with open(ARQUIVO_REGISTROS, "w", encoding="utf-8") as f:
            json.dump(registros, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ERRO CRÍTICO ao guardar o ficheiro: {e}")



def cadastrar_emprestimo(registros, catalogo):
    aluno = input("Nome do aluno: ").strip()
    if not aluno:
        print("ERRO: O nome do aluno é obrigatório.")
        return

    try:
        id_desejado = int(input("Digite o ID do equipamento: "))
    except ValueError:
        print("ERRO: O ID deve ser um número inteiro.")
        return

    equipamento_encontrado = next((eq for eq in catalogo if eq["id_equipamento"] == id_desejado), None)
    if not equipamento_encontrado:
        print("ERRO: Equipamento não existe no sistema.")
        return

    if any(reg["id_equipamento"] == id_desejado and reg["status"] == "Pendente" for reg in registros):
        print(f"ERRO: O equipamento '{equipamento_encontrado['nome']}' já está em empréstimo.")
        return


    novo_id = registros[-1]["id_registro"] + 1 if registros else 1
    
    registros.append({
        "id_registro": novo_id,
        "aluno": aluno,
        "id_equipamento": id_desejado,
        "equipamento": equipamento_encontrado["nome"],
        "quantidade": 1,
        "status": "Pendente"
    })
    salvar_dados(registros) 
    print(f"SUCESSO: Empréstimo do {equipamento_encontrado['nome']} registado para {aluno}.")

def listar_pendentes(registros):
    print("\n--- EQUIPAMENTOS EM USO ---")
    pendentes = [reg for reg in registros if reg["status"] == "Pendente"]
    
    if not pendentes:
        print("Nenhum equipamento está emprestado no momento.")
        return
        
    for reg in pendentes:
        print(f"ID Reg: {reg['id_registro']} | Equipamento: {reg['equipamento']} | Aluno: {reg['aluno']}")

def buscar_emprestimo(registros):
    termo = input("\nDigite o nome do aluno ou equipamento para procurar: ").strip().lower()
    if not termo:
        print("ERRO: Termo de pesquisa inválido.")
        return

    resultados = [reg for reg in registros if termo in reg["aluno"].lower() or termo in reg["equipamento"].lower()]
    
    if not resultados:
        print("Nenhum registo encontrado.")
        return
        
    print(f"\n--- RESULTADOS PARA '{termo.upper()}' ---")
    for reg in resultados:
        print(f"ID Reg: {reg['id_registro']} | Equipamento: {reg['equipamento']} | Aluno: {reg['aluno']} | Status: {reg['status']}")

def confirmar_devolucao(registros, catalogo):
    try:
        id_reg = int(input("\nDigite o ID do REGISTRO para devolução: "))
    except ValueError:
        print("ERRO: O ID do registo deve ser um inteiro.")
        return

    registro = next((reg for reg in registros if reg["id_registro"] == id_reg), None)
    
    if not registro:
        print("ERRO: Registo não encontrado.")
        return

    if registro["status"] == "Devolvido":
        print("ERRO: Este equipamento já consta como Devolvido. (RN04)")
        return

    equipamento_cat = next((eq for eq in catalogo if eq["id_equipamento"] == registro["id_equipamento"]), {})
    itens = equipamento_cat.get("itens_inclusos", [])
    
    print("\nATENÇÃO: Confirma se os seguintes itens estão presentes:")
    for item in itens:
        print(f"- {item}")
        
    if input("Todos os itens estão corretos? (S/N): ").strip().upper() == "S":
        registro["status"] = "Devolvido"
        salvar_dados(registros) 
        print(f"SUCESSO: Devolução confirmada para o registo {id_reg}.")
    else:
        print("Devolução cancelada.")

def excluir_emprestimo(registros):
    try:
        id_reg = int(input("\nDigite o ID do REGISTRO a excluir: "))
    except ValueError:
        print("ERRO: O ID deve ser um inteiro.")
        return

    registro = next((reg for reg in registros if reg["id_registro"] == id_reg), None)
    if not registro:
        print("ERRO: Registo não encontrado.")
        return

    if input(f"Confirma a exclusão do registo de {registro['aluno']}? (S/N): ").strip().upper() == "S":
        registros.remove(registro)
        salvar_dados(registros) 
        print("SUCESSO: Registo excluído permanentemente.")
    else:
        print("Exclusão cancelada.")