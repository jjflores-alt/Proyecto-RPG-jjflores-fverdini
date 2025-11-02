# combate.py
# funcionamiento del combate
import os
import random
from enemigos import dropear_objetos
from items import usar_item

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def combate(equipo, enemigos, inventario):
    limpiar_pantalla()
    print("¡Comienza el combate!")
    drops_oro = 0
    drops_almas = []

    while any(heroes.esta_vivo() for heroes in equipo) and any(Enemigo.esta_vivo() for Enemigo in enemigos):
        for heroe in [heroes for heroes in equipo if heroes.esta_vivo()]:
            if not any(Enemigo.esta_vivo() for Enemigo in enemigos):
                break
            limpiar_pantalla()
            #le da el turno al primer personaje seleccionado y muestra en pantalla las estadisticas de los enemigos y los personajes
            print(f"Turno de {heroe.nombre}")
            print(
                f"Vida: {heroe.vida_actual}/{heroe.vida_max}, Ataque: {heroe.get_ataque()}, Defensa: {heroe.get_defensa()}")
            print("\nEnemigos vivos:")
            for contador, enemigo in enumerate([Enemigo for Enemigo in enemigos if Enemigo.esta_vivo()], 1):
                print(f"{contador}. {enemigo.nombre} (Vida: {enemigo.vida_actual}/{enemigo.vida_max})")
            print("\nOpciones: 1. Atacar, 2. Ataque Especial, 3. Usar Item, 4. Huir")
            try:
                accion = input("Elige una acción (1-4): ")
                if accion == "1":
                    limpiar_pantalla()
                    #Permite atacar al enemigo seleccionado
                    print("Enemigos vivos:")
                    for contador, enemigo in enumerate([Enemigo for Enemigo in enemigos if Enemigo.esta_vivo()], 1):
                        print(f"{contador}. {enemigo.nombre} (Vida: {enemigo.vida_actual}/{enemigo.vida_max})")
                    enemigo_idx = int(input(f"Elige enemigo (1-{len([Enemigo for Enemigo in enemigos if Enemigo.esta_vivo()])}): ")) - 1
                    enemigo = [Enemigo for Enemigo in enemigos if Enemigo.esta_vivo()][enemigo_idx]
                    heroe.atacar(enemigo)
                    print("Presiona Enter para continuar.")
                    input()
                elif accion == "2":
                    if heroe.turnos_para_especial >= 3:
                        limpiar_pantalla()
                        #posibilidad de usar la habilidad especial si se cumplen los requisitos (pocion de habilidad o turnos)
                        print("Enemigos vivos:")
                        for contador, enemigo in enumerate([Enemigo for Enemigo in enemigos if Enemigo.esta_vivo()], 1):
                            print(f"{contador}. {enemigo.nombre} (Vida: {enemigo.vida_actual}/{enemigo.vida_max})")
                        enemigo_idx = int(
                            input(f"Elige enemigo (1-{len([Enemigo for Enemigo in enemigos if Enemigo.esta_vivo()])}): ")) - 1
                        enemigo = [Enemigo for Enemigo in enemigos if Enemigo.esta_vivo()][enemigo_idx]
                        heroe.usar_ataque_especial(enemigo)
                        print("Presiona Enter para continuar.")
                        input()
                    else:
                        limpiar_pantalla()
                        print(f"No puedes usar el ataque especial. Turnos restantes: {3 - heroe.turnos_para_especial}")
                        print("Presiona Enter para continuar.")
                        input()
                        continue
                elif accion == "3":
                    if not inventario:
                        limpiar_pantalla()
                        #permite usar items del inventario
                        print("No tienes ítems en el inventario.Pierdes el turno")
                        for enemigo in [Enemigo for Enemigo in enemigos if Enemigo.esta_vivo()]:
                            heroe_vivo = random.choice([heroes for heroes in equipo if heroes.esta_vivo()])
                            enemigo.atacar(heroe_vivo)
                        print("Presiona Enter para continuar.")
                        input()
                        continue
                    limpiar_pantalla()
                    print("Inventario:")
                    for contador, item in enumerate(inventario, 1):
                        print(f"{contador}. {item.nombre}")
                    item_idx = int(input(f"Elige ítem (1-{len(inventario)}): ")) - 1
                    usar_item(inventario[item_idx], heroe)
                    if inventario[item_idx].tipo in ["pocion_vida", "pocion_fuerza", "pocion_especial"]:
                        inventario.pop(item_idx)
                    print("Presiona Enter para continuar.")
                    input()
                elif accion == "4":
                    limpiar_pantalla()
                    #intenta huir del combate con un 25% de probabilidad de exito, de no poder huir pierdes el turno y el enemigo te ataca
                    if random.random() < 0.25:
                        print("¡Huyes exitosamente! Saltas a la siguiente mazmorra.")
                        print("Presiona Enter para continuar.")
                        input()
                        return True, 0, []
                    else:
                        print("¡Intento de huida fallido! Sufres un ataque sorpresa.")
                        for enemigo in [Enemigo for Enemigo in enemigos if Enemigo.esta_vivo()]:
                            heroe_vivo = random.choice([heroes for heroes in equipo if heroes.esta_vivo()])
                            enemigo.atacar(heroe_vivo)
                        print("Presiona Enter para continuar.")
                        input()
                        continue
                else:
                    limpiar_pantalla()
                    print("Opción inválida. Pierdes el turno")
                    print("Presiona Enter para continuar.")
                    input()
                    continue
            except (ValueError, IndexError):
                limpiar_pantalla()
                print("Entrada inválida. Pierdes el turno.")
                print("Presiona Enter para continuar.")
                input()
                continue

            if any(Enemigo.esta_vivo() for Enemigo in enemigos):
                limpiar_pantalla()
                #comprueba que los enemigos esten vivos, en el caso que esten vivos, atacan (turno de los enemigos)
                enemigo = random.choice([Enemigo for Enemigo in enemigos if Enemigo.esta_vivo()])
                heroe_vivo = random.choice([heroes for heroes in equipo if heroes.esta_vivo()])
                enemigo.atacar(heroe_vivo)
                print("Presiona Enter para continuar.")
                input()

        for enemigo in enemigos:
            #si el enemigo esta muerto dropea oro y alma de mounstro
            if not enemigo.esta_vivo() and enemigo.oro_drop > 0:
                oro, alma = dropear_objetos(enemigo)
                drops_oro += oro
                if alma:
                    drops_almas.append(alma)
                enemigo.oro_drop = 0

    limpiar_pantalla()
    #en caso de que derrotes a todos los enemigos
    if any(heroes.esta_vivo() for heroes in equipo):
        print("¡Victoria! Has derrotado a todos los enemigos.")

                # Recompensa de experiencia por victoria
        xp_ganada = 100  # puedes ajustar este valor o calcularlo según los enemigos derrotados
        print(f"\nCada héroe gana {xp_ganada} puntos de experiencia.")
        
        for heroe in equipo:
            if heroe.esta_vivo():
                heroe.ganar_experiencia(xp_ganada)

        if drops_oro or drops_almas:
            print(
                f"Obtienes {drops_oro} oro y {', '.join(almas for almas in drops_almas) if drops_almas else 'ninguna alma'}.")
        print("Presiona Enter para continuar.")
        input()
        return True, drops_oro, drops_almas
    else:
        #en caso de que todos los heroes pierdan
        print("¡Derrota! Tu equipo ha sido vencido.")
        print("Presiona Enter para continuar.")
        input()

        return False, drops_oro, drops_almas

