# pythonCodingchallenges 🐍

Repositorio con diversos scripts Python: retos de codificación, utilidades, y un sistema modular de generación de contraseñas seguras.

---

## 📁 Estructura de Archivos

### 🔒 MÓDULOS PRINCIPALES (Sistema de Generación de Contraseñas)

#### **security_pass.py** (Generador Estándar)
- **Tipo:** Módulo core reutilizable
- **Funcionalidad:** Genera contraseñas con caracteres diversos
- **Parámetros:**
  - Rango: 4-32 caracteres
  - Tipos: mayúsculas, minúsculas, números, símbolos
  - Modo seguro: excluye caracteres problemáticos
- **Funciones públicas:**
  - `generate_password(size, include_uppercase, include_lowercase, include_numbers, include_symbols, safe_mode)`
  - `calculate_entropy(length, character_set_size)`
  - `get_entropy_strength(entropy_bits)`
- **Uso:** Importable, directa en código o vía `secure_router.py`
- **Estado:** ✅ Productivo
- **Nota:** MIN_PASSWORD_LENGTH reducida a 4 para unificación con PIN

#### **generador_pin.py** (Generador PIN Blindado)
- **Tipo:** Módulo core reutilizable
- **Funcionalidad:** Genera PINs con 5 capas de seguridad
- **Parámetros:**
  - Rango: 4-32 dígitos
  - Strict_security: controla nivel de seguridad
    - `True`: topología + matemática + blacklist (~5 opciones/paso)
    - `False`: números aleatorios (10^n espacio)
- **Capas de seguridad:**
  1. Matemática: sin dígitos consecutivos
  2. Topológica: sin adyacentes en teclado
  3. Semántica: blacklist (años, patrones obvios)
  4. Criptográfica: secrets module (CSPRNG)
  5. Validación: HMAC (tiempo constante)
- **Clase:** `GeneradorPinBlindado`
- **Método principal:** `generar(longitud, strict_security=True)`
- **Uso:** Importable, directo o vía `secure_router.py`
- **Estado:** ✅ Productivo
- **Dependencias:** secrets, logging, hmac

#### **secure_router.py** (Router Inteligente - NUEVO)
- **Tipo:** Módulo orquestador/factoría
- **Funcionalidad:** Elige automáticamente entre PIN_BLINDADO o STANDARD
- **Arquitectura:**
  ```
  DecisionMatrix (lógica pura)
        ↓
  SecurePasswordRouter (orquestación)
        ├→ PIN_BLINDADO (si only_numbers + strict_security)
        └→ STANDARD (resto de casos)
  ```
- **Clases principales:**
  - `DecisionMatrix`: Lógica de selección
  - `SecurePasswordRouter`: Orquestador con validación
  - `GeneratorType`: Enum de tipos
- **Flujo completo:**
  1. Validación de entrada
  2. Decision Matrix (análisis)
  3. Generación (delegación)
  4. Validación de salida
  5. Cálculo de métricas (entropía, fortaleza)
  6. Logging y auditoría
- **Características:**
  - Historial de generaciones (auditoría)
  - Modo debug (logging detallado)
  - Interfaz CLI inteligente
  - Validación exhaustiva entrada/salida
- **Matriz de decisión:**
  ```
  only_numbers=True + length 4-32 + strict_security=True → PIN_BLINDADO
  only_numbers=True + strict_security=False → STANDARD
  only_numbers=False (mixtos) → STANDARD
  ```
- **Uso programático:**
  ```python
  from secure_router import SecurePasswordRouter
  router = SecurePasswordRouter(debug=False, track_history=True)
  result = router.generate({
      'only_numbers': True,
      'length': 6,
      'strict_security': True
  })
  ```
- **Uso CLI:**
  ```bash
  python3 secure_router.py
  ```
- **Estado:** ✅ Productivo (470 líneas, docstrings exhaustivos)
- **Dependencias:** security_pass.py, generador_pin.py

---

### 🧪 TESTING (Validación del Sistema)

#### **test_secure_router.py** (Suite de Tests)
- **Tipo:** Testing/Validación
- **Cobertura:**
  - 17 Unit Tests (lógica pura)
  - 15 Integration Tests (generación)
  - 5 E2E Tests (flujos usuario)
  - 10 Parametrized (combinaciones)
  - 2 Performance (velocidad)
  - **Total: 49 tests**
- **Ejecución:**
  ```bash
  pytest test_secure_router.py -v
  pytest test_secure_router.py --cov=secure_router
  ```
- **Estado:** ✅ 49/49 tests pasando
- **Relaciones:** Prueba secure_router.py, generador_pin.py, security_pass.py

#### **test_emojis.py**
- **Tipo:** Testing individual
- **Funcionalidad:** Tests para manejo de emojis
- **Estado:** ⚠️ Legacy (sin documentación clara)

#### **test_generador_pin.py**
- **Tipo:** Testing individual
- **Funcionalidad:** Tests unitarios para `generador_pin.py`
- **Estado:** ⚠️ Obsoleto (cubierto por test_secure_router.py)

---

### 📚 DOCUMENTACIÓN

**Archivos eliminados (redundancia):**
- ~~GUIA_RAPIDA.py~~ → Info en docstrings de secure_router.py
- ~~INDEX.md~~ → Redundante
- ~~PROYECTO_COMPLETADO.md~~ → Redundante
- ~~README_SECURE_ROUTER.md~~ → Redundante
- ~~examples_secure_router.py~~ → Ejemplos en docstrings

