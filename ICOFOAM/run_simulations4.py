def read_boundary_value(file_path, boundary_name):
    """
    Lê e imprime o valor da pressão de uma fronteira específica no arquivo de OpenFOAM.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    in_boundary = False
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith(boundary_name):  # Detecta o início da seção
            in_boundary = True
        elif in_boundary and "value uniform" in stripped_line:
            # Extrai o valor da pressão
            pressure_value = stripped_line.split()[-1].strip(";")
            print(f"Valor da pressão na fronteira '{boundary_name}': {pressure_value}")
            return pressure_value
        elif in_boundary and stripped_line == "}":  # Sai da seção ao encontrar o fechamento
            in_boundary = False

    print(f"Fronteira '{boundary_name}' não encontrada no arquivo.")
    return None


# Caminho do arquivo '0/p'
file_path = "HagenPouiselle2/0/p"

# Nome da fronteira
boundary_name = "inlet"

# Ler e imprimir o valor da pressão
read_boundary_value(file_path, boundary_name)
