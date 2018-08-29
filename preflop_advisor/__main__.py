#!/usr/bin/env python3

import tkinter as tk
from gui import MainWindow


def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop


if (__name__ == '__main__'):
    main()
