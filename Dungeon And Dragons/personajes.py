# personajes.py

class Heroe:
    def __init__(self, nombre, vida_max, ataque, defensa, ataque_especial_nombre, ataque_especial_desc):
        self.nombre = nombre
        self.vida_max = vida_max
        self.vida_actual = vida_max
        self.ataque_base = ataque
        self.defensa_base = defensa
        self.equipped_items = []
        self.turnos_para_especial = 0
        self.ataque_especial_nombre = ataque_especial_nombre
        self.ataque_especial_desc = ataque_especial_desc
        self.nivel = 1
        self.experiencia = 0
        self.experiencia_necesaria = 100

    def subir_nivel(self):
        self.nivel += 1
        self.experiencia_necesaria = int(self.experiencia_necesaria * 1.25)
        self.vida_max += 10
        self.ataque_base += 2
        self.defensa_base += 1
        self.vida_actual = self.vida_max
        print(f"🎉 {self.nombre} sube al nivel {self.nivel}! Sus estadísticas han aumentado.")

    def ganar_experiencia(self, cantidad):
        self.experiencia += cantidad
        print(f"{self.nombre} gana {cantidad} puntos de experiencia. (Total: {self.experiencia}/{self.experiencia_necesaria})")

        while self.experiencia >= self.experiencia_necesaria:
            self.experiencia -= self.experiencia_necesaria
            self.subir_nivel()

    def atacar(self, enemigo):
        dano = max(0, self.get_ataque() - enemigo.defensa)
        enemigo.recibir_dano(dano)
        print(f"{self.nombre} ataca a {enemigo.nombre} causando {dano} de daño. {enemigo.nombre} tiene {enemigo.vida_actual} vida restante.")
        self.turnos_para_especial += 1

    def usar_ataque_especial(self, enemigo):
        if self.turnos_para_especial >= 3:
            dano = max(0, self.get_ataque() * 2 - enemigo.defensa)
            enemigo.recibir_dano(dano)
            if self.ataque_especial_nombre == "Luz Divina":
                heal = 20
                self.vida_actual = min(self.vida_max, self.vida_actual + heal)
                print(f"{self.nombre} usa {self.ataque_especial_nombre}: {self.ataque_especial_desc}, causando {dano} de daño a {enemigo.nombre} y restaurando {heal} de vida (Vida actual: {self.vida_actual}).")
            else:
                print(f"{self.nombre} usa {self.ataque_especial_nombre}: {self.ataque_especial_desc}, causando {dano} de daño a {enemigo.nombre}.")
            self.turnos_para_especial = 0
        else:
            print(f"{self.nombre} no puede usar el ataque especial aún. Turnos restantes: {3 - self.turnos_para_especial}")

    def recibir_dano(self, cantidad):
        self.vida_actual -= cantidad
        if self.vida_actual < 0:
            self.vida_actual = 0

    def esta_vivo(self):
        return self.vida_actual > 0

    def get_ataque(self):
        return self.ataque_base + sum(item.efecto for item in self.equipped_items if item.tipo == "arma")

    def get_defensa(self):
        return self.defensa_base + sum(item.efecto for item in self.equipped_items if item.tipo == "armadura")

def crear_heroes():
    heroes = [
        Heroe("Caballero", 150, 20, 15, "Golpe de Escudo", "El caballero embiste con su escudo, aturdiendo y dañando al enemigo"),
        Heroe("Arquera", 100, 25, 10, "Flecha Llameante", "Dispara una flecha envuelta en llamas que quema al objetivo"),
        Heroe("Mago", 100, 30, 5, "Bola de Fuego", "Lanza una explosión de fuego que incinera al enemigo"),
        Heroe("Asesino", 80, 25, 10, "Corte Profundo", "Un corte profundo que ignora la defensa del enemigo"),
        Heroe("Clérigo", 110, 15, 12, "Luz Divina", "Invoca luz sagrada que daña al enemigo y cura al clérigo")
    ]
    return heroes