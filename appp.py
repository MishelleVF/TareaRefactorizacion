import csv
import unittest

class CalculaGanador:
    def leerdatos(self, filename):
        """Lee los datos de un archivo CSV y retorna una lista de filas."""
        data = []
        try:
            with open(filename, 'r') as csvfile:
                next(csvfile)
                datareader = csv.reader(csvfile)
                for fila in datareader:
                    if self.dni_valido(fila[3]):
                        data.append(fila)
        except FileNotFoundError:
            print(f"Archivo {filename} no encontrado.")
        return data

    
    # el DNI debe ser valido (8 digitos)
    def dni_valido(self, dni):
        """Valida que el DNI tenga exactamente 8 dígitos."""
        return len(dni) == 8 and dni.isdigit()

    def contar_votos(self, data):
        """Cuenta los votos válidos por candidato."""
        votos_validos = {}
        total_votos_validos = 0
        
        for fila in data:
            candidato = fila[4]
            esvalido = fila[5]
            if esvalido == '1':
                if candidato not in votos_validos:
                    votos_validos[candidato] = 0
                votos_validos[candidato] += 1
                total_votos_validos += 1
        return votos_validos, total_votos_validos

    def obtener_ganador(self, ordenado, total_votos_validos):
        """Obtiene el ganador si tiene más del 50% de los votos válidos."""
        ganador = ordenado[0]
        porcentaje_ganador = (ganador[1] / total_votos_validos) * 100
        # Si hay un candidato con >50% de votos válidos retornar un array con un string con el nombre del ganador
        if porcentaje_ganador > 50:
            return [ganador[0]]
        else:
            return None

    def calcular_ganador(self, data):
        """Calcula el ganador o los candidatos que pasan a la segunda vuelta."""
        votos_validos, total_votos_validos = self.contar_votos(data)
        
        if not total_votos_validos:
            return ["No hay votos válidos"]
        
        ordenado = sorted(votos_validos.items(), key=lambda item: item[1], reverse=True)
        
        ganador = self.obtener_ganador(ordenado, total_votos_validos)
        if ganador:
            return ganador
        
        if len(ordenado) > 1:
            segundo = ordenado[1]
            porcentaje_ganador = (ordenado[0][1] / total_votos_validos) * 100
            porcentaje_segundo = (segundo[1] / total_votos_validos) * 100
            if porcentaje_ganador == 50 and porcentaje_segundo == 50:
                # Si ambos empatan con 50% de los votos se retorna el que apareció primero en el archivo
                # Devuelve el que apareció primero en el archivo
                for fila in data:
                    if fila[4] == ordenado[0][0] or fila[4] == ordenado[1][0]:
                        return [fila[4]]
            # Si no hay un candidato que cumpla la condicion anterior, retornar un array con los dos candidatos que pasan a segunda vuelta
            else:
                return [ordenado[0][0], ordenado[1][0]]            
        else:
            return [ordenado[0][0]]

class TestCalculaGanador(unittest.TestCase):
    def setUp(self):
        self.calcula_ganador = CalculaGanador()
        self.datos = [
            ['Áncash', 'Asunción', 'Acochaca', '40810062', 'Eddie Hinesley', '0'],
            ['Áncash', 'Asunción', 'Acochaca', '57533597', 'Eddie Hinesley', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '86777322', 'Aundrea Grace', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '23017965', 'Aundrea Grace', '1']
        ]

    def test_dni_valido(self):
        self.assertTrue(self.calcula_ganador.dni_valido("40810062"))
        self.assertFalse(self.calcula_ganador.dni_valido("4081006a"))
        self.assertFalse(self.calcula_ganador.dni_valido("408100"))

    def test_calcular_ganador_mayoria(self):
        datos_mayoria = [
            ['Áncash', 'Asunción', 'Acochaca', '57533597', 'Eddie Hinesley', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '57533598', 'Eddie Hinesley', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '57533599', 'Eddie Hinesley', '1']
        ]
        resultado = self.calcula_ganador.calcular_ganador(datos_mayoria)
        self.assertEqual(resultado, ['Eddie Hinesley'])

    def test_calcular_ganador_segunda_vuelta(self):
        resultado = self.calcula_ganador.calcular_ganador(self.datos)
        self.assertEqual(resultado, ['Aundrea Grace'])

    def test_calcular_ganador_empate(self):
        datos_empate = [
            ['Áncash', 'Asunción', 'Acochaca', '57533597', 'Eddie Hinesley', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '57533598', 'Aundrea Grace', '1']
        ]
        resultado = self.calcula_ganador.calcular_ganador(datos_empate)
        self.assertEqual(resultado, ['Eddie Hinesley'])

    def test_leerdatos_archivo_no_existente(self):
        resultado = self.calcula_ganador.leerdatos('test_archivo_inexistente.csv')
        self.assertEqual(resultado, [])

if __name__ == '__main__':
    unittest.main()
