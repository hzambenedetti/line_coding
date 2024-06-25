import tkinter as tk
from tkinter import ttk
import socket
from cryptography import caesar_encrypt
from encode import encode_binary, encode_hdb3
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def encoded_to_signal(message):
    signal = [0] * len(message)
    for i, char in enumerate(message):
        if char == '+':
            signal[i] = 1
        elif char == '-':
            signal[i] = -1
    signal.insert(0, 0)
    return signal

class ServerApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor de Mensagem")

        # Variável para armazenar a mensagem digitada pelo usuário
        self.message = tk.StringVar()

        # Frame para os widgets
        self.main_frame = ttk.Frame(self.root, padding=(20, 10))
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Campo de entrada de texto
        ttk.Label(self.main_frame, text="Digite a mensagem:").grid(row=0, column=0, sticky="w")
        self.entry_message = ttk.Entry(self.main_frame, textvariable=self.message, width=100)
        self.entry_message.grid(row=1, column=0, padx=10, pady=5)

        # Botão de iniciar o servidor
        self.start_button = ttk.Button(self.main_frame, text="Iniciar Servidor", command=self.start_server_thread)
        self.start_button.grid(row=2, column=0, pady=10)

        # Botão de enviar mensagem
        self.send_button = ttk.Button(self.main_frame, text="Enviar Mensagem", command=self.send_message, state=tk.DISABLED)
        self.send_button.grid(row=3, column=0, pady=10)

        # Área para mostrar o status do servidor
        ttk.Label(self.main_frame, text="Status do Servidor:").grid(row=4, column=0, sticky="w")
        self.server_status_text = tk.Text(self.main_frame, wrap=tk.WORD, height=10, width=60)
        self.server_status_text.grid(row=5, column=0, padx=0, pady=5)
        self.server_status_text.config(state=tk.DISABLED)

        # Campos para exibir os diferentes tipos de mensagem
        ttk.Label(self.main_frame, text="Mensagem Original:").grid(row=6, column=0, sticky="w")
        self.original_message_label = ttk.Label(self.main_frame, width=100)
        self.original_message_label.grid(row=7, column=0, padx=10, pady=5)

        ttk.Label(self.main_frame, text="Mensagem Criptografada:").grid(row=8, column=0, sticky="w")
        self.encrypted_message_label = ttk.Label(self.main_frame, width=100)
        self.encrypted_message_label.grid(row=9, column=0, padx=10, pady=5)

        ttk.Label(self.main_frame, text="Mensagem Binária:").grid(row=10, column=0, sticky="w")
        self.binary_message_label = ttk.Label(self.main_frame, width=100)
        self.binary_message_label.grid(row=11, column=0, padx=10, pady=5)

        ttk.Label(self.main_frame, text="Mensagem HDB3:").grid(row=12, column=0, sticky="w")
        self.hdb3_message_label = ttk.Label(self.main_frame, width=100)
        self.hdb3_message_label.grid(row=13, column=0, padx=10, pady=5)

        # Configuração do layout responsivo
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(5, weight=1)

        # Frame para o gráfico
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=2)

        # Socket do servidor e cliente
        self.server_socket = None
        self.client_socket = None

    def start_server_thread(self):
        threading.Thread(target=self.start_server).start()

    def start_server(self):
        self.server_status_text.config(state=tk.NORMAL)
        self.server_status_text.delete(1.0, tk.END)

        try:
            # Criar um socket TCP/IP
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Vincular o socket a um endereço e porta
            self.server_socket.bind(('localhost', 65432))

            # Ouvir por conexões
            self.server_socket.listen()

            self.server_status_text.insert(tk.END, "Servidor esperando por conexões...\n")
            self.server_status_text.update()

            self.start_button.config(state=tk.DISABLED)

            # Aceitar uma nova conexão
            self.client_socket, client_address = self.server_socket.accept()
            self.server_status_text.insert(tk.END, f"Conectado a {client_address}\n")
            self.server_status_text.update()

            self.send_button.config(state=tk.NORMAL)

        except Exception as e:
            self.server_status_text.insert(tk.END, f"Erro: {e}\n")

        self.server_status_text.config(state=tk.DISABLED)

    def send_message(self):
        try:
            message = self.message.get()

            # Criptografar a mensagem
            shift = 4  # Valor de deslocamento para a cifra de César


            # Ativar ou desativar a criptografia

            # Criptografia ativa
            processed_message = caesar_encrypt(message, shift)
            self.server_status_text.insert(tk.END, f"Mensagem criptografada enviada: {processed_message}\n")

            # Critografia desativada
            # processed_message = message

            binary_message = encode_binary(processed_message)
            hdb3_message = encode_hdb3(binary_message)

            self.client_socket.sendall(hdb3_message.encode('utf-8'))

            self.server_status_text.config(state=tk.NORMAL)
            self.server_status_text.insert(tk.END, f"Mensagem enviada: {message}\n")
            self.server_status_text.insert(tk.END, f"Mensagem binária enviada: {binary_message}\n")
            self.server_status_text.insert(tk.END, f"Mensagem HDB3 codificada enviada: {hdb3_message}\n")
            self.server_status_text.config(state=tk.DISABLED)

            self.original_message_label.config(text=message)
            self.encrypted_message_label.config(text=processed_message)
            self.binary_message_label.config(text=binary_message)
            self.hdb3_message_label.config(text=hdb3_message)

            # Exibir o gráfico do sinal codificado
            self.plot_signal(hdb3_message)
        except Exception as e:
            self.server_status_text.config(state=tk.NORMAL)
            self.server_status_text.insert(tk.END, f"Erro ao enviar mensagem: {e}\n")
            self.server_status_text.config(state=tk.DISABLED)

    def plot_signal(self, hdb3_message):
        signal = encoded_to_signal(hdb3_message)
        self.ax.clear()
        self.ax.step(range(len(signal)), signal, where='mid')
        self.ax.axhline(0, color='gray', linestyle='--')
        self.ax.set_ylim(-2, 2)
        self.ax.set_yticks([-1, 0, 1])
        self.ax.set_xlabel("Tempo")
        self.ax.set_ylabel("Nível")
        self.ax.set_title("Sinal Codificado HDB3")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApplication(root)
    root.mainloop()

