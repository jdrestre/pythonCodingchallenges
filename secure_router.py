"""
secure_router.py - Módulo selector inteligente de generadores de contraseña

ARQUITECTURA Y FLUJO:
=====================
Integración de dos generadores mediante un router inteligente que elige
automáticamente la estrategia óptima basada en los requisitos del usuario.

┌─────────────────────────────────────────────────────────────────┐
│               GENERADOR INTELIGENTE v1.0                         │
│         Selector Automático PIN_BLINDADO vs STANDARD             │
└─────────────────────────────────────────────────────────────────┘

FLUJO COMPLETO:
===============
┌──────────────────────────┐
│  Usuario selecciona:     │
│  - only_numbers: bool    │
│  - length: int (4-32)    │
│  - strict_security: bool │
│  - include_*: bool       │
└──────────────────┬───────┘
                   │
        ┌──────────▼─────────────┐
        │ 1. VALIDACIÓN ENTRADA  │
        │ ✓ Tipos correctos      │
        │ ✓ Rangos válidos       │
        │ ✓ Opciones coherentes  │
        └──────────────┬─────────┘
                       │
        ┌──────────────▼──────────────┐
        │ 2. DecisionMatrix.decide()  │
        │    Analiza automáticamente  │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼─────────────────────────┐
        │ ¿only_numbers=True?                    │
        └──────────────┬──────────────┬──────────┘
                     NO │              │ SÍ
            ┌──────────▼┐     ┌────────▼──────────┐
            │ STANDARD  │     │ ¿strict_security? │
            │ (mixtos)  │     └────┬────────┬─────┘
            │ Máx flex  │         NO│        │SÍ
            └──────────┬┘     ┌─────▼─┐  ┌──▼───────────┐
                       │      │STANDARD│  │PIN_BLINDADO  │
                       │      │(números)│ │(4-32 dígitos)│
                       │      └─────┬──┘  └──┬───────────┘
                       │            │        │
        ┌──────────────▼────────────▼────────▼──────┐
        │ 3. GENERACIÓN                             │
        │    PIN_BLINDADO: 5 capas                  │
        │    - Matemática (no consecutivos)         │
        │    - Topológica (no adyacentes teclado)   │
        │    - Semántica (blacklist patrones)       │
        │    - Criptográfica (secrets module)       │
        │    - Validación (HMAC tiempo constante)   │
        │                                           │
        │    STANDARD: Caracteres diversos          │
        │    - Máxima flexibilidad                  │
        │    - Entropía muy alta                    │
        └──────────────┬────────────────────────────┘
                       │
        ┌──────────────▼──────────────┐
        │ 4. VALIDACIÓN SALIDA        │
        │ ✓ Contenido válido          │
        │ ✓ Longitud correcta         │
        │ ✓ Seguridad verificada      │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │ 5. CÁLCULO MÉTRICAS         │
        │ • Entropía (bits)           │
        │ • Fortaleza (OWASP)         │
        │ • Tiempo de crackeo         │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │ 6. RESPUESTA COMPLETA       │
        │ {                            │
        │   password: str,             │
        │   entropy: float,            │
        │   strength: str,             │
        │   generator: GeneratorType,  │
        │   decision_reason: str,      │
        │   timestamp: datetime        │
        │ }                            │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │ 7. LOGGING Y AUDITORÍA      │
        │ • Decisión registrada       │
        │ • Historial actualizado     │
        │ • Logs detallados (debug)   │
        └──────────────────────────────┘

GENERADORES INTEGRABLES:
========================
1. PIN_BLINDADO (de generador_pin.py)
   └─ GeneradorPinBlindado.generar(length, strict_security)
      • Rango: 4-32 dígitos
      • Con seguridad: ~5 opciones válidas por paso
      • Sin seguridad: 10^length combinaciones
      • Entropía: dinámica según modo

2. STANDARD (de security_pass.py)
   └─ generate_password(size, include_uppercase, ...)
      • Rango: 4-32 caracteres
      • Caracteres: mayús, minús, números, símbolos
      • Entropía: log2(charset_size^length)
      • Máxima flexibilidad

MATRIZ DE DECISIÓN:
===================
┌─────────────────────────┬──────────────┬──────────────────┐
│ Condición               │ Generador    │ Razón            │
├─────────────────────────┼──────────────┼──────────────────┤
│ only_numbers=True       │              │                  │
│ length 4-32             │ PIN_BLINDADO │ Máxima robustez  │
│ strict_security=True    │              │ contra patrones  │
├─────────────────────────┼──────────────┼──────────────────┤
│ only_numbers=True       │ STANDARD     │ Sin restricciones│
│ strict_security=False   │              │ topológicas      │
├─────────────────────────┼──────────────┼──────────────────┤
│ only_numbers=False      │ STANDARD     │ Diversidad de    │
│ (caracteres mixtos)     │              │ caracteres       │
└─────────────────────────┴──────────────┴──────────────────┘

MÉTRICAS DE ENTROPÍA (OWASP):
=============================
Tipo                          Bits    Fortaleza  Uso
─────────────────────────────────────────────────────────
PIN 4 dígitos (Blindado)     10.29   ⚠️ WEAK    Prototipos
PIN 6 dígitos (Blindado)     14.93   ⚠️ WEAK    PIN estándar
PIN 8 dígitos (Blindado)     19.58   ⚠️ WEAK    PIN máximo
Números 8 (Standard)         49.98   ✅ GOOD    Casual
Contraseña 12 (Standard)     74.98   🔐 STRONG  Producción
Contraseña 16 (Standard)     99.97   🔐 STRONG  Muy fuerte
Contraseña 24 (Standard)    149.95   🔐 STRONG  Máximo nivel

VALIDACIONES:
=============
ENTRADA:
• Tipos de datos (int, bool, dict)
• Rangos permitidos (4-32 caracteres)
• Opciones coherentes (al menos 1 tipo carácter)
• Presencia de claves requeridas

SALIDA:
• Longitud coincide con solicitado
• Contenido válido para tipo (dígitos para PIN)
• Entropía calculada correctamente
• Fortaleza clasificada según OWASP
• Timestamp registrado

CARACTERÍSTICAS:
================
✓ Detector automático: Elige generador sin intervención usuario
✓ Lógica centralizada: Decision Matrix Pattern
✓ Auditoría completa: Historial + logs detallados
✓ Mitigación de complejidad: Matriz testeable y mantenible
✓ Rango unificado: 4-32 para todos los tipos
✓ Entropía dinámica: Varía según seguridad/tipos
✓ Error handling: Validación exhaustiva
✓ Anti-timing: HMAC validation disponible

DEPENDENCIAS:
=============
- security_pass.py: generate_password(), calculate_entropy(), get_entropy_strength()
- generador_pin.py: GeneradorPinBlindado
- Python: secrets, logging, datetime, typing, enum, math

MODO DE USO:
============
# Programático
from secure_router import SecurePasswordRouter
router = SecurePasswordRouter(debug=False, track_history=True)
result = router.generate({'only_numbers': True, 'length': 6, 'strict_security': True})

# Interactivo (CLI)
python3 secure_router.py

# Testing
pytest test_secure_router.py -v
"""

