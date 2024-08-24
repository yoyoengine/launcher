"""
    This file is a part of yoyoengine. (https://github.com/zoogies/yoyoengine)
    Copyright (C) 2024  Ryan Zmuda

    Licensed under the MIT license. See LICENSE file in the project root for details.
"""

# Creating GUI's in python is miserable, and I dont even want to mess with
# it right now.

import tkinter as tk
from tkinter import ttk, Frame

import sv_ttk

import backend

class YoyoEngineHub:
    def __init__(self, version):
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("YoyoEngine Hub")
        # self.root.iconbitmap("yoyoengine.ico")
        # self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file='cleanlogo.png'))

        self.tab = "editors"

        self.backend = backend.YoyoEngineHubBackend(version)

        self.update_available = self.backend.check_for_hub_update()
        if(self.update_available):
            url = "https://github.com/yoyoengine/launcher/releases/latest"
            
            def open_update():
                # open the browser to the latest release
                import webbrowser
                webbrowser.open(url)
            
            def ignore_update():
                self.update_available = False
                self.clear()
                self.hub() # TODO

            notification_label = ttk.Label(self.root, text="An update is available!", font=("Roboto", 16))
            notification_label.grid(row=0, column=0, columnspan=2, pady=10)

            ignore_button = ttk.Button(self.root, text="Ignore", width=50, command=ignore_update)
            ignore_button.grid(row=1, column=0, padx=5, pady=5)

            install_button = ttk.Button(self.root, text="Install", width=50, command=open_update)
            install_button.grid(row=1, column=1, padx=5, pady=5)

            self.root.grid_columnconfigure(0, weight=1)
            self.root.grid_columnconfigure(1, weight=1)
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_rowconfigure(1, weight=1)

        else:
            self.platform = self.backend.platform
            if(self.platform != "Linux"):
                self.clear()

                self.frame3 = Frame(self.root, width=300, height=300)
                self.frame3.pack()
                self.error_txt = ttk.Label(self.frame3, text='This program only works on Linux.')
                self.error_txt.pack()
            else:
                self.hub()

                print(self.backend.check_installed_versions())

    def clear(self):
        for i in self.root.winfo_children():
            i.destroy()

    def hub(self):
        self.clear()

        self.root.columnconfigure(0, weight=1)  # Sidebar column (20% width)
        self.root.columnconfigure(1, weight=4)  # Main content column (80% width)
        # self.root.rowconfigure(1, weight=1)  # Make the content area expandable

        # make it so the first row is only as tall as the logo
        self.root.grid_rowconfigure(0, minsize=50)
        self.root.grid_rowconfigure(0, weight=0)

        # logo image up top
        self.logo = tk.PhotoImage(file="../media/smalltextlogo.png")
        self.logo_label = tk.Label(self.root, image=self.logo)
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=0, padx=10, sticky="nw")

        # Make the sidebar rows and columns fill the available space
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_rowconfigure(3, weight=1)  # Make the last row expandable

        # sidebar buttons
        self.editors_btn = ttk.Button(self.root, text="Editors")
        self.editors_btn.grid(row=1, column=0, pady=1, padx=20, sticky="nsew")

        self.settings_btn = ttk.Button(self.root, text="Settings")
        self.settings_btn.grid(row=2, column=0, pady=20, padx=20, sticky="nsew")


        # Main content area
        self.content_frame = tk.Frame(self.root, bg="#171617")
        self.content_frame.grid(row=1, column=1, rowspan=3, sticky="nsew", pady=(0, 0))

        if(self.tab == "editors"):
            pass
        else:
            pass

    def run(self):
        sv_ttk.set_theme("dark")
        self.root.mainloop()