import csv
from pathlib import Path
from datetime import datetime
import json

archivo="actividad_2.csv"
DicDias=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
salida = Path("salida")

def leer_excel(arch):
    conjuntos = []
    acceso = Path(arch)

    with acceso.open("r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            fecha_str = fila["timestamp"].strip()
            campeon = fila["campeon"].strip()
            tipo = fila["actividad"].strip()
            coach = fila["entrenador"].strip()

            fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
            conjuntos.append((fecha, campeon, tipo, coach))

    return conjuntos

def analizar_dias(arch):
    dias_por_registro = [r[0].weekday() for r in arch]
    contador_por_dia = {}
    for dia in dias_por_registro:
        if dia in contador_por_dia:
            contador_por_dia[dia] += 1
        else:
            contador_por_dia[dia] = 1
    max_sesiones = max(contador_por_dia.values())
    dias_mas = [d for d, c in contador_por_dia.items() if c == max_sesiones]
    dias=[DicDias[d] for d in dias_mas]
    return dias

def analizar_periodo(arch):
    fechas = sorted(r[0].date() for r in arch)
    primer = min(fechas)
    ultimo = max(fechas)
    periodo = (ultimo - primer).days
    return periodo

def mas_entrenamiento(arch):
    conteo = {}
    for r in arch:
        campeon = r[1]
        if campeon in conteo:
            conteo[campeon] += 1
        else:
            conteo[campeon] = 1
    campeon_top = None
    campeon_top_count = 0
    for campeon, cantidad in conteo.items():
        if cantidad > campeon_top_count:
            campeon_top = campeon
            campeon_top_count = cantidad
    return campeon_top, campeon_top_count

def entrenamientos_semanales(arch, dias_totales):
    contador_por_dia = {}
    for r in arch:
        dia = r[0].weekday()
        contador_por_dia[dia] = contador_por_dia.get(dia, 0) + 1
    semanas = round(dias_totales / 7)
    if semanas == 0:
        semanas = 1
    promedio = []
    for dia, cantidad in contador_por_dia.items():
        dia_nombre = DicDias[dia]
        prom = cantidad / semanas
        promedio.append((dia_nombre, prom))
    return promedio

def finde_semana(arch):
    conteo = {}
    for r in arch:
        campeon = r[1]
        dia = r[0].weekday()
        if dia ==5 or dia==6:
            if campeon in conteo:
                conteo[campeon] += 1
            else:
                conteo[campeon] = 1
    campeon_top = None
    campeon_top_count = 0
    for campeon, cantidad in conteo.items():
        if cantidad > campeon_top_count:
            campeon_top = campeon
            campeon_top_count = cantidad
    return campeon_top, campeon_top_count

def campeones(arch):
    conteo = {}
    for r in arch:
        campeon = r[1]
        if campeon in conteo:
            conteo[campeon] += 1
        else:
            conteo[campeon] = 1
    conteoCampeones = dict(conteo)
    return conteoCampeones

def escribir_csv_campeones(conteo_por_campeon, salida_path):
    """
    8) Genera un CSV (campeon,cantidad) en la carpeta salida.
    """
    salida_path = Path(salida_path)
    salida_path.parent.mkdir(parents=True, exist_ok=True)
    with salida_path.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(["campeon", "cantidad"])
        for campeon, cantidad in sorted(conteo_por_campeon.items(), key=lambda x: (-x[1], x[0])):
            escritor.writerow([campeon, cantidad])

def entrenamientos_y_json(arch, salida_path):
    """
    Genera un JSON con:
    - total de registros
    - primer y último día
    - por día los campeones y cuántas veces entrenó cada uno
    """
    agrupado_por_dia = {}  # diccionario normal
    for fecha, campeon, _, _ in arch:
        dia = fecha.weekday()
        if dia not in agrupado_por_dia:
            agrupado_por_dia[dia] = []
        agrupado_por_dia[dia].append(campeon)

    # Contar entrenamientos por día y campeon
    resumen_por_dia = {}
    for dia, campeones in agrupado_por_dia.items():
        conteo = {}
        for campeon in campeones:
            if campeon in conteo:
                conteo[campeon] += 1
            else:
                conteo[campeon] = 1
        resumen_por_dia[DicDias[dia]] = conteo

    # Fechas
    fechas = sorted([r[0].date() for r in arch])
    primer = fechas[0]
    ultimo = fechas[-1]

    # Crear diccionario final
    resumen_json = {
        "total_registros": len(arch),
        "primer_registro": str(primer),
        "ultimo_registro": str(ultimo),
        "resumen_por_dia": resumen_por_dia
    }

    # Guardar JSON
    salida_path = Path(salida_path)
    salida_path.parent.mkdir(parents=True, exist_ok=True)
    with salida_path.open("w", encoding="utf-8") as f:
        json.dump(resumen_json, f, indent=4, ensure_ascii=False)

    return resumen_json
     

excel=leer_excel(archivo)
dias=analizar_dias(excel)
periodo=analizar_periodo(excel)
preferido,cantidadPref=mas_entrenamiento(excel)
promedio=entrenamientos_semanales(excel,periodo)
campeonfinde,cantidadfinde=finde_semana(excel)

print("Día/s con más sesiones:", dias)
print(f"entre el primer y ultimo dia pasaron {periodo} dias")
print(f"el campeon que más se entreno fue {preferido} con un total de {cantidadPref} entrenamientos")
for dia, prom in promedio:
    print(f"{dia}: {prom:.2f} entrenamientos por semana")
print(f"el campeon que más se entreno los fines de semana fue {campeonfinde} con un total de {cantidadfinde} entrenamientos")

salida.mkdir(exist_ok=True)
csv_path = salida / "entrenamientos.csv"
json_path = salida / "resumen_entrenamientos.json"

escribir_csv_campeones(campeones(excel),csv_path)
entrenamientos_y_json(excel,json_path)