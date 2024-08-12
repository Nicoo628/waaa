class Ciudadano:
    def __init__(self, id, comunidad, estado='S'):
        self._id = id
        self._comunidad = comunidad
        self._estado = estado  # 'S' para susceptible, 'I' para infectado, 'R' para recuperado
        self.pasos_infectado = 0
        self.contactos = []  # Lista de contactos directos

    @property
    def id(self):
        return self._id

    @property
    def comunidad(self):
        return self._comunidad

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        self._estado = value

    def agregar_contacto(self, contacto):
        if contacto not in self.contactos:
            self.contactos.append(contacto)
