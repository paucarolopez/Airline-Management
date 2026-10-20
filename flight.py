class Flight:
    def __init__(self, flight_id, departure_airport, arrival_airport, departure_time, arrival_time, passengers):
        self.id = flight_id
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.passengers = int(passengers)

def PrintFlight(flight):
    print('ID: ', flight.id, 'From: ', flight.departure_airport, 'To:', flight.arrival_airport, 'Dep.time: ', flight.departure_time, 'Arr.time: ', flight.arrival_time, 'Passengers: ', flight.passengers)

def TimeToMinutes(time):
    parts=time.split(':')
    hours=int(parts[0])
    minutes=int(parts[1])
    total_minutes=(hours*60)+minutes
    return total_minutes

def FlightDuration(flight):
    dep_min=TimeToMinutes(flight.departure_time)
    arr_min=TimeToMinutes(flight.arrival_time)
    duration=arr_min-dep_min
    return duration


def PrintFlights(flights):
    for flight in flights:
        PrintFlight(f)

def AddFlight(flights, flight):
    flights.append(flight)

def RemoveFlight(flights, flight_id):
    for f in flights:
        if f.id == flight_id:
            flights.remove(f)
            return 0
    return -1

def LoadFlights(filename):
    flights = []
    try:
        f=open(filename, 'r')
        for line in f:
            parts=line.strip().split()
            if len(parts)>=6:
                if not parts[5].isdigit():
                    continue
                flight_id=parts[0]
                dep_time=parts[1]
                arr_time=parts[2]
                dep_airport=parts[3]
                arr_airport=parts[4]
                passengers=parts[5]
                flights.append(Flight(flight_id, dep_airport, arr_airport, dep_time, arr_time, passengers))
        f.close()
    except FileNotFoundError:
        return[]
    return flights

def SaveFlights(flights, filename):
    f=open(filename, 'w')
    for fl in flights:
        linea = fl.id + '' + fl.departure_airport + '' + fl.arrival_airport + '' + fl.departure_time + '' + fl.arrival_time + '' + str(fl.passengers) + '\n'
        f.write(linea)
    f.close()

if __name__ == "__main__":
    f1 = Flight("A11", "LEBL", "EGLL", "12:30", "14:30", 135)
    f2 = Flight("A12", "EGLL", "LEBL", "16:30", "18:30", 180)
    lista_vuelos = [f1, f2]

    SaveFlights(lista_vuelos, "Flights.txt")
    vuelos_cargados = LoadFlights("Flights.txt")

    print("Vuelos cargados desde archivo:")
    PrintFlights(vuelos_cargados)