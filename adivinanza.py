#!/usr/bin/env python3
# Juego de adivinanza mejorado: el usuario debe adivinar un número entre 1 y 100
# - Valida entradas no numéricas (no truena)
# - Máximo 10 intentos por partida
# - Mensajes más amigables y pistas (demasiado alto/bajo, y "muy cerca")
# - Informa al final si ganó y en cuántos intentos, o si perdió

import random
import sys

MAX_INTENTOS = 10
RANGO_MIN = 1
RANGO_MAX = 100
CERCA_UMBRAL = 5  # si la diferencia absoluta <= 5, decimos "¡Muy cerca!"

def pedir_intento(intentos_restantes):
    """
    Pide al usuario un intento, valida que sea un entero dentro del rango.
    No cuenta intentos por entradas inválidas; devuelve None en caso de interrupción.
    """
    prompt = f"Introduce un número entre {RANGO_MIN} y {RANGO_MAX} (te quedan {intentos_restantes} intentos) o escribe 'salir' para terminar: "
    while True:
        try:
            entrada = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n¡Juego interrumpido! ¡Hasta pronto!")
            return None

        if entrada == "":
            print("No escribiste nada. Intenta de nuevo, por favor.")
            continue

        if entrada.lower() in ("salir", "s", "q", "quit"):
            return "SALIR"

        # Intentar convertir a entero
        try:
            intento = int(entrada)
        except ValueError:
            print("No reconocí eso como un número entero. Prueba con un número del 1 al 100.")
            continue

        if intento < RANGO_MIN or intento > RANGO_MAX:
            print(f"Valor fuera de rango. Por favor elige un número entre {RANGO_MIN} y {RANGO_MAX}.")
            continue

        return intento

def jugar_una_partida():
    secreto = random.randint(RANGO_MIN, RANGO_MAX)
    intentos_hechos = 0

    print("\nHe pensado un número... ¿podrás adivinarlo?")
    # Bucle de intentos
    while intentos_hechos < MAX_INTENTOS:
        restantes = MAX_INTENTOS - intentos_hechos
        respuesta = pedir_intento(restantes)
        if respuesta is None:
            # interrupción (Ctrl+C / EOF)
            return None, False  # señal de salida
        if respuesta == "SALIR":
            print("Has elegido salir de la partida. ¡Nos vemos!")
            return None, False

        intento = respuesta
        intentos_hechos += 1
        restantes = MAX_INTENTOS - intentos_hechos

        if intento == secreto:
            # Ganó
            intent_word = "intento" if intentos_hechos == 1 else "intentos"
            print(f"¡🎉 Enhorabuena! Has adivinado el número {secreto} en {intentos_hechos} {intent_word}.")
            return intentos_hechos, True

        # Dar pistas
        diferencia = abs(intento - secreto)
        if intento < secreto:
            mensaje_base = "Demasiado bajo."
        else:
            mensaje_base = "Demasiado alto."

        if diferencia <= CERCA_UMBRAL:
            pista = " ¡Muy cerca! Sigue así."
        else:
            pista = ""

        if restantes > 0:
            print(f"{mensaje_base}{pista} Te quedan {restantes} intento{'s' if restantes != 1 else ''}.")
        else:
            print(f"{mensaje_base}{pista} No te quedan intentos.")

    # Si sale del bucle sin adivinar, perdió
    print(f"\nHas agotado los {MAX_INTENTOS} intentos. Lo siento — el número era {secreto}.")
    return MAX_INTENTOS, False

def main():
    print("=== Juego de Adivinanza (1–100) ===")
    print("Tienes 10 intentos para adivinar el número secreto. Te daré pistas si tu número es demasiado alto o bajo.")
    while True:
        resultado = jugar_una_partida()
        if resultado == (None, False):
            # Partida interrumpida o usuario salió; terminamos el programa
            break

        intentos_usados, gano = resultado
        if gano:
            print("¡Buen trabajo! Gracias por jugar.")
        else:
            print("No te rindas: puedes intentarlo de nuevo para mejorar tu resultado.")

        # Preguntar si quiere jugar otra vez
        try:
            volver = input("\n¿Quieres jugar otra vez? (s/n): ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nInterrumpido. ¡Hasta luego!")
            break

        if volver not in ("s", "si", "y", "yes"):
            print("¡Gracias por jugar! ¡Que tengas un gran día!")
            break

if __name__ == "__main__":
    main()
