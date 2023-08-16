import os
from tkinter import Tk, scrolledtext, Button, END, PhotoImage
import subprocess



class GUI:
    def __init__(self, master):
        # Create the main window
        self.master = master
        self.master.title("WiFi Password Extractor")
        self.master.config(bg="light grey")
        script_directory = os.path.dirname(os.path.abspath(__file__))

        if os.name == "nt":  # Windows
            icon_path = os.path.join(script_directory, "resources/icon.ico")
            self.master.iconbitmap(icon_path)

        elif os.name == "posix":  # Linux
            icon_path = os.path.join(script_directory, "resources/icon.png")
            self.master.iconphoto(True, PhotoImage(file=icon_path))

        # Create a button for Wi-Fi password extraction
        self.extract_button = Button(master, text="Extract WiFi Passwords", command=self.extract_wifi_passwords, font=("Arial", 12, "bold"), bg="#000000", fg="#b02aea", relief="flat", borderwidth=0, padx=10, pady=5)
        self.extract_button.pack(pady=(25, 10))
        self.extract_button.bind("<Enter>", self.on_button_hover)
        self.extract_button.bind("<Leave>", self.on_button_leave)

        # Create a box to display the results
        self.results_text = scrolledtext.ScrolledText(master, width=52, height=21, font=("Courier New", 12), state="disabled")
        self.results_text.pack(pady=(30, 10))

        # get screen width and height
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()

        # calculate position x and y coordinates
        x = (ws / 2) - (550 / 2)
        y = (hs / 2) - (530 / 2)

        root.geometry('%dx%d+%d+%d' % (550, 530, x, y))



    def on_button_hover(self, event):
        self.extract_button.config(background='#b02aea', foreground='#fff', relief='ridge', borderwidth=0)


    def on_button_leave(self, event):
        self.extract_button.config(background='#000000', foreground='#b02aea', relief='flat', borderwidth=0)


    def extract_wifi_passwords(self):
        self.results_text.configure(state="normal")
        self.results_text.delete(1.0, END)  # Clear previous results

        self.results_text.insert(END, "{:<27}| {:<}\n".format("WiFi Name", "Password"))
        self.results_text.insert(END, "---------------------------------------------------\n")

        if os.name == "nt":  # Windows
            data = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True, shell=True).stdout.split('\n')
            profiles = [i.split(":")[1][1::] for i in data if "All User Profile" in i]

            for i in profiles:
                results = subprocess.run(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'], capture_output=True, text=True, shell=True).stdout.split('\n')
                passwords = [b.split(":")[1][1::] for b in results if "Key Content" in b]

                try:
                    self.results_text.insert(END, "{:<27}| {:<}\n".format(i, passwords[0]))
                except IndexError:
                    self.results_text.insert(END, "{:<27}| {:<}\n".format(i, ""))


        elif os.name == "posix":  # Linux
            results = subprocess.run(['sudo', 'grep', '-r', '^psk=', '/etc/NetworkManager/system-connections/'], capture_output=True, text=True).stdout.split('\n')
            profiles = [r.split(':')[0].split('/')[4] for r in results if r]

            for i in profiles:
                profile_content = subprocess.run(['sudo', 'cat', f'/etc/NetworkManager/system-connections/{i}'], capture_output=True, text=True).stdout
                password_line = [line for line in profile_content.split('\n') if line.startswith('psk=')]

                if password_line:
                    password = password_line[0].split('=')[1]
                    wifi_name = i.split('.nmconnection')[0]
                    self.results_text.insert(END, "{:<27}| {:<}\n".format(wifi_name, password))

                else:
                    self.results_text.insert(END, "{:<27}| {:<}\n".format(i, ""))


        self.results_text.insert(END, "\n")
        self.results_text.configure(state="disabled")



############################################################################################################################################
############################################################################################################################################

# Start the GUI event loop
root = Tk()
gui = GUI(root)
root.mainloop()