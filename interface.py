import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import encode

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Criptografia de Mensagem")
        
        # Variável para armazenar a mensagem digitada pelo usuário
        self.message = tk.StringVar()
        
        # Frame para os widgets
        self.main_frame = ttk.Frame(self.root, padding=(20, 10))
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Campo de entrada de texto
        ttk.Label(self.main_frame, text="Digite a mensagem:").grid(row=0, column=0, sticky="w")
        self.entry_message = ttk.Entry(self.main_frame, textvariable=self.message, width=100)
        self.entry_message.grid(row=1, column=0, padx=10, pady=5)
        
        # Botão de criptografia
        self.encrypt_button = ttk.Checkbutton(self.main_frame, text="Ativar Criptografia", command=self.switch_encription)
        self.encrypt_button.grid(row=1, column=1, padx=10, pady=5)
        
        # Área para mostrar a mensagem codificada em binário
        ttk.Label(self.main_frame, text="Mensagem codificada em binário:").grid(row=2, column=0, sticky="w")
        self.binary_message_label = ttk.Label(self.main_frame, text="")
        self.binary_message_label.grid(row=3, column=0, padx=10, pady=5)
        
        # Gráfico para mostrar o sinal digital
        self.figure, self.ax = plt.subplots(figsize=(20, 8))
        plt.grid()
        # self.ax.set_axis_off()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=5, padx=10, pady=5)
        
        # Botão de enviar
        self.send_button = ttk.Button(self.main_frame, text="Enviar", command=self.send_message)
        self.send_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Configuração do layout responsivo
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(4, weight=1)

        #local variables
        self.encrypt_message_var = False
        
    def encrypt_message(self):
        message = self.message.get()
        if message:
            # Converter a mensagem para binário
            binary_message = ' '.join(format(ord(char), '08b') for char in message)
            self.binary_message_label.config(text=binary_message)
            
            # Plotar o sinal digital (0s e 1s) no gráfico
            digital_signal = [int(bit) for char in binary_message.split() for bit in char]
            self.ax.clear()
            self.ax.grid()
            self.ax.plot(digital_signal, color='blue', marker='o', markersize=5)
            self.ax.set_xlim(-0.5, len(digital_signal) - 0.5)
            self.ax.set_ylim(-0.5, 1.5)
            self.ax.set_yticks([0, 1])
            self.ax.set_xticks(range(len(digital_signal)))
            self.canvas.draw()
    
    def plot_signal(self, message):
        signal = self.gen_signal(message)

        self.ax.clear()
        self.ax.grid()
        self.ax.plot(signal, color='red', marker='o')
        self.canvas.draw()
        

    def gen_signal(self, message):
        binary_string = encode.encode_binary(message)
        hdb3_string = encode.encode_hdb3(binary_string)
        signal = encode.encoded_to_signal(hdb3_string)

        return signal

    def switch_encription(self):
        self.encrypt_message_var = not self.encrypt_message_var
        print(self.encrypt_message_var)

    def send_message(self):
        message = self.message.get()
        self.plot_signal(message)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

