import requests
import json
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
import time
from ecdsa import SigningKey, SECP256k1
import codecs


def sendcoins():
    x = 1


def getmybalance():
    return "42"


def minecoins():
    mininglabelvar.set("please wait while we mine coins")
    miningprogressbar['value'] = 20
    window.update_idletasks()
    time.sleep(.5)
    miningprogressbar['value'] = 40
    window.update_idletasks()
    time.sleep(.5)
    miningprogressbar['value'] = 50
    window.update_idletasks()
    time.sleep(.5)
    miningprogressbar['value'] = 60
    window.update_idletasks()
    time.sleep(.5)
    miningprogressbar['value'] = 80
    window.update_idletasks()
    time.sleep(.5)
    miningprogressbar['value'] = 100
    mininglabelvar.set("1 newbcoin mined")


def on_enter_privkey(e):
    privatekeytext['foreground'] = 'black'


def on_leave_privkey(e):
    privatekeytext['foreground'] = 'white'


def generatewallet():
    x = 3


url = "http://127.0.0.1:5000/api/"


def testfunc():
    response = requests.request("GET", url)
    json_data = json.loads(response.text)
    print(json_data["Blocks"][-1]["BlockNumber"])
    print(json_data["Blocks"][-1]["Amount"])


window = Tk()
window.geometry('1100x800')

##

amountbox = StringVar()
recipientkeybox = StringVar()

amount = Label(window, text="Please enter the ammount to send below")
amount.grid(row=1, column=1)

amountentry = Entry(window, textvariable=amountbox)
amountentry.grid(row=2, column=1)

recipientkey = Label(window, text="Please enter the recipients public key")
recipientkey.grid(row=3, column=1)

recipientkeyentry = Entry(window, textvariable=amountbox)
recipientkeyentry.grid(row=4, column=1)

sendcoinsbutton = Button(window, text="send coins",
                         width=30, command=sendcoins)
sendcoinsbutton.grid(row=5, column=1)

##

welcome = Label(window, text="welcome to newbcoin", font=('Arial', 20))
welcome.grid(row=1, column=3)

balancelabel = Label(window, text="current balance", font=('Arial', 15))
balancelabel.grid(row=2, column=3)

balancevariable = Label(window, text=getmybalance(), font=('Arial', 20))
balancevariable.grid(row=3, column=3)

newbcoinlabel = Label(window, text="NEWBCOIN", font=('Arial', 20))
newbcoinlabel.grid(row=4, column=3)

#####

image1 = Image.open("newbcoin.png")
image1 = image1.resize((475, 475), Image.ANTIALIAS)
test = ImageTk.PhotoImage(image1)
label1 = Label(image=test)
label1.image = test
label1.grid(row=6, column=2)

#####

mininglabelvar = StringVar()
mininglabelvar.set("mining info here")

mininglabel = Label(window, textvariable=mininglabelvar)
mininglabel.grid(row=7, column=1)

miningprogressbar = Progressbar(
    window, orient=HORIZONTAL, length=200, mode='determinate')
miningprogressbar.grid(row=8, column=1)

startminingbutton = Button(window, text="start mining",
                           width=30, command=minecoins)
startminingbutton.grid(row=9, column=1)

testvar = StringVar()
testvar.set("testvar")
testlabel = Label(window, textvariable=testvar)
testlabel.grid(row=10, column=1)
testbutton = Button(window, text="test", width=30, command=testfunc)
testbutton.grid(row=11, column=1)

##

privatekeystringvar = StringVar()
# get privatekey from the secure text file
privktxt = open('walletdata.txt', 'r')
privkstr = privktxt.read()
privktxt.close()
privatekeystringvar.set(privkstr)


publickeystringvar = StringVar()
pubkstr = SigningKey.from_string(
    codecs.decode((privkstr), 'hex'), curve=SECP256k1)
publickeystringvar.set(pubkstr.to_string().hex())

privatekeylabel = Label(window, text="private key \n hover to show key")
privatekeylabel.grid(row=7, column=3)


privatekeytext = Entry(window, textvariable=privatekeystringvar,
                       state='readonly', foreground="white")
privatekeytext.grid(row=8, column=3)
privatekeytext.bind("<Enter>", on_enter_privkey)
privatekeytext.bind("<Leave>", on_leave_privkey)

publickeylabel = Label(window, text="public key")
publickeylabel.grid(row=9, column=3)

publickeytext = Entry(
    window, textvariable=publickeystringvar, state='readonly')
publickeytext.grid(row=10, column=3)

generatewalletbutton = Button(
    window, text="generate wallet", width=30, command=generatewallet)
generatewalletbutton.grid(row=11, column=3)

##

window.mainloop()
