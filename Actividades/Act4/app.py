import tkinter as tk
import re
from difflib import get_close_matches
from tkinter import scrolledtext

class Aplicacion:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Analizador Léxico y Sintáctico")
        self.ventana.geometry("1000x600")
        
        self.entrada = scrolledtext.ScrolledText(ventana, width=60, height=10)
        self.entrada.pack()
        
        self.boton = tk.Button(ventana, text="Analizar", command=self.analizar)
        self.boton.pack()
        
        self.lexico = scrolledtext.ScrolledText(ventana, width=50, height=15)
        self.lexico.pack(side="left")
        self.lexico.insert(tk.INSERT, "Léxico\n")
        
        self.sintactico = scrolledtext.ScrolledText(ventana, width=50, height=15)
        self.sintactico.pack(side="right")
        self.sintactico.insert(tk.INSERT, "Sintáctico\n")
        
    def analizar(self):
        entrada = self.entrada.get("1.0", tk.END).strip()
        
        self.lexico.delete("1.0", tk.END)
        self.lexico.insert(tk.INSERT, "Léxico\n")
        
        self.sintactico.delete("1.0", tk.END)
        self.sintactico.insert(tk.INSERT, "Sintáctico\n")
        
        palabras_reservadas = ["for", "system","out","printl"]
        operadores = ["=", "<=", "+", "++"]
        delimitadores = ["(", ")", "{", "}"]
        comillas = ['"']
        puntos = ["."]
        
        lineas = entrada.split('\n')
        regex = re.compile(r'(\W)')
        
        # Análisis Léxico
        for num_linea, linea in enumerate(lineas, start=1):
            tokens = [token for token in re.split(regex, linea) if token.strip()]
            for token in tokens:
                matches = get_close_matches(token, palabras_reservadas, n=1, cutoff=0.8)
                if any(reservada in token for reservada in palabras_reservadas):
                    self.lexico.insert(tk.INSERT, f"Palabra Reservada: {token}, Línea: {num_linea}\n")
                elif any(operador in token for operador in operadores):
                    self.lexico.insert(tk.INSERT, f"Operador: {token}, Línea: {num_linea}\n")
                elif any(delimitador in token for delimitador in delimitadores):
                    self.lexico.insert(tk.INSERT, f"Delimitador: {token}, Línea: {num_linea}\n")
                elif any(comilla in token for comilla in comillas):
                    self.lexico.insert(tk.INSERT, f"Comilla: {token}, Línea: {num_linea}\n")
                elif any(punto in token for punto in puntos):
                    self.lexico.insert(tk.INSERT, f"Punto: {token}, Línea: {num_linea}\n")
                elif token.isnumeric():
                    self.lexico.insert(tk.INSERT, f"Número: {token}, Línea: {num_linea}\n")
                elif token.startswith("\"") and token.endswith("\""):
                    self.lexico.insert(tk.INSERT, f"Cadena de Texto: {token}, Línea: {num_linea}\n")
                else:
                    self.lexico.insert(tk.INSERT, f"Identificador: {token}, Línea: {num_linea}\n")
        
        # Análisis Sintáctico Básico
        for num_linea, linea in enumerate(lineas, start=1):
            if '..' in linea:
                    self.sintactico.insert(tk.INSERT, f"Error Sintáctico: Existe un punto de más en {token} en línea {num_linea}\n")
                    continue  # Continuar con el siguiente token
                    
            tokens = [token for token in re.split(regex, linea) if token.strip()]
            for token in tokens:
                matches = get_close_matches(token, palabras_reservadas, n=1, cutoff=0.7)  # Ajustado el cutoff para más flexibilidad
                if matches and token != matches[0]:
                    self.sintactico.insert(tk.INSERT, f"Error Sintáctico: Falta una o más letras en {token}, debería ser {matches[0]} en línea {num_linea}\n")
                    continue


ventana = tk.Tk()
app = Aplicacion(ventana)
ventana.mainloop()
