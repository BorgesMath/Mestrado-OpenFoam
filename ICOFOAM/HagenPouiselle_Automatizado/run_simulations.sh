#!/bin/bash

# Valores de pressão para variação
pressures=(110 120 130 140 150)

# Nome do caso base
base_case="HagenPouiselle_Malha4"

# Verificar se o caso base existe
if [ ! -d "$base_case" ]; then
    echo "Erro: Diretório do caso base '$base_case' não encontrado."
    exit 1
fi

# Loop para executar simulações com diferentes valores de pressão
for pressure in "${pressures[@]}"; do
    # Nome do novo caso
    case_name="${base_case}_P${pressure}"
    echo "Criando caso: $case_name com pressão $pressure"

    # Copiar o caso base
    cp -r "$base_case" "$case_name"

    # Modificar a pressão no arquivo '0/p'
    foamDictionary "$case_name/0/p" -entry boundaryField.inlet.value -set "uniform $pressure"

    # Executar blockMesh e icoFoam
    cd "$case_name" || exit
    blockMesh
    icoFoam
    cd ..

    echo "Simulação finalizada para: $case_name"
done
