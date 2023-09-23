import tkinter as tk
from tkinter import Menu, Text

# Funciones para las etiquetas
def mostrar_opciones_archivo():
    archivo_menu.post(label1.winfo_rootx(), label1.winfo_rooty() + label1.winfo_height())

def cargar_archivo():
    # Aquí puedes agregar el código para cargar un archivo XML en la caja de texto
    archivo_text.delete(1.0, tk.END)  # Limpia el contenido existente en la caja de texto
    archivo_text.insert(tk.END, "Aquí va el contenido del archivo XML")  # Inserta el contenido del archivo XML

def guardar_como():
    # Aquí puedes agregar el código para guardar el contenido de la caja de texto como un archivo XML
    contenido = archivo_text.get(1.0, tk.END)  # Obtiene el contenido de la caja de texto
    # Agrega el código para guardar 'contenido' como archivo XML

def salir():
    ventana2.quit()

def generar_archivo_xml():
    # Coloca aquí el código para generar un archivo XML
    pass

def gestion_drones():
    # Coloca aquí el código para gestionar drones
    pass

def gestion_mensajes():
    # Coloca aquí el código para gestionar mensajes
    pass

def ayuda():
    # Coloca aquí el código para mostrar ayuda
    pass

# Función para cambiar de ventana
def cambiar_ventana():
    ventana1.destroy()
    ventana2.deiconify()

# Configurar la primera ventana
ventana1 = tk.Tk()
ventana1.title("Ventana 1")

btn_inicializar = tk.Button(ventana1, text="Inicializar", command=cambiar_ventana)
btn_inicializar.pack()
ventana1.geometry("300x150")

# Configurar la segunda ventana
ventana2 = tk.Tk()
ventana2.title("Ventana 2")
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

# Crear una caja de texto para visualizar y editar archivos XML (reducida a 10 líneas y 40 columnas)
archivo_text = Text(ventana2, width=40, height=10)
archivo_text.pack(fill="both", expand=True)

# Empaquetar las etiquetas horizontalmente
label1.pack(side="left")
label2.pack(side="left")
label3.pack(side="left")
label4.pack(side="left")
label5.pack(side="left")

ventana2.geometry("600x400")

# Ejecutar la aplicación
ventana1.mainloop()
