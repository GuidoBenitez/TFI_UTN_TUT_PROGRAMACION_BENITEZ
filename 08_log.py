def analizar_linea(linea):
    """
    Analiza una línea del log. Devuelve (medicion, motivo)[cite: 12].
    Una línea en blanco o comentario se ignora (None, None).
    Una línea con errores o campos inválidos se rechaza[cite: 12].
    """
    linea_str = linea.strip()
    if not linea_str or linea_str.startswith("#"):
        return None, None
        
    # split() sin argumentos parte por cualquier espacio en blanco, tabulaciones incluidas[cite: 13]
    campos = linea.split()
    
    if len(campos) != 6:
        return None, f"Cantidad incorrecta de campos ({len(campos)})"
        
    fecha, hora, equipo, canal, magnitud, valor_str = campos
    
    try:
        partes_hora = hora.split(":")
        if len(partes_hora) != 3:
            return None, "Formato de hora inválido"
        h, m, s = int(partes_hora[0]), int(partes_hora[1]), int(partes_hora[2])
        if not (0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59):
            return None, f"Hora imposible ({hora})"
    except ValueError:
        return None, f"Hora inválida ({hora})"
        
    if canal not in ["CH1", "CH2"]:
        return None, f"Canal inválido ({canal})"
        
    if magnitud not in ["FREQ", "PKPK", "CYCRMS"]:
        return None, f"Magnitud inválida ({magnitud})"
        
    val_limpio = valor_str.replace(",", ".")
    try:
        valor = float(val_limpio)
    except ValueError:
        return None, f"Valor no numérico ({valor_str})"
        
    medicion = {
        "fecha": fecha,
        "hora": hora,
        "equipo": equipo,
        "canal": canal,
        "magnitud": magnitud,
        "valor": valor
    }
    return medicion, None

def leer_log(ruta):
    """Recorre el archivo de log y agrupa series, además de registrar líneas rechazadas[cite: 12]."""
    series = {}
    rechazadas = []
    
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            for num_linea, linea in enumerate(f, 1):
                medicion, motivo = analizar_linea(linea)
                if motivo is not None:
                    rechazadas.append({
                        "linea": num_linea,
                        "texto": linea.strip(),
                        "motivo": motivo
                    })
                elif medicion is not None:
                    eq = medicion["equipo"]
                    ch = medicion["canal"]
                    mag = medicion["magnitud"]
                    
                    clave = (eq, ch, mag)
                    if clave not in series:
                        series[clave] = []
                    series[clave].append(medicion["valor"])
    except FileNotFoundError:
        pass
        
    return series, rechazadas

if __name__ == "__main__":
    m1, mot1 = analizar_linea("2026-09-08 09:14:00 ADS3202 CH1 FREQ 9.993761E+02")
    assert m1 is not None and mot1 is None
    assert m1["valor"] == 999.3761
    
    m_vacio, mot_vacio = analizar_linea("   ")
    assert m_vacio is None and mot_vacio is None
    
    m_err, mot_err = analizar_linea("2026-09-08 25:61:00 ADS3202 CH2 FREQ 2.500000E+03")
    assert m_err is None and mot_err is not None
    print("pruebas 08_log OK")
