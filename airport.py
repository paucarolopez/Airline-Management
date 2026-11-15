class Airport:
    def __init__(self, icao, latitude, longitude):
        self.icao = icao.strip().upper()
        self.latitude = float(latitude)
        self.longitude = float(longitude)

def PrintAirport(airport):
    print('ICAO:', airport.icao, 'Latitude:', airport.latitude, 'Longitude:', airport.longitude)

def PrintAirports(airports):
    for airport in airports:
        PrintAirport(airport)

def LoadAirports(filename):
    airports = []
    try:
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()

        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) >= 2:
                icao = parts[0]
                coords = parts[1].split(',')
                if len(coords) == 2:
                    longitude = coords[0]
                    latitude = coords[1]
                    airport_obj = Airport(icao, latitude, longitude)
                    airports.append(airport_obj)
    except FileNotFoundError:
        print('El archivo de aeropuertos no se encontró')
    return airports

def SaveAirports(airports, filename):
    f = open(filename, 'w')
    f.write("AIRP CoordinateLongitude,Latitude Description\n")
    for a in airports:
        f.write(f"{a.icao} {a.longitude},{a.latitude} Airport\n")
    f.close()

if __name__ == "__main__":
    print("--- Probando módulo Airport ---")
    lista_prueba = LoadAirports("Airports.txt")
    print(f"Aeropuertos cargados: {len(lista_prueba)}")
    if lista_prueba:
        PrintAirport(lista_prueba[0])