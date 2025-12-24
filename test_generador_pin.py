"""
Módulo de pruebas unitarias para el Generador de PINs Seguros.

Este módulo verifica la lógica de negocio, las restricciones criptográficas,
la validación de listas negras y el manejo de errores de la clase GeneradorPinSeguro.
"""

import unittest
from unittest.mock import patch
import string

# Asumimos que el archivo principal se llama generador_pin.py
from generador_pin import GeneradorPinSeguro


class TestGeneradorPinSeguro(unittest.TestCase):
    """
    Suite de pruebas para la clase GeneradorPinSeguro.
    Cubre casos de éxito, bordes y excepciones.
    """

    def setUp(self):
        """
        Configuración inicial que se ejecuta antes de cada prueba.
        Instancia un generador limpio.
        """
        self.generador = GeneradorPinSeguro()

    def test_inicializacion_blacklist_base(self):
        """
        Verifica que la lista negra base se cargue con patrones y años comunes.
        """
        # Verificar un patrón de repetición alterna
        self.assertIn("1212", self.generador.blacklist)
        # Verificar un patrón de teclado
        self.assertIn("1379", self.generador.blacklist)
        # Verificar un año común (ej. 2000)
        self.assertIn("2000", self.generador.blacklist)

    def test_inicializacion_blacklist_extra(self):
        """
        Verifica que se puedan agregar elementos extra a la lista negra
        durante la instanciación.
        """
        pines_prohibidos = ["9999", "1111"]
        gen_extra = GeneradorPinSeguro(blacklist_extra=pines_prohibidos)

        for pin in pines_prohibidos:
            self.assertIn(pin, gen_extra.blacklist)

    def test_transicion_valida_logica_matematica(self):
        """
        Verifica la lógica matemática entre dos dígitos (método protegido).
        Se suprime la advertencia de acceso protegido ya que es un test de caja blanca.
        """
        # pylint: disable=protected-access

        # --- Casos que deben ser FALSOS ---
        # Repetidos
        self.assertFalse(self.generador._es_transicion_valida(5, 5))
        # Consecutivo ascendente (+1)
        self.assertFalse(self.generador._es_transicion_valida(4, 5))
        # Consecutivo descendente (-1)
        self.assertFalse(self.generador._es_transicion_valida(6, 5))
        # Consecutivo circular (0-9 y 9-0)
        self.assertFalse(self.generador._es_transicion_valida(0, 9))
        self.assertFalse(self.generador._es_transicion_valida(9, 0))

        # --- Casos que deben ser VERDADEROS ---
        # Salto de 2
        self.assertTrue(self.generador._es_transicion_valida(1, 3))
        # Salto grande
        self.assertTrue(self.generador._es_transicion_valida(0, 5))

    def test_validacion_longitud_incorrecta(self):
        """
        Verifica que el método generar lance ValueError si la longitud
        está fuera del rango permitido (4-8).
        """
        # Caso: Longitud muy corta
        with self.assertRaises(ValueError):
            self.generador.generar(3)

        # Caso: Longitud muy larga
        with self.assertRaises(ValueError):
            self.generador.generar(9)

    def test_generacion_estructura_y_reglas(self):
        """
        Prueba de estrés (Fuzzing): Genera múltiples PINs y verifica
        que NINGUNO viole las reglas de adyacencia.
        """
        cantidad_pruebas = 50
        longitud_pin = 6

        for _ in range(cantidad_pruebas):
            pin = self.generador.generar(longitud_pin)

            # 1. Verificar longitud
            self.assertEqual(len(pin), longitud_pin)

            # 2. Verificar que es numérico
            self.assertTrue(pin.isdigit())

            # 3. Verificar reglas internas (no confía solo en el generador)
            for i in range(len(pin) - 1):
                actual = int(pin[i])
                siguiente = int(pin[i+1])

                # No iguales
                self.assertNotEqual(actual, siguiente,
                                    f"Fallo repetición en PIN {pin}")
                # No consecutivos lineales
                self.assertNotEqual(abs(actual - siguiente),
                                    1, f"Fallo consecutivo en PIN {pin}")
                # No circulares
                self.assertNotEqual({actual, siguiente}, {
                                    0, 9}, f"Fallo circular en PIN {pin}")

    def test_entropia_calculo_positivo(self):
        """
        Verifica que el cálculo de entropía devuelva un valor flotante positivo.
        """
        # pylint: disable=protected-access
        entropia = self.generador._calcular_entropia_bits(6)
        self.assertIsInstance(entropia, float)
        self.assertGreater(entropia, 0.0)

    @patch('secrets.choice')
    def test_reintento_por_blacklist(self, mock_secrets):
        """
        Verifica que el sistema reintente si genera un PIN que está en la blacklist.
        Utiliza Mocking para forzar una generación específica.
        """
        # Escenario:
        # Intento 1: Genera "1313".
        #   - 1, 3, 1, 3 son matemáticamente válidos entre sí.
        #   - Pero "1313" está en la Blacklist predeterminada.
        #   - El sistema debe rechazarlo y reintentar.

        # Intento 2: Genera "5151".
        #   - Matemáticamente válido.
        #   - No está en blacklist.
        #   - Debe retornarlo.

        # Mockeamos secrets.choice para que devuelva esta secuencia exacta de dígitos
        mock_secrets.side_effect = [
            '1', '3', '1', '3',  # Primer PIN completo (Rechazado)
            '5', '1', '5', '1'   # Segundo PIN completo (Aceptado)
        ]

        # Nota: El generador llama a secrets.choice primero para el digito inicial
        # y luego para los siguientes candidatos.
        # Asumimos que el candidato deseado siempre está disponible en la lista filtrada.

        pin_resultante = self.generador.generar(4)

        # Verificaciones
        self.assertEqual(pin_resultante, "5151")

        # Verificamos que secrets.choice se llamó 8 veces (4 para el fallido + 4 para el exitoso)
        self.assertEqual(mock_secrets.call_count, 8)


if __name__ == '__main__':
    unittest.main()
