
from python.downloader.instagramPostDownloader import downloadAsset
from tkinter import Button, Entry, Listbox, Tk
from tkinter.constants import BOTH, LEFT
from instagramPostDownloader import *


root = Tk()
root.geometry("300x300")
def inputWindow(root):
    strlist = []
    url = Entry(root, width=35)
    url.grid(row=0, column=0)
    def returnVal():
        return downloadAsset(url.get())

    konfirmasi = Button(root,text="konfirmasi", command=returnVal, width=10)
    konfirmasi.grid(row=0, column=1)
    return True

inputWindow(root)







root.mainloop()