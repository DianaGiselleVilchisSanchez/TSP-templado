from flask import Flask, request, jsonify, send_from_directory
import math
import random
import os

app = Flask(__name__, static_folder='static')

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta) - 1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i + 1]
        total += distancia(coord[ciudad1], coord[ciudad2])
    return total

def simulated_annealing(ruta, coord, T, T_MIN, V_enfriamiento):
    while T > T_MIN:
        dist_actual = evalua_ruta(ruta, coord)
        for _ in range(V_enfriamiento):
            i = random.randint(1, len(ruta) - 2)  # No mover origen/destino
            j = random.randint(1, len(ruta) - 2)
            while j == i:
                j = random.randint(1, len(ruta) - 2)

            ruta_tmp = ruta[:]
            ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]

            dist_nueva = evalua_ruta(ruta_tmp, coord)
            delta = dist_actual - dist_nueva

            if dist_nueva < dist_actual or random.random() < math.exp(delta / T):
                ruta = ruta_tmp[:]
                break
        T -= 0.005
    return ruta

coord = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754472859146, -103.34625354877137),
    'Monterrey': (25.69161110159454, -100.321838480256),
    'QuintanaRoo': (21.163111924844458, -86.80231502121464),
    'Michohacan': (19.701400113725654, -101.20829680213464),
    'Aguascalientes': (21.87641043660486, -102.26438663286967),
    'CDMX': (19.432713075976878, -99.13318344772986),
    'QRO': (20.59719437542255, -100.38667040246602)
}

@app.route("/")
def index():
    return send_from_directory('static', 'index.html')

@app.route("/optimizar", methods=["POST"])
def optimizar():
    data = request.get_json()
    origen = data["origen"]
    destino = data["destino"]
    T = float(data["temperatura"])
    T_MIN = float(data["minima"])
    V_enfriamiento = int(data["velocidad"])

    if origen not in coord or destino not in coord:
        return jsonify({"error": "Ciudad de origen o destino no válida"}), 400

    # Crear lista de ciudades sin origen y destino
    intermedias = [c for c in coord.keys() if c != origen and c != destino]
    random.shuffle(intermedias)

    ruta = [origen] + intermedias + [destino]
    ruta_optimizada = simulated_annealing(ruta, coord, T, T_MIN, V_enfriamiento)

    # Asegurar que la ruta empieza en origen y termina en destino
    if ruta_optimizada[0] != origen:
        ruta_optimizada.remove(origen)
        ruta_optimizada.insert(0, origen)
    if ruta_optimizada[-1] != destino:
        ruta_optimizada.remove(destino)
        ruta_optimizada.append(destino)

    distancia_total = evalua_ruta(ruta_optimizada, coord)

    return jsonify({
        "ruta": ruta_optimizada,
        "distancia": round(distancia_total, 2)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
