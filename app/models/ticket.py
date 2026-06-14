"""
Módulo que representa un Ticket de soporte dentro del sistema.
"""
from datetime import datetime

class Ticket:
    def __init__(self, id_ticket, creador, categoria, descripcion, prioridad="Media"):
        self.id_ticket = id_ticket
        self.creador = creador
        self.categoria = categoria
        self.descripcion = descripcion

        if prioridad not in ["Baja", "Media", "Alta"]:
            raise ValueError("Prioridad inválida. Use Baja, Media o Alta.")
        self.prioridad = prioridad

        self.estado = "Abierto"
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tecnico_asignado = None
        self.resolucion = ""

    def asignar_tecnico(self, username_tecnico):
        """Asigna el ticket a un miembro del equipo de soporte."""
        self.tecnico_asignado = username_tecnico
        self.estado = "En Progreso"

    def resolver_ticket(self, solucion):
        """Cambia el estado a Resuelto e incluye la solución."""
        if not solucion.strip():
            raise ValueError("La resolución no puede estar vacía.")
        self.resolucion = solucion
        self.estado = "Resuelto"
