#!/bin/bash

# Diretório base onde estão todas as simulações
BASE_DIR="HagenPouiselle_Automatizado"

# Nome do arquivo de resultados
RESULT_FILE="postProcessing/inletFlow/0/surfaceFieldValue.dat"

# Arquivo de saída para consolidar os resultados
OUTPUT_FILE="integrate_U_results.csv"

# Limpar o arquivo de saída
echo "Simulação,Pressão,Último_Valor" > "$OUTPUT_FILE"

# Mensagem de log
echo "Iniciando processamento..."

# Loop por todas as pastas no diretório base
for SIMULATION_DIR in HagenPouiselle_Malha4_*; do
    if [ -d "$case_dir" ]; then
        echo "Processando: $case_dir"
        # Verifica se o arquivo existe
        if [ -f "$case_dir/$RESULT_FILE" ]; then
            echo "Arquivo encontrado: $case_dir/$RESULT_FILE"
            # Extrai o último valor do arquivo
            last_line=$(tail -n 1 "$case_dir/$RESULT_FILE")
            
            # Extrai a pressão do nome do diretório (assumindo formato _P<number>)
            pressure=$(basename "$case_dir" | grep -oP '_P\K[0-9]+')

            # Adiciona a linha extraída ao arquivo de saída
            echo "$(basename "$case_dir"),$pressure,$last_line" >> "$OUTPUT_FILE"
        else
            echo "Arquivo de resultados não encontrado em $case_dir"
        fi
    fi
done

echo "Resultados consolidados em $OUTPUT_FILE"
