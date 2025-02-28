import tkinter as tk
from tkinter import ttk, messagebox
import api

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consulta de Casos COVID-19")
        self.geometry("800x500")  # Ajustado para mayor comodidad
        self.resizable(True, True)  # Permitir ajuste dinámico

        # Configurar filas y columnas para expandirse
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Etiquetas y entradas
        ttk.Label(self, text="Departamento:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.departamento_entry = ttk.Entry(self)
        self.departamento_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(self, text="Número de registros:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.limite_entry = ttk.Entry(self)
        self.limite_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Botón de consulta
        self.consulta_btn = ttk.Button(self, text="Consultar", command=self.consultar_datos)
        self.consulta_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Tabla para mostrar los resultados
        columnas = ("Ciudad", "Departamento", "Edad", "Tipo", "Estado", "País de procedencia")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings")
        
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)
        
        self.tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def actualizar_tabla(self, df):
        """Limpia y actualiza la tabla con los nuevos datos."""
        # Limpiar filas anteriores
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar nuevos datos
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    def consultar_datos(self):
        """Obtiene los datos desde la API y los muestra en la tabla."""
        departamento = self.departamento_entry.get().strip()
        limite = self.limite_entry.get().strip()

        if not departamento or not limite.isdigit():
            messagebox.showerror("Error", "Ingrese un departamento válido y un número de registros.")
            return

        limite = int(limite)
        if limite > 1000:
            messagebox.showwarning("Advertencia", "El número máximo recomendado es 1000 registros.")
            return

        df = api.obtener_datos(departamento, limite)  # Obtener datos desde la API
        if df.empty:
            messagebox.showwarning("Sin resultados", "No se encontraron datos para la consulta.")
        else:
            self.actualizar_tabla(df)


def iniciar_ui():
    app = App()
    app.mainloop()