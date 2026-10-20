import tkinter as tk
from tkinter import messagebox, ttk

from aircraft import Aircraft, LoadAircraft
from airline import Airline, PlotFlights
from flight import Flight, LoadFlights

# -------------------------------------------------------------
# 1. CARGA DE DATOS
# -------------------------------------------------------------
lista_aviones = LoadAircraft("Aircrafts.txt")
lista_vuelos = LoadFlights("operations.txt")
aerolinea = Airline("MiAerolinea", lista_aviones, lista_vuelos)

VERDE_CLARO = "#90EE90"
VERDE_OSCURO = "#2E8B57"
VERDE_LIMA_CLARO = "#E6F9E6"
GRIS_CLARO = "#F0F0F0"


# -------------------------------------------------------------
# 2. MOSTRAR TABLAS Y GRÁFICO (COLUMNAS UNIFICADAS Y CENTRADAS)
# -------------------------------------------------------------
def mostrar_aviones():
    tabla["columns"] = ("Matricula", "Modelo", "Capacidad")

    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center")

    for elemento in tabla.get_children():
        tabla.delete(elemento)

    for avion in aerolinea.fleet:
        tabla.insert(
            "",
            "end",
            values=(avion.callsign, avion.type, avion.capacity),
        )


def mostrar_vuelos():
    tabla["columns"] = (
        "ID",
        "Salida",
        "Llegada",
        "Origen",
        "Destino",
        "Pasajeros",
    )

    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center")

    for elemento in tabla.get_children():
        tabla.delete(elemento)

    for vuelo in aerolinea.operations:
        tabla.insert(
            "",
            "end",
            values=(
                vuelo.id,
                vuelo.departure_time,
                vuelo.arrival_time,
                vuelo.departure_airport,
                vuelo.arrival_airport,
                vuelo.passengers,
            ),
        )


def abrir_grafico():
    PlotFlights(aerolinea)


# -------------------------------------------------------------
# 3. VENTANAS EMERGENTES
# -------------------------------------------------------------
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
            aerolinea.fleet.append(Aircraft(c, t, cap))
            mostrar_aviones()
            messagebox.showinfo("OK", "Avión guardado correctamente.")
            v.destroy()
        else:
            messagebox.showerror(
                "Error", "Introduce datos válidos y número en capacidad."
            )

    tk.Button(v, text="Guardar", command=guardar, bg=VERDE_CLARO, width=12).pack(
        pady=10
    )


def ventana_eliminar_avion():
    v = tk.Toplevel(root)
    v.title("Eliminar Avión")
    v.configure(bg=VERDE_LIMA_CLARO)

    tk.Label(v, text="Matrícula a borrar:", bg=VERDE_LIMA_CLARO).pack(pady=5)
    c_borrar = tk.Entry(v)
    c_borrar.pack(pady=5)

    def borrar():
        callsign_ingresado = c_borrar.get().strip().upper()

        if not callsign_ingresado:
            messagebox.showerror("Error", "Escribe una matrícula.")
            return

        encontrado = False
        for avion in aerolinea.fleet:
            if avion.callsign.strip().upper() == callsign_ingresado:
                aerolinea.fleet.remove(avion)
                encontrado = True
                break

        if encontrado:
            mostrar_aviones()
            messagebox.showinfo("OK", "Avión borrado correctamente.")
            v.destroy()
        else:
            messagebox.showerror("Error", "Matrícula no encontrada.")

    tk.Button(v, text="Borrar", command=borrar, bg=VERDE_CLARO, width=12).pack(
        pady=10
    )


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
            messagebox.showinfo("OK", "Vuelo guardado correctamente.")
            v.destroy()
        else:
            messagebox.showerror(
                "Error", "Introduce datos válidos y número en pasajeros."
            )

    tk.Button(v, text="Guardar", command=guardar, bg=VERDE_CLARO, width=12).pack(
        pady=10
    )


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
            messagebox.showinfo("OK", "Vuelo borrado correctamente.")
            v.destroy()
        else:
            messagebox.showerror("Error", "ID no encontrado.")

    tk.Button(v, text="Borrar", command=borrar, bg=VERDE_CLARO, width=12).pack(
        pady=10
    )


