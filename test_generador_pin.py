"""
Auditoría de Seguridad y Pruebas Unitarias para el Generador de PIN.
Archivo: test_generador_pin.py
"""

import unittest
from unittest.mock import patch

# Importamos la clase desde tu archivo principal 'generador_pin.py'
from generador_pin import GeneradorPinBlindado


class TestAuditoriaPinBlindado(unittest.TestCase):
    """
    Suite de pruebas de seguridad y funcionalidad.
    Cubre: Matemáticas, Topología, Blacklist y Timing Attacks.
    """

    def setUp(self):
        self.generador = GeneradorPinBlindado()

    # ==========================================
    # CAPA 1 y 2: LÓGICA (Matemática + Física)
    # ==========================================

    def test_01_seguridad_matematica_rechaza_consecutivos(self):
        """Verifica que se rechacen secuencias numéricas (1-2, 9-8)."""
        # pylint: disable=protected-access
        self.assertFalse(self.generador._es_transicion_valida("1", "2"))
        self.assertFalse(self.generador._es_transicion_valida("9", "8"))
        self.assertFalse(self.generador._es_transicion_valida("5", "5"))

    def test_02_seguridad_topologica_rechaza_adyacentes_fisicos(self):
        """
        Verifica el BLINDAJE FÍSICO.
        Debe rechazar vecinos de teclado (arriba/abajo/lados) aunque no sean consecutivos.
        """
        # pylint: disable=protected-access
        
        # 1 está arriba del 4
        self.assertFalse(
            self.generador._es_transicion_valida("4", "1"),
            "FALLO: Permitió '1-4' (Vecinos verticales)"
        )
        # 0 está debajo del 8
        self.assertFalse(
            self.generador._es_transicion_valida("0", "8"),
            "FALLO: Permitió '8-0' (Vecinos verticales)"
        )
        # 5 está al lado del 6 (Consecutivo y físico)
        self.assertFalse(self.generador._es_transicion_valida("6", "5"))

    def test_03_transiciones_seguras_permitidas(self):
        """Verifica que SÍ permita saltos complejos (caballo ajedrez, distantes)."""
        # pylint: disable=protected-access
        # 1 y 6 son diagonales lejanas -> Válido
        self.assertTrue(self.generador._es_transicion_valida("6", "1"))
        # 7 y 3 esquinas opuestas -> Válido
        self.assertTrue(self.generador._es_transicion_valida("3", "7"))

    # ==========================================
    # CAPA 3: DEFENSA SEMÁNTICA (Blacklist)
    # ==========================================

    def test_04_blacklist_incluye_patrones(self):
        """Verifica carga de blacklist."""
        self.assertIn("1379", self.generador.blacklist) # Esquinas
        self.assertIn("2025", self.generador.blacklist) # Año

    @patch('secrets.choice')
    def test_05_mecanismo_reintento_por_blacklist(self, mock_secrets):
        """Simula generación de PIN prohibido y fuerza reintento."""
        # Intento 1: 2-5-8-0 (Cruz -> Blacklist)
        # Intento 2: 1-6-0-3 (Válido)
        mock_secrets.side_effect = ['2','5','8','0', '1','6','0','3']

        pin = self.generador.generar(4)
        self.assertEqual(pin, "1603")
        self.assertEqual(mock_secrets.call_count, 8)

    # ==========================================
    # CAPA 4: VALIDACIÓN CRIPTOGRÁFICA
    # ==========================================

    def test_06_validacion_segura_hmac(self):
        """Verifica comparación de tiempo constante."""
        pin_real = "927451"
        self.assertTrue(self.generador.validar_pin_seguro(pin_real, pin_real))
        self.assertFalse(self.generador.validar_pin_seguro("000000", pin_real))

    # ==========================================
    # INTEGRACIÓN
    # ==========================================

    def test_07_fuzzing_generacion_masiva(self):
        """Genera 100 PINs y audita cada transición."""
        for _ in range(100):
            pin = self.generador.generar(6)
            self.assertEqual(len(pin), 6)
            
            for i in range(len(pin)-1):
                es_valido = self.generador._es_transicion_valida(pin[i+1], pin[i]) # pylint: disable=protected-access
                self.assertTrue(es_valido, f"PIN inseguro: {pin}")

    def test_08_validacion_limites(self):
        """Verifica errores en longitudes inválidas."""
        with self.assertRaises(ValueError):
            self.generador.generar(3)
        with self.assertRaises(ValueError):
            self.generador.generar(9)


if __name__ == '__main__':
    unittest.main(verbosity=2)
