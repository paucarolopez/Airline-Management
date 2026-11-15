import tkinter as tk
from tkinter import messagebox, ttk

from aircraft import Aircraft, LoadAircraft, LoadInitialPositions
from airline import Airline, PlotFlights, PlotComparisonFlights, PlotAircraftRoute
from flight import Flight, LoadFlights
from airport import LoadAirports, Airport

lista_aviones = LoadAircraft("Aircrafts.txt")
LoadInitialPositions("AircraftInitialPositions_A.txt", lista_aviones)

lista_vuelos = LoadFlights("Operations.txt")
aerolinea = Airline("MiAerolinea", lista_aviones, lista_vuelos)
aerolinea.airports = LoadAirports("Airports.txt")

VERDE_CLARO = "#90EE90"
VERDE_OSCURO = "#2E8B57"
VERDE_LIMA_CLARO = "#E6F9E6"
GRIS_CLARO = "#F0F0F0"

def mostrar_vuelos():
    tabla["columns"] = ("ID", "Salida", "Llegada", "Origen", "Destino", "Pasajeros", "Algoritmo A", "Algoritmo B")
    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center")

    for item in tabla.get_children():
        tabla.delete(item)

    for vuelo in aerolinea.operations:
        avion_a = vuelo.assigned_aircraft if vuelo.assigned_aircraft else "Sin asignar"
        avion_b = vuelo.assigned_aircraft_b if vuelo.assigned_aircraft_b else "Sin asignar"
        tabla.insert("", "end", values=(vuelo.id, vuelo.departure_time, vuelo.arrival_time, vuelo.departure_airport, vuelo.arrival_airport, vuelo.passengers, avion_a, avion_b))

def mostrar_aviones():
    tabla["columns"] = ("Matricula", "Modelo", "Capacidad", "Ubicación")
    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center")

    for item in tabla.get_children():
        tabla.delete(item)

    for avion in aerolinea.fleet:
        tabla.insert("", "end", values=(avion.callsign, avion.type, avion.capacity, avion.location))

def actualizar_tabla_aeropuertos():
    tabla["columns"] = ("ICAO", "Latitude", "Longitude")
    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center")

    for item in tabla.get_children():
        tabla.delete(item)

    for a in aerolinea.airports:
        tabla.insert("", "end", values=(a.icao, a.latitude, a.longitude))

def reiniciar_asignaciones():
    for vuelo in aerolinea.operations:
        vuelo.assigned_aircraft = None
        vuelo.assigned_aircraft_b = None
    mostrar_vuelos()
    messagebox.showinfo("OK", "Asignaciones reseteadas.")

def ventana_anadir_avion():
    v = tk.Toplevel(root)
    v.title("Añadir Avión")
    v.configure(bg=VERDE_LIMA_CLARO)

    tk.Label(v, text="Matrícula:", bg=VERDE_LIMA_CLARO).pack(pady=2)
    c_callsign = tk.Entry(v)
    c_callsign.pack(pady=2)

    tk.Label(v, text="Modelo:", bg=VERDE_LIMA_CLARO).pack(pady=2)
    c_tipo = tk.Entry(v)
    c_tipo.pack(pady=2)

    tk.Label(v, text="Capacidad:", bg=VERDE_LIMA_CLARO).pack(pady=2)
    c_capacidad = tk.Entry(v)
    c_capacidad.pack(pady=2)

    def guardar():
        c = c_callsign.get().strip()
        t = c_tipo.get().strip()
        cap = c_capacidad.get().strip()
        if c != "" and t != "" and cap.isdigit():
            aerolinea.fleet.append(Aircraft(c, t, cap, location=None))
            mostrar_aviones()
            messagebox.showinfo("OK", "Avión guardado.")
            v.destroy()
        else:
            messagebox.showerror("Error", "Datos no válidos.")

    tk.Button(v, text="Guardar", command=guardar, bg=VERDE_CLARO, width=12).pack(pady=10)

def ventana_eliminar_avion():
    v = tk.Toplevel(root)
    v.title("Eliminar Avión")
    v.configure(bg=VERDE_LIMA_CLARO)

    tk.Label(v, text="Matrícula a borrar:", bg=VERDE_LIMA_CLARO).pack(pady=5)
    c_borrar = tk.Entry(v)
    c_borrar.pack(pady=5)

    def borrar():
        mat = c_borrar.get().strip().upper()
        encontrado = False
        for avion in aerolinea.fleet:
            if avion.callsign.strip().upper() == mat:
                aerolinea.fleet.remove(avion)
                encontrado = True
                break
        if encontrado:
            mostrar_aviones()
            messagebox.showinfo("OK", "Avión borrado.")
            v.destroy()
        else:
            messagebox.showerror("Error", "No encontrado.")

    tk.Button(v, text="Borrar", command=borrar, bg=VERDE_CLARO, width=12).pack(pady=10)

