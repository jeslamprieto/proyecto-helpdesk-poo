"""
Controlador encargado de la gestión y persistencia de los tickets.
"""
import json
import os
from app.models.ticket import Ticket

class TicketController:
    def __init__(self, ruta_json="data/tickets.json"):
        self.ruta_json = ruta_json
        self.tickets = []
        self.cargar_tickets()

    def cargar_tickets(self):
        """Carga e instancia los objetos Ticket desde el archivo JSON."""
        if not os.path.exists(self.ruta_json) or os.path.getsize(self.ruta_json) == 0:
            self.tickets = []
            return

        with open(self.ruta_json, "r", encoding="utf-8") as f:
            datos = json.load(f)
            self.tickets = []
            for t in datos:
                ticket = Ticket(
                    id_ticket=t["id_ticket"],
                    creador=t["creador"],
                    categoria=t["categoria"],
                    descripcion=t["descripcion"],
                    prioridad=t["prioridad"]
                )
                ticket.estado = t["estado"]
                ticket.tecnico_asignado = t["tecnico_asignado"]
                ticket.resolucion = t["resolucion"]
                ticket.fecha_creacion = t["fecha_creacion"]
                self.tickets.append(ticket)

    def guardar_tickets(self):
        """Convierte la lista de Tickets en JSON y los almacena."""
        datos_a_guardar = []
        for t in self.tickets:
            datos_a_guardar.append({
                "id_ticket": t.id_ticket,
                "creador": t.creador,
                "categoria": t.categoria,
                "descripcion": t.descripcion,
                "prioridad": t.prioridad,
                "estado": t.estado,
                "fecha_creacion": t.fecha_creacion,
                "tecnico_asignado": t.tecnico_asignado,
                "resolucion": t.resolucion
            })
        os.makedirs(os.path.dirname(self.ruta_json), exist_ok=True)
        with open(self.ruta_json, "w", encoding="utf-8") as f:
            json.dump(datos_a_guardar, f, indent=4, ensure_ascii=False)

    def crear_nuevo_ticket(self, creador, categoria, descripcion, prioridad="Media"):
        """Instancia un nuevo ticket con ID correlativo y lo persiste."""
        nuevo_id = len(self.tickets) + 1
        nuevo_ticket = Ticket(nuevo_id, creador, categoria, descripcion, prioridad)
        self.tickets.append(nuevo_ticket)
        self.guardar_tickets()
        return nuevo_ticket

    def listar_tickets_por_usuario(self, username):
        """Retorna únicamente los tickets creados por un empleado específico."""
        return [t for t in self.tickets if t.creador == username]

    def listar_todos_los_tickets(self):
        """Retorna la lista completa de tickets (uso de Soporte IT)."""
        return self.tickets
