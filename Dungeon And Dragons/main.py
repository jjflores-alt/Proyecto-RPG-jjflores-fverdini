# main.py

import os
from personajes import crear_heroes
from enemigos import generar_enemigos
from combate import combate
from campamento import campamento
from guardado import cargar_partida
from items import Item

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    limpiar_pantalla()
    #muestra las distintas opciones que tomar
    print("=== Dungeon and Dragons ===")
    print("1. Jugar partida nueva")
    print("2. Cargar partida")
    print("3. Tutorial")
    print("4. Créditos")
    print("5. Salir")
    return input("Elige una opción (1-5): ")

def main():
    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            # Selección de héroes
            heroes_disponibles = crear_heroes()
            equipo = []
            while len(equipo) < 3:
                limpiar_pantalla()
                print(f"\nElige héroe {len(equipo)+1}/3:")
                print("Héroes disponibles:")
                for i, heroe in enumerate(heroes_disponibles, 1):
                    print(f"{i}. {heroe.nombre} (Vida: {heroe.vida_max}, Ataque: {heroe.get_ataque()}, Defensa: {heroe.get_defensa()})")
                try:
                    idx = int(input(f"Elige héroe (1-{len(heroes_disponibles)}): ")) - 1
                    if idx < 0 or idx >= len(heroes_disponibles):
                        print("Índice inválido. Presiona Enter para continuar.")
                        input()
                        continue
                    nombre_personalizado = input(f"Nombre para {heroes_disponibles[idx].nombre} (Enter para mantener): ")
                    heroe = heroes_disponibles.pop(idx)
                    heroe.nombre = nombre_personalizado if nombre_personalizado else heroe.nombre
                    equipo.append(heroe)
                    limpiar_pantalla()
                    print(f"{heroe.nombre} añadido al equipo.")
                    print("Presiona Enter para continuar.")
                    input()
                except ValueError:
                    print("Entrada inválida. Presiona Enter para continuar.")
                    input()
            inventario = []
            oro = 100
            mazmorra_actual = 1
            costo_guardado = 10

            # Flujo de mazmorras
            while mazmorra_actual <= 4 and any(h.esta_vivo() for h in equipo):
                limpiar_pantalla()
                print(f"\nEntrando en la Mazmorra {mazmorra_actual}")
                enemigos = generar_enemigos(mazmorra_actual)
                victoria, oro_ganado, almas = combate(equipo, enemigos, inventario)
                oro += oro_ganado
                inventario.extend([Item(alma, "alma", 0, 0) for alma in almas if alma])
                if not victoria:
                    limpiar_pantalla()
                    print("Game Over.")
                    print("Presiona Enter para volver al menú.")
                    input()
                    break
                if mazmorra_actual < 4:
                    limpiar_pantalla()
                    print("¿Ir al campamento? (s/n)")
                    if input().lower() == "s":
                        oro, costo_guardado = campamento(equipo, inventario, oro, mazmorra_actual, costo_guardado)
                mazmorra_actual += 1
            if mazmorra_actual > 4:
                limpiar_pantalla()
                print("¡Felicidades! Has derrotado al Dragón y completado el juego.")
                print("Presiona Enter para volver al menú.")
                input()

        elif opcion == "2":
            partida = cargar_partida()
            if partida:
                equipo, inventario, oro, mazmorra_actual = partida
                costo_guardado = 10 * (2 ** max(0, mazmorra_actual - 1))
                while mazmorra_actual <= 4 and any(h.esta_vivo() for h in equipo):
                    limpiar_pantalla()
                    print(f"\nEntrando en la Mazmorra {mazmorra_actual}")
                    enemigos = generar_enemigos(mazmorra_actual)
                    victoria, oro_ganado, almas = combate(equipo, enemigos, inventario)
                    oro += oro_ganado
                    inventario.extend([Item(alma, "alma", 0, 0) for alma in almas if alma])
                    if not victoria:
                        limpiar_pantalla()
                        print("Game Over.")
                        print("Presiona Enter para volver al menú.")
                        input()
                        break
                    if mazmorra_actual < 4:
                        limpiar_pantalla()
                        print("¿Ir al campamento? (s/n)")
                        if input().lower() == "s":
                            oro, costo_guardado = campamento(equipo, inventario, oro, mazmorra_actual, costo_guardado)
                    mazmorra_actual += 1
                if mazmorra_actual > 4:
                    limpiar_pantalla()
                    print("¡Felicidades! Has derrotado al Dragón y completado el juego.")
                    print("Presiona Enter para volver al menú.")
                    input()

        elif opcion == "3":
            limpiar_pantalla()
            with open("tutorial.txt", "r") as f:
                print(f.read())
            print("Presiona Enter para volver al menú.")
            input()

        elif opcion == "4":
            limpiar_pantalla()
            with open("creditos.txt", "r") as f:
                print(f.read())
            print("Presiona Enter para volver al menú.")
            input()

        elif opcion == "5":
            limpiar_pantalla()
            print("¡Gracias por jugar!")
            break
        else:
            limpiar_pantalla()
            print("Opción inválida. Presiona Enter para continuar.")
            input()

if __name__ == "__main__":
    main()