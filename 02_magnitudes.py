def a_numero(texto):
    """Convierte un texto en notación científica a número flotante[cite: 8]. Devuelve None si falla."""
    if not isinstance(texto, str):
        return None
    try:
        return float(texto.strip())
    except ValueError:
        return None

def con_unidad(valor, unidad):
    """
    Convierte un valor numérico y su unidad base a una cadena legible con prefijo SI (1 a 999)[cite: 8, 9].
    """
    if valor is None:
        return None
        
    if valor == 0.0:
        return f"0 {unidad}"
        
    prefijos = [
        (1e-12, "p"),
        (1e-9, "n"),
        (1e-6, "u"),
        (1e-3, "m"),
        (1.0, ""),
        (1e3, "k"),
        (1e6, "M"),
        (1e9, "G")
    ]
    
    escala_elegida = 1.0
    prefijo_elegido = ""
    
    for factor, pref in sorted(prefijos, key=lambda x: x[0], reverse=True):
        scaled = valor / factor
        if abs(scaled) >= 1.0:
            escala_elegida = factor
            prefijo_elegido = pref
            break
    else:
        escala_elegida = 1e-12
        prefijo_elegido = "p"
        
    scaled = valor / escala_elegida
    
    # Manejo del caso especial de redondeo (ej: 999.9999 Hz -> 1 kHz)[cite: 9]
    if round(scaled, 3) >= 1000.0:
        idx = [p[0] for p in prefijos].index(escala_elegida)
        if idx < len(prefijos) - 1:
            escala_elegida = prefijos[idx+1][0]
            prefijo_elegido = prefijos[idx+1][1]
            scaled = valor / escala_elegida

    redondeado = round(scaled, 3)
    if redondeado.is_integer():
        num_str = str(int(redondeado))
    else:
        num_str = str(redondeado)
        
    return f"{num_str} {prefijo_elegido}{unidad}"

if __name__ == "__main__":
    assert a_numero("1.000000E+03") == 1000.0
    assert a_numero("texto_roto") is None
    assert con_unidad(1000.0, "Hz") == "1 kHz"
    assert con_unidad(2500.0, "Hz") == "2.5 kHz"
    assert con_unidad(2.0, "V") == "2 V"
    assert con_unidad(0.707, "V") == "707 mV"
    assert con_unidad(0.0005, "s") == "500 us"
    assert con_unidad(0.0, "V") == "0 V"
    assert con_unidad(999.9999, "Hz") == "1 kHz"
    print("pruebas 02_magnitudes OK")
