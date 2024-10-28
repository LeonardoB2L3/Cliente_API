import tkinter as tk
from tkinter import ttk
from tkinter import *
import requests
import pandas as pd

def Filtrar():
    """Filtra los datos según la magnitud mínima ingresada"""
    try:
        magnitud_minima = float(Captura.get())
    except ValueError:
        print("Introduce una magnitud válida")
        return

    df_terremotos_filtrados = ObtenerTerremotos(magnitud_minima)
    ActualizarTabla(df_terremotos_filtrados)

def ObtenerTerremotos(min_magnitude=0):
    URL = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-01-02&minmagnitude={min_magnitude}"
    response = requests.get(URL)
    data = response.json()
    terremotos = data['features']
    
    lista_terremotos = []
    for terremoto in terremotos:
        props = terremoto['properties']
        place = props['place']
        mag = props['mag']
        lista_terremotos.append({
            'place': place,
            'mag': mag,
        })

    df = pd.DataFrame(lista_terremotos)
    return df

def ActualizarTabla(df):
    """Limpia y actualiza la tabla con nuevos datos"""
    for row in tree.get_children():
        tree.delete(row)

    # Insertar los nuevos datos en la tabla
    for index, row in df.iterrows():
        tree.insert("", "end", values=(row['place'], row['mag']))

def IniciarInformacion():
    """Carga los datos de terremotos al iniciar"""
    dfTerremotos = ObtenerTerremotos()  # Obtener terremotos con magnitud mínima 0
    ActualizarTabla(dfTerremotos)


# Crear ventana
Ventana = tk.Tk()
Ventana.resizable(0, 0)  # Impide redimensionar la ventana
Ventana.geometry("600x350")  # Tamaño de la ventana
Ventana.title("Terremotos")

# Variables
Captura = StringVar()

# Etiqueta
Titulo = Label(Ventana, text="Informacion de Terremotos", font=("Arial", 16))
Titulo.pack(pady=5)  # Espacio arriba y abajo de la etiqueta

# Crear un frame para alinear los widgets horizontalmente
frame_filtro = Frame(Ventana)
frame_filtro.pack(anchor="w", pady=5, padx=5)  # anchor="w" alinea a la izquierda, `padx/pady` añade espacio

# Etiqueta
TextoFiltrar = Label(frame_filtro, text="Filtrar por magnitud mínima: ", font=("Arial", 10))
TextoFiltrar.pack(side="left")

# Entrada de texto
Entrada = Entry(frame_filtro, textvariable=Captura, width=20)
Entrada.pack(side="left", padx=10)

# Botón
Boton = Button(frame_filtro, text="Filtrar", command=Filtrar)
Boton.pack(side="left")

# Crear el marco principal para contener los widgets
frame = tk.Frame(Ventana)
frame.pack(padx=10, pady=10)

# Crear un árbol (treeview) para mostrar los datos en forma de tabla
global tree
tree = ttk.Treeview(frame, columns=("place", "mag"), show="headings")
tree.heading("place", text="Lugar")
tree.heading("mag", text="Magnitud")
tree.pack(padx=10, pady=10)

# Iniciar los datos antes del bucle principal
IniciarInformacion()

# Bucle principal
Ventana.mainloop()

