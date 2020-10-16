import csv
import numpy as np
import tkinter as tk
from datetime import datetime
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pymsgbox
import picamera
import time


class App():
    def __init__(self):
        """Initialize the App class to start with the camera and overlay on"""
        self.camera_on()

        self.overlay = np.zeros((720, 1280, 3), dtype=np.uint8)
        self.overlay[360, :, :] = 0xFF
        self.overlay[:, 640, :] = 0xFF
        self.over = camera.add_overlay(self.overlay.tobytes(), size=(
            1280, 720), layer=3, alpha=30, fullscreen=False, window=self.window_size)

        self.overlay_on = True
        self.is_recording = False

    def save_file(self):
        """Saves a new run to a file"""
        entry = entry_field.get()
        if entry == '':
            pymsgbox.alert('Enter the Entry Location')
            return

        self.filepath = asksaveasfilename(
            defaultextension='.txt',
            filetypes=[("Text Files", "*.txt"), ('All Files', '*.*')]
        )
        if not self.filepath:
            return

        # Create a file and init with date and time
        with open(self.filepath, 'w') as txt_file:
            txt_file.write(f'Date: {datetime.now().strftime("%m/%d/%Y")}\n')
            txt_file.write(f'Entry Location: {entry}\n\n')

    def encoder(self):
        """Replace with encoder value instead of time"""
        string = datetime.today().now().strftime('%H:%M:%S %p')
        encoder_frame.config(text=string)
        # Resets every 1000ms
        encoder_frame.after(1000, self.encoder)
        return string

        # TODO poll the arduino for value to start, set as baseline. Display the delta between current value and baseline as
        # distance. Pass that delta variable to the mark function or just return it and call inside mark like it's doing now.
        # Will probably implement in separate file and import

    def open_file(self):
        """Opens an already existing file to edit"""
        self.filepath = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ('All Files', '*.*')]
        )

    def mark(self):
        """Tries to write to the filepath, but if no file has been saved or opened then
        alerts to create one."""
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

    def camera_on(self):
        """Uses preview of picamera to display video, changes window size in preview.window"""
        camera.resolution = (1280, 720)
        camera.framerate = 30
        camera.sensor_mode = 6
        camera.start_preview()
        camera.preview.fullscreen = False
        camera.preview.window = (
            int((screen_width - camera.resolution[0])/2), 0, 1280, int(screen_height/1.5))
        self.window_size = camera.preview.window

    def camera_overlay(self):
        """Checks to see if overlay is present and turns it on/off"""
        if self.overlay_on:
            camera.remove_overlay(self.over)

            self.overlay_on = False
        else:
            # alpha changes transparency of overlay
            self.over = camera.add_overlay(self.overlay.tobytes(
            ), layer=3, alpha=30, fullscreen=False, window=self.window_size)

            self.overlay_on = True

    def record(self):
        """Recording functionality, asks location to save file, default extension is .h264. Need an mp4 converter functionality"""
        if not self.is_recording:
            record_filepath = asksaveasfilename(
                defaultextension='.h264',
                filetypes=[("h264 Files", "*.h264"), ('All Files', '*.*')]
            )
            if not record_filepath:
                return

            camera.start_recording(record_filepath)
            self.is_recording = True
        else:
            camera.stop_recording()
            self.is_recording = False


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Encoder App")
    # Change background color
    window['bg'] = '#B47676'

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    camera = picamera.PiCamera()

    # Instantiates the class as an object "run"
    run = App()

    # Creates a frame for the buttons and binds it to the sides
    buttons_frame = tk.Frame(window, bg='#B47676')
    buttons_frame.grid(row=0, column=0, sticky='ew')

    # Making and displaying buttons
    btn_record = tk.Button(
        buttons_frame,
        text='Record',
        font=('calibri', 12),
        command=run.record,
        relief=tk.RAISED,
        highlightthickness=0
    )
    btn_record.grid(row=0, column=6, padx=(10), pady=10)

    btn_camera_overlay = tk.Button(
        buttons_frame,
        text='Camera Overlay (On/Off)',
        font=('calibri', 12),
        command=run.camera_overlay,
        relief=tk.RAISED,
        highlightthickness=0
    )
    btn_camera_overlay.grid(row=0, column=5, padx=(10), pady=10)

    btn_start_run = tk.Button(
        buttons_frame,
        text='Start Run',
        font=('calibri', 12),
        command=run.save_file,
        relief=tk.RAISED,
        highlightthickness=0
    )
    btn_start_run.grid(row=0, column=0, padx=(10), pady=10)

    btn_mark = tk.Button(
        buttons_frame,
        text='Mark',
        command=run.mark,
        relief=tk.RAISED,
        highlightthickness=0,
        font=('calibri', 12)
    )
    btn_mark.grid(row=0, column=1, padx=(10), pady=10)

    btn_open = tk.Button(
        buttons_frame,
        text='Open File',
        command=run.open_file,
        highlightthickness=0,
        relief=tk.RAISED,
        font=('calibri', 12)
    )
    btn_open.grid(row=0, column=2, padx=10, pady=10)

    # Making and displaying entry label/field
    entry_label = tk.Label(
        buttons_frame,
        text='Entry Location',
        bg='#B47676',
        font=('calibri', 12, 'bold')
    )
    entry_label.grid(row=0, column=3, padx=10, pady=10)

    entry_field = tk.Entry(
        buttons_frame,
        highlightbackground='#B47676',
        bd=3,
        relief=tk.SUNKEN,
        highlightthickness=0
    )
    entry_field.grid(row=0, column=4, padx=(5), pady=10)

    # Run the encoder
    encoder_frame = tk.Label(
        buttons_frame,
        font=('calibri', 32, 'bold'),
        background='grey',
        fg='black',
        bd=3
    )
    encoder_frame.grid(row=1, column=0, columnspan=5,
                       padx=10, pady=5, sticky='nsew')
    # Update the encoder
    run.encoder()

    # Create a frame for the comment box
    group1 = tk.LabelFrame(
        window,
        text="Comments",
        padx=5,
        pady=5,
        font=('calibri', 20, 'bold'),
        borderwidth=3,
        bg='#B47676',
        highlightthickness=0,
        relief=tk.RIDGE
    )
    # Create a comment box that spans 3 columns and reconfigures itself when scaled
    group1.grid(row=1, column=0, columnspan=3, padx=10,
                pady=10, sticky='nswe')

    # Reconfigure when scaled
    window.columnconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)

    group1.rowconfigure(0, weight=1)
    group1.columnconfigure(0, weight=1)

    # Create the textbox
    txtbox = tk.Text(
        group1,
        width=40,
        height=10,
        font=('calibri', 12),
        relief=tk.SUNKEN,
        highlightthickness=0,
        bd=4
    )
    txtbox.grid(row=0, column=0, sticky='nswe')

    # Where to open and size of the window
    w = 950
    h = 275
    x = screen_width/2 - w/2
    y = screen_height - h*1.15

    window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    window.mainloop()
