def es_consulta(comando):
    """Devuelve True si el comando termina en ?[cite: 9]."""
    if not isinstance(comando, str):
        return False
    return comando.endswith("?")

def validar(comando):
    """
    Valida un comando SCPI según las reglas de la cátedra[cite: 9]:
    - No puede estar vacío
    - Empieza con ':' o '*'
    - No hay dos espacios seguidos
    - Hay a lo sumo un '?'
    - El '?' va al final
    - Una orden lleva un solo argumento
    - Una consulta no lleva argumento
    Devuelve None si está bien, o un mensaje de error si está mal[cite: 9].
    """
    if not isinstance(comando, str) or not comando.strip():
        return "El comando no puede estar vacío"
    
    if not (comando.startswith(":") or comando.startswith("*")):
        return "El comando debe empezar con ':' o '*'"
        
    if "  " in comando:
        return "No puede haber dos espacios seguidos"
        
    if comando.count("?") > 1:
        return "Hay más de un signo de interrogación"
        
    if "?" in comando and not comando.endswith("?"):
        return "El signo de interrogación debe ir al final"
        
    partes = comando.split()
    es_q = es_consulta(comando)
    
    if es_q and len(partes) > 1:
        return "Una consulta no lleva argumento"
    elif not es_q and len(partes) > 2:
        return "Una orden lleva a lo sumo un argumento"
            
    return None

if __name__ == "__main__":
    assert es_consulta(":CH1:FREQuency?") is True
    assert es_consulta(":CH1:DISPlay ON") is False
    assert validar("") == "El comando no puede estar vacío"
    assert validar("CH1:DISPlay ON") == "El comando debe empezar con ':' o '*'"
    assert validar(": CH1: DISPlay ON") == "No puede haber dos espacios seguidos"
    assert validar(":CH1:DISPlay??") == "Hay más de un signo de interrogación"
    assert validar(":CH1:DIS?Play") == "El signo de interrogación debe ir al final"
    assert validar(":CH1:DISPlay ON?") == "Una consulta no lleva argumento"
    assert validar(":CH1:DISPlay ON") is None
    print("pruebas 03_comandos OK")
