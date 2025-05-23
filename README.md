# Disulfide_Bridges
Este repositorio contiene un programa de detección de puentes disulfurp en estructuras PDB.
El programa de búsqueda de puentes disulfuro se compone de un programa principal, que maneja dos scripts secundarios con distintas funciones: detección de posibles puentes disulfuro, y preparación de un script para una visualización fácil mediante *Pymol*.
Para una correcta ejecución del programa, desde la terminal de `bash`, será necesario tener previamente instalado el intérprete de Python (si es posible en su última versión), así como el programa Pymol. Se recomienda crear un directorio con un entorno virtual de Python (versión 3.X). Deberá instalarse el paquete *Biopython* para el funcionamiento completo del programa. Puede instalarse con el comando siguiente:

`pip install biopython`

Una vez iniciado el programa y especificado el archivo `.pdb` de partida, no será necesaria ninguna interacción más con el programa, ya que los argumentos por línea de comandos especificados anteriormente serán gestionados por la *shell* en el programa principal. Este programa puede ejecutarse con el comando `./disulfuros.sh`.
Una vez obtenida la salida del programa, este finalizará, y podrá abrirse el archivo `.pml` generado mediante el visualizador de *Pymol*.
