import tkinter as tk
import re
from tkinter import ttk

class Lexer:
    def __init__(self):
        self.RESERVADA = ['for', 'do', 'while', 'if', 'else', 'public', 'static', 'void', 'int','main']
        self.OPERADOR = ['=', '+', '-', '*', '/']
        # self.DELIMITADOR = ['(', ')', '{', '}', ';']
        self.PARENTESISABIERTA = ['(']
        self.PARENTESISCERRADA = [')']
        self.LLAVEABIERTA = ['{']
        self.LLAVECERRADA = ['}']
        self.PUNTOCOMA = [';']
        self.tokens_regex = {
            'RESERVADA': '|'.join(r'\b' + re.escape(keyword) + r'\b' for keyword in self.RESERVADA),
            'OPERADOR': '|'.join(map(re.escape, self.OPERADOR)),
            'PARENTESISABIERTA': '|'.join(map(re.escape, self.PARENTESISABIERTA)),
            'PARENTESISCERRADA': '|'.join(map(re.escape, self.PARENTESISCERRADA)),
            'LLAVEABIERTA': '|'.join(map(re.escape, self.LLAVEABIERTA)),
            'LLAVECERRADA': '|'.join(map(re.escape, self.LLAVECERRADA)),
            'PUNTOCOMA': '|'.join(map(re.escape, self.PUNTOCOMA)),
            'NUMERO': r'\d+(\.\d+)?',
            'IDENTIFICADOR': r'[A-Za-z_]+'
        }
        self.token_patterns = re.compile('|'.join(f'(?P<{t}>{self.tokens_regex[t]})' for t in self.tokens_regex))
        
    def tokenize(self, text):
        tokens = []
        token_count = {}
        lines = text.split('\n')  # Split the input text into lines
        NumeroLinea = 1  # Inicializar el número de línea en 1
        for line in lines:
            line_has_tokens = False  # Flag to check if the line has any tokens
            for match in self.token_patterns.finditer(line):
                line_has_tokens = True
                for token_type, token_value in match.groupdict().items():
                    if token_type == 'IDENTIFICADOR' and token_value and len(token_value) > 1:
                        tokens.append((NumeroLinea, 'ERROR LEXICO', token_value))
                    elif token_type == 'IDENTIFICADOR' and token_value and len(token_value) == 1:
                        tokens.append((NumeroLinea, 'IDENTIFICADOR', token_value))
                    elif token_value:
                        tokens.append((NumeroLinea, token_type, token_value))
            if line_has_tokens:
                NumeroLinea += 1
                
        for NumeroLinea, token_type, token_value in tokens:
            token_count[token_type] = token_count.get(token_type, 0) + 1
        return tokens, token_count


    def analyze(self, text):
        tokens = self.tokenize(text)
        result = "Token\t\tLexema\t\tLinea\n"
        for line_number, token_type, token_value in tokens:
            result += f"{token_type}\t\t{token_value}\t\t{line_number}\n"
        return result

class LexerApp: 
    def __init__(self):  #Define una clase llamda LexerApp para la interfaz grafica de usuario
        self.windows = tk.Tk() #Crea una ventana de la clase
        self.windows.title("Analizador léxico") #Establece el titulo de la ventana

        #Crea una etiqueta para el titulo de la aplicacion
        self.text_label = tk.Label(text="ANALIZADOR LÉXICO", height=2, width=45, font=("Arial", 10, 'bold'))
        self.text_label.pack(pady=5)

        #Crea un cuadro de texto para la entrada de texto
        self.text_input = tk.Text(self.windows, height=8, width=55, font=("Arial", 12))
        self.text_input.pack(pady=5)

        #Crea un marco para los botones
        self.button_frame = tk.Frame(self.windows)
        self.button_frame.pack()

        #crea un boton para realizar el analisis lexico del texto de entrada
        self.analyze_button = tk.Button(self.button_frame, text="Analizar", command=self.analyze_text,  font=("Arial", 10, 'bold'))
        self.analyze_button.grid(row=0, column=0, padx=30, pady=5)

        #crea un boton para limpiar el cuadro de texto
        self.clean_button = tk.Button(self.button_frame, text="Limpiar", command=self.clean_text, font=("Arial", 10, 'bold'))
        self.clean_button.grid(row=0, column=1, padx=30, pady=5)

        self.treeview = ttk.Treeview(self.windows, columns=("Token", "Lexema", "Línea"), show="headings")

        # Configura la alineación de las columnas para centrar el contenido
        self.treeview.column("Token", anchor="center")
        self.treeview.column("Lexema", anchor="center")
        self.treeview.column("Línea", anchor="center")

        self.treeview = ttk.Treeview(self.windows, columns=("Token", "Lexema", "Línea"), show="headings")
        self.treeview.heading("Token", text="Token")
        self.treeview.heading("Lexema", text="Lexema")
        self.treeview.heading("Línea", text="Línea")
        self.treeview.pack()

    def analyze_text(self):  #Define un metodo para realizar el analisis lexico del texto de entrada
        #lexer = Lexer()     #crea una instancia de la clase Lexer
        #text = self.text_input.get("1.0", "end") #Obtiene el texto de entrada del cuadro de texto
        #result = lexer.analyze(text)  #Realiza el analisis lexico utilizando el metodo "analyze" de Lexer
        #self.result_label.config(text=result , justify="center") #Configura la etiqueta de resultados con el resultado del analisis

        lexer = Lexer()
        text = self.text_input.get("1.0", "end")
        result, token_count = lexer.tokenize(text)
        
        # Limpia las entradas existentes en el Treeview
        self.treeview.delete(*self.treeview.get_children())

        # Inserta los resultados en el Treeview
        for line_number, token_type, token_value in result:
            self.treeview.insert("", "end", values=(token_type, token_value, line_number))
        
        count_text = "\n".join(f"{key} = {value}" for key, value in token_count.items())
        self.count_label.config(text=count_text)



    def clean_text(self): #Define un metodo para limpiar el cuadro de texto y la etiqueta de resultados
        self.text_input.delete("1.0", "end") #Borra el contenido del cuadro del texto
        self.result_label.config(text="") #Limpia el contenido de la etiqueta de resultados

  

    def run(self): #Define un metodo para ejecutar la aplicacion de la interfaz grafica
        self.count_label = tk.Label(self.windows, text="", font=("Arial", 12))
        self.count_label.pack(pady=5)

        self.windows.mainloop() #inicia el bucle de la interfaz grafica

app = LexerApp() #Crea una instancia de la clase Lexer app
app.run()   #Ejecuta la aplicacion de la interfaz grafica llamando al metodo "Run"
