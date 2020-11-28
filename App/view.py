"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import map as m
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import stack
import timeit
assert config
from time import process_time

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


# ___________________________________________________
#  Menu principal
# ___________________________________________________

"""
Menu principal
"""

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar viajes")
    print("3- Conocer cantidad de Clusters de viajes")
    print("4- Obtener una ruta turística circular")
    print("5- Conocer estaciones críticas")
    print("6- Obtener ruta turística por resistencia")
    print("7- Recomendador de rutas por rango de edades")
    print("8- Conocer ruta de interés turístico")
    print("9- Identificar estaciones para publicidad")
    print("10- Identificar bicicletas para mantenimiento")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        t1_start = process_time() #tiempo inicial
        print('\nIniciando analizador...')
        analizer = controller.init()
        t1_stop = process_time() #tiempo final
        print("\nTiempo de ejecución",t1_stop-t1_start,"segundos\n")
        
    elif int(inputs[0]) == 2:
        t1_start = process_time() #tiempo inicial
        print('\nCargando los datos...')
        cont = controller.loadTrips(analizer)
        numedges = controller.totalConnections(cont[0])
        numvertex = controller.totalStops(cont[0])
        print('\nNúmero de estaciones: ' + str(numvertex))
        print('\nNúmero de conecciones: ' + str(numedges))
        print('\nEl total de viajes cargados es de: ' + str(cont[1]))
        t1_stop = process_time() #tiempo final
        print("\nTiempo de ejecución",t1_stop-t1_start,"segundos\n")

    elif int(inputs[0]) == 3:
        t1_start = process_time() #tiempo inicial
        estacion1 = (input('\nEscriba la identificación de la estación 1: '))
        estacion2 = (input('\nEscriba la identificación de la estación 2: '))
        print('\nEl total de Clusters encontrados es: ' + str(controller.cantidad_componentes_fconectados(analizer)))
        pertenecen = controller.pertenecen_al_mismo_cluster(analizer,estacion1,estacion2)
        if pertenecen:
            print('\nLas dos estaciones pertenecen al mismo Cluster.')
        else:
            print('\nLas dos estaciones no pertenecen al mismo Cluster.')
        t1_stop = process_time() #tiempo final
        print("\nTiempo de ejecución",t1_stop-t1_start,"segundos\n")

    elif int(inputs[0]) == 4:
        t1_start = process_time() #tiempo inicial
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución",t1_stop-t1_start,"segundos\n")
        source_id= input('Por favor digite el id de la estación donde va a empezar su recorrido: ')
        conexiones = controller.conexiones_source(analizer, source_id)
        print(conexiones)
        
    elif int(inputs[0]) == 5: #conocer estaciones criticas
        t1_start = process_time() #tiempo inicial
        cont = controller.conocerEstacionesCriticas(analizer)
        print('\nLos nombres de las 3 estaciones Top de llegada son:')
        iterador_llegada = it.newIterator(cont[0])
        iterador_salida = it.newIterator(cont[1])
        iterador_peores = it.newIterator(cont[2])
        while it.hasNext(iterador_llegada):
            estacion = it.next(iterador_llegada)
            print(estacion)
        print('\nLos nombres de las 3 estaciones Top de salida son:')
        while it.hasNext(iterador_salida):
            estacion = it.next(iterador_salida)
            print(estacion)
        print('\nLos nombres de las 3 estaciones menos utilizadas son:')
        while it.hasNext(iterador_peores):
            estacion = it.next(iterador_peores)
            print(estacion)
        t1_stop = process_time() #tiempo final
        print("\nTiempo de ejecución",t1_stop-t1_start,"segundos\n")

    elif int(inputs[0]) == 7:
        t1_start = process_time() #tiempo inicial
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución",t1_stop-t1_start,"segundos\n")

    elif int(inputs[0]) == 8:
        t1_start = process_time() #tiempo inicial
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución",t1_stop-t1_start,"segundos\n")
    
    elif int(inputs[0]) == 9:
        t1_start = process_time() #tiempo inicial
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución",t1_stop-t1_start,"segundos\n")
    
    elif int(inputs[0]) == 10:
        t1_start = process_time() #tiempo inicial
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución",t1_stop-t1_start,"segundos\n")

    else:
        sys.exit(0)
sys.exit(0)