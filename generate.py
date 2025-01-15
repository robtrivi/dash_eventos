import pandas as pd
import random
import datetime

# Generar datos sintéticos para ventas
eventos = ["Concierto A", "Obra de Teatro B", "Feria C", "Conferencia D", "Exposición E"]
categorias = ["Música", "Teatro", "Cultura", "Educación", "Arte"]
ubicaciones = ["Manta", "Guayaquil", "Cuenca", "Quito", "Ambato"]

# Crear dataset
data_ventas = []
for i in range(500):  # Generar 500 filas de datos
    fecha = datetime.date(2024, random.randint(1, 12), random.randint(1, 28))
    evento = random.choice(eventos)
    categoria = categorias[eventos.index(evento)]
    entradas_vendidas = random.randint(1, 10)
    ubicacion = random.choice(ubicaciones)
    satisfaccion = round(random.uniform(3, 5), 1)  # Escala de 1 a 5
    total = round(entradas_vendidas * random.uniform(20, 100), 2)  # Total en USD
    descuento = round(total * random.uniform(0.05, 0.3), 2)  # Descuento aplicado
    
    data_ventas.append([fecha, evento, categoria, entradas_vendidas, ubicacion, satisfaccion, total, descuento])

df_ventas = pd.DataFrame(data_ventas, columns=["Fecha", "Evento", "Categoría", "Entradas Vendidas", "Ubicación", "Satisfacción", "Total", "Descuento"])

df_ventas.to_csv("ventas_eventos.csv", index=False)
print("Archivo ventas_eventos.csv generado.")


# Generar datos sintéticos para vistas
data_vistas = []
for i in range(1000):  # Generar 1000 filas de datos
    fecha = datetime.date(2024, random.randint(1, 12), random.randint(1, 28))
    id_usuario = f"user_{random.randint(1, 300)}"
    tiempo_visualizacion = random.randint(1, 300)  # En segundos
    ubicacion = random.choice(ubicaciones)

    data_vistas.append([fecha, id_usuario, tiempo_visualizacion, ubicacion])

df_vistas = pd.DataFrame(data_vistas, columns=["Fecha", "ID Usuario", "Tiempo de Visualización", "Ubicación"])
df_vistas.to_csv("vistas_eventos.csv", index=False)
print("Archivo vistas_eventos.csv generado.")
