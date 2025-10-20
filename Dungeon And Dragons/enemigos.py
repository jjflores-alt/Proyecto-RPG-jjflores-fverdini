# enemigos.py

import random

class Enemigo:
    def __init__(self, nombre, tipo, vida_max, ataque, defensa, oro_drop, alma):
        self.nombre = nombre
        self.tipo = tipo
        self.vida_max = vida_max
        self.vida_actual = vida_max
        self.ataque = ataque
        self.defensa = defensa
        self.oro_drop = oro_drop
        self.alma = alma

    def atacar(self, heroe):
        dano = max(0, self.ataque - heroe.get_defensa())
        heroe.recibir_dano(dano)
        print(f"{self.nombre} ({self.tipo}) ataca a {heroe.nombre} causando {dano} de daño. {heroe.nombre} tiene {heroe.vida_actual} vida restante.")

    def recibir_dano(self, cantidad):
        self.vida_actual -= cantidad
        if self.vida_actual < 0:
            self.vida_actual = 0

    def esta_vivo(self):
        return self.vida_actual > 0

def generar_enemigos(nivel_mazmorra):
    enemigos = []
    if nivel_mazmorra == 1:
        for i in range(3):
            enemigos.append(Enemigo(f"Duende {i+1}", "Duende", 60, 15, 5, random.randint(10, 20), "Alma de Monstruo I"))
    elif nivel_mazmorra == 2:
        for i in range(3):
            enemigos.append(Enemigo(f"Lobo {i+1}", "Lobo", 100, 25, 10, random.randint(20, 30), "Alma de Monstruo II"))
    elif nivel_mazmorra == 3:
        for i in range(3):
            enemigos.append(Enemigo(f"Orco {i+1}", "Orco", 150, 35, 15, random.randint(30, 50), "Alma de Monstruo III"))
    elif nivel_mazmorra == 4:
        enemigos.append(Enemigo("Dragón", "Dragón", 300, 50, 20, 500, None))
    return enemigos

def dropear_objetos(enemigo):
    return enemigo.oro_drop, enemigo.alma