"""
Generador de PIN Criptográficamente Seguro.

Este módulo genera un PIN aleatorio de longitud variable (4-8 dígitos)
utilizando fuentes de entropía segura (secrets), validando que no existan
dígitos consecutivos, repetidos o patrones comunes (lista negra).
"""

import secrets
import string
import logging
import math
import sys
from typing import List, Set, Optional

# Configuración de Logging (Para auditoría del sistema, no para el usuario final)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("GeneradorPin")


class GeneradorPinSeguro:
    """
    Clase encargada de la generación segura de PINs.
    Implementa reglas de negocio y validaciones criptográficas.
    """

    def __init__(self, blacklist_extra: Optional[List[str]] = None):
        """
        Inicializa el generador con una lista negra base y opcional.
        """
        # Blacklist base: patrones visuales o numéricos comunes
        self.blacklist: Set[str] = {
            "1010", "1212", "6969", "1313",  # Repeticiones alternas
            "1379", "2580",  # Patrones de esquinas/cruz en teclado
            "0000", "1111", "2222", "3333", "4444",
            "5555", "6666", "7777", "8888", "9999"
        }

        # Agregar años comunes (ej. 1950-2030) a la blacklist
        for year in range(1950, 2031):
            self.blacklist.add(str(year))

        if blacklist_extra:
            self.blacklist.update(blacklist_extra)

    def _es_transicion_valida(self, actual: int, previo: int) -> bool:
        """
        Verifica reglas matemáticas entre dos dígitos adyacentes.

        Args:
            actual (int): Dígito candidato.
            previo (int): Dígito anterior en el PIN.

        Returns:
            bool: True si la transición cumple las reglas de seguridad.
        """
        # Regla 1: No repetir (ej: 44)
        if actual == previo:
            return False

        # Regla 2: No consecutivos lineales (ej: 45 o 54)
        if abs(actual - previo) == 1:
            return False

        # Regla 3: No consecutivos circulares (ej: 09 o 90)
        # Esto es opcional, pero recomendado para alta seguridad en teclados numéricos.
        if {actual, previo} == {0, 9}:
            return False

        return True

    def _calcular_entropia_bits(self, longitud: int) -> float:
        """
        Calcula la entropía estimada (fuerza) del PIN en bits.
        Considera la reducción del espacio muestral por las restricciones.
        """
        if longitud < 1:
            return 0.0

        # Primer dígito: 10 opciones.
        # Siguientes dígitos: ~7 opciones válidas (se descarta mismo, +1, -1).
        espacio_muestral = 10 * (7 ** (longitud - 1))
        entropia = math.log2(espacio_muestral)
        return round(entropia, 2)

    def generar(self, longitud: int) -> str:
        """
        Genera un PIN seguro verificando reglas y blacklist.

        Args:
            longitud (int): Longitud deseada del PIN.

        Returns:
            str: PIN generado.

        Raises:
            ValueError: Si la longitud es inválida.
            RuntimeError: Si no se logra generar un PIN tras múltiples intentos.
        """
        if not (4 <= longitud <= 8):
            raise ValueError("La longitud debe estar entre 4 y 8 dígitos.")

        max_intentos = 10000

        for _ in range(max_intentos):
            pin_lista: List[str] = []

            # 1. Elegir primer dígito (CSPRNG)
            primer_digito = secrets.choice(string.digits)
            pin_lista.append(primer_digito)

            # 2. Construir el resto dígito a dígito
            valido_constructivamente = True
            for _ in range(longitud - 1):
                ultimo_int = int(pin_lista[-1])

                # Filtrar candidatos válidos (0-9) usando comprensión de listas
                candidatos = [
                    str(d) for d in range(10)
                    if self._es_transicion_valida(d, ultimo_int)
                ]

                # Si llegamos a un callejón sin salida (raro, pero posible)
                if not candidatos:
                    valido_constructivamente = False
                    break

                # Elegir siguiente de forma segura
                siguiente = secrets.choice(candidatos)
                pin_lista.append(siguiente)

            if not valido_constructivamente:
                continue

            pin_final = "".join(pin_lista)

            # 3. Verificar Blacklist
            if pin_final in self.blacklist:
                logger.warning("PIN '%s' rechazado por Blacklist. Reintentando...", pin_final)
                continue

            # Éxito: Loguear métrica y retornar
            entropia = self._calcular_entropia_bits(longitud)
            logger.info("PIN generado. Longitud: %d. Entropía: %s bits.", longitud, entropia)
            return pin_final

        logger.critical("Fallo crítico: No se generó PIN tras %d intentos.", max_intentos)
        raise RuntimeError("No se pudo generar un PIN válido (demasiadas restricciones).")


def solicitar_longitud() -> int:
    """Solicita y valida la longitud del PIN al usuario."""
    while True:
        try:
            entrada = input("\nIngrese la longitud del PIN (4-8 dígitos): ")
            longitud = int(entrada)
            if 4 <= longitud <= 8:
                return longitud
            print("❌ Error: La longitud debe ser entre 4 y 8.")
        except ValueError:
            print("❌ Error: Por favor ingrese un número entero válido.")


def main():
    """Función principal de interacción con el usuario."""
    print("=" * 60)
    print("🔒 GENERADOR DE PIN SEGURO (CSPRNG + Anti-Patrones)")
    print("=" * 60)

    # Instancia del generador (Lógica)
    generador = GeneradorPinSeguro()

    try:
        # Interacción (UI)
        longitud = solicitar_longitud()

        # Proceso
        print("⚙️  Generando PIN criptográficamente seguro...")
        pin_generado = generador.generar(longitud)

        # Salida
        print(f"\n✅ PIN Generado exitosamente: {pin_generado}")
        print("-" * 30)
        print("ℹ️  Detalles de Seguridad:")
        print("   • Método: secrets (CSPRNG del Sistema Operativo)")
        print("   • Validación: No consecutivos, no repetidos, no blacklist")

    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Ocurrió un error inesperado: {e}")
        logger.exception("Error no controlado en main")
        sys.exit(1)


if __name__ == "__main__":
    main()
