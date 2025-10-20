# items.py

class Item:
    def __init__(self, nombre, tipo, efecto, precio):
        self.nombre = nombre
        self.tipo = tipo
        self.efecto = efecto
        self.precio = precio

def crear_items_disponibles():
    return [
        Item("Poción de Vida", "pocion_vida", 50, 20),
        Item("Poción de Fuerza", "pocion_fuerza", 10, 30),
        Item("Poción de Ataque Definitivo", "pocion_especial", 3, 50),
        Item("Espada Básica", "arma", 5, 40),
        Item("Armadura Básica", "armadura", 5, 40),
    ]

def usar_item(item, heroe):
    if item.tipo == "pocion_vida":
        aplicar_pocion_vida(heroe, item.efecto)
    elif item.tipo == "pocion_fuerza":
        aplicar_pocion_fuerza(heroe, item.efecto)
    elif item.tipo == "pocion_especial":
        aplicar_pocion_ataque_definitivo(heroe, item.efecto)
    elif item.tipo == "arma":
        equipar_arma(heroe, item)
    elif item.tipo == "armadura":
        equipar_armadura(heroe, item)

def equipar_arma(heroe, arma):
    heroe.equipped_items.append(arma)
    print(f"{heroe.nombre} equipa {arma.nombre}. Ataque ahora: {heroe.get_ataque()}")

def equipar_armadura(heroe, armadura):
    heroe.equipped_items.append(armadura)
    print(f"{heroe.nombre} equipa {armadura.nombre}. Defensa ahora: {heroe.get_defensa()}")

def aplicar_pocion_vida(heroe, cantidad):
    heroe.vida_actual = min(heroe.vida_max, heroe.vida_actual + cantidad)
    print(f"{heroe.nombre} usa Poción de Vida, restaurando {cantidad} de vida. Vida actual: {heroe.vida_actual}")

def aplicar_pocion_fuerza(heroe, cantidad):
    heroe.ataque_base += cantidad
    print(f"{heroe.nombre} usa Poción de Fuerza. Ataque ahora: {heroe.get_ataque()}")

def aplicar_pocion_ataque_definitivo(heroe, turnos):
    heroe.turnos_para_especial = turnos
    print(f"{heroe.nombre} usa Poción de Ataque Definitivo. Listo para especial.")