"""
Controlador de interfaz para el panel de Empleado.
Conecta TicketView con TicketController.
"""

class TicketUIController:
    """
    Orquesta las acciones del panel de Empleado:
    crear tickets y consultar los propios.
    """

    def __init__(self, vista, ticket_controller, username):
        self.vista             = vista
        self.ticket_controller = ticket_controller
        self.username          = username

    def crear_ticket(self):
        """Recoge el formulario, valida y crea el ticket."""
        categoria, descripcion, prioridad = self.vista.obtener_datos_formulario()

        if not descripcion:
            self.vista.mostrar_advertencia("La descripción no puede estar vacía.")
            return

        try:
            nuevo = self.ticket_controller.crear_nuevo_ticket(
                creador=self.username,
                categoria=categoria,
                descripcion=descripcion,
                prioridad=prioridad
            )
            self.vista.mostrar_exito(nuevo.id_ticket)
            self.vista.limpiar_formulario()
            self.cargar_mis_tickets()   # Refrescar tabla

        except ValueError as e:
            self.vista.mostrar_error(str(e))

    def cargar_mis_tickets(self):
        """Carga y muestra los tickets del usuario actual."""
        mis_tickets = self.ticket_controller.listar_tickets_por_usuario(self.username)
        self.vista.mostrar_tickets(mis_tickets)
