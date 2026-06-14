"""
Módulo que define las entidades de usuarios del sistema Help Desk.
Aplica encapsulamiento y herencia.
"""

class Usuario:
    def __init__(self, username, password, nombre, rol):
        self.username = username
        self.__password = password  # Atributo privado (Encapsulamiento)
        self.nombre = nombre
        self.rol = rol  # 'Empleado' o 'SoporteIT'

    def verificar_password(self, password):
        """Valida si la contraseña ingresada coincide."""
        return self.__password == password


class Empleado(Usuario):
    def __init__(self, username, password, nombre):
        super().__init__(username, password, nombre, rol="Empleado")

    def asignar_ticket(self, ticket):
        """Un empleado no puede asignarse tickets."""
        return "❌ Los empleados no pueden asignarse tickets.", False

    def resolver_ticket(self, ticket, solucion):
        """Un empleado no puede resolver tickets."""
        return "❌ Los empleados no pueden resolver tickets.", False


class SoporteIT(Usuario):
    def __init__(self, username, password, nombre):
        super().__init__(username, password, nombre, rol="SoporteIT")

    def asignar_ticket(self, ticket):
        """Asigna el ticket al técnico actual."""
        if ticket.estado != "Abierto":
            return f"⚠️ El ticket #{ticket.id_ticket} ya está en progreso o resuelto.", False
        ticket.asignar_tecnico(self.username)
        return f"✅ Ticket #{ticket.id_ticket} asignado a {self.nombre}.", True

    def resolver_ticket(self, ticket, solucion):
        """Resuelve el ticket con la solución indicada."""
        if ticket.estado == "Resuelto":
            return f"⚠️ El ticket #{ticket.id_ticket} ya fue resuelto.", False
        ticket.resolver_ticket(solucion)
        return f"✅ Ticket #{ticket.id_ticket} marcado como Resuelto.", True
