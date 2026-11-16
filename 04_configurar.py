try:
    from _03_comandos import validar
except ImportError:
    def validar(comando):
        if not comando or not (comando.startswith(":") or comando.startswith("*")):
            return "Error"
        if "  " in comando or comando.count("?") > 1:
            return "Error"
        return None

def comandos_de_canal(canal, display, acoplamiento, sonda, escala):
    """
    Devuelve la lista de cuatro órdenes de configuración para el canal indicado[cite: 9, 10].
    Si el canal no es CH1 ni CH2, devuelve None[cite: 9, 10].
    """
    if canal not in ["CH1", "CH2"]:
        return None
        
    return [
        f":{canal}:DISPlay {display}",
        f":{canal}:COUPling {acoplamiento}",
        f":{canal}:PROBe {sonda}",
        f":{canal}:SCALe {escala}"
    ]

if __name__ == "__main__":
    cmds = comandos_de_canal("CH1", "ON", "DC", "10X", "1v")
    assert cmds == [
        ":CH1:DISPlay ON",
        ":CH1:COUPling DC",
        ":CH1:PROBe 10X",
        ":CH1:SCALe 1v"
    ]
    assert comandos_de_canal("CH3", "ON", "DC", "10X", "1v") is None
    
    # Prueba cruzada: todos los comandos generados pasan la validación[cite: 10]
    for c in cmds:
        assert validar(c) is None
    print("pruebas 04_configurar OK")
