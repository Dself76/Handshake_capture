import tkinter as tk
from threading import Thread
import capture_handshake
import parse_packets

class HandshakeCapturer:
    def __init__(self, master):
        self.master = master
        self.interface = tk.StringVar()
        self.bssid = tk.StringVar()
        self.channel = tk.IntVar(value=1)
        self.write_file = 'handshake.cap'
        self.handshake = None

        tk.Label(master, text='Wireless Interface:').pack()
        tk.Entry(master, textvariable=self.interface, width=30).pack()

        tk.Label(master, text='AP MAC Address:').pack()
        tk.Entry(master, textvariable=self.bssid, width=30).pack()

        tk.Label(master, text='Channel:').pack()
        tk.Entry(master, textvariable=self.channel, width=10).pack()

        tk.Button(master, text='Start Capture', command=self.start_capture).pack()
        tk.Label(master, text='', textvariable=self.status).pack()

        tk.Label(master, text='Handshake:').pack()
        self.handshake_text = tk.Text(master, height=10, width=30, wrap='word')
        self.handshake_text.pack()

    def start_capture(self):
        self.status.set('Capturing handshake...')
        thread = Thread(target=self.capture_and_parse)
        thread.start()

    def capture_and_parse(self):
        try:
            capture_handshake.capture_handshake(self.interface.get(), self.bssid.get(), self.channel.get(), self.write_file)
            handshake = parse_packets.parse_packets(self.write_file)
            self.handshake = handshake
            self.display_handshake()
            print(f'Handshake captured: {handshake}')
        except KeyboardInterrupt:
            print('Exiting...')
        except Exception as e:
            print(f'Error: {e}')

    def display_handshake(self):
        if self.handshake:
            self.handshake_text.config(state='normal')
            self.handshake_text.delete('1.0', 'end')
            for packet in self.handshake:
                self.handshake_text.insert('end', str(packet) + '\n')
            self.handshake_text.config(state='disabled')

root = tk.Tk()
app = HandshakeCapturer(root)
root.mainloop()