# -------------------------------------------------------------
# 4. GUARDAR CAMBIOS EN FICHEROS .TXT
# -------------------------------------------------------------
def guardar_en_archivos():
    f1 = open("Aircrafts.txt", "w")
    f1.write("CALLSIGN TYPE SEATS\n")
    for a in aerolinea.fleet:
        f1.write(f"{a.callsign} {a.type} {a.capacity}\n")
    f1.close()

    f2 = open("Operations.txt", "w")
    f2.write("ID TIMD TIMA DEPT ARRV PASS\n")
    for v in aerolinea.operations:
        f2.write(
            f"{v.id} {v.departure_time} {v.arrival_time} {v.departure_airport} {v.arrival_airport} {v.passengers}\n"
        )
    f2.close()

    messagebox.showinfo("Guardado", "Cambios guardados en los archivos .txt")


# -------------------------------------------------------------
# 5. VENTANA PRINCIPAL Y ESTILOS
# -------------------------------------------------------------
root = tk.Tk()
root.title("Airline Management System")
root.geometry("800x500")
root.configure(bg=VERDE_LIMA_CLARO)

# Estilo unificado para la tabla de datos
estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure(
    "Treeview",
    background=GRIS_CLARO,
    fieldbackground=GRIS_CLARO,
    foreground="black",
    font=("Arial", 10),
)
estilo.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold"),
    background="#D5D8DC",
    foreground="black",
)

# Panel lateral
f_sidebar = tk.Frame(root, bg=VERDE_LIMA_CLARO)
f_sidebar.pack(side="left", fill="y", padx=10, pady=10)

mb_aviones = tk.Menubutton(
    f_sidebar,
    text="Aviones ▾",
    bg=VERDE_OSCURO,
    fg="white",
    width=15,
    relief="raised",
)
menu_aviones = tk.Menu(
    mb_aviones, tearoff=0, bg=VERDE_CLARO, activebackground="#76D7C4"
)
menu_aviones.add_command(label="Ver Aviones", command=mostrar_aviones)
menu_aviones.add_command(label="Añadir Avión", command=ventana_anadir_avion)
menu_aviones.add_command(label="Eliminar Avión", command=ventana_eliminar_avion)
mb_aviones.config(menu=menu_aviones)
mb_aviones.pack(pady=8)

mb_vuelos = tk.Menubutton(
    f_sidebar,
    text="Vuelos ▾",
    bg=VERDE_OSCURO,
    fg="white",
    width=15,
    relief="raised",
)
menu_vuelos = tk.Menu(
    mb_vuelos, tearoff=0, bg=VERDE_CLARO, activebackground="#76D7C4"
)
menu_vuelos.add_command(label="Ver Vuelos", command=mostrar_vuelos)
menu_vuelos.add_command(label="Añadir Vuelo", command=ventana_anadir_vuelo)
menu_vuelos.add_command(label="Eliminar Vuelo", command=ventana_eliminar_vuelo)
mb_vuelos.config(menu=menu_vuelos)
mb_vuelos.pack(pady=8)

tk.Button(
    f_sidebar,
    text="Ver Gráfico",
    command=abrir_grafico,
    bg=VERDE_OSCURO,
    fg="white",
    width=15,
).pack(pady=8)

tk.Button(
    f_sidebar,
    text="Guardar Cambios",
    command=guardar_en_archivos,
    bg=VERDE_OSCURO,
    fg="white",
    width=15,
).pack(pady=8)

# Tabla única limpia sin divisiones visuales extra
tabla = ttk.Treeview(root, show="headings")
tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

mostrar_aviones()

root.mainloop()