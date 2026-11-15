import os
import platform
import subprocess
import math
import matplotlib.pyplot as plt
from aircraft import Aircraft, LoadAircraft
from flight import Flight, LoadFlights, TimeToMinutes
from datetime import datetime, timedelta


class Airline:
    def __init__(self, name, fleet, operations, airports=None):
        self.name = name
        self.fleet = fleet
        self.operations = operations
        self.airports = airports if airports is not None else []

    def ejecutar_algoritmo_a(self):
        for vuelo in self.operations:
            vuelo.assigned_aircraft = None

        asignados = 0
        no_asignados = 0

        for vuelo in self.operations:
            vuelo_asignado = False
            for avion in self.fleet:
                avion_ya_usado = any(v.assigned_aircraft == avion.callsign for v in self.operations)

                if not avion_ya_usado:
                    capacidad_ok = avion.capacity >= vuelo.passengers
                    ubicacion_ok = avion.location and avion.location.strip().upper() == vuelo.departure_airport.strip().upper()

                    if capacidad_ok and ubicacion_ok:
                        vuelo.assigned_aircraft = avion.callsign
                        vuelo_asignado = True
                        asignados += 1
                        break
            if not vuelo_asignado:
                no_asignados += 1

        print(f"Algoritmo A -> Asignados: {asignados}, Sin asignar: {no_asignados}")
        return asignados

    def ejecutar_algoritmo_b(self):
        for vuelo in self.operations:
            vuelo.assigned_aircraft_b = None

        aviones_vuelos = {avion.callsign: [] for avion in self.fleet}
        asignados_exito = 0
        vuelos_ordenados = sorted(self.operations, key=lambda v: v.departure_time)

        for vuelo in vuelos_ordenados:
            avion_asignado = None
            for avion in self.fleet:
                vuelos_actuales = aviones_vuelos[avion.callsign]

                if len(vuelos_actuales) >= 2 or avion.capacity < vuelo.passengers:
                    continue

                if len(vuelos_actuales) == 0:
                    if avion.location.strip().upper() == vuelo.departure_airport.strip().upper():
                        avion_asignado = avion
                        break
                elif len(vuelos_actuales) == 1:
                    primer_vuelo = vuelos_actuales[0]
                    llega_bien = primer_vuelo.arrival_airport.strip().upper() == vuelo.departure_airport.strip().upper()
                    h1_llegada = datetime.strptime(primer_vuelo.arrival_time, "%H:%M")
                    h2_salida = datetime.strptime(vuelo.departure_time, "%H:%M")

                    if llega_bien and (h2_salida - h1_llegada >= timedelta(hours=2)):
                        avion_asignado = avion
                        break

            if avion_asignado:
                vuelo.assigned_aircraft_b = avion_asignado.callsign
                aviones_vuelos[avion_asignado.callsign].append(vuelo)
                asignados_exito += 1

        print(f"Algoritmo B -> Asignados: {asignados_exito}")
        return asignados_exito

    def guardar_posiciones_fin_dia(self, filename, algoritmo='A'):
        f = open(filename, 'w')
        f.write("CALLSIGN INITIAL-LOCATION\n")

        for avion in self.fleet:
            vuelos_asignados = [v for v in self.operations if
                                (algoritmo == 'A' and v.assigned_aircraft == avion.callsign) or (
                                            algoritmo == 'B' and v.assigned_aircraft_b == avion.callsign)]

            if vuelos_asignados:
                vuelos_asignados.sort(key=lambda v: v.arrival_time)
                ubicacion_final = vuelos_asignados[-1].arrival_airport
            else:
                ubicacion_final = avion.location if avion.location else "UNKNOWN"

            f.write(f"{avion.callsign} {ubicacion_final}\n")
        f.close()
        print(f"Archivo guardado: {filename}")


