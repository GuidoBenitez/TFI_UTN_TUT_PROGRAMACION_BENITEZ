import math

def resumen(valores):
    """
    Devuelve un diccionario con n, minimo, maximo, promedio y desvio.
    Desvío estándar de la muestra calculado dividiendo por (n-1). Si n=1, el desvío es 0.0[cite: 13].
    """
    if not valores:
        return None
        
    n = len(valores)
    minimo = min(valores)
    maximo = max(valores)
    promedio = sum(valores) / n
    
    if n == 1:
        desvio = 0.0
    else:
        suma_cuadrados = sum((v - promedio) ** 2 for v in valores)
        desvio = math.sqrt(suma_cuadrados / (n - 1))
        
    return {
        "n": n,
        "minimo": minimo,
        "maximo": maximo,
        "promedio": promedio,
        "desvio": desvio
    }

def fuera_de_rango(valores, minimo, maximo):
    """Devuelve las posiciones de los valores que se salen del rango[cite: 13]."""
    fuera = []
    for i, v in enumerate(valores):
        if v < minimo or v > maximo:
            fuera.append(i)
    return fuera

if __name__ == "__main__":
    res = resumen([10.0, 20.0, 30.0])
    assert res["n"] == 3
    assert res["minimo"] == 10.0
    assert res["maximo"] == 30.0
    assert res["promedio"] == 20.0
    
    res_unico = resumen([5.0])
    assert res_unico["desvio"] == 0.0
    
    assert fuera_de_rango([5, 15, 25], 10, 20) == [0, 2]
    print("pruebas 09_estadistica OK")
