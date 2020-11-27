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
from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config
from DISClib.ADT import stack
from DISClib.ADT import minpq
from DISClib.Algorithms.Sorting import quicksort as qs
from math import radians, cos, sin, asin, sqrt

import datetime


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
                    'grafo_tiempos': None,
                    'latitud_longitud': None,
                    'bicicletas': None,
                    'entradasysalidas': None,
                    'par_estaciones': None
                    }

        analyzer['conecciones'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        
        analyzer['edades'] = m.newMap(numelements=768,comparefunction= compararEdades)

        analyzer['grafo_tiempos'] = m.newMap(numelements=768, comparefunction=compararEdades)

        analyzer['latitud_longitud'] = m.newMap(numelements=768, comparefunction=compararIdentificador)

        analyzer['bicicletas'] = m.newMap(numelements=500, comparefunction=compararIdentificador)
                                        
        analyzer['entradasysalidas'] = m.newMap(numelements=768, comparefunction=compareStopIds)

        analyzer['par_estaciones'] = m.newMap(numelements=100000, comparefunction=compararEdades)

        
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
        edad =  2018 - int(trip['birth year'])
        duracion = int(trip['tripduration'])

        #Requerimiento 6
        longitud_origen = float(trip['start station longitude'])
        latitud_origen = float(trip['start station latitude'])
        longitud_destino = float(trip['end station longitude'])
        latitud_destino = float(trip['end station latitude'])
        addStationLongitudLatitud(citybike, origen, longitud_origen, latitud_origen)
        addStationLongitudLatitud(citybike, destino, longitud_destino, latitud_destino)

        #Requerimiento 7
        user_type = trip['usertype']
        if user_type == 'Customer':
            addParEstaciones(citybike, origen, destino, edad)

        #Requerimiento 8

        bikeid = int(trip['bikeid'])
        fecha = trip['starttime'][:10]
        addBike(citybike, bikeid, fecha, origen, destino, duracion)


        addStation(citybike, origen)
        addStation(citybike, destino)
        addStationHash(citybike,origen,edad, 0, user_type)
        addStationHash(citybike,destino,edad, 1, user_type)
        
        addConection(citybike, origen, destino, duracion)
        addEntradaySalida(citybike, origen, 0)
        addEntradaySalida(citybike, destino, 1)
        return citybike
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

def addParEstaciones(citybike, origen, destino, edad):
    par = (origen, destino)
    if not m.contains(citybike['par_estaciones'], par):
        m.put(citybike['par_estaciones'], par, m.newMap(numelements=7, comparefunction=compararRangos))
    rangos = m.get(citybike['par_estaciones'], par)
    rangos = rangos['value']
    if edad <= 10:
        rango = '0-10'
    elif edad <= 20:
        rango = '11-20'
    elif edad <= 30:
        rango = '21-30'
    elif edad <= 40:
        rango = '31-40'
    elif edad <= 50:
        rango = '41-50'
    elif edad <= 60:
        rango = '51-60'
    else:
        rango = '60+'
    if not m.contains(rangos, rango):
        m.put(rangos, rango, 0)
    datos = m.get(rangos, rango)
    datos['value'] += 1
    m.put(citybike['par_estaciones'], par, rangos)
    return citybike

def addBike(citybike, bikeid, fecha, origen, destino, duracion):
    if not m.contains(citybike['bicicletas'], bikeid):
        m.put(citybike['bicicletas'], bikeid, m.newMap(numelements=365, comparefunction=compararBikeid))
    mapa_fechas = m.get(citybike['bicicletas'], bikeid)
    mapa_fechas = mapa_fechas['value']
    if not m.contains(mapa_fechas, fecha):
        m.put(mapa_fechas, fecha, (0, lt.newList()))

    datos = m.get(mapa_fechas, fecha)
    datos = datos['value']
    tiempo_recorrido = datos[0]
    tiempo_recorrido += duracion

    lista_estaciones = datos[1]
    lt.addLast(lista_estaciones, origen)
    lt.addLast(lista_estaciones, destino)

    m.put(mapa_fechas, fecha, (tiempo_recorrido, lista_estaciones))
    m.put(citybike['bicicletas'], bikeid, mapa_fechas)
    return citybike


def addStationLongitudLatitud(citybike, id, longitud, latitud):
    if not m.contains(citybike['latitud_longitud'], id):
        m.put(citybike['latitud_longitud'], id, (longitud, latitud))
    return citybike


def addStationHash(citybike, id, edad, identificador, user_type):
    try:
        id = int(id)
        if not m.contains(citybike['edades'], id):
            m.put(citybike['edades'],id, m.newMap(numelements=2, comparefunction=compararIdentificador))
        tabla = m.get(citybike['edades'],id)
        tabla = tabla['value']
        if not m.contains(tabla,identificador):
            m.put(tabla,identificador,m.newMap(numelements=7, comparefunction=compararRangos))
        rangos = m.get(tabla,identificador)
        rangos = rangos['value']
        if edad <= 10:
            rango = '0-10'
        elif edad <= 20:
            rango = '11-20'
        elif edad <= 30:
            rango = '21-30'
        elif edad <= 40:
            rango = '31-40'
        elif edad <= 50:
            rango = '41-50'
        elif edad <= 60:
            rango = '51-60'
        else:
            rango = '60+'
        if not m.contains(rangos, rango):
            m.put(rangos, rango, [0,0])
        datos = m.get(rangos, rango)
        datos['value'][0] += 1
        if user_type == 'Customer':
            datos['value'][1] += 1
        m.put(tabla,identificador,rangos)
        m.put(citybike['edades'],id,tabla)
        return citybike
    except Exception as exp:
        error.reraise(exp, 'model:addStationHash')

def addStationGraph(citybike):
    print('\nCalculando rutas cortas...')
    vertices = gr.vertices(citybike['conecciones'])
    cant_vertices = gr.numVertices(citybike['conecciones'])
    i = 1
    while i <= cant_vertices:
        station = lt.getElement(vertices, i)
        grafo = djk.Dijkstra(citybike['conecciones'], station)
        m.put(citybike['grafo_tiempos'], station, grafo)
        i += 1
    return grafo




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


def recomendar_ruta(citybike, rango):
    if rango == 1:
        rango = '0-10'
    elif rango == 2:
        rango = '11-20'
    elif rango == 3:
        rango = '21-30'
    elif rango == 4:
        rango = '31-40'
    elif rango == 5:
        rango = '41-50'
    elif rango == 6:
        rango = '51-60'
    else:
        rango = '60+'
    
    mapa_edades = citybike['edades']
    estaciones = m.keySet(mapa_edades)
    mayor_inicio = 0 
    id_mayor_inicio = ''
    mayor_final = 0 
    id_mayor_final = ''
    iterador = it.newIterator(estaciones)
    while it.hasNext(iterador):
        id_estacion = it.next(iterador)
        datos = m.get(mapa_edades, id_estacion)
        datos = datos['value']
        if m.contains(datos, 0):
            mapa_origen = m.get(datos, 0)
            mapa_origen = mapa_origen['value']
            if m.contains(mapa_origen, rango):
                origen = m.get(mapa_origen, rango)
                origen = origen['value'][0]
                if int(origen) > mayor_inicio:
                    mayor_inicio = int(origen)
                    id_mayor_inicio = id_estacion
        if m.contains(datos, 1):
            mapa_destino = m.get(datos ,1)
            mapa_destino = mapa_destino['value']
            if m.contains(mapa_destino, rango):
                destino = m.get(mapa_destino, rango)
                destino = destino['value'][0]
                if int(destino) > mayor_final:
                    mayor_final = destino
                    id_mayor_final = id_estacion
    camino = ''
    if id_mayor_inicio != '' and id_mayor_final != '':
        dijsktra_origen = m.get(citybike['grafo_tiempos'],str(id_mayor_inicio))
        dijsktra_origen = dijsktra_origen['value']
        camino = djk.pathTo(dijsktra_origen, str(id_mayor_final))
    return camino

def identificar_estaciones_publicidad(citybike, rango):
    if rango == 1:
        rango = '0-10'
    elif rango == 2:
        rango = '11-20'
    elif rango == 3:
        rango = '21-30'
    elif rango == 4:
        rango = '31-40'
    elif rango == 5:
        rango = '41-50'
    elif rango == 6:
        rango = '51-60'
    else:
        rango = '60+'

    estaciones_mayor = 0
    estaciones = lt.newList()

    par_estaciones = m.keySet(citybike['par_estaciones'])
    iterador = it.newIterator(par_estaciones)
    while it.hasNext(iterador):
        par_estacion = it.next(iterador)
        mapa_rangos = m.get(citybike['par_estaciones'], par_estacion)
        mapa_rangos = mapa_rangos['value']
        if m.contains(mapa_rangos, rango):
            cant_rango = m.get(mapa_rangos, rango)
            cant_rango = cant_rango['value']
            if cant_rango == estaciones_mayor:
                lt.addLast(estaciones, par_estacion)
            elif cant_rango > estaciones_mayor:
                estaciones_mayor = cant_rango
                estaciones = lt.newList()
                lt.addLast(estaciones, par_estacion)
                
    return estaciones, estaciones_mayor

def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def ruta_interes_turistico(citybike, longitud_origen, latitud_origen, longitud_destino, latitud_destino):
    vertices = m.keySet(citybike['latitud_longitud'])
    menor_origen = 10000000
    menor_vertice_origen = ''
    menor_destino = 10000000
    menor_vertice_destino = ''
    iterador = it.newIterator(vertices)
    while it.hasNext(iterador):
        vertice = it.next(iterador)
        datos_vertice = m.get(citybike['latitud_longitud'], vertice)
        longitud_vertice = datos_vertice['value'][0]
        latitud_vertice = datos_vertice['value'][1]

        distancia_origen = 1000000000000
        distancia_destino = 10000000000000
        if gr.outdegree(citybike['latitud_longitud'], vertice) != 0:
            distancia_origen = haversine(longitud_origen, latitud_origen, longitud_vertice, latitud_vertice)
        if gr.indegree(citybike['latitud_longitud'], vertice) != 0:
            distancia_destino = haversine(longitud_destino, latitud_destino, longitud_vertice, latitud_vertice)
        if distancia_origen < menor_origen:
            menor_origen = distancia_origen
            menor_vertice_origen = vertice
        if distancia_destino < menor_destino:
            menor_destino = distancia_destino
            menor_vertice_destino = vertice

    camino = ''
    if menor_vertice_origen != '' and menor_vertice_destino != '':
        dijsktra_origen = m.get(citybike['grafo_tiempos'],str(menor_vertice_origen))
        dijsktra_origen = dijsktra_origen['value']
        camino = djk.pathTo(dijsktra_origen, str(menor_vertice_destino))
    if not lt.isEmpty(camino):
        return camino
    else:
        return menor_vertice_origen



def calcular_ruta(citybike, tiempo, id, lista_rutas, vertices_utilizados, tiempo_recorrido):
    """ 
    Esta funcion calcula la ruta que recorre mas estacionoes en el menor tiempo posible

    """
    vertices_adyacentes = gr.adjacents(citybike['conecciones'], id)
    cola_id = minpq.newMinPQ(compararArcos)
    iterador = it.newIterator(vertices_adyacentes)
    while it.hasNext(iterador):
        vertice = it.next(iterador)
        valor = gr.getEdge(citybike['conecciones'], id, vertice)
        minpq.insert(cola_id, valor)
    
    primer_valor = minpq.min(cola_id)

    vertice_utilizar = ''
    encontre = False
    while minpq.size(cola_id) != 0 and not encontre:
        primer_vertice = minpq.min(cola_id)
        vertexB = primer_vertice['vertexB']
        if not m.contains(vertices_utilizados, vertexB):
            vertices_adyacentes_b = gr.adjacents(citybike['conecciones'], vertexB)
            cant_vertices_adyacentes_b = lt.size(vertices_adyacentes_b)
            if cant_vertices_adyacentes_b != 0:
                encontre = True
                vertice_utilizar = vertexB
                m.put(vertices_utilizados, vertice_utilizar, 0)
        minpq.delMin(cola_id)

    if vertice_utilizar == '':
        if primer_valor != None:
            if not m.contains(vertices_utilizados, primer_valor['vertexB']) and primer_valor['weight']+ tiempo_recorrido <= tiempo:
                m.put(vertices_utilizados,primer_valor['vertexB'],0)
                lt.addLast(lista_rutas, primer_valor)
        return lista_rutas
    arco = gr.getEdge(citybike['conecciones'], id, vertice_utilizar)
    peso = arco['weight']
    if tiempo_recorrido + peso > tiempo:
        return lista_rutas
    tiempo_recorrido += peso
    lt.addLast(lista_rutas, arco)
    calcular_ruta(citybike, tiempo, vertice_utilizar, lista_rutas, vertices_utilizados, tiempo_recorrido)


def ruta_turistica_resistencia(citybike, tiempo, id):
    esta_id = gr.containsVertex(citybike['conecciones'], id)
    if esta_id:
        tiempo = tiempo * 60
        vertices_utilizados = m.newMap(comparefunction=compararIdentificador)
        m.put(vertices_utilizados, id, 0)
        lista_total = lt.newList()
        termine = False
        while not termine:
            lista_rutas = lt.newList(datastructure='ARRAY_LIST')
            calcular_ruta(citybike, tiempo, id, lista_rutas, vertices_utilizados, 0)
            if lt.size(lista_rutas) == 1 or lt.size(lista_rutas) == 0:
                termine = True
            elif lt.size(lista_rutas) > lt.size(lista_total):
                lista_total = lista_rutas
        return lista_total
    else:
        return None

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

def identificar_bicicleta(citybike, bikeid, fecha):
    if m.contains(citybike['bicicletas'], bikeid):
        mapa = m.get(citybike['bicicletas'], bikeid)
        mapa = mapa['value']
        if m.contains(mapa, fecha):
            llaves_horas = m.get(mapa, fecha)
            llaves_horas = llaves_horas['value']
            tiempo_uso = llaves_horas[0]
            tiempo_parqueada = 86400 - tiempo_uso
            lista_estaciones = llaves_horas[1]

            return tiempo_uso, tiempo_parqueada, lista_estaciones


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

def compararEdades(keyname, productora):
    """
    Compara dos productoras. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(productora)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def compararIdentificador(keyname, productora):
    """
    Compara dos productoras. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(productora)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
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

def compararRangos(keyname, productora):
    """
    Compara dos productoras. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(productora)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
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

def compararVertices(v1, v2):
    if int(v1) == int(v2):
        return 0
    elif int(v1) > int(v2):
        return 1
    return -1

def compararArcos(v1, v2):
    v1 = v1['weight']
    v2 = v2['weight']
    if int(v1) == int(v2):
        return 0
    elif int(v1) > int(v2):
        return 1
    return -1

def compararHoras(v1, v2):
    v1 = v1[0]
    v2 = v2[0]
    if v1 == v2:
        return 0
    elif int(v1) > int(v2):
        return 1
    return -1

def compararBikeid(keyname, productora):
    """
    Compara dos productoras. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(productora)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
      return 1
    else:
        return -1

