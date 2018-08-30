import tkinter as tk
import psutil

import asyncio
from concurrent.futures import ThreadPoolExecutor

FileIOPool = ThreadPoolExecutor(8)

from tkinter import *
from tkinter import messagebox
import asyncio
import threading
import random
import time

import tkinter as tk
from tkinter.font import Font

def demo():
    root = Tk()
    root.title("WareCloud")

    root.configure(background='SteelBlue1')
    root.columnconfigure(1, weight=1)

    nb_of_columns = 2  # to be replaced by the relevant number
    titleframe = tk.Frame(root, bg="blue")
    titleframe.grid(row=0, column=0, columnspan=nb_of_columns, sticky='ew')


    titlelabel = tk.Label(titleframe, text="my Title", fg="blue4", bg="gray80")
    titlelabel.grid(row=0, column=1)

    # other widgets on the same row:
    tk.Button(titleframe, text='Ok').grid(row=0, column=2)

    # title = tk.Label(titleframe, text="my Title", fg="blue4", bg="white")
    # title.grid(row=1, column=1)


    root.geometry('800x460')

    # lab = Label(root)
    # lab.pack()
    # t = Text()
    # t.grid()

    def callback():
        return

    # b = Button(root, text="SEND", command=callback)
    # b.grid(row=0, column=0)
    #
    # b2 = Button(root, text="SEND2", command=callback)
    # b2.grid(row=1, column=1)

    # def clock():
    #     t.delete('1.0', END)
    #     with open("AgentWareCloud.log") as myfile:
    #         t.insert("1.0", myfile.read())
    #     root.after(1000, clock) # run itself again after 1000 ms

    # run first time
    # clock()


    root.mainloop()

if __name__ == "__main__":
    demo()
