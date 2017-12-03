import tkinter
import os

def wifi_ip_address():
    pass

def ethernet_ip_address():
    response = os.system('netsh interface ipv4 show config')
    print(response)

def set_wifi_ip_address():
    pass

def set_ethernet_ip_address():
    pass









class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.interface_select = tkinter.Radiobutton()
        self.interface_select['text'] = 'WIFI'
        self.interface_select.grid(row=0, column=0)


        self.ip_address_label = tkinter.Label(self)
        self.ip_address_label['text'] = 'IP Addr:'
        self.ip_address_label.grid(row=1, column=0)

        self.ip_address_value = tkinter.Entry(self)
        self.ip_address_value.grid(row=1, column=1)

        self.subnet_label = tkinter.Label(self)
        self.subnet_label['text'] = 'Subnet:'
        self.subnet_label.grid(row=2, column=0)

        self.subnet_value = tkinter.Entry(self)
        self.subnet_value.grid(row=2, column=1)


        self.submit = tkinter.Button(self)
        self.submit["text"] = 'Change IP'
        self.submit["command"] = self.change_ip
        self.submit.grid(row=3, column=2)



    def change_ip(self):
        print('ip_address: ' + self.ip_address_value.get())
        print('subnet: ' + self.subnet_value.get())


if __name__ == '__main__':
    ethernet_ip_address()
    set_wifi_ip_address()

    root = tkinter.Tk()
    app = Application(master=root)
    root.geometry('400x300')
    root.maxsize(width=300, height=300)
    root.minsize(width=300, height=200)
    app.mainloop()