def ventana_anadir_vuelo():
    v = tk.Toplevel(root)
    v.title("Añadir Vuelo")
    v.configure(bg=VERDE_LIMA_CLARO)

    tk.Label(v, text="ID Vuelo:", bg=VERDE_LIMA_CLARO).pack(pady=2)
    c_id = tk.Entry(v)
    c_id.pack(pady=2)

    tk.Label(v, text="Hora Salida (HH:MM):", bg=VERDE_LIMA_CLARO).pack(pady=2)
    c_salida = tk.Entry(v)
    c_salida.pack(pady=2)

    tk.Label(v, text="Hora Llegada (HH:MM):", bg=VERDE_LIMA_CLARO).pack(pady=2)
    c_llegada = tk.Entry(v)
    c_llegada.pack(pady=2)

    tk.Label(v, text="Origen:", bg=VERDE_LIMA_CLARO).pack(pady=2)
    c_origen = tk.Entry(v)
    c_origen.pack(pady=2)

    tk.Label(v, text="Destino:", bg=VERDE_LIMA_CLARO).pack(pady=2)
    c_destino = tk.Entry(v)
    c_destino.pack(pady=2)

    tk.Label(v, text="Pasajeros:", bg=VERDE_LIMA_CLARO).pack(pady=2)
    c_pasajeros = tk.Entry(v)
    c_pasajeros.pack(pady=2)

    def guardar():
        v_id = c_id.get().strip()
        s = c_salida.get().strip()
        ll = c_llegada.get().strip()
        o = c_origen.get().strip()
        d = c_destino.get().strip()
        p = c_pasajeros.get().strip()

        if v_id != "" and p.isdigit():
            aerolinea.operations.append(Flight(v_id, o, d, s, ll, p))
            mostrar_vuelos()
            messagebox.showinfo("OK", "Vuelo guardado.")
            v.destroy()
        else:
            messagebox.showerror("Error", "Datos no válidos.")

    tk.Button(v, text="Guardar", command=guardar, bg=VERDE_CLARO, width=12).pack(pady=10)

def ventana_eliminar_vuelo():
    v = tk.Toplevel(root)
    v.title("Eliminar Vuelo")
    v.configure(bg=VERDE_LIMA_CLARO)

    tk.Label(v, text="ID del vuelo a borrar:", bg=VERDE_LIMA_CLARO).pack(pady=5)
    c_borrar = tk.Entry(v)
    c_borrar.pack(pady=5)

    def borrar():
        v_id = c_borrar.get().strip()
        encontrado = False
        for vuelo in aerolinea.operations:
            if str(vuelo.id).strip() == v_id:
                aerolinea.operations.remove(vuelo)
                encontrado = True
                break
        if encontrado:
            mostrar_vuelos()
            messagebox.showinfo("OK", "Vuelo borrado.")
            v.destroy()
        else:
            messagebox.showerror("Error", "ID no encontrado.")

    tk.Button(v, text="Borrar", command=borrar, bg=VERDE_CLARO, width=12).pack(pady=10)

def ventana_anadir_aeropuerto():
    v = tk.Toplevel(root)
    v.title("Añadir Aeropuerto")
    v.configure(bg=VERDE_LIMA_CLARO)

    tk.Label(v, text="ICAO:", bg=VERDE_LIMA_CLARO).pack(pady=2)
    c_icao = tk.Entry(v)
    c_icao.pack(pady=2)

    tk.Label(v, text="Latitud:", bg=VERDE_LIMA_CLARO).pack(pady=2)
    c_lat = tk.Entry(v)
    c_lat.pack(pady=2)

    tk.Label(v, text="Longitud:", bg=VERDE_LIMA_CLARO).pack(pady=2)
    c_lon = tk.Entry(v)
    c_lon.pack(pady=2)

    def guardar():
        icao = c_icao.get().strip().upper()
        lat = c_lat.get().strip()
        lon = c_lon.get().strip()
        if not icao or not lat or not lon:
            messagebox.showerror("Error", "Rellena todo.")
            return
        try:
            nuevo = Airport(icao, float(lat), float(lon))
            aerolinea.airports.append(nuevo)
            guardar_aeropuertos()
            actualizar_tabla_aeropuertos()
            messagebox.showinfo("OK", "Aeropuerto guardado.")
            v.destroy()
        except ValueError:
            messagebox.showerror("Error", "Lat y Lon deben ser números.")

    tk.Button(v, text="Guardar", command=guardar, bg=VERDE_CLARO, width=12).pack(pady=10)

