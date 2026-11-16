try:
    from _02_magnitudes import con_unidad
except ImportError:
    def con_unidad(valor, unidad):
        return f"{valor} {unidad}"

def armar_informe(idn, series, verificaciones):
    """
    Genera el informe completo como una sola cadena de texto pura 
    (no imprime nada ni abre archivos por sí misma)[cite: 13].
    """
    lineas = []
    lineas.append("=== INFORME DEL BANCO DE MEDICIONES AUTOMATIZADO ===")
    
    if idn:
        lineas.append(f"Instrumento: {idn.get('fabricante')} {idn.get('modelo')} (Serie: {idn.get('serie')}, FW: {idn.get('version')})")
    else:
        lineas.append("Instrumento: No identificado")
        
    lineas.append("-" * 50)
    lineas.append("RESUMEN DE SERIES:")
    
    for clave, valores in series.items():
        eq, ch, mag = clave
        unidad = "Hz" if mag == "FREQ" else "V"
        n = len(valores)
        prom = sum(valores) / n if n > 0 else 0
        min_v = min(valores) if n > 0 else 0
        max_v = max(valores) if n > 0 else 0
        
        prom_fmt = con_unidad(prom, unidad)
        min_fmt = con_unidad(min_v, unidad)
        max_fmt = con_unidad(max_v, unidad)
        
        lineas.append(f" - [{eq}] {ch} {mag}: n={n}, Promedio={prom_fmt}, Mín={min_fmt}, Máx={max_fmt}")
        
    lineas.append("-" * 50)
    lineas.append("VERIFICACIONES:")
    if isinstance(verificaciones, list):
        for v in verificaciones:
            estado = "COINCIDE" if v.get("coincide") else "NO COINCIDE"
            lineas.append(f" - Canal {v.get('canal')}: {estado} (PKPK={v.get('pkpk')}, Vrms={v.get('vrms_medido')})")
    elif isinstance(verificaciones, dict):
        estado = "COINCIDE" if verificaciones.get("coincide") else "NO COINCIDE"
        lineas.append(f" - Canal {verificaciones.get('canal')}: {estado}")
        
    lineas.append("=" * 50)
    return "\n".join(lineas)

if __name__ == "__main__":
    idn_mock = {"fabricante": "OWON", "modelo": "ADS3202", "serie": "12345", "version": "V1.0"}
    series_mock = {("ADS3202", "CH1", "FREQ"): [1000.0, 1001.0]}
    verif_mock = [{"canal": "CH1", "coincide": True, "pkpk": 2.0, "vrms_medido": 0.707}]
    
    informe = armar_informe(idn_mock, series_mock, verif_mock)
    assert "OWON ADS3202" in informe
    assert "CH1 FREQ" in informe
    assert "COINCIDE" in informe
    print("pruebas 10_informe OK")
