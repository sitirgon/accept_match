from tkinter import *
import threading
import pyautogui
import time
from discord_webhook import DiscordWebhook
import configparser


root = Tk()
root.title('Akcpetowanie meczu')
root.iconbitmap('accept.ico')
root.geometry('500x300')
root.configure(background='#1A1744')

class Main:

    def __init__(self, master):
        self.master = master
        myFrame = Frame(master)
        myFrame.pack()
        self.exit_flag = False

        #buttons
        self.myButton1 = Button(master, text="Akcpetuj mecz",command=self.test, border=2)
        self.myButton1.pack(pady=20)

        # checkboxs
        self.r = StringVar()
        self.myCheckbox1 = Radiobutton(master, text='TOP', font=('Lucida Console', 12), variable=self.r, value='TOP',tristatevalue=0)
        self.myCheckbox1.place(x=395, y=10)
        self.myCheckbox2 = Radiobutton(master, text='JGL', font=('Lucida Console', 12), variable=self.r, value='JGL', tristatevalue=0)
        self.myCheckbox2.place(x=395, y=40)
        self.myCheckbox3 = Radiobutton(master, text='MID', font=('Lucida Console', 12), variable=self.r, value='MID', tristatevalue=0)
        self.myCheckbox3.place(x=395, y=70)
        self.myCheckbox4 = Radiobutton(master, text='ADC', font=('Lucida Console', 12), variable=self.r, value='ADC', tristatevalue=0)
        self.myCheckbox4.place(x=395, y=100)
        self.myCheckbox5 = Radiobutton(master, text='SUP', font=('Lucida Console', 12), variable=self.r, value='SUPP', tristatevalue=0)
        self.myCheckbox5.place(x=395, y=130)

        self.myLabel = Label(master, text='', border=0, background='#1A1744', font=('Lucida Console', 12))
        self.myLabel.pack(pady=20)

        self.myButton2 = Button(master, text='Zatrzymaj szukanie', command=self.stop_thread)
        self.myButton2.place(x=5,y=260)

        self.myButton3 = Button(master, text='Wyjscie', command=self.exit)
        self.myButton3.place(x=395,y=260)

        #config button
        self.myButton1.config(font=('Lucida Console', 12))
        self.myButton2.config(font=('Lucida Console', 12))
        self.myButton3.config(font=('Lucida Console', 12))

    def stop_thread(self):
        self.exit_flag = True

    def exit(self):
        self.exit_flag = True
        self.master.destroy()

    def test(self):
        self.match = threading.Thread(target=self.looking_for, args=(self.r.get(),))
        self.match.start()
    def getContent(self):
        config = c.config_ini['CONFIG']['IDDiscord']
        return config

    def getUrlAPI(self):
        config = c.config_ini['CONFIG']['IDDiscord']
        return config


    def discord_send_message(self):
        webhook = DiscordWebhook(
            url = c.api_url,
            content = c.content)
        webhook.execute()

    def looking_for(self, prefer_role):
        pyautogui.FAILSAFE = False
        self.exit_flag = False
        self.myLabel.config(text='Czekam na mecz...', fg='Yellow')
        path = str(prefer_role) + '.png'
        while True:
            time.sleep(0.2)
            accept = pyautogui.locateCenterOnScreen(r'images\test.png', confidence=0.7)
            role = pyautogui.locateCenterOnScreen("images\\" + path, confidence=0.8)
            if accept != None:
                pyautogui.click(accept)
                self.myLabel.config(text='Mecz zaakcpetowany!', fg='Green')
                self.discord_send_message()
            if accept == None:
                self.myLabel.config(text='Czekam na mecz...', fg='Yellow')
            if role != None:
                time.sleep(3)
                lobby = pyautogui.locateCenterOnScreen(r'images\lobby.png', confidence=0.7)
                if lobby != None:
                    pyautogui.click(lobby)
                    pyautogui.write(f'Can I go {prefer_role}')
                    pyautogui.press('enter')
                    self.myLabel.config(text='Zapytałem o preferowaną role', fg='Purple')
                    break
                self.myLabel.config(text='Odpowiednia linia', fg='Purple')
                break
            if self.exit_flag:
                self.myLabel.config(text='Zatrzymanie szukania', fg='Red')
                break

class Config_File:

    def __init__(self):
        self.config_ini = configparser.ConfigParser()
        if self.config_ini.read('config.ini'):
            self.config_ini.read('config.ini')
            self.content = self.config_ini['CONFIG']['IDDiscord']
            self.api_url = self.config_ini['CONFIG']['DiscordWebHook']
        else:
            self.config_ini['CONFIG'] = {'IDDiscord': '<@ID>',
                                         'DiscordWebHook': 'URLDiscordWebHook'}
            with open('config.ini', 'w', encoding='utf-8') as configfile:
                self.config_ini.write(configfile)

if __name__ == "__main__":
    c = Config_File()
    m = Main(root)
    root.mainloop()