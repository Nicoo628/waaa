import pandas as pd
import random

# Lista de nombres y apellidos
nombres = [
    "Juan", "Maria", "Carlos", "Ana", "Pedro", "Laura", "Diego", "Sofia",
    "Luis", "Elena", "Javier", "Marta", "Fernando", "Carmen", "Pablo", "Lucia",
    "Alberto", "Rosa", "Manuel", "Paula", "Ricardo", "Sara", "Enrique", "Clara",
    "Nicolas", "Catalina", "Fabio", "Cristopher", "Danilo", "Cristobal", "Patricio", "Sebastian",
    "Andrea", "Valentina", "Gabriel", "Emilia", "Andres", "Victoria", "Felipe", "Matias",
    "Mariana", "Julian", "Daniela", "Leonardo", "Angela", "Hugo", "Isabel", "Gonzalo",
    "Martina", "Rodrigo", "Renata", "Francisco", "Alicia", "Ignacio", "Camila", "Esteban",
    "Silvia", "Raul", "Teresa", "Marcos", "Luciana", "Eduardo", "Valeria", "Sergio"
]

apellidos = [
    "Perez", "Gomez", "Rodriguez", "Martinez", "Diaz", "Fernandez", "Alvarez",
    "Ruiz", "Torres", "Gutierrez", "Jimenez", "Sanchez", "Lopez", "Morales",
    "Ortega", "Vargas", "Ramos", "Castro", "Romero", "Molina", "Suarez", "Ordoñez",
    "Hernandez", "Garcia", "Rivera", "Vega", "Cortes", "Figueroa", "Acosta", "Mendoza",
    "Vasquez", "Navarro", "Medina", "Reyes", "Castillo", "Soto", "Silva", "Carrasco",
    "Cruz", "Flores", "Moreno", "Herrera", "Rojas", "Sosa", "Lozano", "Guerrero",
    "Paredes", "Miranda", "Castellanos", "Espinoza", "Blanco", "Campos", "Mejia", "Aguilar",
    "Pineda", "Nunez", "Cabrera", "Salazar", "Robles", "Cardenas", "Benitez", "Ferrer"
]

# Generar 2000 nombres y apellidos aleatorios
nombres_aleatorios = random.choices(nombres, k=2000)
apellidos_aleatorios = random.choices(apellidos, k=2000)

# Crear DataFrame de nombres y apellidos combinados
nombres_apellidos_df = pd.DataFrame({
    "nombre": nombres_aleatorios,
    "apellido": apellidos_aleatorios
})

# Escribir los nombres y apellidos en un archivo CSV usando pandas
nombres_apellidos_df.to_csv("nombres_apellidos.csv", index=False)

print("Archivo CSV generado con éxito.")

# Clase para manejar nombres y apellidos
class NombresApellidosManager:
    def __init__(self, archivo_nombres):
        self.df = pd.read_csv(archivo_nombres)  # Cargar nombres y apellidos desde el archivo usando pandas

    def obtener_nombre_apellido(self):
        row = self.df.sample()  # Seleccionar una fila aleatoria del DataFrame
        nombre = row['nombre'].values[0]
        apellido = row['apellido'].values[0]
        return nombre, apellido
