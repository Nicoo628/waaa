class Enfermedad:
    def __init__(self, infeccion_probable, recuperacion_probable):
        self._infeccion_probable = infeccion_probable
        self._recuperacion_probable = recuperacion_probable

    @property
    def infeccion_probable(self):
        return self._infeccion_probable

    @infeccion_probable.setter
    def infeccion_probable(self, value):
        self._infeccion_probable = value

    @property
    def recuperacion_probable(self):
        return self._recuperacion_probable

    @recuperacion_probable.setter
    def recuperacion_probable(self, value):
        self._recuperacion_probable = value
