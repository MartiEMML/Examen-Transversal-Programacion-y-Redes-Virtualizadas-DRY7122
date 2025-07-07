import requests
import urllib.parse

# URLs base
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"

# Tu clave de API de Graphhopper
key = "fca7e935-f032-4713-888e-a143fcc1be4d"

def geocodificar(ciudad, key):
    while ciudad.strip() == "":
        ciudad = input("Por favor, ingrese nuevamente la ciudad: ")

    url = geocode_url + urllib.parse.urlencode({"q": ciudad, "limit": "1", "key": key})
    respuesta = requests.get(url)
    datos = respuesta.json()
    estado = respuesta.status_code

    if estado == 200 and len(datos["hits"]) != 0:
        lat = datos["hits"][0]["point"]["lat"]
        lon = datos["hits"][0]["point"]["lng"]
        nombre = datos["hits"][0]["name"]
        pais = datos["hits"][0].get("country", "")
        estado_region = datos["hits"][0].get("state", "")
        descripcion = f"{nombre}, {estado_region}, {pais}".strip(", ")
        return estado, lat, lon, descripcion
    else:
        print(f"Error ({estado}): No se pudo encontrar la ciudad '{ciudad}'.")
        return estado, None, None, ciudad

# 🚀 INICIO DEL PROGRAMA
while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Medios de transporte disponibles:")
    print("car (auto), bike (bicicleta), foot (a pie)")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    transporte = input("Ingrese un medio de transporte (o 's' para salir): ").lower()

    if transporte in ["s", "salir", "q", "quit"]:
        print("¡Gracias por usar el programa!")
        break

    if transporte not in ["car", "bike", "foot"]:
        print("Medio inválido, se usará 'car' por defecto.")
        transporte = "car"

    origen = input("\nCiudad de Origen en Chile (o 's' para salir): ")
    if origen.lower() == "s":
        break
    estado_o, lat_o, lon_o, desc_o = geocodificar(origen, key)

    destino = input("Ciudad de Destino en Argentina (o 's' para salir): ")
    if destino.lower() == "s":
        break
    estado_d, lat_d, lon_d, desc_d = geocodificar(destino, key)

    if estado_o != 200 or estado_d != 200:
        print("No se pudo completar la geocodificación de alguna ciudad.")
        continue

    print("\n=================================================")
    print(f"Desde {desc_o} hasta {desc_d} en {transporte}")
    print("=================================================")

    puntos = f"&point={lat_o}%2C{lon_o}&point={lat_d}%2C{lon_d}"
    ruta_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": transporte}) + puntos
    r = requests.get(ruta_url)
    datos_ruta = r.json()
    estado_ruta = r.status_code

    if estado_ruta == 200:
        distancia_metros = datos_ruta["paths"][0]["distance"]
        duracion_ms = datos_ruta["paths"][0]["time"]

        km = distancia_metros / 1000
        millas = km / 1.61
        seg = int(duracion_ms / 1000 % 60)
        minutos = int(duracion_ms / 1000 / 60 % 60)
        horas = int(duracion_ms / 1000 / 60 / 60)

        print(f"🛣️ Distancia: {km:.1f} km / {millas:.1f} millas")
        print(f"⏱️ Duración estimada: {horas:02d}:{minutos:02d}:{seg:02d}")
        print("=================================================")
        print("📌 Indicaciones del viaje:")

        for paso in datos_ruta["paths"][0]["instructions"]:
            texto = paso["text"]
            dist = paso["distance"]
            print(f"{texto} ( {dist/1000:.1f} km / {dist/1000/1.61:.1f} millas )")

    else:
        print(f"❌ Error {estado_ruta} en la API de rutas: {datos_ruta.get('message', 'Sin mensaje')}")

    print("=================================================")