import sys
import math
import logging
from datetime import datetime
from typing import Dict, Tuple, Optional, Any
from enum import Enum

# Imports de módulos locales
try:
    from security_pass import generate_password, calculate_entropy, get_entropy_strength
except ImportError as e:
    raise ImportError(f"No se pudo importar security_pass: {e}")

try:
    from generador_pin import GeneradorPinBlindado
except ImportError as e:
    raise ImportError(f"No se pudo importar generador_pin: {e}")


# ============================= CONFIGURACIÓN =============================

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SecureRouter")


class GeneratorType(Enum):
    """Tipos de generadores disponibles"""
    PIN_BLINDADO = "PIN_BLINDADO"
    STANDARD = "STANDARD"


# Constantes de decisión
PIN_MIN_LENGTH = 4
PIN_MAX_LENGTH = 32
STANDARD_MIN_LENGTH = 4
STANDARD_MAX_LENGTH = 32


# ============================= DECISION MATRIX =============================

class DecisionMatrix:
    """
    Matriz de decisión centralizada y testeable.
    
    Define todas las reglas para elegir qué generador usar.
    Estructura: clara, mantenible, extensible.
    """

    @staticmethod
    def decide(options: Dict[str, Any]) -> Tuple[GeneratorType, str]:
        """
        Decide qué generador usar basado en las opciones.
        
        Args:
            options: Diccionario con keys:
                - only_numbers (bool): ¿Solo números?
                - length (int): Longitud deseada
                - strict_security (bool): ¿Máxima seguridad?
                - (opcional) use_pin_armor (bool): Forzar PIN Blindado
        
        Returns:
            Tuple[GeneratorType, str]: (tipo_generador, razón_lectura)
        
        Raises:
            ValueError: Si opciones inválidas
        """
        # ========== CAPA 1: Validaciones ==========
        DecisionMatrix._validate_options(options)

        # ========== CAPA 2: Override explícito ==========
        # Si usuario fuerza explícitamente PIN Blindado
        if options.get('use_pin_armor', False):
            if options.get('only_numbers', False):
                return GeneratorType.PIN_BLINDADO, "Usuario solicitó PIN Blindado explícitamente"
            else:
                logger.warning("use_pin_armor=True pero no es solo números, usando STANDARD")

        # ========== CAPA 3: Lógica de decisión principal ==========
        
        # Si caracteres mixtos → siempre STANDARD
        if not options.get('only_numbers', False):
            return GeneratorType.STANDARD, "Caracteres mixtos: usando generador estándar"
        
        # Si solo números + strict_security=True → PIN_BLINDADO
        if options.get('only_numbers', False) and options.get('strict_security', False):
            length = options.get('length', PIN_MIN_LENGTH)
            if PIN_MIN_LENGTH <= length <= PIN_MAX_LENGTH:
                return GeneratorType.PIN_BLINDADO, "Solo números + seguridad: PIN Blindado (4-32 dígitos)"
            else:
                raise ValueError(f"Solo números permite 4-32 dígitos, solicitados: {length}")
        
        # Si solo números + strict_security=False → STANDARD (números sin topología)
        if options.get('only_numbers', False):
            return GeneratorType.STANDARD, "Solo números estándar (sin restricciones de topología)"

    @staticmethod
    def _validate_options(options: Dict[str, Any]) -> None:
        """
        Valida estructura y valores de opciones.
        
        Raises:
            ValueError: Si hay problemas
        """
        if not isinstance(options, dict):
            raise ValueError(f"Options debe ser dict, recibido: {type(options)}")

        # Validar longitud si existe
        if 'length' in options:
            length = options['length']
            if not isinstance(length, int):
                raise ValueError(f"Length debe ser int, recibido: {type(length)}")
            if length < 4:
                raise ValueError(f"Length mínima es 4, recibido: {length}")
            if length > STANDARD_MAX_LENGTH:
                raise ValueError(f"Length máxima es {STANDARD_MAX_LENGTH}, recibido: {length}")

        # Validar booleans
        for key in ['only_numbers', 'strict_security', 'use_pin_armor']:
            if key in options and not isinstance(options[key], bool):
                raise ValueError(f"{key} debe ser bool, recibido: {type(options[key])}")


