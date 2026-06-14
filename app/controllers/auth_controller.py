"""
Controlador encargado de la autenticación de usuarios.
"""
import json
import os
from app.models.usuario import Empleado, SoporteIT

class AuthController:
    def __init__(self, ruta_json="data/usuarios.json"):
        self.ruta_json = ruta_json
        self.usuarios = {}
        self.cargar_usuarios()

    def cargar_usuarios(self):
        """Lee el archivo JSON y reconstruye los objetos Usuario."""
        if not os.path.exists(self.ruta_json) or os.path.getsize(self.ruta_json) == 0:
            self.usuarios = {
                "weylis12": Empleado("weylis12", "secure123", "Weylis Solano"),
                "tecnico_juan": SoporteIT("tecnico_juan", "admin123", "Juan Pérez")
            }
            self.guardar_usuarios()
            return

        with open(self.ruta_json, "r", encoding="utf-8") as f:
            datos = json.load(f)
            for username, info in datos.items():
                if info["rol"] == "Empleado":
                    self.usuarios[username] = Empleado(username, info["password"], info["nombre"])
                elif info["rol"] == "SoporteIT":
                    self.usuarios[username] = SoporteIT(username, info["password"], info["nombre"])

    def guardar_usuarios(self):
        """Guarda el diccionario de usuarios en el archivo JSON."""
        datos_a_guardar = {}
        for username, u in self.usuarios.items():
            password_secreta = u._Usuario__password if hasattr(u, "_Usuario__password") else "123"
            datos_a_guardar[username] = {
                "password": password_secreta,
                "nombre": u.nombre,
                "rol": u.rol
            }
        os.makedirs(os.path.dirname(self.ruta_json), exist_ok=True)
        with open(self.ruta_json, "w", encoding="utf-8") as f:
            json.dump(datos_a_guardar, f, indent=4, ensure_ascii=False)

    def iniciar_sesion(self, username, password):
        """Valida credenciales y retorna el objeto Usuario o None."""
        if username in self.usuarios:
            usuario = self.usuarios[username]
            if usuario.verificar_password(password):
                return usuario
        return None
