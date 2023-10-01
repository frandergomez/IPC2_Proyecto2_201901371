import tkinter as tk
import os
import webbrowser
from tkinter import ttk, Menu, Text, filedialog, messagebox
import PyPDF2
import xml.etree.ElementTree as ET
import graphviz

# Lista para almacenar los nombres de los drones
lista_drones = []

manuales_dir = "E:\\USAC_2023\\SEGUNDO SEMESTRE\\LAB_IPC2\\IPC2_Proyecto2_#201901371"


# Estructura de ejemplo para los mensajes e instrucciones
mensajes = {
    "Mensaje1": {
        "SistemaDrones": "Sistema 1",
        "Mensaje": "Mensaje de prueba 1",
        "TiempoOptimo": "5 minutos",
        "Instrucciones": ["Instrucción 1", "Instrucción 2", "Instrucción 3"],
    },
    "Mensaje2": {
        "SistemaDrones": "Sistema 2",
        "Mensaje": "Mensaje de prueba 2",
        "TiempoOptimo": "10 minutos",
        "Instrucciones": ["Instrucción 4", "Instrucción 5", "Instrucción 6"],
    },
}

# Funciones para las etiquetas
def mostrar_opciones_archivo():
    archivo_menu.post(label1.winfo_rootx(), label1.winfo_rooty() + label1.winfo_height())

def cargar_archivo():
    archivo_path = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])

    if archivo_path:
        with open(archivo_path, "r") as archivo:
            contenido = archivo.read()
            archivo_text.delete(1.0, tk.END)
            archivo_text.insert(tk.END, contenido)

def guardar_como():
    archivo_guardar = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("Archivos XML", "*.xml")])

    if archivo_guardar:
        try:
            contenido = archivo_text.get(1.0, tk.END)
            
            with open(archivo_guardar, "w") as archivo:
                archivo.write(contenido)

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el archivo: {str(e)}")

def salir():
    ventana2.quit()

def generar_archivo_xml():
    root = ET.Element("Instrucciones")

    # Agregar instrucciones para el sistema de drones 1
    sistema_drones_1 = ET.SubElement(root, "SistemaDrones")
    sistema_drones_1.set("Nombre", "Sistema 1")

    instruccion_1 = ET.SubElement(sistema_drones_1, "Instruccion")
    instruccion_1.text = "Configurar ruta de vuelo"

    instruccion_2 = ET.SubElement(sistema_drones_1, "Instruccion")
    instruccion_2.text = "Enviar mensaje de prueba"

    tiempo_1 = ET.SubElement(sistema_drones_1, "TiempoOptimo")
    tiempo_1.text = "10 minutos"

    # Agregar instrucciones para el sistema de drones 2
    sistema_drones_2 = ET.SubElement(root, "SistemaDrones")
    sistema_drones_2.set("Nombre", "Sistema 2")

    instruccion_3 = ET.SubElement(sistema_drones_2, "Instruccion")
    instruccion_3.text = "Calibrar sensores"

    instruccion_4 = ET.SubElement(sistema_drones_2, "Instruccion")
    instruccion_4.text = "Enviar mensaje de emergencia"

    tiempo_2 = ET.SubElement(sistema_drones_2, "TiempoOptimo")
    tiempo_2.text = "15 minutos"

    tree = ET.ElementTree(root)

    nombre_archivo_salida = "instrucciones_drones.xml"

    try:
        tree.write(nombre_archivo_salida)

        print(f"Archivo XML generado con éxito: {nombre_archivo_salida}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al generar el archivo XML: {str(e)}")

def gestion_drones():
    lista_drones.sort()  # Ordenar la lista alfabéticamente
    mensaje = "\n".join(lista_drones) if lista_drones else "No hay drones registrados."
    messagebox.showinfo("Listado de Drones", mensaje)

# Función para agregar un nuevo dron
def agregar_dron():
    nuevo_dron = entrada_nombre_dron.get().strip()
    if nuevo_dron:
        if nuevo_dron not in lista_drones:
            lista_drones.append(nuevo_dron)
            messagebox.showinfo("Éxito", f"Se ha agregado el dron '{nuevo_dron}' con éxito.")
            entrada_nombre_dron.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"El dron '{nuevo_dron}' ya existe.")
    else:
        messagebox.showerror("Error", "Por favor, ingresa un nombre de dron válido.")

