"""
Módulo que representa un artículo de solución en la Base de Conocimiento.
"""

class ArticuloConocimiento:
    def __init__(self, id_articulo, titulo, categoria, solucion):
        self.id_articulo = id_articulo
        self.titulo = titulo
        self.categoria = categoria
        self.solucion = solucion

    def contiene_palabra_clave(self, palabra):
        """Busca si una palabra clave está en el título o la solución."""
        palabra = palabra.lower()
        return palabra in self.titulo.lower() or palabra in self.solucion.lower()
