def parsear_idn(respuesta):
    """
    Recibe el texto que devuelve *IDN? y devuelve un diccionario con las claves:
    fabricante, modelo, serie y version. Devuelve None si la respuesta no sirve.
    El multímetro devuelve 5 campos (el 5to se descarta) y el osciloscopio 4[cite: 8].
    """
    if not respuesta or not isinstance(respuesta, str):
        return None
    
    if "ERROR:" in respuesta:
        return None
        
    partes = [p.strip() for p in respuesta.split(",")]
    
    if len(partes) < 4:
        return None
        
    return {
        "fabricante": partes[0],
        "modelo": partes[1],
        "serie": partes[2],
        "version": partes[3]
    }

if __name__ == "__main__":
    # Pruebas
    assert parsear_idn("OWON, ADS3202,25470803, V1.2.0") == {
        "fabricante": "OWON",
        "modelo": "ADS3202",
        "serie": "25470803",
        "version": "V1.2.0"
    }
    assert parsear_idn("OWON, XDM1041,25470803,V4.4.0,3") == {
        "fabricante": "OWON",
        "modelo": "XDM1041",
        "serie": "25470803",
        "version": "V4.4.0"
    }
    assert parsear_idn("OWON, ADS3202,254") is None
    assert parsear_idn("") is None
    assert parsear_idn("ERROR: comando desconocido") is None
    print("pruebas 01_identificacion OK")
