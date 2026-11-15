class Flight:
    def __init__(self, id, departure_airport, arrival_airport, departure_time, arrival_time, passengers,
                 assigned_aircraft=None, assigned_aircraft_b=None):
        self.id = str(id).strip()
        self.departure_airport = departure_airport.strip().upper()
        self.arrival_airport = arrival_airport.strip().upper()
        self.departure_time = departure_time.strip()
        self.arrival_time = arrival_time.strip()
        self.passengers = int(passengers)
        self.assigned_aircraft = assigned_aircraft
        self.assigned_aircraft_b = assigned_aircraft_b


def TimeToMinutes(time_str):
    """Convierte una cadena de hora formato 'HH:MM' a minutos totales desde las 00:00."""
    try:
        parts = time_str.strip().split(":")
        return int(parts[0]) * 60 + int(parts[1])
    except (ValueError, IndexError):
        return 0


def PrintFlight(flight):
    print(
        f"Flight ID: {flight.id}, From: {flight.departure_airport} to {flight.arrival_airport}, Dep: {flight.departure_time}, Arr: {flight.arrival_time}, Pax: {flight.passengers}")


def LoadFlights(filename):
    flights = []
    try:
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()

        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) >= 6:
                flight_id = parts[0]
                departure_time = parts[1]
                arrival_time = parts[2]
                departure_airport = parts[3]
                arrival_airport = parts[4]
                passengers = parts[5]

                flight_obj = Flight(flight_id, departure_airport, arrival_airport, departure_time, arrival_time,
                                    passengers)
                flights.append(flight_obj)
    except FileNotFoundError:
        print(f"No se encontró el archivo {filename}")
    return flights