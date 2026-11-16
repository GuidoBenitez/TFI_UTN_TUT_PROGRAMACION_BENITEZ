import math

def vrms_teorico(vpp):
    """Calcula el Vrms teórico para una senoide a partir de Vpp[cite: 5, 11]."""
    if vpp is None or vpp < 0:
        return None
    vp = vpp / 2.0
    vrms = vp / math.sqrt(2.0)
    return vrms

def coincide(medido, teorico, tolerancia=0.02):
    """Devuelve True si el valor medido cae dentro de la tolerancia relativa del teórico (2% por defecto)[cite: 11]."""
    if medido is None or teorico is None or teorico == 0:
        return False
    error = abs(medido - teorico) / abs(teorico)
    return error <= tolerancia

def verificar_canal(filas, canal):
    """Busca PKPK y CYCRMS de ese canal en el resultado del barrido y verifica si coinciden[cite: 11]."""
    pkpk = None
    vrms_medido = None
    
    for fila in filas:
        if fila["canal"] == canal:
            if fila["magnitud"] == "PKPK":
                pkpk = fila["valor"]
            elif fila["magnitud"] == "CYCRMS":
                vrms_medido = fila["valor"]
                
    if pkpk is None or vrms_medido is None:
        return {"canal": canal, "coincide": False, "motivo": "Faltan datos"}
        
    teorico = vrms_teorico(pkpk)
    resultado = coincide(vrms_medido, teorico)
    
    return {
        "canal": canal,
        "pkpk": pkpk,
        "vrms_medido": vrms_medido,
        "vrms_teorico": teorico,
        "coincide": resultado
    }

if __name__ == "__main__":
    assert vrms_teorico(2.0) is not None
    assert round(vrms_teorico(2.0), 4) == 0.7071
    assert coincide(0.707, 0.7071, 0.02) is True
    
    # La trampa del ejercicio 7: señal cuadrada de 2V Vpp tiene Vrms = 1.0 V, no senoide (0.707 V)[cite: 12]
    barrido_cuadrada = [
        {"canal": "CH1", "magnitud": "PKPK", "valor": 2.0},
        {"canal": "CH1", "magnitud": "CYCRMS", "valor": 1.0}
    ]
    res_verif = verificar_canal(barrido_cuadrada, "CH1")
    assert res_verif["coincide"] is False
    print("pruebas 07_verificacion OK")
