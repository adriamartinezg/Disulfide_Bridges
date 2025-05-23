from Bio.PDB import *
from itertools import combinations
import math
import sys

def abrir_estructura(path:str)->(bool, Structure):
    """
    Esta función permite abrir una archivo PDB del directorio.
    Parameters: 
      path(str): ruta al archivo que se quiere abrir.
    Returns:
      bool: devuelve True si se ha podido abrir el archivo y False
            en caso contrario.
      Structure: en caso que se haya podido abrir, devuelve la estructura
            y todas sus características.
    """
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", path)
    if structure:
        abierto = True
    else:
        abierto = False
    return abierto, structure


def isalphafold(path:str)->bool:
    """
    Comprueba si la estructura del archivo .pdb
    ha sido modelada mediante AlphaFold.
    Parameters:
        path(str): ruta al archivo que se quiere comprobar.
    Returns:
        bool: devuelve True si es AlphaFold y False en caso contrario
    """
    alphafold = False
    
    archivo = open(path, 'r', encoding='UTF-8')
    for line in archivo:
        if "ALPHAFOLD" in line.upper():
            alphafold = True
            break
    archivo.close()
    return alphafold


def potenciales_disulfuro(structure:Structure)->list:
    """
    Esta función permite evaluar potenciales puentes disulfuro entre
    átomos de cisteína de una cadena aminoacídica con los criterios
    establecidos.
    Parameters:
        structure(Structure): objeto Structure de Bio.PDB con toda la
            información estructural de la proteína
    Returns:
        list: lista con los pares de átomos cisteína que superan los
            criterios establecidos
    """
    # Todas las cisteínas de la secuencia de aa
    cys = [atom for atom in structure.get_atoms() 
           if atom.get_name() == "SG"]
    puentes = []
    for atom1, atom2 in combinations(cys, 2):
        puente = True
        # Calcular distancia entre las cisteínas
        distance = abs(atom1 - atom2)
        # Si la distancia es adecuada, evaluamos el angulo diedro:
        if 1.5 <= distance <= 2.5:
            # Buscamos los residuos de donde provienen
            res1 = atom1.get_parent()
            res2 = atom2.get_parent()
            try:
                # Y buscamos sus C-beta para obtener el ángulo diedro
                atomSG1 = Vector(atom1.coord)
                atomCB1 = Vector(res1["CB"].coord)
                atomCB2 = Vector(res2["CB"].coord)
                atomSG2 = Vector(atom2.coord)

                if atomCB1 and atomCB2:
                    # Calculamos en grados el ángulo diedro
                    angulo_diedro = abs(
                        calc_dihedral(atomCB1, atomSG1, atomSG2, atomCB2))
                    diedro_grados = math.degrees(angulo_diedro)

                    # Corroborar si cumple la condición

                    if 84 <= diedro_grados <= 96:
                        # Puente correcto
                        puente = True
                    else:
                        puente = False
                else:
                    puente = False
            except:
                continue
        # Si distancia ya no es adecuada, no habrá puente
        else:
            puente = False
            
        if puente:
            # Si puente está comprobado, se añade a la lista
            puentes.append([atom1, atom2])
    return puentes

def descartar(structure, puentes:list)->list:
    # Ver si la estructura es AlphaFold o cristalizada
    alphafold = isalphafold(structure)
    puentes_filtrados = []
    for puente in puentes:
        if alphafold:
            # Eliminar si algún pLDDT < 40
            pLDDT1 = puente[0].get_bfactor()
            pLDDT2 = puente[1].get_bfactor()
            if pLDDT1 < 40 or pLDDT2 < 40:
                continue
            else:
                puentes_filtrados.append(puente)    
        else:
            # Eliminar si el b-factor > 35
            b1 = puente[0].get_bfactor()
            b2 = puente[1].get_bfactor()
            if b1 > 35 or b2 > 35:
                continue
            else:
                puentes_filtrados.append(puente)    
    return puentes_filtrados

def crear_salida(archivo:str, puentes_filtrados:list):

    salida = open(f'Puentes_disulfuro_{archivo[:-4]}.csv', 'w', encoding='UTF-8')
    salida.write("cadena1,res1,cadena2,res2\n")

    # Mensaje de control de puentes encontrados
    encontrados = len(puentes_filtrados)
    print(f"Se ha(n) encontrado {encontrados} puente(s).")

    for a1, a2 in puentes_filtrados:
        # Buscamos el resido, como 'parent' de átomo
        r1 = a1.get_parent()
        r2 = a2.get_parent()
        # Buscamos la cadena, como 'parent' del residuo
        c1 = r1.get_parent().id
        c2 = r2.get_parent().id
        salida.write(f"{c1},{r1.id[1]},{c2},{r2.id[1]}\n")
    salida.close()

def main():
    
    # Leemos línea de comandos
    if len(sys.argv) < 2:
        print("Debes proporcionar el archivo PDB como argumento.")
        sys.exit(1)

    archivo = sys.argv[1]

    # Abrimos estructura
    abierto, estructura = abrir_estructura(archivo)

    if abierto:
        # Estudiamos disulfuro posibles
        disulfuros = potenciales_disulfuro(estructura)

        # Evaluamos su calidad
        disulfuros_filtrados = descartar(archivo, disulfuros)

        # creamos el csv de salida si hay puentes disulfuro
        if len(disulfuros_filtrados)>1:
            crear_salida(archivo, disulfuros_filtrados)
        else:
            print("No se ha creado el archivo .csv ya que", 
                  "no se han detectado puentes")
    else:
        print("Error al abrir el archivo")
        sys.exit(1)

if __name__ == "__main__":
    main()
