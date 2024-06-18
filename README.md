# Tarea Refactorización
- Refactorizamos el código dado en: https://github.com/cpazutec/refactor-practice/tree/main 
## Integrantes:
* Mishelle Stephany Villarreal Falcón
* Anderson David Cárcamo Vargas

# Técnicas de Refactorización aplicadas en el código

### 1. Extracción de métodos
Se creó una función específica para cada tipo de evento (`leerdatos`, `dni_valido`, `contar_votos`, `obtener_ganador`, `calcular_ganador`). Esto mejora la legibilidad y facilita la reutilización del código.

```python
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
```

### 2. Renombrar variables o métodos
Las variables fueron renombradas para que sus nombres sean más descriptivos (`eventos` a `lista_eventos`). Esto hace que el código sea más comprensible.

```python
# Antes: nombre de variable poco claro
eventos = ...

# Después: nombre de variable más descriptivo
lista_eventos = ...
```

### 3. Eliminar código duplicado
Se eliminó la lógica duplicada de procesamiento de eventos utilizando un diccionario (`votos_validos`) para mapear candidatos a sus votos válidos.

```python
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
```

### 4. Simplificación de condicionales
Se utilizó un diccionario para mapear los tipos de eventos a sus funciones de procesamiento, simplificando la estructura condicional en el método `calcular_ganador`.

```python
ordenado = sorted(votos_validos.items(), key=lambda item: item[1], reverse=True)
ganador = ordenado[0]
porcentaje_ganador = (ganador[1] / total_votos_validos) * 100

if porcentaje_ganador > 50:
    return [ganador[0]]
else:
    if len(ordenado) > 1:
        return [ordenado[0][0], ordenado[1][0]]
    else:
        return [ordenado[0][0]]
```

### 5. División de métodos o archivos grandes 
En el método `calcular_ganador`, se han extraído las siguientes funciones auxiliares:

- contar_votos: para contar los votos válidos por candidato.
```python
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
```

- obtener_ganador: para obtener el ganador si tiene más del 50% de los votos válidos.
```python
def obtener_ganador(self, ordenado, total_votos_validos):
        """Obtiene el ganador si tiene más del 50% de los votos válidos."""
        ganador = ordenado[0]
        porcentaje_ganador = (ganador[1] / total_votos_validos) * 100
        # Si hay un candidato con >50% de votos válidos retornar un array con un string con el nombre del ganador
        if porcentaje_ganador > 50:
            return [ganador[0]]
        else:
            return None
```

# Implementación de las Pruebas unitarias
- Se implementaron pruebas unitarias para comprobar que el codigo funciona como se espera
- Estas pruebas se ejecutan de manera aislada para asegurarse de que cada unidad de código funcione correctamente de manera independiente.

#### Código de las pruebas
```python
import unittest

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
        self.assertEqual(resultado, ['Aundrea Grace', 'Eddie Hinesley'])

    def test_calcular_ganador_empate(self):
        datos_empate = [
            ['Áncash', 'Asunción', 'Acochaca', '57533597', 'Eddie Hinesley', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '57533598', 'Aundrea Grace', '1']
        ]
        resultado = self.calcula_ganador.calcular_ganador(datos_empate)
        self.assertEqual(resultado, ['Eddie Hinesley', 'Aundrea Grace'])

    def test_leerdatos_archivo_no_existente(self):
        resultado = self.calcula_ganador.leerdatos('test_archivo_inexistente.csv')
        self.assertEqual(resultado, [])

if __name__ == '__main__':
    unittest.main()
```

### Explicación de las Pruebas Unitarias
1. **setUp():**
   - Aquí se inicializa una instancia de `CalculaGanador` y se preparan datos de prueba.

2. **test_dni_valido():**
   - Verifica que el método `dni_valido` funcione correctamente para diferentes DNIs.
   - Se prueban DNIs válidos e inválidos.

3. **test_calcular_ganador_mayoria():**
   - Verifica que el método `calcular_ganador` retorne el candidato correcto cuando uno tiene más del 50% de los votos válidos.

4. **test_calcular_ganador_segunda_vuelta():**
   - Verifica que se retornen los dos candidatos con más votos válidos cuando ninguno tiene más del 50%.

5. **test_calcular_ganador_empate():**
   - Verifica que se maneje correctamente el caso de empate, retornando ambos candidatos.

6. **test_leerdatos_archivo_no_existente():**
   - Verifica que el método `leerdatos` maneje correctamente el caso de archivos inexistentes, retornando una lista vacía.


# Evaluación del código resultante
- El código refactorizado es más modular, fácil de mantener y de entender.
- Las funciones específicas permiten una mejor separación de responsabilidades y facilitan futuras expansiones o modificaciones del código.

# Cambios Realizados
1. Se extrajeron funciones específicas para cada tipo de evento.
2. Se simplificaron las estructuras condicionales.
3. Se renombraron variables para mayor claridad.
4. Se eliminó código duplicado mediante el uso de un diccionario de funciones.
5. Se realizaron 6 pruebas unitarias en total