---

### 🎯 RETOS DE CODIFICACIÓN (Legacy)

Archivos de retos individuales (sin relación con security system):

**Recursión:**
- `factorial_number_with_recursion.py`
- `factorial_number_without_recursion.py`
- `fibonacci_con_recursion.py`
- `fibonacci_sin_recursion.py`
- `binary_equivalent_with_recursion.py`
- `binary_equivalent_without_recursion.py`
- `calculatePowerRecursion.py`
- `even_or_odd_recursion.py`
- `even_or_odd_with_recursion.py`
- `letters_occurs_string.py`
- `letters_occurs_string_recursively.py`
- `letters_occurs_string_without_recursevily.py`

**Strings:**
- `count_number_letter_in_string.py`
- `count_vowels_string.py`
- `length_string_without_library.py`
- `newstring_first_last2char.py`
- `palindrome.py`
- `remove_odd_indexed_char_string.py`
- `replace_blank_to_hyphen.py`
- `swap_first_to_last_charstring.py`
- `anagramas_2strings.py`

**Matemáticas:**
- `gcd_two_numbers.py`
- `lcm_two_numbers.py`
- `pascal_number.py`
- `count_set_bits_integer.py`
- `odd_palindrome_range.py`

**Diccionarios/Listas:**
- `add_keyvaluepair_dictionary.py`
- `concatenate_two_dictionaries.py`
- `count_frequency_word_dict.py`
- `count_occurrences_word.py`
- `remove_key_dict.py`

**Conversiones:**
- `celcius_farenheit.py`
- `cm_to_inch_feet.py`

**Permutaciones:**
- `permutations_string_lexico_order.py`

**Números:**
- `swap_two_numbers_without3var.py`
- `countdown.py`
- `asterisksSequence.py`

**Utilidades:**
- `country_codes.py`
- `font_art.py`
- `printingColoured.py`
- `pythonpath.py`

**Otros:**
- `calendar_1.py`
- `day22ene.py`
- `day249.py`
- `day270.py`
- `eidmubarak.py`
- `OTPGenerate.py`

**APIs/Web:**
- `audioYt.py`
- `bing_trends_python.py`
- `google_trends_python.py`
- `googleSearch.py`
- `youtubePlayingVideo.py`
- `yt_videos.py`

**Procesamiento de Imágenes:**
- `imageMirror.py`
- `removeBackground.py`

---

## 🔗 Relaciones de Dependencia

```
security_pass.py (standalone)
         ↑
         │ importada por
         │
    secure_router.py ←────────────────┐
         ↑                             │
         │ importada por               │
         │                        test_secure_router.py
    generador_pin.py (standalone)     │
         ↑                             │
         │ importada por               │
         └─────────────────────────────┘

Test files (legacy, sin relación):
- test_emojis.py (aislado)
- test_generador_pin.py (solo generador_pin.py)
```

---

## 📊 Matriz de Archivos

| Categoría | Archivo | Tipo | Estado | Dependencias | Crítico |
|-----------|---------|------|--------|--------------|---------|
| **CORE** | security_pass.py | Módulo | ✅ | - | ✅ |
| **CORE** | generador_pin.py | Módulo | ✅ | - | ✅ |
| **CORE** | secure_router.py | Orquestador | ✅ | security_pass, generador_pin | ✅ |
| **TESTING** | test_secure_router.py | Tests | ✅ | secure_router | ✓ |
| **LEGACY** | test_emojis.py | Tests | ⚠️ | - | ✗ |
| **LEGACY** | test_generador_pin.py | Tests | ⚠️ | generador_pin | ✗ |
| **LEGACY** | *.py (retos) | Scripts | ⚠️ | Various | ✗ |
| **CONFIG** | requirements.txt | Config | ✅ | - | ✓ |
| **CONFIG** | .env | Config | ✅ | - | ✓ |

---

## 🚀 Para Limpiar el Repositorio

### Archivos recomendados para eliminar:
```bash
# Tests legacy (redundancia)
rm test_emojis.py
rm test_generador_pin.py

# Retos individuales (separar a otro repo o branch)
rm factorial_number_with_recursion.py
rm fibonacci_con_recursion.py
# ... (resto de retos)
```

### Archivos a mantener:
```
security_pass.py          ← Core
generador_pin.py          ← Core
secure_router.py          ← Orquestador
test_secure_router.py     ← Tests exhaustivos
requirements.txt          ← Dependencias
.env                      ← Configuración
README.md                 ← Este archivo
```

---

## 📋 Estados

- ✅ **Productivo:** Listo para usar en producción
- ⚠️ **Legacy:** Obsoleto o sin mantenimiento
- ✓ **Auxiliar:** Soporte pero no core
- ✗ **Remisible:** Puede eliminarse sin impacto

---

## 💡 Resumen del Sistema de Seguridad

El sistema `security_pass.py` + `generador_pin.py` integrados por `secure_router.py` forma un
generador inteligente que:

1. **Automático:** Usuario no elige generador, el router decide
2. **Seguro:** PIN con 5 capas, estándares con entropía máxima
3. **Flexible:** Rango unificado 4-32 para todos tipos
4. **Auditado:** Historial completo y logs detallados
5. **Validado:** 49 tests exhaustivos (unit + integration + e2e)

---

**Última actualización:** 26 de diciembre de 2025  
**Versión:** 1.0  
**Status:** 🟢 Productivo
