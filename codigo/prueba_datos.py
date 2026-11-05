import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.verificar_datos import validar


class TestDataset(unittest.TestCase):
    def test_validacion_general(self):
        errores, resumen = validar()
        self.assertEqual(errores, [])
        self.assertEqual(resumen["total"], 6101)
        self.assertEqual(resumen["categorias"]["motos_combustion"], 1099)
        self.assertEqual(resumen["categorias"]["motos_electricas"], 2201)
        self.assertEqual(resumen["categorias"]["bicicletas_electricas"], 2576)
        self.assertEqual(resumen["categorias"]["patinetes"], 225)

    def test_corte_26(self):
        _, resumen = validar()
        self.assertEqual(resumen["cortes"]["2026-10-26"], 30)


if __name__ == "__main__":
    unittest.main()