def eliminar_aeropuerto():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un aeropuerto.")
        return
    item = tabla.item(seleccion)
    icao_a_borrar = item['values'][0]
    aerolinea.airports = [a for a in aerolinea.airports if a.icao != icao_a_borrar]
    guardar_aeropuertos()
    actualizar_tabla_aeropuertos()
    messagebox.showinfo("OK", "Aeropuerto eliminado.")

def guardar_aeropuertos():
    if not aerolinea.airports:
        return
    f = open("Airports.txt", "w")
    f.write("ICAO LATITUDE LONGITUDE\n")
    for a in aerolinea.airports:
        f.write(f"{a.icao} {a.latitude} {a.longitude}\n")
    f.close()

def guardar_en_archivos():
    if not aerolinea.fleet:
        return
    f1 = open("Aircrafts.txt", "w")
    f1.write("CALLSIGN AC-TYPE SEATS\n")
    for a in aerolinea.fleet:
        f1.write(f"{a.callsign} {a.type} {a.capacity}\n")
    f1.close()

    f2 = open("Operations.txt", "w")
    f2.write("ID TIMD TIMA DEPT ARRV PASS\n")
    for v in aerolinea.operations:
        f2.write(f"{v.id} {v.departure_time} {v.arrival_time} {v.departure_airport} {v.arrival_airport} {v.passengers}\n")
    f2.close()

    guardar_aeropuertos()
    messagebox.showinfo("OK", "¡Datos guardados correctamente en los archivos!")

def ejecutar_algoritmo_a():
    LoadInitialPositions("AircraftInitialPositions_A.txt", aerolinea.fleet)
    aerolinea.ejecutar_algoritmo_a()
    mostrar_vuelos()
    messagebox.showinfo("Algoritmo A", "Ejecutado con éxito.")

def ejecutar_algoritmo_b():
    LoadInitialPositions("AircraftInitialPositions_B.txt", aerolinea.fleet)
    aerolinea.ejecutar_algoritmo_b()
    mostrar_vuelos()
    messagebox.showinfo("Algoritmo B", "Ejecutado con éxito.")

def generar_fin_dia_a():
    aerolinea.guardar_posiciones_fin_dia("AircraftInitialPositions_NextDay_A.txt", algoritmo='A')
    messagebox.showinfo("Fin de Día", "Guardado: AircraftInitialPositions_NextDay_A.txt")

def generar_fin_dia_b():
    aerolinea.guardar_posiciones_fin_dia("AircraftInitialPositions_NextDay_B.txt", algoritmo='B')
    messagebox.showinfo("Fin de Día", "Guardado: AircraftInitialPositions_NextDay_B.txt")

def abrir_grafico_v1():
    PlotFlights(aerolinea)

def abrir_grafico_comparativo():
    PlotComparisonFlights(aerolinea)

def abrir_grafico_ruta():
    v = tk.Toplevel(root)
    v.title("Ver Ruta en Google Earth")
    v.configure(bg=VERDE_LIMA_CLARO)

    tk.Label(v, text="Matrícula del Avión:", bg=VERDE_LIMA_CLARO).pack(pady=5)
    c_mat = tk.Entry(v)
    c_mat.pack(pady=5)

    def mostrar():
        callsign = c_mat.get().strip().upper()
        if callsign:
            PlotAircraftRoute(aerolinea, callsign)
            v.destroy()
        else:
            messagebox.showerror("Error", "Introduce una matrícula.")

    tk.Button(v, text="Abrir Google Earth", command=mostrar, bg=VERDE_CLARO, width=15).pack(pady=10)

root = tk.Tk()
root.title("Airline Management System - Version 2")
root.geometry("1000x620")
root.configure(bg=VERDE_LIMA_CLARO)

# Estilos de la tabla
estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure("Treeview", background=GRIS_CLARO, fieldbackground=GRIS_CLARO, foreground="black", font=("Arial", 10))
estilo.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#D5D8DC", foreground="black")

f_sidebar = tk.Frame(root, bg=VERDE_LIMA_CLARO)
f_sidebar.pack(side="left", fill="y", padx=10, pady=10)

