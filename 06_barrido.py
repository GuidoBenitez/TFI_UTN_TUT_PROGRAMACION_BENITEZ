try:
    from _02_magnitudes import a_numero
except ImportError:
    def a_numero(texto):
        try:
            return float(texto.strip())
        except:
            return None

def barrer(instrumento, canales):
    """
    Le pide al instrumento las tres magnitudes de cada canal especificado[cite: 10, 11].
    Devuelve una lista de diccionarios con: canal, magnitud, unidad, texto_crudo, valor[cite: 10, 11].
    """
    magnitudes = [
        ("FREQ", "Hz"),
        ("PKPK", "V"),
        ("CYCRMS", "V")
    ]
    
    resultados = []
    
    for canal in canales:
        for mag, unidad in magnitudes:
            comando = f":MEASUrement:{canal}:{mag}?"
            texto_crudo = instrumento.preguntar(comando)
            
            if "ERROR:" in texto_crudo or not texto_crudo:
                valor = None
            else:
                valor = a_numero(texto_crudo)
                
            resultados.append({
                "canal": canal,
                "magnitud": mag,
                "unidad": unidad,
                "texto_crudo": texto_crudo,
                "valor": valor
            })
            
    return resultados

if __name__ == "__main__":
    class InstrumentoMock:
        def preguntar(self, comando):
            if "FREQ" in comando:
                return "1.000000E+03"
            elif "PKPK" in comando:
                return "2.000000E+00"
            elif "CYCRMS" in comando:
                return "7.071000E-01"
            return "ERROR: desconocido"

    mock = InstrumentoMock()
    res = barrer(mock, ["CH1"])
    assert len(res) == 3
    assert res[0]["canal"] == "CH1"
    assert res[0]["magnitud"] == "FREQ"
    assert res[0]["valor"] == 1000.0
    print("pruebas 06_barrido OK")
