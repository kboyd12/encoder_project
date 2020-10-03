import tkinter as tk
import pymsgbox
from datetime import datetime
import csv
from tkinter.filedialog import asksaveasfilename, askopenfilename
import time

window = tk.Tk()
window.title("Encoder App")


class App():
    # Saves a new run to a file
    def save_file(self):
        entry = entry_field.get()
        if entry == '':
            pymsgbox.alert('Enter the Entry Location')
            return

        self.filepath = asksaveasfilename(
            defaultextension='txt',
            filetypes=[("Text Files", "*.txt"), ('All Files', '*.*')]
        )
        if not self.filepath:
            return

        # Create a file and init with date and time
        with open(self.filepath, 'w') as txt_file:
            txt_file.write(f'Date: {datetime.now().strftime("%m/%d/%Y")}\n')
            txt_file.write(f'Entry Location: {entry}\n\n')

    def encoder(self):
        # Replace with encoder value instead of time
        string = datetime.today().now().strftime('%H:%M:%S %p')
        encoder_frame.config(text=string)
        # Resets every 1000ms
        encoder_frame.after(1000, self.encoder)
        return string

    def open_file(self):
        # Opens an already existing file to edit
        self.filepath = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ('All Files', '*.*')]
        )

    def mark(self):
        # Tries to write to the filepath, but if no file has been saved or opened then alerts to create one.
        try:
            comment = txtbox.get('1.0', 'end-1c')
            encoder_value = self.encoder()
            arr = [encoder_value, comment]

            with open(self.filepath, 'a') as runfile:
                writer = csv.writer(runfile, delimiter='\t')
                writer.writerow(arr)

            txtbox.delete('1.0', 'end')
        except:
            pymsgbox.alert('No run has been started. Click Start Run')


if __name__ == "__main__":
    # Instantiates the class as an object "run"
    run = App()

    # Creates a frame for the buttons and binds it to the sides
    buttons_frame = tk.Frame(window)
    buttons_frame.grid(row=0, column=0, sticky=tk.W+tk.E)

    # Making and displaying buttons
    btn_start_run = tk.Button(buttons_frame, text='Start Run',
                              command=run.save_file)
    btn_start_run.grid(row=0, column=0, padx=(10), pady=10)

    btn_mark = tk.Button(buttons_frame, text='Mark', command=run.mark)
    btn_mark.grid(row=0, column=1, padx=(10), pady=10)

    btn_open = tk.Button(buttons_frame, text='Open File',
                         command=run.open_file)
    btn_open.grid(row=0, column=2, padx=10, pady=10)

    # Making and displaying entry label/field
    entry_label = tk.Label(buttons_frame, text='Entry Location')
    entry_label.grid(row=0, column=3, padx=10, pady=10)

    entry_field = tk.Entry(buttons_frame)
    entry_field.grid(row=0, column=4, padx=(5), pady=10)

    # Run the encoder
    encoder_frame = tk.Label(buttons_frame, font=(
        'calibri', 32, 'bold'), background='grey', fg='black')
    encoder_frame.grid(row=1, column=0, columnspan=5,
                       padx=10, pady=5, sticky='nsew')
    # Update the encoder
    run.encoder()

    # Create a frame for the comment box
    group1 = tk.LabelFrame(window, text="Comments", padx=5, pady=5)
    # Create a comment box that spans 3 columns and reconfigures itself when scaled
    group1.grid(row=1, column=0, columnspan=3, padx=10,
                pady=10, sticky=tk.E+tk.W+tk.N+tk.S)
    # Reconfigure when scaled
    window.columnconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)

    group1.rowconfigure(0, weight=1)
    group1.columnconfigure(0, weight=1)

    # Create the textbox
    txtbox = tk.Text(group1, width=40, height=10)
    txtbox.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)

    window.mainloop()