# Menú Aviones
mb_aviones = tk.Menubutton(f_sidebar, text="Aviones ▾", bg=VERDE_OSCURO, fg="white", width=16, relief="raised")
menu_aviones = tk.Menu(mb_aviones, tearoff=0, bg=VERDE_CLARO, activebackground="#76D7C4")
menu_aviones.add_command(label="Ver Aviones", command=mostrar_aviones)
menu_aviones.add_command(label="Añadir Avión", command=ventana_anadir_avion)
menu_aviones.add_command(label="Eliminar Avión", command=ventana_eliminar_avion)
mb_aviones.config(menu=menu_aviones)
mb_aviones.pack(pady=6)

# Menú Vuelos
mb_vuelos = tk.Menubutton(f_sidebar, text="Vuelos ▾", bg=VERDE_OSCURO, fg="white", width=16, relief="raised")
menu_vuelos = tk.Menu(mb_vuelos, tearoff=0, bg=VERDE_CLARO, activebackground="#76D7C4")
menu_vuelos.add_command(label="Ver Vuelos", command=mostrar_vuelos)
menu_vuelos.add_command(label="Añadir Vuelo", command=ventana_anadir_vuelo)
menu_vuelos.add_command(label="Eliminar Vuelo", command=ventana_eliminar_vuelo)
menu_vuelos.add_command(label="Reiniciar Asignaciones", command=reiniciar_asignaciones)
mb_vuelos.config(menu=menu_vuelos)
mb_vuelos.pack(pady=6)

# Menú Aeropuertos
mb_aeropuertos = tk.Menubutton(f_sidebar, text="Aeropuertos ▾", bg=VERDE_OSCURO, fg="white", width=16, relief="raised")
menu_aeropuertos = tk.Menu(mb_aeropuertos, tearoff=0, bg=VERDE_CLARO, activebackground="#76D7C4")
menu_aeropuertos.add_command(label="Ver Aeropuertos", command=actualizar_tabla_aeropuertos)
menu_aeropuertos.add_command(label="Añadir Aeropuerto", command=ventana_anadir_aeropuerto)
menu_aeropuertos.add_command(label="Eliminar Aeropuerto", command=eliminar_aeropuerto)
mb_aeropuertos.config(menu=menu_aeropuertos)
mb_aeropuertos.pack(pady=6)

# Menú Algoritmos
mb_algoritmos = tk.Menubutton(f_sidebar, text="Algoritmos ▾", bg=VERDE_OSCURO, fg="white", width=16, relief="raised")
menu_algoritmos = tk.Menu(mb_algoritmos, tearoff=0, bg=VERDE_CLARO, activebackground="#76D7C4")
menu_algoritmos.add_command(label="Ejecutar Algoritmo A", command=ejecutar_algoritmo_a)
menu_algoritmos.add_command(label="Ejecutar Algoritmo B", command=ejecutar_algoritmo_b)
mb_algoritmos.config(menu=menu_algoritmos)
mb_algoritmos.pack(pady=6)

# Menú Fin de Día
mb_findia = tk.Menubutton(f_sidebar, text="Fin de Día ▾", bg=VERDE_OSCURO, fg="white", width=16, relief="raised")
menu_findia = tk.Menu(mb_findia, tearoff=0, bg=VERDE_CLARO, activebackground="#76D7C4")
menu_findia.add_command(label="Generar Posiciones NextDay A", command=generar_fin_dia_a)
menu_findia.add_command(label="Generar Posiciones NextDay B", command=generar_fin_dia_b)
mb_findia.config(menu=menu_findia)
mb_findia.pack(pady=6)

# Menú Gráficos
mb_graficos = tk.Menubutton(f_sidebar, text="Gráficos ▾", bg=VERDE_OSCURO, fg="white", width=16, relief="raised")
menu_graficos = tk.Menu(mb_graficos, tearoff=0, bg=VERDE_CLARO, activebackground="#76D7C4")
menu_graficos.add_command(label="Ver Gráfico (Versión 1)", command=abrir_grafico_v1)
menu_graficos.add_command(label="Gráfico Comparativo (A vs B)", command=abrir_grafico_comparativo)
menu_graficos.add_command(label="Ver Ruta en Google Earth", command=abrir_grafico_ruta)
mb_graficos.config(menu=menu_graficos)
mb_graficos.pack(pady=6)

# Botón Guardar Cambios
tk.Button(
    f_sidebar,
    text="Guardar Cambios",
    command=guardar_en_archivos,
    bg=VERDE_OSCURO,
    fg="white",
    width=16,
).pack(pady=10)

# Tabla a la derecha
tabla = ttk.Treeview(root, show="headings")
tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

mostrar_vuelos()
root.mainloop()