def gestion_mensajes():
    ventana_mensajes = tk.Toplevel(ventana2)
    ventana_mensajes.title("Gestión de Mensajes")

    # Ver listado de mensajes y sus instrucciones
    tabla_mensajes = ttk.Treeview(ventana_mensajes, columns=("Mensaje", "Sistema", "Tiempo Óptimo"), show="headings")
    tabla_mensajes.heading("Mensaje", text="Mensaje")
    tabla_mensajes.heading("Sistema", text="Sistema")
    tabla_mensajes.heading("Tiempo Óptimo", text="Tiempo Óptimo")

    for mensaje, info in mensajes.items():
        sistema = info["SistemaDrones"]
        tiempo_optimo = info["TiempoOptimo"]
        tabla_mensajes.insert("", "end", values=(mensaje, sistema, tiempo_optimo))

    tabla_mensajes.pack()

    # Ver instrucciones para enviar un mensaje
    def mostrar_info_mensaje():
        seleccion = tabla_mensajes.selection()
        if seleccion:
            mensaje_seleccionado = tabla_mensajes.item(seleccion[0], "values")[0]
            info = mensajes.get(mensaje_seleccionado)
            if info:
                sistema = info["SistemaDrones"]
                mensaje = info["Mensaje"]
                tiempo_optimo = info["TiempoOptimo"]
                instrucciones = "\n".join(info["Instrucciones"])

                info_mensaje = f"Nombre del Sistema de Drones: {sistema}\nMensaje: {mensaje}\nTiempo Óptimo: {tiempo_optimo}\nInstrucciones:\n{instrucciones}"
                messagebox.showinfo("Información del Mensaje", info_mensaje)
            else:
                messagebox.showerror("Error", "No se encontró información para el mensaje seleccionado.")

    boton_ver_info = tk.Button(ventana_mensajes, text="Ver Información", command=mostrar_info_mensaje)
    boton_ver_info.pack()

     # Ver gráficamente (utilizando Graphviz) el listado de instrucciones
    def mostrar_diagrama():
        seleccion = tabla_mensajes.selection()
        if seleccion:
            mensaje_seleccionado = tabla_mensajes.item(seleccion[0], "values")[0]
            info = mensajes.get(mensaje_seleccionado)
            if info and "Instrucciones" in info:
                instrucciones = info["Instrucciones"]

                # Crear un diagrama con Graphviz
                dot = graphviz.Digraph(comment="Instrucciones del Mensaje")
                for i, instruccion in enumerate(instrucciones, start=1):
                    dot.node(f"Instrucción {i}", instruccion)

                # Guardar el diagrama en un archivo y abrirlo
                dot.render("instrucciones_diagrama")
                dot.view("instrucciones_diagrama")
            else:
                messagebox.showerror("Error", "No se encontraron instrucciones para el mensaje seleccionado.")

    boton_ver_diagrama = tk.Button(ventana_mensajes, text="Ver Diagrama de Instrucciones", command=mostrar_diagrama)
    boton_ver_diagrama.pack()

def abrir_manual1():
    # Abre el Manual 1 en PDF
    manual1_path = os.path.join(manuales_dir, "ManualUsuario_201901371.pdf")
    webbrowser.open_new(manual1_path)

def abrir_manual2():
    # Abre el Manual 2 en PDF
    manual2_path = os.path.join(manuales_dir, "ManualTecnico_201901371.pdf")
    webbrowser.open_new(manual2_path)

def ayuda():
    ventana_ayuda = tk.Toplevel(ventana2)
    ventana_ayuda.title("Ayuda")

    # Crear botones para abrir los manuales
    boton_manual1 = tk.Button(ventana_ayuda, text="ManualUsuario_201901371", command=abrir_manual1)
    boton_manual1.pack()

    boton_manual2 = tk.Button(ventana_ayuda, text="ManualTecnico_201901371", command=abrir_manual2)
    boton_manual2.pack()

def cambiar_ventana():
    ventana1.destroy()
    ventana2.deiconify()

ventana1 = tk.Tk()
ventana1.title("201901371_Frander_Carreto")

btn_inicializar = tk.Button(ventana1, text="Inicializar", command=cambiar_ventana)
btn_inicializar.pack()
ventana1.geometry("300x150")

ventana2 = tk.Tk()
ventana2.title("201901371_Frander_Carreto")
ventana2.withdraw()

# Crear un menú desplegable para "Archivo"
archivo_menu = Menu(ventana2, tearoff=0)
archivo_menu.add_command(label="Cargar Archivo XML", command=cargar_archivo)
archivo_menu.add_command(label="Guardar como", command=guardar_como)
archivo_menu.add_separator()
archivo_menu.add_command(label="Salir", command=salir)

# Configurar las etiquetas
label1 = tk.Label(ventana2, text="Archivo", cursor="hand2")
label1.bind("<Button-1>", lambda event: mostrar_opciones_archivo())

label2 = tk.Label(ventana2, text="Generar archivo XML", cursor="hand2")
label2.bind("<Button-1>", lambda event: generar_archivo_xml())

label3 = tk.Label(ventana2, text="Gestion de drones", cursor="hand2")
label3.bind("<Button-1>", lambda event: gestion_drones())

label4 = tk.Label(ventana2, text="Gestion de mensajes", cursor="hand2")
label4.bind("<Button-1>", lambda event: gestion_mensajes())

label5 = tk.Label(ventana2, text="Ayuda", cursor="hand2")
label5.bind("<Button-1>", lambda event: ayuda())

# Crear una caja de texto para visualizar y editar archivos XML
archivo_text = Text(ventana2, width=40, height=10) 
archivo_text.pack(fill="both", expand=True)

# Empaquetar las etiquetas horizontalmente
label1.pack(side="left")
label2.pack(side="left")
label3.pack(side="left")
label4.pack(side="left")
label5.pack(side="left")

# Crear campos para gestionar drones
frame_gestion_drones = tk.Frame(ventana2)
frame_gestion_drones.pack()

etiqueta_nombre_dron = tk.Label(frame_gestion_drones, text="Nombre del dron:")
etiqueta_nombre_dron.pack(side="left")

entrada_nombre_dron = tk.Entry(frame_gestion_drones)
entrada_nombre_dron.pack(side="left")

boton_agregar_dron = tk.Button(frame_gestion_drones, text="Agregar Dron", command=agregar_dron)
boton_agregar_dron.pack(side="left")

boton_ver_drones = tk.Button(frame_gestion_drones, text="Ver Drones", command=gestion_drones)
boton_ver_drones.pack(side="left")

ventana2.geometry("600x400")


# Ejecutar la aplicación
ventana1.mainloop()