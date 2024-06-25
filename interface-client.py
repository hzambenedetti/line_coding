import tkinter as tk
from tkinter import ttk
import socket
from decode import decode_hdb3, binary_to_ascii
from cryptography import caesar_decrypt
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

class ClientApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente de Mensagem")

        # Variáveis para armazenar dados recebidos
        self.hdb3_message = tk.StringVar()
        self.binary_message = tk.StringVar()
        self.encrypted_message = tk.StringVar()
        self.decrypted_message = tk.StringVar()

        # Frame para os widgets
        self.main_frame = ttk.Frame(self.root, padding=(20, 10))
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Campo para exibir a mensagem HDB3 recebida
        ttk.Label(self.main_frame, text="Mensagem HDB3 Recebida:").grid(row=0, column=0, sticky="w")
        self.hdb3_message_label = ttk.Label(self.main_frame, textvariable=self.hdb3_message, width=100)
        self.hdb3_message_label.grid(row=1, column=0, padx=10, pady=5)

        # Campo para exibir a mensagem binária recebida
        ttk.Label(self.main_frame, text="Mensagem Binária Recebida:").grid(row=2, column=0, sticky="w")
        self.binary_message_label = ttk.Label(self.main_frame, textvariable=self.binary_message, width=100)
        self.binary_message_label.grid(row=3, column=0, padx=10, pady=5)

        # Campo para exibir a mensagem criptografada recebida
        ttk.Label(self.main_frame, text="Mensagem Criptografada Recebida:").grid(row=4, column=0, sticky="w")
        self.encrypted_message_label = ttk.Label(self.main_frame, textvariable=self.encrypted_message, width=100)
        self.encrypted_message_label.grid(row=5, column=0, padx=10, pady=5)

        # Campo para exibir a mensagem decifrada
        ttk.Label(self.main_frame, text="Mensagem Decifrada Recebida:").grid(row=6, column=0, sticky="w")
        self.decrypted_message_label = ttk.Label(self.main_frame, textvariable=self.decrypted_message, width=100)
        self.decrypted_message_label.grid(row=7, column=0, padx=10, pady=5)

        # Botão de conectar e receber mensagem
        self.connect_button = ttk.Button(self.main_frame, text="Conectar ao Servidor", command=self.start_client_thread)
        self.connect_button.grid(row=8, column=0, pady=10)

        # Frame para o gráfico
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().grid(row=9, column=0, columnspan=2)

        # Configuração do layout responsivo
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(8, weight=1)

    def start_client_thread(self):
        threading.Thread(target=self.start_client).start()

    def start_client(self):
        try:
            # Criar um socket TCP/IP
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Conectar ao servidor
            self.client_socket.connect(('localhost', 65432))  # Substituir 'IP-SERVER' pelo IP do servidor

            # Desativar o botão de conectar
            self.connect_button.config(state=tk.DISABLED)

            self.receive_messages()
        except Exception as e:
            self.decrypted_message.set(f"Erro: {e}")

    def receive_messages(self):
        while True:
            try:
                # Receber a mensagem do servidor
                hdb3_message = self.client_socket.recv(1024).decode('utf-8')
                if not hdb3_message:
                    break
                self.hdb3_message.set(hdb3_message)

                binary_message = decode_hdb3(hdb3_message)
                self.binary_message.set(binary_message)

                encrypted_message = binary_to_ascii(binary_message)
                self.encrypted_message.set(encrypted_message)

                shift = 4  # O mesmo valor de deslocamento usado para criptografar

                # Ativar ou desativar a criptografia

                # Criptografia ativa
                decrypted_message = caesar_decrypt(encrypted_message, shift)

                # Criptografia desativada
                # decrypted_message = encrypted_message

                self.decrypted_message.set(decrypted_message)

                print(f"HDB3 message received: {hdb3_message}")
                print(f"Binary message received: {binary_message}")
                print(f"Encrypted message received: {encrypted_message}")
                print(f"Received: {decrypted_message}")

                # Exibir o gráfico do sinal codificado
                self.plot_signal(hdb3_message)
            except Exception as e:
                self.decrypted_message.set(f"Erro: {e}")
                break

        # Ativar o botão de conectar novamente
        self.connect_button.config(state=tk.NORMAL)
        self.client_socket.close()

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
    app = ClientApplication(root)
    root.mainloop()

