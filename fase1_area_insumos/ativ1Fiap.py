import time
import csv

print("Tarefa: Cap 1 - Play na sua carreira em IA")
print("Os dois tipos de cultura escolhidos são: café e milho")
print("As figuras geométricas são: ")
time.sleep(1)
print("Retângulo para o café")
print("Retângulo para o milho")
time.sleep(1)
print("O produto aplicado no café é Fosfato Foliar (0,5 L/m)")
print("O produto aplicado no milho é Nitrogenado Líquido (0,1 L/m)")
time.sleep(1)

culturas = ["cafe", "milho"]
insumos = ["Fosfatado Foliar", "Nitrogenado Líquido"]
taxa_insumos = [0.5, 0.1]   # L por metro de linha

# Vetores com 2 posições (café, milho)
larguras = [0.0, 0.0]
alturas  = [0.0, 0.0]
areas    = [0.0, 0.0]
ruas     = [0, 0]
total_insumo = [0.0, 0.0]

def area():
    # define a area das duas culturas
    for x in range(2):
        larguras[x] = float(input(f"Largura da área do {culturas[x]} (m): "))
        alturas[x]  = float(input(f"Altura da área do {culturas[x]} (m): "))
        areas[x] = larguras[x] * alturas[x]
        print(f"Área do {culturas[x]}: {areas[x]:.2f} m²")

def calculoLitros():
    # define a quantidade de litros de cada cultura
    for x in range(2):
        ruas[x] = int(input(f"Quantidade de ruas na área de {culturas[x]}: "))
        total_insumo[x] = alturas[x] * ruas[x] * taxa_insumos[x]
        print(f"Total de {insumos[x]} para {culturas[x]}: {total_insumo[x]:.2f} L")

def saida_dados():
    # printa os dados de ambas as culturas 
    for x in range(2):
        print(f"Cultura: {culturas[x]} | Área: {areas[x]:.2f} m² | Ruas: {ruas[x]} | Insumo: {total_insumo[x]:.2f} L")

def atualiza_dados():
    print("1) Café  |  2) Milho")
    escolha = int(input("Qual cultura deseja alterar? "))
    w = 0 if escolha == 1 else 1 if escolha == 2 else None
    if w is None:
        print("Valor inválido"); return

    print("1) Altura  2) Largura  3) Número de ruas")
    escolhaX = int(input("Qual campo deseja alterar? "))

    if escolhaX == 1:
        alturas[w] = float(input("Nova altura (m): "))
        areas[w] = larguras[w] * alturas[w]
        total_insumo[w] = alturas[w] * ruas[w] * taxa_insumos[w]
    elif escolhaX == 2:
        larguras[w] = float(input("Nova largura (m): "))
        areas[w] = larguras[w] * alturas[w]
        # ⚠️ sempre usa ALTURA no cálculo de insumo
        total_insumo[w] = alturas[w] * ruas[w] * taxa_insumos[w]
    elif escolhaX == 3:
        ruas[w] = int(input("Novo número de ruas: "))
        total_insumo[w] = alturas[w] * ruas[w] * taxa_insumos[w]
    else:
        print("Valor inválido"); return

    print("Atualizado!")
    saida_dados()

def deleta_dados():
    print("1) Apagar dados de Café  |  2) Apagar dados de Milho")
    escolhaX = int(input("Escolha: "))
    w = 0 if escolhaX == 1 else 1 if escolhaX == 2 else None
    if w is None:
        print("Valor inválido"); return
    # Zera valores (não usa pop) para manter o tamanho dos vetores
    alturas[w] = 0.0
    larguras[w] = 0.0
    areas[w] = 0.0
    ruas[w] = 0
    total_insumo[w] = 0.0
    print(f"Dados de {culturas[w]} zerados com sucesso")

def salvar_dados():
    dados_csv = []
    for i in range(2):
        dados_csv.append([culturas[i], larguras[i], alturas[i], areas[i], ruas[i], total_insumo[i]])
    with open("dadosR.csv", "w", newline="") as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow(["Cultura", "Largura", "Altura", "Area", "Ruas", "InsumoTotal"])
        escritor.writerows(dados_csv)
    print("Dados salvos em 'dadosR.csv' com sucesso!")

while True:
    try:
        resposta = int(input(
            "\nMenu:\n"
            "1) Entrada de dados para cálculos\n"
            "2) Saída de dados\n"
            "3) Atualização de dados\n"
            "4) Deleção de dados\n"
            "5) Sair do programa\n"
            "Escolha: "
        ))
    except ValueError:
        print("Digite um número de 1 a 5."); continue

    if resposta == 1:
        area()
        calculoLitros()
    elif resposta == 2:
        saida_dados()
    elif resposta == 3:
        atualiza_dados()
    elif resposta == 4:
        deleta_dados()
    elif resposta == 5:
        print("Fim do programa")
        salvar_dados()
        break
    else:
        print("Opção inválida.")
