from django.test import TestCase
from wagtail.models import Page

class SimpleTest(TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)

def minha_funcao(nome):
  return f"Olá, {nome}!"

class MinhaFuncaoTest(TestCase):
    def test_minha_funcao(self):
        resultado = minha_funcao("Mundo")
        self.assertEqual(resultado, "Olá, Mundo!")