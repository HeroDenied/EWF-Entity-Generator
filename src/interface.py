class Ui():
    def __init__(self) -> None:
        import tkinter as tk
        self.root = tk.Tk()
        self.input_label = tk.LabelFrame(self.root, text='Nome da Entidade')
        self.input_entry = tk.Entry(self.input_label)
        self.button_runp = tk.Button(self.input_label, text='Gerar Entidade')

    def RunRootConfiguration(self, rbc):
        self.root.title('Gerador de Entidade')
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.input_label.grid(column=0, row=0, padx=10, pady=10)
        self.input_entry.grid(column=0, row=0, padx=10, pady=10)
        self.button_runp.grid(column=0, row=1, padx=5, pady=5)
        self.button_runp.config(
            command=lambda: rbc(self))

    def CheckEntry(self):
        while True:
            if self.input_entry.get() == '':
                self.button_runp.config(state='disabled')
            else:
                self.button_runp.config(state='normal')

    def Start(self, run_button_command):
        self.RunRootConfiguration(run_button_command)
        self.root.mainloop()

    def Close(self):
        self.root.destroy()