def PlotFlights(airline):
    hourly_counts = [0] * 24
    for fl in airline.operations:
        dep_min = TimeToMinutes(fl.departure_time)
        arr_min = TimeToMinutes(fl.arrival_time)
        for hour in range(24):
            if dep_min < (hour + 1) * 60 and arr_min > hour * 60:
                hourly_counts[hour] += 1

    plt.bar([f"{h}:00" for h in range(24)], hourly_counts, color='skyblue')
    plt.xlabel('Hours Of The Day')
    plt.ylabel('Number Of Flights On Air')
    plt.title('Flights On Air Per Hour')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def PlotComparisonFlights(airline):
    hourly_sched = [0] * 24
    hourly_a = [0] * 24
    hourly_b = [0] * 24

    for fl in airline.operations:
        dep_min = TimeToMinutes(fl.departure_time)
        arr_min = TimeToMinutes(fl.arrival_time)
        for hour in range(24):
            if dep_min < (hour + 1) * 60 and arr_min > hour * 60:
                hourly_sched[hour] += 1
                if fl.assigned_aircraft:
                    hourly_a[hour] += 1
                if fl.assigned_aircraft_b:
                    hourly_b[hour] += 1

    plt.figure(figsize=(10, 5))
    plt.bar([f"{h}:00" for h in range(24)], hourly_sched, color='lightgray', label='Programados', width=0.8)
    plt.bar([f"{h}:00" for h in range(24)], hourly_a, color='green', label='Algoritmo A', width=0.5)
    plt.bar([f"{h}:00" for h in range(24)], hourly_b, color='orange', label='Algoritmo B', width=0.2)
    plt.xlabel('Hora del día')
    plt.ylabel('Vuelos en el aire')
    plt.title('Comparación de Vuelos')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


def calcular_heading(lon1, lat1, lon2, lat2):
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dLon_rad = math.radians(lon2 - lon1)

    y = math.sin(dLon_rad) * math.cos(lat2_rad)
    x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dLon_rad)
    bearing_rad = math.atan2(y, x)
    bearing_deg = math.degrees(bearing_rad)
    return (bearing_deg + 360) % 360


def PlotAircraftRoute(airline, callsign):
    callsign = callsign.strip().upper()

    vuelos_a = []
    vuelos_b = []

    for v in airline.operations:
        asig_a = str(v.assigned_aircraft).strip().upper() if v.assigned_aircraft else ""
        asig_b = str(v.assigned_aircraft_b).strip().upper() if v.assigned_aircraft_b else ""

        if asig_a == callsign:
            vuelos_a.append(v)
        if asig_b == callsign:
            vuelos_b.append(v)

    if not vuelos_a and not vuelos_b:
        print(f"⚠️ ATENCIÓN: El avión '{callsign}' no tiene ningún vuelo asignado en ningún algoritmo.")
        return

    airport_coords = {a.icao.strip().upper(): (a.longitude, a.latitude) for a in airline.airports}

    aeropuertos_usados = set()
    for v in vuelos_a + vuelos_b:
        aeropuertos_usados.add(v.departure_airport.strip().upper())
        aeropuertos_usados.add(v.arrival_airport.strip().upper())

    valid_coords = [airport_coords[icao] for icao in aeropuertos_usados if icao in airport_coords]
    if not valid_coords:
        print("⚠️ Error: No se encontraron coordenadas válidas para los aeropuertos.")
        return

    center_lon = sum(c[0] for c in valid_coords) / len(valid_coords)
    center_lat = sum(c[1] for c in valid_coords) / len(valid_coords)

    kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Ruta del Avión: {callsign} (A vs B)</name>
    <open>1</open>

    <LookAt>
      <longitude>{center_lon}</longitude>
      <latitude>{center_lat}</latitude>
      <range>2500000</range>
      <tilt>0</tilt>
      <heading>0</heading>
    </LookAt>

    <!-- Aeropuertos (Punto ROJO) -->
    <Style id="airportStyle">
      <IconStyle>
        <scale>1.2</scale>
        <Icon>
          <href>https://maps.google.com/mapfiles/kml/paddle/red-circle.png</href>
        </Icon>
      </IconStyle>
    </Style>

    <!-- Ruta Algoritmo A (Línea ROJA) -->
    <Style id="routeStyleA">
      <LineStyle>
        <color>ff0000ff</color>
        <width>5</width>
      </LineStyle>
    </Style>

    <!-- Ruta Algoritmo B (Línea AZUL) -->
    <Style id="routeStyleB">
      <LineStyle>
        <color>ffff0000</color>
        <width>5</width>
      </LineStyle>
    </Style>
