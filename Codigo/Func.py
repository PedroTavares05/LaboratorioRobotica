import json

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

    # Valida catálogo
    equipamento_encontrado = next((eq for eq in catalogo if eq["id_equipamento"] == id_desejado), None)
    if not equipamento_encontrado:
        print("ERRO: Equipamento não existe no sistema.")
        return

    # Valida RN05
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

    # Mostra os acessórios para conferência física
    equipamento_cat = next((eq for eq in catalogo if eq["id_equipamento"] == registro["id_equipamento"]), {})
    itens = equipamento_cat.get("itens_inclusos", [])
    
    print("\nATENÇÃO: Confirma se os seguintes itens estão presentes:")
    for item in itens:
        print(f"- {item}")
        
    if input("Todos os itens estão corretos? (S/N): ").strip().upper() == "S":
        registro["status"] = "Devolvido"
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
        print("SUCESSO: Registo excluído permanentemente.")
    else:
        print("Exclusão cancelada.")


def salvar_dados(registros):
    print("\nA guardar dados...")
    try:
        with open("controle_emprestimos.json", "w", encoding="utf-8") as f:
            json.dump(registros, f, indent=4, ensure_ascii=False)
        print("Dados guardados com sucesso no ficheiro JSON.")
    except Exception as e:
        print(f"ERRO CRÍTICO ao guardar o ficheiro: {e}")