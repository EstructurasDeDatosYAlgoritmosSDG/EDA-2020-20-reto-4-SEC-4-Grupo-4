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
from App import model
from DISClib.ADT import map as m
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import stack
import timeit
assert config
from time import process_time
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import map as m
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
        controller.addStationGraph(analizer)
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

    elif int(inputs[0]) == 6:
        t1_start = process_time() #tiempo inicial
        tiempo = int(input('\nTiempo máximo en minutos de resitencia: '))
        id = input('\nCual es la identificación de la estacion de inicio: ')
        print('')
        ruta = controller.ruta_turistica_resistencia(analizer,tiempo, id)
        if ruta != None:
            iterador = it.newIterator(ruta)
            while it.hasNext(iterador):
                camino = it.next(iterador)
                print(camino['vertexA']+' hacia '+ camino['vertexB'] + '. Tiempo estimado: '+ str(camino['weight']))
        else:
            print('La identificación de la estación escrita no existe')
        t1_stop = process_time() #tiempo final
        print("\nTiempo de ejecución",t1_stop-t1_start,"segundos\n")

    elif int(inputs[0]) == 7:
        t1_start = process_time() #tiempo inicial
        print('En que rango de edad se encuentra el turista:')
        print('1) 0-10 años')
        print('2) 11-20 años')
        print('3) 21-30 años')
        print('4) 31-40 años')
        print('5) 41-50 años')
        print('6) 51-60 años')
        print('7) 60+ años')
        rango = int(input('\nIngrese el número: '))
        ruta = controller.recomendar_ruta(analizer, rango)
        if ruta != None:
            estacion_inicio = lt.firstElement(ruta)
            estacion_final = lt.lastElement(ruta)
            print('\nLa estación de inicio recomendada es: '+estacion_inicio)
            print('\nLa estación de finalización recomendada es: ' + estacion_final)
            if lt.size(ruta) != 2:
                print('\nLas estaciónes que estan entre la ruta recomendada son: ')
                i = 1
                while i <= lt.size(ruta):
                    estacion = lt.getElement(ruta, i)
                    if estacion != estacion_inicio and estacion != estacion_final:
                        print(estacion)
        else:
            print('\nNo existen rutas recomendadas para ese rango de edades')
        t1_stop = process_time() #tiempo final
        print("\nTiempo de ejecución",t1_stop-t1_start,"segundos\n")
    
    elif int(inputs[0]) == 8:
        t1_start = process_time() #tiempo inicial
        longitud_origen = float(input('\nIndique la longitud del punto de su ubicación actual: '))
        latitud_origen = float(input('\nIndique la latitud del punto de su ubicación actual: '))
        longitud_destino = float(input('\nIndique la longitud del sitio turístico al que quiere viajar: '))
        latitud_destino = float(input('\nIndique la latitud del sitio turístico al que quiere viajar: '))
        datos = controller.ruta_interes_turistico(analizer,longitud_origen, latitud_origen, longitud_destino, latitud_destino)
        if datos != None:
            print('\nLa estación más cercana a su ubicación actual es: ' + str(lt.firstElement(datos[0])['vertexA']))
            print('\nLa estación más cercana al sitio turístico que quiere visitar es: ' + str(lt.lastElement(datos[0])['vertexB']))
            print('\nEl tiempo estimado de viaje es de: ' + str(datos[1]))
            print('\nLas estaciones en la ruta son: ')
            print(str(lt.firstElement(datos[0])['vertexA']))
            iterador = it.newIterator(datos[0])
            while it.hasNext(iterador):
                siguiente = it.next(iterador)
                print(siguiente['vertexB'])
        t1_stop = process_time() #tiempo final
        print("\nTiempo de ejecución",t1_stop-t1_start,"segundos\n")
    
    elif int(inputs[0]) == 9:
        t1_start = process_time() #tiempo inicial
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución",t1_stop-t1_start,"segundos\n")

    elif int(inputs[0]) == 10:
        t1_start = process_time() #tiempo inicial
        print(m.get(analizer['bicicletas'], 31956))
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución",t1_stop-t1_start,"segundos\n")

    else:
        sys.exit(0)
sys.exit(0)