"""

    for icao in aeropuertos_usados:
        if icao in airport_coords:
            lon, lat = airport_coords[icao]
            kml_content += f"""
    <Placemark>
      <name>{icao}</name>
      <visibility>1</visibility>
      <styleUrl>#airportStyle</styleUrl>
      <Point>
        <coordinates>{lon},{lat},0</coordinates>
      </Point>
    </Placemark>"""

    for vuelo in vuelos_a:
        dep = vuelo.departure_airport.strip().upper()
        arr = vuelo.arrival_airport.strip().upper()
        if dep in airport_coords and arr in airport_coords:
            lon1, lat1 = airport_coords[dep]
            lon2, lat2 = airport_coords[arr]
            mid_lon, mid_lat = (lon1 + lon2) / 2, (lat1 + lat2) / 2
            heading_deg = calcular_heading(lon1, lat1, lon2, lat2)

            kml_content += f"""
    <Placemark>
      <name>[Algoritmo A] Vuelo {vuelo.id}</name>
      <visibility>1</visibility>
      <styleUrl>#routeStyleA</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          {lon1},{lat1},0 {lon2},{lat2},0
        </coordinates>
      </LineString>
    </Placemark>

    <Placemark>
      <name>[A] V:{vuelo.id}</name>
      <visibility>1</visibility>
      <Style>
        <IconStyle>
          <scale>0.9</scale>
          <heading>{heading_deg}</heading>
          <Icon>
            <href>https://maps.google.com/mapfiles/kml/shapes/arrow.png</href>
          </Icon>
        </IconStyle>
      </Style>
      <Point>
        <coordinates>{mid_lon},{mid_lat},0</coordinates>
      </Point>
    </Placemark>"""

    for vuelo in vuelos_b:
        dep = vuelo.departure_airport.strip().upper()
        arr = vuelo.arrival_airport.strip().upper()
        if dep in airport_coords and arr in airport_coords:
            lon1, lat1 = airport_coords[dep]
            lon2, lat2 = airport_coords[arr]
            mid_lon, mid_lat = (lon1 + lon2) / 2, (lat1 + lat2) / 2
            heading_deg = calcular_heading(lon1, lat1, lon2, lat2)

            kml_content += f"""
    <Placemark>
      <name>[Algoritmo B] Vuelo {vuelo.id}</name>
      <visibility>1</visibility>
      <styleUrl>#routeStyleB</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>
          {lon1},{lat1},0 {lon2},{lat2},0
        </coordinates>
      </LineString>
    </Placemark>

    <Placemark>
      <name>[B] V:{vuelo.id}</name>
      <visibility>1</visibility>
      <Style>
        <IconStyle>
          <scale>0.9</scale>
          <heading>{heading_deg}</heading>
          <Icon>
            <href>https://maps.google.com/mapfiles/kml/shapes/arrow.png</href>
          </Icon>
        </IconStyle>
      </Style>
      <Point>
        <coordinates>{mid_lon},{mid_lat},0</coordinates>
      </Point>
    </Placemark>"""

    kml_content += """
  </Document>
</kml>"""

    filename = f"ruta_{callsign}.kml"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(kml_content)

    ruta_absoluta = os.path.abspath(filename)
    try:
        if platform.system() == "Windows":
            os.startfile(ruta_absoluta)
        elif platform.system() == "Darwin":
            subprocess.call(["open", ruta_absoluta])
        else:
            subprocess.call(["xdg-open", ruta_absoluta])
        print(f"🌍 Google Earth abierto correctamente para {callsign}")
    except Exception as e:
        print(f"Error al abrir Google Earth: {e}")