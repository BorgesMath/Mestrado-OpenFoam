import os
import subprocess

# Parâmetros para variação
pressures = [150]  # Valores de pressão para 'left'
lengths = [2]  # Comprimento (distância entre 'left' e 'right')
heights = [0.5]  # Altura total

# Caminho do caso base
base_case = "HagenPouiselle2"

def replace_boundary_value(file_path, boundary_name, new_value):
    with open(file_path, "r") as file:
        lines = file.readlines()

    with open(file_path, "w") as file:
        in_boundary = False
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith(boundary_name):  # Detecta o início da seção
                in_boundary = True
            elif in_boundary and "value uniform" in stripped_line:
                # Substitui o valor da pressão
                line = f"        value           uniform {new_value};\n"
                in_boundary = False  # Sai da seção após a substituição
            elif in_boundary and stripped_line == "}":  # Detecta o fechamento da seção
                in_boundary = False
            file.write(line)



# Função para atualizar os vértices no blockMeshDict
def update_vertices(block_file, length, height):
    vertices = f"""
    vertices
    (
        (0 {-height/2} 0)  // 0
        ({length} {-height/2} 0)  // 1
        ({length} {height/2} 0)  // 2
        (0 {height/2} 0)  // 3
        (0 {-height/2} 1)  // 4
        ({length} {-height/2} 1)  // 5
        ({length} {height/2} 1)  // 6
        (0 {height/2} 1)  // 7
    );
    """
    with open(block_file, "r") as file:
        lines = file.readlines()

    with open(block_file, "w") as file:
        in_vertices = False
        for line in lines:
            if line.strip().startswith("vertices"):
                in_vertices = True
                file.write(vertices + "\n")  # Escreve os novos vértices
            elif in_vertices and line.strip() == ");":  # Detecta o final da seção
                in_vertices = False
            elif not in_vertices:
                file.write(line)

# Loop para varrer os parâmetros
for pressure in pressures:
    for length in lengths:
        for height in heights:
            # Nome do caso atual
            case_name = f"{base_case}_P{pressure}_L{length}_H{height}"
            print(f"Running case: {case_name}")

            # Copiar o caso base
            subprocess.run(["cp", "-r", base_case, case_name])

            # Modificar a pressão no arquivo '0/p'
            p_file = os.path.join(case_name, "0/p")
            replace_boundary_value(p_file, "left", pressure)

            # Atualizar os vértices no 'constant/polyMesh/blockMeshDict'
            block_file = os.path.join(case_name, "system/blockMeshDict")
            update_vertices(block_file, length, height)

            # Executar a simulação
            os.chdir(case_name)
            subprocess.run(["blockMesh"])

            # Criar o arquivo ".foam" para visualização no ParaView
            foam_file = f"{case_name}.foam"
            open(foam_file, "w").close()  # Cria um arquivo vazio com o nome do caso

            subprocess.run(["icoFoam"])
            os.chdir("..")

            print(f"Simulation completed for: {case_name}")
