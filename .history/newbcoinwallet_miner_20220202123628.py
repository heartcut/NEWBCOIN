from urllib import response
import requests
import json
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
import time
from ecdsa import SigningKey, SECP256k1
import codecs
import random

url = "http://127.0.0.1:5000/api/"
statusurl = "http://127.0.0.1:5000/api/statuscheck/"
balanceurl = "http://127.0.0.1:5000/api/balancecheck?pubkey="
solveurl = "http://127.0.0.1:5000/api/solveblock?pubkey="  # also need &answer=
lastblockurl = "http://127.0.0.1:5000/api/getlastblock/"


window = Tk()
window.geometry('1100x800')

privatekeystringvar = StringVar()
publickeystringvar = StringVar()
# get privatekey from the secure text file
privktxt = open('walletdata.txt', 'r')
try:
    privkstr = SigningKey.from_string(codecs.decode(
        privktxt.read(), 'hex'), curve=SECP256k1)
except:
    privkeyhex = hex(random.getrandbits(256))[2:]
    f = open('walletdata.txt', 'w')
    f.write(privkeyhex)
    f.close()
    privktxt = open('walletdata.txt', 'r')
    privkstr = SigningKey.from_string(codecs.decode(
        privktxt.read(), 'hex'), curve=SECP256k1)
    privktxt.close()
    privatekeystringvar.set(privkstr.to_string().hex())
    pubkstr = privkstr.get_verifying_key()
    publickeystringvar.set(pubkstr.to_string().hex())


privktxt.close()
privatekeystringvar.set(privkstr.to_string().hex())
pubkstr = privkstr.get_verifying_key()
publickeystringvar.set(pubkstr.to_string().hex())

try:
    statusfromapi = requests.request("GET", statusurl)
    statusvar = True
except:
    statusvar = False


def sendcoins():
    x = 1


def getmybalance():
    if statusvar:
        balanceresponse = requests.request(
            "GET", balanceurl+str(publickeystringvar.get()))
        balance = json.loads(balanceresponse.text)
        return balance
    else:
        return "no connection"


def minecoins():
    mininglabelvar.set("please wait while we mine coins")
    # miningprogressbar['value'] = 20
    # window.update_idletasks()
    # time.sleep(.5)
    # miningprogressbar['value'] = 40
    # window.update_idletasks()
    # time.sleep(.5)
    # miningprogressbar['value'] = 50
    # window.update_idletasks()
    # time.sleep(.5)
    # miningprogressbar['value'] = 60
    # window.update_idletasks()
    # time.sleep(.5)
    # miningprogressbar['value'] = 80
    # window.update_idletasks()
    # time.sleep(.5)
    # miningprogressbar['value'] = 100
    response = requests.request("GET", lastblockurl)
    json_data = json.loads(response.text)
    print(json_data["Blocks"][-1]["BlockNumber"])
    mininglabelvar.set("1 newbcoin mined")


def on_enter_privkey(e):
    privatekeytext['foreground'] = 'black'


def on_leave_privkey(e):
    privatekeytext['foreground'] = 'white'


l2text = StringVar()


def generatewallet():
    genwalletpopup = Toplevel()
    genwalletpopup.geometry('500x500')

    l = Label(genwalletpopup,
              text="are you sure you want to generate new keys? \n this will delete any current keys")
    l.grid(row=0, column=1)

    gen = Button(genwalletpopup, text="Yes i want new ones",
                 command=makenewkey)
    gen.grid(row=1, column=0)

    closebutt = Button(genwalletpopup, text="close this window",
                       command=genwalletpopup.destroy
                       )
    closebutt.grid(row=1, column=2)

    l2 = Label(genwalletpopup,
               textvariable=l2text)
    l2.grid(row=2, column=0)


def makenewkey():
    privkeyhex = hex(random.getrandbits(256))[2:]
    f = open('walletdata.txt', 'w')
    f.write(privkeyhex)
    f.close()
    privktxt = open('walletdata.txt', 'r')
    privkstr = SigningKey.from_string(codecs.decode(
        privktxt.read(), 'hex'), curve=SECP256k1)
    privktxt.close()
    privatekeystringvar.set(privkstr.to_string().hex())
    pubkstr = privkstr.get_verifying_key()
    publickeystringvar.set(pubkstr.to_string().hex())
    l2text.set("new keys generated")


def testfunc():
    if statusvar:
        response = requests.request("GET", url)
        json_data = json.loads(response.text)
        print(json_data["Blocks"][-1]["BlockNumber"])
    else:
        print("hmm")


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

coinimage = Image.open("newbcoin.png")
coinimage = coinimage .resize((475, 475), Image.ANTIALIAS)
tkcoinimage = ImageTk.PhotoImage(coinimage)
coinimagelabel = Label(image=tkcoinimage)
coinimagelabel.image = tkcoinimage
coinimagelabel.grid(row=6, column=2)

statusstr = StringVar()
if statusvar:
    statusstr.set("newbcoin server status: connected")
else:
    statusstr.set("newbcoin server status: not connected")

statuslabel = Label(
    window, textvariable=statusstr, font=('Arial', 15))
statuslabel.grid(row=6, column=3)
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
