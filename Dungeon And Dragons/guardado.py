# guardado.py
#permite guardar las estadisticas y objetos en un archivo de texto llamado "partida"

def guardar_partida(heroes, inventario, oro, mazmorra_actual):
    with open("partida.txt", "w") as f:
        f.write(f"Oro: {oro}\n")
        f.write(f"Mazmorra: {mazmorra_actual + 1}\n")
        f.write("Héroes:\n")
        for heroe in heroes:
            equipped = ";".join(item.nombre for item in heroe.equipped_items) if heroe.equipped_items else "None"
            f.write(f"{heroe.nombre},{heroe.vida_actual},{heroe.vida_max},{heroe.ataque_base},{heroe.defensa_base},{heroe.turnos_para_especial},{equipped}\n")
        f.write("Inventario:\n")
        for item in inventario:
            f.write(f"{item.nombre},{item.tipo},{item.efecto},{item.precio}\n")
    print("Partida guardada exitosamente.")

def cargar_partida():
    #lee el archivo de texto para continuar donde lo guardamos
    try:
        from personajes import Heroe
        from items import Item
        heroes = []
        inventario = []
        oro = 0
        mazmorra_actual = 0
        with open("partida.txt", "r") as f:
            lines = f.readlines()
            oro = int(lines[0].split(": ")[1])
            mazmorra_actual = int(lines[1].split(": ")[1])
            i = 3
            while lines[i] != "Inventario:\n":
                nombre, vida_actual, vida_max, ataque_base, defensa_base, turnos, equipped = lines[i].strip().split(",")
                heroe = Heroe(nombre, int(vida_max), int(ataque_base), int(defensa_base), "", "")
                heroe.vida_actual = int(vida_actual)
                heroe.turnos_para_especial = int(turnos)
                if equipped != "None":
                    equipped_names = equipped.split(";")
                    for name in equipped_names:
                        if "Espada" in name:
                            heroe.equipped_items.append(Item(name, "arma", 5, 40))
                        elif "Armadura" in name:
                            heroe.equipped_items.append(Item(name, "armadura", 5, 40))
                heroes.append(heroe)
                i += 1
            for line in lines[i+1:]:
                nombre, tipo, efecto, precio = line.strip().split(",")
                inventario.append(Item(nombre, tipo, int(efecto), int(precio)))
        return heroes, inventario, oro, mazmorra_actual
    except FileNotFoundError:
        print("No se encontró una partida guardada.")
        return None