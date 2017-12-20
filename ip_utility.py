import tkinter
import subprocess


class Network:

    def __init__(self):
        self.config = self.get_config()

    def set_interface(self, interface, ip, subnet, gateway=None):
        if gateway:
            process = subprocess.run('netsh interface ipv4 set address "%s" static %s %s %s' %
                                     (interface, ip, subnet, gateway))
        else:
            process = subprocess.run('netsh interface ipv4 set address "%s" static %s %s' %
                                     (interface, ip, subnet))
        dns_process = subprocess.run('netsh interface ipv4 set dnsservers "%s" static %s primary' % (interface, '8.8.8.8'))
        return process.returncode, dns_process.returncode

    def set_dhcp(self, interface):
        # TODO: fix setting interface to DHCP. Returns DCHP is already enabled on this interface when called
        process = subprocess.run('netsh interface ipv4 set address name="%s" source=dhcp' % interface)
        dns_process = subprocess.run('netsh interface ipv4 set dnsservers "%s" source=dhcp' % interface)

        return process.returncode, dns_process.returncode

    def check_for_local_interface(self):
        if "Local Area Connection" in self.config:
            print("found lan interface")
            return True
        else:
            return False

    def check_for_wifi_interface(self):
        if "Wireless Network Connection" in self.config:
            print("found wifi interface")
            return True
        else:
            return False

    def get_ethernet_info(self, config):
        # TODO: use regex to get LAN ip address and subnet
        pass

    def get_config(self):
        # runs the OS command which returns the computers network interfaces and their respective information
        process = subprocess.run('netsh interface ipv4 show config', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # runcode being 0 means there were no process errors
        if process.returncode == 0:
            # returns the stdout response from the command as a string (stdout must be decoded from bytes)
            print(process.stdout.decode('utf-8'))
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


        self.network = Network()

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

        self.static_select = tkinter.BooleanVar()
        self.static_select.set(True)

        self.lan_interface = tkinter.Radiobutton(self, text='LAN', value=False, variable=self.interface_select)
        self.lan_interface.grid(row=0, column=0)

        self.wifi_interface = tkinter.Radiobutton(self, text='WIFI', value=True, variable=self.interface_select)
        self.wifi_interface.grid(row=0, column=1)

        self.static = tkinter.Radiobutton(self, text='Static', value=True, variable=self.static_select, command=self.toggle_hide)
        self.static.grid(row=1, column=0)

        self.dhcp = tkinter.Radiobutton(self, text='DHCP', value=False, variable=self.static_select, command=self.toggle_hide)
        self.dhcp.grid(row=1, column=1)

        self.ip_address_label = tkinter.Label(self, text='IP Addr:')
        self.ip_address_label.grid(row=2, column=0, sticky='e')

        self.ip_address_value = tkinter.Entry(self)
        self.ip_address_value.grid(row=2, column=1, columnspan=2, sticky='we')

        self.subnet_label = tkinter.Label(self, text='Subnet:')
        self.subnet_label.grid(row=3, column=0, sticky='e')

        self.subnet_value = tkinter.Entry(self)
        self.subnet_value.grid(row=3, column=1, columnspan=2, sticky='we')

        self.gateway_label = tkinter.Label(self, text='Gateway:')
        self.gateway_label.grid(row=4, column=0, sticky='e')

        self.gateway_value = tkinter.Entry(self)
        self.gateway_value.grid(row=4, column=1, columnspan=2, sticky='we')

        self.change = tkinter.Button(self, text='Change IP', command=self.change_ip)
        self.change.grid(row=5, column=0, sticky='we')

        self.load = tkinter.Button(self, text='Load IP', command=self.change_ip)
        self.load.grid(row=5, column=1, sticky='we')

        self.save = tkinter.Button(self, text='Save IP', command=self.change_ip)
        self.save.grid(row=5, column=2, sticky='we')


    def toggle_hide(self):
        if self.static_select.get():
            self.ip_address_value['state'] = 'normal'
            self.subnet_value['state'] = 'normal'
            self.gateway_value['state'] = 'normal'
        else:
            self.ip_address_value['state'] = 'disabled'
            self.subnet_value['state'] = 'disabled'
            self.gateway_value['state'] = 'disabled'
            self.network.set_dhcp("Local Area Connection")

    def change_ip(self):
        print('ip_address: ' + self.ip_address_value.get())
        print('subnet: ' + self.subnet_value.get())
        print('gateway: ' + self.gateway_value.get())

        if self.network.check_for_local_interface():
            self.network.set_interface("Local Area Connection", self.ip_address_value.get(), self.subnet_value.get(),
                                  self.gateway_value.get())


if __name__ == '__main__':

    # starts the GUI
    root = tkinter.Tk()
    app = Application(master=root)
    root.geometry('250x150')
    root.maxsize(width=250, height=150)
    root.minsize(width=250, height=150)
    app.mainloop()