# ============================= GENERADOR PRINCIPAL =============================

class SecurePasswordRouter:
    """
    Router inteligente que orquesta la generación de contraseñas/PINs.
    
    Responsabilidades:
    - Decidir qué generador usar
    - Validar inputs y outputs
    - Loguear decisiones (debugging)
    - Guardar history (auditoría)
    - Manejar errores gracefully
    """

    def __init__(self, debug: bool = False, track_history: bool = True):
        """
        Inicializa el router.
        
        Args:
            debug: Si True, imprime logs detallados
            track_history: Si True, guarda historial de generaciones
        """
        self.debug = debug
        self.track_history = track_history
        self.history: list = []
        self.pin_generator = GeneradorPinBlindado()

        if debug:
            logger.setLevel(logging.DEBUG)

    def generate(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera contraseña o PIN seleccionando la estrategia automáticamente.
        
        Args:
            options: Diccionario con configuración
                {
                    'only_numbers': bool,
                    'length': int,
                    'strict_security': bool,
                    'include_uppercase': bool (si not only_numbers),
                    'include_lowercase': bool (si not only_numbers),
                    'include_symbols': bool (si not only_numbers),
                    'safe_mode': bool (si include_symbols)
                }
        
        Returns:
            {
                'password': str,                    # La contraseña/PIN generado
                'entropy': float,                   # Bits de entropía
                'strength': str,                    # Clasificación de fortaleza
                'generator': GeneratorType,         # Tipo de generador usado
                'decision_reason': str,             # Por qué se eligió
                'length': int,                      # Longitud real
                'validation': bool,                 # Pasó validaciones
                'timestamp': datetime               # Cuándo se generó
            }
        
        Raises:
            ValueError: Si opciones inválidas
            RuntimeError: Si generación falla
        """
        try:
            # ========== FASE 1: VALIDACIÓN DE ENTRADA ==========
            self._validate_options(options)
            logger.debug(f"Opciones validadas: {options}")

            # ========== FASE 2: DECISIÓN ==========
            generator_type, decision_reason = DecisionMatrix.decide(options)
            logger.info(f"Generator elegido: {generator_type.value} - {decision_reason}")

            # ========== FASE 3: GENERACIÓN ==========
            if generator_type == GeneratorType.PIN_BLINDADO:
                password, entropy = self._generate_pin_armor(options)
            else:
                password, entropy = self._generate_standard(options)

            # ========== FASE 4: VALIDACIÓN DE SALIDA ==========
            self._validate_result(password, generator_type, options)
            logger.debug(f"Resultado validado: {len(password)} chars, {entropy:.2f} bits")

            # ========== FASE 5: CLASIFICACIÓN DE FORTALEZA ==========
            strength_label, strength_desc = get_entropy_strength(entropy)

            # ========== FASE 6: CONSTRUCCIÓN DE RESPUESTA ==========
            result = {
                'password': password,
                'entropy': entropy,
                'strength': strength_label,
                'strength_description': strength_desc,
                'generator': generator_type.value,
                'decision_reason': decision_reason,
                'length': len(password),
                'validation': True,
                'timestamp': datetime.now()
            }

            # ========== FASE 7: LOGGING Y HISTORIAL ==========
            if self.track_history:
                self.history.append({
                    'timestamp': result['timestamp'],
                    'options': options,
                    'generator': generator_type.value,
                    'entropy': entropy,
                    'decision_reason': decision_reason,
                    'success': True
                })
                logger.debug(f"Historial actualizado. Total: {len(self.history)} generaciones")

            return result

        except (ValueError, RuntimeError) as e:
            logger.error(f"Error durante generación: {e}")
            if self.track_history:
                self.history.append({
                    'timestamp': datetime.now(),
                    'options': options,
                    'error': str(e),
                    'success': False
                })
            raise

    def _generate_pin_armor(self, options: Dict[str, Any]) -> Tuple[str, float]:
        """
        Genera PIN usando GeneradorPinBlindado con opciones de seguridad.
        
        Args:
            options: Debe contener 'length' y opcionalmente 'strict_security'
        
        Returns:
            Tuple[password, entropy]
        """
        length = options.get('length', PIN_MIN_LENGTH)
        strict_security = options.get('strict_security', False)
        
        if not (PIN_MIN_LENGTH <= length <= PIN_MAX_LENGTH):
            raise ValueError(f"PIN length debe ser {PIN_MIN_LENGTH}-{PIN_MAX_LENGTH}, recibido: {length}")

        try:
            pin = self.pin_generator.generar(length, strict_security=strict_security)
            entropy = self.pin_generator._calcular_entropia_bits(length, strict_security=strict_security)
            logger.debug(f"PIN Blindado generado: {length} chars, {entropy:.2f} bits, strict_security={strict_security}")
            return pin, entropy
        except Exception as e:
            raise RuntimeError(f"Error generando PIN Blindado: {e}")

    def _generate_standard(self, options: Dict[str, Any]) -> Tuple[str, float]:
        """
        Genera contraseña usando generate_password de security_pass.py.
        
        Args:
            options: Configuración para generate_password
        
        Returns:
            Tuple[password, entropy]
        """
        # Mapear opciones del router a parámetros de generate_password
        size = options.get('length', STANDARD_MIN_LENGTH)
        include_uppercase = options.get('include_uppercase', True)
        include_lowercase = options.get('include_lowercase', True)
        include_numbers = options.get('include_numbers', True)
        include_symbols = options.get('include_symbols', True)
        safe_mode = options.get('safe_mode', True)

        try:
            password, entropy, strength = generate_password(
                size=size,
                include_uppercase=include_uppercase,
                include_lowercase=include_lowercase,
                include_numbers=include_numbers,
                include_symbols=include_symbols,
                safe_mode=safe_mode
            )
            logger.debug(f"Standard generado: {size} chars, {entropy:.2f} bits, {strength}")
            return password, entropy
        except Exception as e:
            raise RuntimeError(f"Error generando password standard: {e}")

    def _validate_options(self, options: Dict[str, Any]) -> None:
        """
        Validación exhaustiva de opciones.
        
        Raises:
            ValueError: Si hay problemas
        """
        DecisionMatrix._validate_options(options)

        # Validaciones adicionales del router
        if not options.get('only_numbers', False):
            # Si no solo números, validar opciones de caracteres
            char_options = [
                options.get('include_uppercase', True),
                options.get('include_lowercase', True),
                options.get('include_numbers', True),
                options.get('include_symbols', True),
            ]
            if not any(char_options):
                raise ValueError("Al menos un tipo de carácter debe estar habilitado")

    def _validate_result(self, password: str, generator_type: GeneratorType, options: Dict[str, Any]) -> None:
        """
        Validación post-generación del resultado.
        
        Raises:
            RuntimeError: Si el resultado es inválido
        """
        if not password or not isinstance(password, str):
            raise RuntimeError(f"Password inválido: {password}")

        if len(password) == 0:
            raise RuntimeError("Password vacío")

        if generator_type == GeneratorType.PIN_BLINDADO:
            if not password.isdigit():
                raise RuntimeError(f"PIN debe ser solo dígitos, recibido: {password}")
            if not (PIN_MIN_LENGTH <= len(password) <= PIN_MAX_LENGTH):
                raise RuntimeError(f"PIN length inválida: {len(password)}")
        else:
            if len(password) < STANDARD_MIN_LENGTH:
                raise RuntimeError(f"Password muy corta: {len(password)}")
            if len(password) > STANDARD_MAX_LENGTH:
                raise RuntimeError(f"Password muy larga: {len(password)}")

    def get_history(self) -> list:
        """
        Retorna historial de generaciones.
        
        Returns:
            Lista de eventos de generación
        """
        return self.history.copy()

    def clear_history(self) -> None:
        """Limpia el historial"""
        self.history.clear()
        logger.info("Historial limpiado")


# ============================= INTERFAZ CLI =============================

def request_size(generator_type: GeneratorType) -> int:
    """
    Solicita longitud al usuario con validaciones según tipo.
    
    Args:
        generator_type: PIN_BLINDADO o STANDARD
    
    Returns:
        int: Longitud validada
    """
    if generator_type == GeneratorType.PIN_BLINDADO:
        min_len, max_len, recommended = PIN_MIN_LENGTH, PIN_MAX_LENGTH, 6
        prompt = f"Longitud PIN [{min_len}-{max_len}] (recomendado: {recommended}): "
    else:
        min_len, max_len, recommended = STANDARD_MIN_LENGTH, STANDARD_MAX_LENGTH, 16
        prompt = f"Longitud contraseña [{min_len}-{max_len}] (recomendado: {recommended}): "

    while True:
        try:
            size = int(input(prompt))
            if size < min_len or size > max_len:
                print(f"❌ Debe estar entre {min_len} y {max_len}")
                continue
            return size
        except ValueError:
            print("❌ Ingrese un número válido")
        except KeyboardInterrupt:
            print("\n👋 Cancelado por usuario")
            sys.exit(0)


def request_size_numbers() -> int:
    """
    Solicita longitud para solo números (4-32 dígitos con PIN Blindado).
    
    Returns:
        int: Longitud validada
    """
    min_len, max_len, recommended = PIN_MIN_LENGTH, PIN_MAX_LENGTH, 6
    prompt = f"Longitud números [{min_len}-{max_len}] (recomendado: {recommended}): "

    while True:
        try:
            size = int(input(prompt))
            if size < min_len or size > max_len:
                print(f"❌ Debe estar entre {min_len} y {max_len}")
                continue
            return size
        except ValueError:
            print("❌ Ingrese un número válido")
        except KeyboardInterrupt:
            print("\n👋 Cancelado por usuario")
            sys.exit(0)


def request_pin_options() -> Dict[str, Any]:
    """Solicita opciones para PIN Blindado"""
    print("\n" + "-" * 50)
    print("Opciones de PIN:")
    print("-" * 50)

    while True:
        try:
            strict = input("¿Máxima seguridad (topología + blacklist)? [Y/n]: ").lower()
            strict_security = strict != 'n'
            break
        except KeyboardInterrupt:
            print("\n👋 Cancelado")
            sys.exit(0)

    length = request_size(GeneratorType.PIN_BLINDADO)

    return {
        'only_numbers': True,
        'length': length,
        'strict_security': strict_security
    }


def request_password_options() -> Dict[str, Any]:
    """Solicita opciones para contraseña estándar"""
    print("\n" + "-" * 50)
    print("Opciones de carácter:")
    print("-" * 50)

    options = {'only_numbers': False}

    for prompt, key in [
        ("¿Mayúsculas (A-Z)? [Y/n]: ", 'include_uppercase'),
        ("¿Minúsculas (a-z)? [Y/n]: ", 'include_lowercase'),
        ("¿Números (0-9)? [Y/n]: ", 'include_numbers'),
        ("¿Símbolos? [Y/n]: ", 'include_symbols'),
    ]:
        while True:
            try:
                response = input(prompt).lower()
                options[key] = response != 'n'
                break
            except KeyboardInterrupt:
                print("\n👋 Cancelado")
                sys.exit(0)

    if options.get('include_symbols'):
        while True:
            try:
                safe = input("¿Usar solo símbolos seguros? [Y/n]: ").lower()
                options['safe_mode'] = safe != 'n'
                break
            except KeyboardInterrupt:
                print("\n👋 Cancelado")
                sys.exit(0)

    # Si solo números, preguntar sobre PIN Blindado
    if (options.get('include_numbers') and 
        not options.get('include_uppercase') and 
        not options.get('include_lowercase') and 
        not options.get('include_symbols')):
        
        print("\n" + "-" * 50)
        print("Detectado: Solo números seleccionados")
        print("-" * 50)
        
        while True:
            try:
                use_pin = input("¿Usar PIN Blindado con seguridad (topología + blacklist)? [Y/n]: ").lower()
                if use_pin != 'n':
                    options['use_pin_armor'] = True
                    options['strict_security'] = True
                    options['only_numbers'] = True
                    print("✓ PIN Blindado CON seguridad activado (4-32 dígitos)")
                else:
                    options['only_numbers'] = True
                    options['use_pin_armor'] = False
                    print("✓ Números estándar sin seguridad (4-32 dígitos)")
                break
            except KeyboardInterrupt:
                print("\n👋 Cancelado")
                sys.exit(0)

    options['length'] = request_size(GeneratorType.STANDARD)
    return options


def display_result(result: Dict[str, Any]) -> None:
    """Muestra el resultado de forma amigable"""
    print("\n" + "=" * 60)
    print("✅ CONTRASEÑA/PIN GENERADO")
    print("=" * 60)
    print(f"\nContraseña: {result['password']}")
    print(f"\nDatos de seguridad:")
    print(f"  • Generador: {result['generator']}")
    print(f"  • Razón: {result['decision_reason']}")
    print(f"  • Longitud: {result['length']} caracteres")
    print(f"  • Entropía: {result['entropy']:.2f} bits")
    print(f"  • Fortaleza: {result['strength']} - {result['strength_description']}")
    print(f"  • Generado: {result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


def main():
    """Programa principal - Una sola opción inteligente"""
    print("\n" + "=" * 60)
    print("🔐 GENERADOR INTELIGENTE DE CONTRASEÑAS Y PINs")
    print("=" * 60)
    print("\nDetección automática de PIN Blindado para seguridad óptima")
    print("=" * 60)

    router = SecurePasswordRouter(debug=False, track_history=True)

    while True:
        try:
            # Una sola opción: seleccionar caracteres
            options = request_password_options()
            
            # Generar
            result = router.generate(options)
            display_result(result)

            # Otra generación?
            while True:
                again = input("\n¿Generar otro? (s/n): ").lower()
                if again in ['s', 'n']:
                    break
                print("❌ Ingrese 's' o 'n'")

            if again == 'n':
                print("\n📌 Tips de seguridad:")
                print("  • Usa contraseñas únicas para cada servicio")
                print("  • Guárdalas en un gestor de contraseñas")
                print("  • Habilita 2FA cuando sea posible")
                print("=" * 60 + "\n")
                sys.exit(0)

        except KeyboardInterrupt:
            print("\n\n👋 Cancelado por usuario")
            sys.exit(0)
        except ValueError as e:
            print(f"\n❌ Error de entrada: {e}")
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            logger.exception("Error inesperado en main")


if __name__ == "__main__":
    main()
