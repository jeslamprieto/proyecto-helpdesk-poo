"""
Controlador encargado de generar reportes estadísticos con matplotlib.
"""
import os
import matplotlib.pyplot as plt

class ReporteController:
    def __init__(self, ticket_controller):
        self.ticket_controller = ticket_controller

    def generar_grafico_estados(self, ruta_guardado="docs/capturas/reporte_estados.png"):
        """Genera y guarda un gráfico de barras del estado de los tickets."""
        tickets = self.ticket_controller.listar_todos_los_tickets()

        estados = {"Abierto": 0, "En Progreso": 0, "Resuelto": 0}
        for t in tickets:
            if t.estado in estados:
                estados[t.estado] += 1

        fig, ax = plt.subplots(figsize=(6, 4))
        colores = ["#e74c3c", "#f39c12", "#2ecc71"]
        ax.bar(estados.keys(), estados.values(), color=colores)
        ax.set_title("Desempeño de Soporte IT - Estado de Tickets", fontsize=12, fontweight='bold')
        ax.set_ylabel("Cantidad de Incidencias")
        ax.set_xlabel("Estados de las Solicitudes")

        os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)
        plt.savefig(ruta_guardado, bbox_inches='tight')
        plt.close()
        return ruta_guardado
