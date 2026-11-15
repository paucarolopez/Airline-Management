class Aircraft:
    def __init__(self, callsign, aircraft_type, capacity, location=None):
        self.callsign = callsign
        self.type = aircraft_type
        self.capacity = int(capacity)
        self.location = location

def PrintAircraft(aircraft):
    print('Callsign:', aircraft.callsign, 'Type:', aircraft.type, 'Capacity:', aircraft.capacity, 'Ubicación:', aircraft.location)

def LoadAircraft(filename):
    aircraft = []
    try:
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()

        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) >= 3:
                callsign = parts[0]
                aircraft_type = parts[1]
                capacity = parts[2]
                avion = Aircraft(callsign, aircraft_type, capacity, location=None)
                aircraft.append(avion)
    except FileNotFoundError:
        print(f"No se encontró el archivo {filename}")
    return aircraft

def LoadInitialPositions(filename, fleet):
    try:
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()

        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) >= 3:
                callsign = parts[0]
                airport = parts[2]
                for avion in fleet:
                    if avion.callsign.upper() == callsign.upper():
                        avion.location = airport.upper()
    except FileNotFoundError:
        print(f"No se encontró el archivo de posiciones {filename}")