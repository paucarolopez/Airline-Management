class Aircraft:
    def __init__(self, callsign, aircraft_type, capacity):
        self.callsign = callsign
        self.type=aircraft_type
        self.capacity=int(capacity)

def PrintAircraft(aircraft):
    print('Callsign: ', aircraft.callsign, 'Type: ', aircraft.type, ' Capacity: ', aircraft.capacity)

def LoadAircraft(filename):
    aircraft = []
    try:
        f = open(filename, 'r')
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                if not parts[2].isdigit():
                    continue
                callsign = parts[0]
                aircraft_type = parts[1]
                capacity = parts[2]
                aircraft.append(Aircraft(callsign, aircraft_type, capacity))
        f.close()
    except FileNotFoundError:
        return[]
    return aircraft