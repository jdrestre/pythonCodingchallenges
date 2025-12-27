"""
Generador de PIN Criptográficamente Seguro y Blindado.

Combina:
1. CSPRNG (secrets)
2. Reglas Matemáticas (No consecutivos)
3. Reglas Topológicas (No adyacentes físicos en teclado)
4. Reglas Semánticas (Blacklist de años y patrones)
5. Validación de tiempo constante (Anti-Timing Attacks).
"""

import secrets
import string
import logging
import math
import sys
import hmac
from typing import List, Set, Optional, Dict

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("GeneradorBlindado")


class GeneradorPinBlindado:
    """
    Generador de PINs de alta seguridad.
    Integra validaciones matemáticas, espaciales y de listas negras.
    """

    def __init__(self, blacklist_extra: Optional[List[str]] = None):
        """
        Inicializa reglas semánticas (blacklist) y físicas (mapa de teclado).
        """
        # --- CAPA 1: Semántica (Blacklist) ---
        self.blacklist: Set[str] = {
            "1010", "1212", "6969", "1313",
            "1379", "2580",  # Patrones cruzados muy obvios
            "0000", "1111", "2222", "3333", "4444",
            "5555", "6666", "7777", "8888", "9999"
        }
        # Agregar años comunes (1950-2030)
        for year in range(1950, 2031):
            self.blacklist.add(str(year))

        if blacklist_extra:
            self.blacklist.update(blacklist_extra)

        # --- CAPA 2: Topológica (Mapa del Teclado) ---
        # Define vecinos físicos (vertical/horizontal) en teclado numérico.
        # 1 2 3
        # 4 5 6
        # 7 8 9
        #   0
        self.adyacencias_fisicas: Dict[str, List[str]] = {
            '0': ['8'],
            '1': ['2', '4'],
            '2': ['1', '3', '5'],
            '3': ['2', '6'],
            '4': ['1', '5', '7'],
            '5': ['2', '4', '6', '8'],  # El 5 es crítico
            '6': ['3', '5', '9'],
            '7': ['4', '8'],
            '8': ['5', '7', '9', '0'],
            '9': ['6', '8']
        }

    def _es_transicion_valida(self, actual: str, previo: str) -> bool:
        """
        Valida reglas matemáticas Y físicas entre dos dígitos.
        """
        i_actual = int(actual)
        i_previo = int(previo)

        # 1. Regla: No repetir
        if actual == previo:
            return False

        # 2. Regla Matemática: No consecutivos lineales (1-2, 2-1)
        if abs(i_actual - i_previo) == 1:
            return False

        # 3. Regla Matemática: No salto circular estricto (0-9)
        if {i_actual, i_previo} == {0, 9}:
            return False

        # 4. Regla Topológica: No vecinos físicos
        if actual in self.adyacencias_fisicas[previo]:
            return False

        return True

    def _calcular_entropia_bits(self, longitud: int, strict_security: bool = True) -> float:
        """
        Calcula entropía ajustada según el modo de seguridad.
        
        Con seguridad (strict_security=True):
            - Espacio muestral: 10 * (5 ^ (n-1)) = ~5 opciones válidas por paso
            - Debido a: no consecutivos, no adyacentes, sin blacklist
            
        Sin seguridad (strict_security=False):
            - Espacio muestral: 10 ^ n = todas las combinaciones posibles
        """
        if longitud < 1:
            return 0.0
        
        if strict_security:
            # Con restricciones: ~5 opciones por paso después del primero
            espacio_muestral = 10 * (5 ** (longitud - 1))
        else:
            # Sin restricciones: 10 dígitos en cualquier posición
            espacio_muestral = 10 ** longitud
        
        return round(math.log2(espacio_muestral), 2)

    def generar(self, longitud: int, strict_security: bool = True) -> str:
        """
        Genera el PIN con opciones de seguridad.
        
        Args:
            longitud: Longitud del PIN (4-32)
            strict_security: Si True, aplica todas las capas (topología + blacklist)
                           Si False, genera números aleatorios sin restricciones
        
        Returns:
            PIN generado
        """
        if not (4 <= longitud <= 32):
            raise ValueError("Longitud debe ser entre 4 y 32.")
        
        if longitud < 6:
            logger.warning("Generando PIN de longitud %s. Se recomienda mínimo 6.", longitud)

        # Si NO requiere seguridad estricta, generar sin restricciones
        if not strict_security:
            pin_final = "".join(secrets.choice(string.digits) for _ in range(longitud))
            entropia = self._calcular_entropia_bits(longitud, strict_security=False)
            logger.info("PIN generado (sin seguridad). Longitud: %d. Entropía Real: %s bits.", longitud, entropia)
            return pin_final

        # Si SÍ requiere seguridad estricta, aplicar todas las capas
        max_intentos = 10000

        for _ in range(max_intentos):
            pin_lista: List[str] = []
            
            # 1. Primer dígito
            primer_digito = secrets.choice(string.digits)
            pin_lista.append(primer_digito)

            # 2. Construcción paso a paso
            valido_constructivamente = True
            for _ in range(longitud - 1):
                ultimo_char = pin_lista[-1]

                candidatos = [
                    d for d in string.digits
                    if self._es_transicion_valida(d, ultimo_char)
                ]

                if not candidatos:
                    valido_constructivamente = False
                    break

                siguiente = secrets.choice(candidatos)
                pin_lista.append(siguiente)

            if not valido_constructivamente:
                continue

            pin_final = "".join(pin_lista)

            # 3. Capa Semántica (Blacklist)
            if pin_final in self.blacklist:
                continue

            # Éxito
            entropia = self._calcular_entropia_bits(longitud, strict_security=True)
            logger.info("PIN generado (CON seguridad). Longitud: %d. Entropía Real: %s bits.", longitud, entropia)
            return pin_final

        raise RuntimeError("No se pudo generar PIN válido (demasiadas restricciones).")

    def validar_pin_seguro(self, pin_ingresado: str, pin_real: str) -> bool:
        """
        Compara dos PINs usando tiempo constante (HMAC) para evitar Timing Attacks.
        """
        return hmac.compare_digest(pin_ingresado.encode(), pin_real.encode())


# --- INTERFAZ DE USUARIO ---

def solicitar_longitud() -> int:
    while True:
        try:
            val = int(input("\nIngrese longitud (Recomendado 6-8): "))
            if 4 <= val <= 8:
                return val
            print("❌ Rango permitido: 4-8.")
        except ValueError:
            print("❌ Ingrese número válido.")

def main():
    print("=" * 60)
    print("🛡️  GENERADOR DE PIN BLINDADO (Topológico + Semántico)")
    print("=" * 60)

    generador = GeneradorPinBlindado()

    try:
        longitud = solicitar_longitud()
        
        print("⚙️  Analizando topología del teclado y entropía...")
        pin = generador.generar(longitud)
        
        print(f"\n✅ PIN Generado: {pin}")
        print("-" * 30)
        print("ℹ️  Capas de Defensa:")
        print("   1. [Matemática] Sin consecutivos")
        print("   2. [Física] Sin adyacentes de teclado")
        print("   3. [Semántica] Sin Blacklist")
        print("   4. [Cripto] Secrets + HMAC validation")

        # Simulación de validación
        print("-" * 30)
        prueba = input("📝 (Simulación) Ingrese el PIN para validar: ")
        if generador.validar_pin_seguro(prueba, pin):
            print("🔓 Acceso Concedido")
        else:
            print("🔒 Acceso Denegado")

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.exception("Error fatal")

if __name__ == "__main__":
    main()
