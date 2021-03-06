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
import hashlib
from datetime import datetime

url = "http://api.newbcoin.page/api/"
statusurl = "http://api.newbcoin.page/api/statuscheck/"
balanceurl = "http://api.newbcoin.page/api/balancecheck?pubkey="
solveurl = "http://api.newbcoin.page/api/solveblock?pubkey="  # also need &answer=
lastblockurl = "http://api.newbcoin.page/api/getlastblock/"
transurl = "http://api.newbcoin.page/api/dotransaction?"


window = Tk()
window.geometry('1100x800')

privatekeystringvar = StringVar()
publickeystringvar = StringVar()
balancestr = StringVar()
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


amountbox = StringVar()
recipientkeybox = StringVar()


def sendcoins():

    transhash = "Reciever:"+str(recipientkeybox.get()) + \
        ",Amount:"+str(amountbox.get())
    print(transhash)
    transhash = privkstr.sign(str.encode(transhash))
    print(str(recipientkeybox.get()))
    print(str(amountbox.get()))
    send = requests.request("GET", transurl+"mykey=" +
                            str(publickeystringvar.get())+"&reckey=" +
                            str(recipientkeybox.get())+"&amount=" +
                            str(amountbox.get())+"&transactionhash=" +
                            str(transhash.hex()))
    time.sleep(1)
    if str(json.loads(send.text)) == "True":
        sendcoinpopup = Toplevel()
        sendcoinpopup.geometry('500x500')

        closebutt = Button(sendcoinpopup, text="close this window",
                           command=sendcoinpopup.destroy
                           )
        closebutt.grid(row=1, column=2)
        l2 = Label(sendcoinpopup,
                   text="trans worked")
        l2.grid(row=0, column=1)
    else:
        sendcoinpopup = Toplevel()
        sendcoinpopup.geometry('500x500')

        closebutt = Button(sendcoinpopup, text="close this window",
                           command=sendcoinpopup.destroy
                           )
        closebutt.grid(row=1, column=2)
        l2 = Label(sendcoinpopup,
                   text="transaction failed")
        l2.grid(row=0, column=1)


def getmybalance():
    if statusvar:
        balanceresponse = requests.request(
            "GET", balanceurl+str(publickeystringvar.get()))
        balance = json.loads(balanceresponse.text)
        balancestr.set(balance)
    else:
        balancestr.set("balance not available")


def minecoins():
    mininglabelvar.set("please wait while we mine coins")
    window.update_idletasks()
    miningprogressbar['value'] = 0
    window.update_idletasks()
    if statusvar:
        gotthecoin = False
        response = requests.request("GET", lastblockurl)
        json_data = json.loads(response.text)
        answerhash = json_data["POWhash"]
        guess = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        try:
            for q in range(52):
                miningprogressbar['value'] = q*2
                window.update_idletasks()
                for w in range(52):
                    for e in range(52):
                        for r in range(52):
                            if answerhash == (hashlib.md5(str(guess[q]+guess[w]+guess[e]+guess[r]).encode())).hexdigest():
                                miningprogressbar['value'] = 100
                                window.update_idletasks()
                                trytoanswer = requests.request(
                                    "GET", solveurl+str(publickeystringvar.get())+"&answer="+str(guess[q]+guess[w]+guess[e]+guess[r]))
                                if str(json.loads(trytoanswer.text)) == "True":
                                    gotthecoin = True
                                    raise StopIteration
                                else:
                                    gotthecoin = False
                                    raise StopIteration
        except StopIteration:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            if gotthecoin:
                mininglabelvar.set("you just mined one coin "+current_time)
                getmybalance()
                window.update_idletasks()
            else:
                mininglabelvar.set(
                    "please wait while we mine coins "+current_time)
                window.update_idletasks()


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


##
amount = Label(window, text="Please enter the ammount to send below")
amount.grid(row=1, column=1)

amountentry = Entry(window, textvariable=amountbox)
amountentry.grid(row=2, column=1)

recipientkey = Label(window, text="Please enter the recipients public key")
recipientkey.grid(row=3, column=1)

recipientkeyentry = Entry(window, textvariable=recipientkeybox)
recipientkeyentry.grid(row=4, column=1)

sendcoinsbutton = Button(window, text="send coins",
                         width=30, command=sendcoins)
sendcoinsbutton.grid(row=5, column=1)

##

welcome = Label(window, text="welcome to newbcoin", font=('Arial', 20))
welcome.grid(row=1, column=3)

balancelabel = Label(window, text="current balance", font=('Arial', 15))
balancelabel.grid(row=2, column=3)

getmybalance()
balancevariable = Label(window, textvariable=balancestr, font=('Arial', 20))
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
