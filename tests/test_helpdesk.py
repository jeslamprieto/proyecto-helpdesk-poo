"""
Pruebas del sistema Help Desk con pytest.
Incluye pruebas válidas e inválidas según lo pedido por el profesor.
"""
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.models.ticket import Ticket
from app.models.usuario import Empleado, SoporteIT


# ── Pruebas válidas ────────────────────────────────────────────────────────

def test_crear_ticket_valido():
    """Un ticket debe crearse correctamente con los datos esperados."""
    t = Ticket(1, "weylis12", "Redes", "No tengo acceso a internet", "Alta")
    assert t.id_ticket == 1
    assert t.creador == "weylis12"
    assert t.estado == "Abierto"
    assert t.prioridad == "Alta"


def test_asignar_tecnico_cambia_estado():
    """Al asignar un técnico, el estado debe cambiar a 'En Progreso'."""
    t = Ticket(2, "weylis12", "Software", "El sistema no abre", "Media")
    t.asignar_tecnico("tecnico_juan")
    assert t.tecnico_asignado == "tecnico_juan"
    assert t.estado == "En Progreso"


def test_resolver_ticket_valido():
    """Al resolver un ticket con solución, el estado debe ser 'Resuelto'."""
    t = Ticket(3, "weylis12", "Hardware", "Teclado dañado", "Baja")
    t.asignar_tecnico("tecnico_juan")
    t.resolver_ticket("Se reemplazó el teclado por uno nuevo.")
    assert t.estado == "Resuelto"
    assert t.resolucion != ""


def test_verificar_password_correcto():
    """Un usuario debe poder verificar su contraseña correctamente."""
    emp = Empleado("weylis12", "secure123", "Weylis Solano")
    assert emp.verificar_password("secure123") is True


def test_verificar_password_incorrecto():
    """Una contraseña incorrecta debe retornar False."""
    emp = Empleado("weylis12", "secure123", "Weylis Solano")
    assert emp.verificar_password("wrongpass") is False


# ── Prueba inválida ────────────────────────────────────────────────────────

def test_prioridad_invalida_lanza_error():
    """Crear un ticket con prioridad inválida debe lanzar ValueError."""
    with pytest.raises(ValueError):
        Ticket(4, "weylis12", "Redes", "Problema de red", "Urgente")


def test_resolver_sin_solucion_lanza_error():
    """Resolver un ticket con solución vacía debe lanzar ValueError."""
    t = Ticket(5, "weylis12", "Software", "App colgada", "Media")
    with pytest.raises(ValueError):
        t.resolver_ticket("   ")
