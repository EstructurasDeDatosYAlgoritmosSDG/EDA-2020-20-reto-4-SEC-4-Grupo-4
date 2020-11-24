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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador

   estaciones: Tabla de hash para guardar los vertices del grafo
   conecciones: Grafo para representar las rutas entre estaciones
    """
    try:
        analyzer = {
                    'conecciones': None,
                    'edades': None,
                    'entradasysalidas': None
                    }

        analyzer['conecciones'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
                                        
        analyzer['entradasysalidas'] = m.newMap(numelements=768, comparefunction=compareStopIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al grafo

def addTrip(citybike, trip):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    try:
        origen = trip['start station id']
        destino = trip['end station id']
        edad = int(trip['birth year']) - 2018
        duracion = int(trip['tripduration'])
        addStation(citybike, origen)
        addStation(citybike, destino)
        addConection(citybike, origen, destino, duracion)
        addEntradaySalida(citybike, origen, 0)
        addEntradaySalida(citybike, destino, 1)
        return citybike
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

def addStation(citybike, stationId):
    """
    Adiciona una estacion como un vertice de un grafo
    """
    if not gr.containsVertex(citybike['conecciones'], stationId):
        gr.insertVertex(citybike['conecciones'], stationId)
    return citybike

def addConection(citybike, origen, destino, duracion):
    """
    Adiciona un arco entre dos estaciones
    """
    arco = gr.getEdge(citybike['conecciones'], origen, destino)
    if arco is None:
        gr.addEdge(citybike['conecciones'],origen, destino, duracion)
    else:
        antes = gr.getEdge(citybike['conecciones'],origen,destino)
        peso_inicial = antes['weight']
        promedio = (peso_inicial + duracion)/2
        arco['weight'] = promedio
    return citybike

def addEntradaySalida(citybike, stationId, identificador):
    """
    Adiciona una entrada y salida a la tabla de hash
    """
    if not m.contains(citybike['entradasysalidas'], stationId):
        mapa_interior = m.newMap(numelements=2, comparefunction=compareEntradasySalidas)
        m.put(citybike['entradasysalidas'], stationId, mapa_interior)
    mapa_interior = m.get(citybike['entradasysalidas'], stationId)
    mapa_interior = mapa_interior['value']
    if identificador == 0:
        if not m.contains(mapa_interior, identificador):
            m.put(mapa_interior, identificador, 0)
        suma1 = m.get(mapa_interior, identificador)
        suma1['value'] += 1
    else:
        if not m.contains(mapa_interior, identificador):
            m.put(mapa_interior, identificador, 0)
        suma2 = m.get(mapa_interior, identificador)
        suma2['value'] += 1
    return citybike
# ==============================
# Funciones de consulta
# ==============================

def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['conecciones'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['conecciones'])

def numSCC(citybike):
    sc = scc.KosarajuSCC(citybike)
    return scc.connectedComponents(sc)

def sameCC(citybike, parada1, parada2):
    return scc.stronglyConnected(scc.KosarajuSCC(citybike), parada1, parada2)


def recomendar_ruta(citybike):
    pass

def EstacionesCriticas(citybike):
    mapa_estaciones = citybike['entradasysalidas']
    llaves = m.keySet(mapa_estaciones)
    iterador = it.newIterator(llaves)
    entradas = 0
    salidas = 0
    mayor_entradas1 = -10
    mayor_entradas2 = -10
    mayor_entradas3 = -10
    mejor_entradas1 = ''
    mejor_entradas2 = ''
    mejor_entradas3 = ''
    mejor_salidas1 = ''
    mejor_salidas2 = ''
    mejor_salidas3 = ''
    peor_suma1 = ''
    peor_suma2 = ''
    peor_suma3 = ''
    mayor_salidas1 = -10
    mayor_salidas2 = -10
    mayor_salidas3 = -10
    menor_suma1 = 100000
    menor_suma2 = 100000
    menor_suma3 = 100000
    lista_entradas = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compararvertices)
    lista_salidas = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compararvertices)
    lista_peores = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compararvertices)
    while it.hasNext(iterador):
        estacion = it.next(iterador)
        mapa_interior = m.get(mapa_estaciones, estacion)
        mapa_salidas = mapa_interior['value']
        if m.contains(mapa_salidas, 0):
            entradas = m.get(mapa_salidas, 0)
            entradas = entradas['value']
            if entradas > mayor_entradas1:
                auxiliar_nombre = mejor_entradas1
                auxiliar_valor = mayor_entradas1
                mayor_entradas1 = entradas
                mejor_entradas1 = estacion
                auxiliar_nombre1 = mejor_entradas2
                auxiliar_valor1 = mayor_entradas2
                mejor_entradas2 = auxiliar_nombre
                mayor_entradas2 = auxiliar_valor
                mejor_entradas3 = auxiliar_nombre1
                mayor_entradas3 = auxiliar_valor1
            elif mayor_entradas2 < entradas:
                auxiliar_valor = mayor_entradas2
                mayor_entradas2 = entradas
                auxiliar_nombre = mejor_entradas2
                mejor_entradas2 = estacion
                mejor_entradas3 = auxiliar_nombre
                mayor_entradas3 = auxiliar_valor
            elif mayor_entradas3 < entradas:
                mayor_entradas3 = entradas
                mejor_entradas3 = estacion
                
        if m.contains(mapa_salidas, 1):
            salidas = m.get(mapa_salidas, 1)
            salidas = salidas['value']
            if salidas > mayor_salidas1:
                auxiliar_nombre = mejor_salidas1
                auxiliar_valor = mayor_salidas1
                mayor_salidas1 = salidas
                mejor_salidas1 = estacion
                auxiliar_nombre1 = mejor_salidas2
                auxiliar_valor1 = mayor_salidas2
                mejor_salidas2 = auxiliar_nombre
                mayor_salidas2 = auxiliar_valor
                mejor_salidas3 = auxiliar_nombre1
                mayor_salidas3 = auxiliar_valor1
            elif mayor_salidas2 < salidas:
                auxiliar_valor = mayor_salidas2
                mayor_salidas2 = salidas
                auxiliar_nombre = mejor_salidas2
                mejor_salidas2 = estacion
                mejor_salidas3 = auxiliar_nombre
                mayor_salidas3 = auxiliar_valor
            elif mayor_salidas3 < salidas:
                mayor_salidas3 = salidas
                mejor_salidas3 = estacion
        suma = int(entradas) + int(salidas)
        if suma < menor_suma1:
            auxiliar_nombre = peor_suma1
            auxiliar_valor = menor_suma1
            menor_suma1 = suma
            peor_suma1 = estacion
            auxiliar_nombre1 = peor_suma2
            auxiliar_valor1 = menor_suma2
            peor_suma2 = auxiliar_nombre
            menor_suma2 = auxiliar_valor
            peor_suma3 = auxiliar_nombre1
            menor_suma3 = auxiliar_valor1
        elif menor_suma2 > suma:
            auxiliar_valor = menor_suma2
            menor_suma2 = suma
            auxiliar_nombre = peor_suma2
            peor_suma2 = estacion
            peor_suma3 = auxiliar_nombre
            menor_suma3 = auxiliar_valor
        elif menor_suma3 > suma:
            menor_suma3 = suma
            peor_suma3 = estacion

    lt.addLast(lista_entradas, mejor_entradas1)
    lt.addLast(lista_entradas, mejor_entradas2)
    lt.addLast(lista_entradas, mejor_entradas3)

    lt.addLast(lista_salidas, mejor_salidas1)
    lt.addLast(lista_salidas, mejor_salidas2)
    lt.addLast(lista_salidas, mejor_salidas3)

    lt.addLast(lista_peores, peor_suma1)
    lt.addLast(lista_peores, peor_suma2)
    lt.addLast(lista_peores, peor_suma3)


    return (lista_entradas, lista_salidas, lista_peores)


# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

def compararvertices(vertice1, vertice2):
    """
    Compara dos vertices
    """
    if (vertice1 == vertice2):
        return 0
    elif (vertice1 > vertice2):
        return 1
    else:
        return -1

def compareEntradasySalidas(keyname, productora):
    """
    Compara dos entradas o salidas
    """
    authentry = me.getKey(productora)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1
