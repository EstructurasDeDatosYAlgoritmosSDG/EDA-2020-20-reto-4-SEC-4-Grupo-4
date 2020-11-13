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
                    'edades': None
                    }

        analyzer['conecciones'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
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