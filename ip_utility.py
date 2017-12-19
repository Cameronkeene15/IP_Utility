import tkinter
import subprocess


class Network:

    def __init__(self):
        self.config = self.get_config()

    def set_interface(self, interface, ip, subnet, gateway=None):
        if gateway:
            process = subprocess.run('netsh interface ipv4 set address "%s" static %s %s' % (interface, ip, subnet))
        else:
            process = subprocess.run('netsh interface ipv4 set address "%s" static %s %s %s' %
                                     (interface, ip, subnet, gateway))
        return process.returncode

    def get_interfaces(self, config):
        # TODO: get interface names using regex
        pass

    def get_wifi_info(self, config):
        # TODO: use regex to get WIFI ip address and subnet
        pass

    def get_ethernet_info(self, config):
        # TODO: use regex to get LAN ip address and subnet
        pass

    def get_config(self):
        # runs the OS command which returns the computers network interfaces and their respective information
        process = subprocess.run('netsh interface ipv4 show config', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # runcode being 0 means there were no process errors
        if process.runcode == 0:
            # returns the stdout response from the command as a string (stdout must be decoded from bytes)
            return process.stdout.decode('utf-8')
        else:
            # TODO: figure out how to handle stderr if runcode is not 0
            return None


def hello():
    print("hello")


class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        # example code for a menu bar. Might not even use this.

        # self.menubar = tkinter.Menu(root)

        # self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        # self.filemenu.add_command(label="Open", command=hello)
        # self.filemenu.add_command(label="Save", command=hello)
        # self.filemenu.add_separator()
        # self.filemenu.add_command(label="Exit", command=root.quit)
        # self.menubar.add_cascade(label="File", menu=self.filemenu)
        #
        # self.editmenu = tkinter.Menu(self.menubar, tearoff=0)
        # self.editmenu.add_command(label="Cut", command=hello)
        # self.editmenu.add_command(label="Copy", command=hello)
        # self.editmenu.add_command(label="Paste", command=hello)
        # self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        #
        # self.helpmenu = tkinter.Menu(self.menubar, tearoff=0)
        # self.helpmenu.add_command(label="About", command=hello)
        # self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        #
        # root.config(menu=self.menubar)

        self.interface_select = tkinter.BooleanVar()
        self.interface_select.set(False)

        self.lan_interface = tkinter.Radiobutton(self, text='LAN', value=False, variable=self.interface_select)
        self.lan_interface.grid(row=0, column=0)

        self.wifi_interface = tkinter.Radiobutton(self, text='WIFI', value=True, variable=self.interface_select)
        self.wifi_interface.grid(row=0, column=1)

        self.ip_address_label = tkinter.Label(self, text='IP Addr:')
        self.ip_address_label.grid(row=1, column=0, sticky='e')

        self.ip_address_value = tkinter.Entry(self)
        self.ip_address_value.grid(row=1, column=1, columnspan=2, sticky='we')

        self.subnet_label = tkinter.Label(self, text='Subnet:')
        self.subnet_label.grid(row=2, column=0, sticky='e')

        self.subnet_value = tkinter.Entry(self)
        self.subnet_value.grid(row=2, column=1, columnspan=2, sticky='we')

        self.gateway_label = tkinter.Label(self, text='Gateway:')
        self.gateway_label.grid(row=3, column=0, sticky='e')

        self.gateway_value = tkinter.Entry(self)
        self.gateway_value.grid(row=3, column=1, columnspan=2, sticky='we')

        self.change = tkinter.Button(self, text='Change IP', command=self.change_ip)
        self.change.grid(row=4, column=0, sticky='we')

        self.load = tkinter.Button(self, text='Load IP', command=self.change_ip)
        self.load.grid(row=4, column=1, sticky='we')

        self.save = tkinter.Button(self, text='Save IP', command=self.change_ip)
        self.save.grid(row=4, column=2, sticky='we')

    def change_ip(self):
        print('ip_address: ' + self.ip_address_value.get())
        print('subnet: ' + self.subnet_value.get())


if __name__ == '__main__':

    # calls the network class which finds out all necessary information about interfaces and IP's
#    network_info = Network()

    # starts the GUI
    root = tkinter.Tk()
    app = Application(master=root)
    root.geometry('250x150')
    root.maxsize(width=250, height=150)
    root.minsize(width=250, height=150)
    app.mainloop()
