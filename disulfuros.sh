#!/bin/bash

# Listado de archivos disponibles
echo "Archivos disponibles:"
ls *.pdb
# Interacción con el usuario: escoger el archivo
read -p "Introduce el nombre del archivo PDB (con extensión .pdb): " pdb_file

# Corroborar que exista
if [[ ! -f "$pdb_file" ]]; then
  echo "El archivo no existe."
  exit 1
fi

# Nombre del archivo sin extensión 
base_name="${pdb_file%.pdb}"

# Ejecutar el primer script python para detectar puentes
echo "Identificando puentes disulfuro en la estructura PDB..."
python3 puentes_disulfuro.py "$pdb_file"


# Lectura del archivo .csv y generación del script de pymol
csv="Puentes_disulfuro_${base_name}.csv"
if [[ ! -f "$csv" ]]; then
  echo "Como no se han detectado puentes, no se creará el archivo .pml"
  echo "¡Gracias por utilizar este programa!"
  exit 1
fi

echo ""
echo "Archivo con los posibles puentes disulfuro identificados creado."
echo "Puede consultarlo en 'Puentes_disulfuro_$base_name.csv'"
# Salida en .csv

echo ""
echo "Creando el archivo pymol para visualizar..."

python3 generar_pymol.py "$pdb_file" "$csv"

echo ""
echo "Puede consultar el archivo Pymol generado en $base_name.pml"
# Salida en .pml
echo "¡Gracias por utilizar este programa!"