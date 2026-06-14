"""
Vista de Reporte — muestra el gráfico de estados de tickets dentro de una ventana tkinter.
Usa matplotlib integrado con tkinter mediante FigureCanvasTkAgg.
"""
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


AZUL_OSCURO = "#1a2332"
AZUL_MEDIO  = "#243447"
BLANCO      = "#f0f4ff"
GRIS_TEXTO  = "#8fa3bf"


class ReporteView:
    """
    Ventana emergente que muestra el gráfico de desempeño de soporte.
    Se abre desde el panel de Soporte IT.
    """

    def mostrar_grafico(self, parent, tickets):
        """
        Crea una ventana Toplevel con el gráfico de barras integrado.
        
        Args:
            parent: ventana padre (la de soporte IT)
            tickets: lista de objetos Ticket para graficar
        """
        ventana = tk.Toplevel(parent)
        ventana.title("Reporte de Desempeño — Soporte IT")
        ventana.geometry("560x440")
        ventana.configure(bg=AZUL_OSCURO)
        ventana.resizable(False, False)

        tk.Label(ventana, text="📊 Estado de Tickets",
                 font=("Segoe UI", 14, "bold"), bg=AZUL_OSCURO, fg=BLANCO).pack(pady=(16, 4))

        # Contar estados
        estados = {"Abierto": 0, "En Progreso": 0, "Resuelto": 0}
        for t in tickets:
            if t.estado in estados:
                estados[t.estado] += 1

        # Crear figura de matplotlib
        fig, ax = plt.subplots(figsize=(5.2, 3.4))
        fig.patch.set_facecolor("#243447")
        ax.set_facecolor("#1a2332")

        colores = ["#e74c3c", "#f39c12", "#2ecc71"]
        barras = ax.bar(estados.keys(), estados.values(), color=colores, width=0.5)

        # Etiquetas encima de cada barra
        for barra in barras:
            altura = barra.get_height()
            ax.text(barra.get_x() + barra.get_width() / 2, altura + 0.05,
                    str(int(altura)), ha="center", va="bottom",
                    color="#f0f4ff", fontsize=11, fontweight="bold")

        ax.set_title("Desempeño de Soporte IT", color=BLANCO, fontsize=12, fontweight="bold", pad=10)
        ax.set_ylabel("Tickets", color=GRIS_TEXTO)
        ax.tick_params(colors=BLANCO)
        ax.spines[:].set_color("#243447")
        ax.yaxis.label.set_color(GRIS_TEXTO)

        # Total de tickets como subtítulo
        total = sum(estados.values())
        ax.set_xlabel(f"Total de incidencias registradas: {total}", color=GRIS_TEXTO, fontsize=9)

        # Incrustar figura en tkinter
        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=16, pady=(0, 16))

        plt.close(fig)

    def mostrar_notificacion_generando(self, parent):
        """Mensaje temporal mientras se genera el reporte."""
        messagebox.showinfo("Generando reporte", "Calculando estadísticas...", parent=parent)

    def mostrar_error(self, mensaje, parent):
        messagebox.showerror("Error en reporte", mensaje, parent=parent)
