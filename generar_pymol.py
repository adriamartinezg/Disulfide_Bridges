def generar_pml(pdb:str, csv:str):

    output = f"{pdb[:-4]}.pml"
    salida = open(output, 'w', encoding='UTF-8')
    # Cargar la estructura de la proteína
    # Formato cartoon y color pastel para que destaquen los residuos marcados
    salida.write(f"load {pdb}\n")
    salida.write("hide everything\n")
    salida.write("show cartoon\n")
    salida.write("color palecyan, all\n")
    
    datos = open(csv, 'r', encoding='UTF-8')
    datos.readline() # Saltar cabecera

    index = 1
    for line in datos:
        # Separamos elementos de la línea del csv
        cadena1, residuo1, cadena2, residuo2 = line.strip().split(',')

        # Residuos
        sele1 = f"resi {residuo1} and chain {cadena1} and name SG"
        sele2 = f"resi {residuo2} and chain {cadena2} and name SG"

        # Puentes
        salida.write(f"select puente{index}_1, {sele1}\n")
        salida.write(f"select puente{index}_2, {sele2}\n")

        # Resaltar SG en puentes
        salida.write(f"show spheres, puente{index}_1 or puente{index}_2\n")
        salida.write(f"color yellow, puente{index}_1 or puente{index}_2\n")

        """
        # Crear línea entre los dos
        salida.write(f"distance puente{index}_line, puente{index}_1, puente{index}_2\n ")
        salida.write(f"set dash_color, red, puente{index}_1, puente{index}_2\n")
        salida.write("\n")"""

        index += 1
    datos.close()
    # Zoom automático en la estructura
    salida.write("zoom\n")
    salida.close()
    return


import sys
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python generar_pml.py estructura.pdb disulfuros.csv")
        sys.exit(1)

    pdb = sys.argv[1]
    csv = sys.argv[2]
    generar_pml(pdb, csv)