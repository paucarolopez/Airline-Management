import matplotlib.pyplot as plt
from aircraft import Aircraft, LoadAircraft
from flight import Flight, LoadFlights, TimeToMinutes

class Airline:
    def __init__ (self, name, fleet, operations):
        self.name = name
        self.fleet = fleet
        self.operations = operations

def PrintAirline(airline):
    print('===AIRLINE: ', airline.name, '===')
    print('---FLEET---')
    for aircraft in airline.fleet:
        print('Callsign: ', aircraft.callsign, 'Type: ', aircraft.type, ' Capacity: ', aircraft.capacity)

    print('---OPERATIONS---')
    for fl in airline.operations:
        print('ID: ', fl.id, 'From: ', fl.departure_airport, 'To: ', fl.arrival_airport, 'Dep.time: ', fl.departure_time, 'Arr.time: ', fl.arrival_time, 'Passengers: ', fl.passengers)

def PlotFlights(airline):
    hourly_counts = [0]*24
    for fl in airline.operations:
        dep_min=TimeToMinutes(fl.departure_time)
        arr_min=TimeToMinutes(fl.arrival_time)

        for hour in range(24):
            hour_start_min=hour*60
            hour_end_min=(hour+1)*60

            if dep_min<hour_end_min and arr_min>hour_start_min:
                hourly_counts[hour]+=1

    hours_labels=[str(h)+':00' for h in range(24)]
    plt.bar(hours_labels, hourly_counts, color='skyblue')
    plt.xlabel('hours of the day')
    plt.ylabel('number of flights on air')
    plt.title('flights on air per hour - ' + airline.name)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    fleet = LoadAircraft("Aircrafts.txt")
    operations = LoadFlights("Operations.txt")  # <--- Cambiado a Operations.txt

    airline = Airline("Vueling", fleet, operations)
    PrintAirline(airline)
    PlotFlights(airline)
