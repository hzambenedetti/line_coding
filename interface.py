import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
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
        self.binary_message_text = tk.Text(self.main_frame, wrap=tk.WORD, height=10, width=60)
        self.binary_message_text.grid(row=3, column=0, padx=0, pady=5)
        self.binary_message_text.config(state=tk.DISABLED)
        
        # Gráfico para mostrar o sinal digital
        #self.figure, self.ax = plt.subplots(figsize=(10, 4))
        #plt.grid()
        # self.ax.set_axis_off()
        #self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        #self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.grid(row=4, column=0, columnspan=2, padx=0, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.canvas = tk.Canvas(self.canvas_frame, width=1200, height=400)
        self.scroll_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_x = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.figure, self.ax = Figure(figsize=(20, 4)), None
        self.ax = self.figure.add_subplot(111)
        self.plot_canvas = FigureCanvasTkAgg(self.figure, master=self.canvas)
        self.plot_canvas.draw()
        
        self.plot_widget = self.plot_canvas.get_tk_widget()
        self.plot_widget.pack()
        
        self.canvas.create_window((0, 0), window=self.plot_widget, anchor="nw")
        self.plot_widget.bind("<Configure>", self.on_configure)
        
        # Botão de enviar
        self.send_button = ttk.Button(self.main_frame, text="Enviar", command=self.send_message)
        self.send_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Configuração do layout responsivo
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(4, weight=1)

        #local variables
        self.encrypt_message_var = False
    
    def plot_signal(self, message):
        signal = self.gen_signal(message)

        self.ax.clear()
        self.ax.grid()
        self.ax.step(range(len(signal)), signal ,color='red', marker = 'o')
        self.ax.set_yticks([-1,0,1])
        self.plot_canvas.draw()
        self.on_configure(None)

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
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
        bin_message = encode.encode_binary(message)
        self.binary_message_text.config(state=tk.NORMAL)
        self.binary_message_text.delete(1.0, tk.END)
        self.binary_message_text.insert(tk.END, bin_message)
        self.binary_message_text.config(state=tk.DISABLED)
        self.plot_signal(message)
    
    def limit_message(message):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

