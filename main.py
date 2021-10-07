import tkinter as tk
from tkinter import ttk
import psutil, platform


def get_size(bytes, suffix="B"):
    """Make memory value more intuitive

    Args:
        bytes (int): memory size
        suffix (str, optional): conversion prefix. Defaults to "B".

    Returns:
        str: converted value
    
    >>> get_size(1000)
    '1000.00 B'
    
    >>> get_size(2654)
    '2.59 KB'
    
    >>> get_size(1024, suffix='K')
    '1.00 KK'

    >>> get_size(2049, suffix='M')
    '2.00 KM'
    
    >>> get_size(755848, suffix='G')
    '738.13 KG'
    
    >>> get_size(955582648, suffix='T')
    '911.31 MT'
    """

    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor


class DeviceState(tk.LabelFrame):
    """
        Device info interface
    """

    def __init__(self, *args, **kw):
        """
            Create view
        """

        tk.LabelFrame.__init__(self, *args, **kw)
        self.pack(expand=1, fill='both', padx=10, pady=10)
        self.master.option_add('*Foreground', '#777FFF')
        self.master.option_add('*Background', '#FFFFFF')
        self.master.wm_attributes('-topmost', 1)
        self.master.resizable(0, 0)
        self.master.wm_overrideredirect(True)


        uname = platform.uname()

        if uname.system == 'darwin':
            self.master.wm_overrideredirect(False)

        # SYSTEME
        frame1 = tk.LabelFrame(self)
        frame1.grid(row=1, column=1, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=5)

        name = tk.Label(frame1, anchor='w', text=' Systeme:')
        name.grid(row=1, column=1, sticky='ew')
        name = tk.Label(frame1, text=uname.system, anchor='e')
        name.grid(row=1, column=2, padx='50 0', sticky='ew')

        arch = tk.Label(frame1, anchor='w', text=' Machine:')
        arch.grid(row=2, column=1, sticky='ew')
        arch = tk.Label(frame1, text=uname.machine, anchor='e')
        arch.grid(row=2, column=2, padx='50 0', sticky='ew')

        proc = tk.Label(frame1, anchor='w', text=' Processor:')
        proc.grid(row=3, column=1, sticky='ew')
        proc = tk.Label(frame1, text=uname.processor, anchor='e')
        proc.grid(row=3, column=2, padx='50 0', sticky='ew')

        ttlc = tk.Label(frame1, anchor='w', text=' Total Core:')
        ttlc.grid(row=4, column=1, sticky='ew')
        ttlc = tk.Label(frame1, text=psutil.cpu_count(logical=True), anchor='e')
        ttlc.grid(row=4, column=2, padx='50 0', sticky='ew')
    
        cpuu = tk.Label(frame1, anchor='w', text=' CPU Usage:')
        cpuu.grid(row=5, column=1, sticky='ew')
        self.cpuu = tk.Label(frame1, text=f'{psutil.cpu_percent()} %', anchor='e')
        self.cpuu.grid(row=5, column=2, padx='50 0', sticky='ew')


        # RAM INFO
        sysram = psutil.virtual_memory()

        frame2 = tk.LabelFrame(self)
        frame2.grid(row=1, column=2, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=5)

        name = tk.Label(frame2, text=' RAM INFO ')
        name.grid(row=1, column=1, columnspan=2, sticky='ew')

        total = tk.Label(frame2, anchor='w', text=' Total:')
        total.grid(row=2, column=1, sticky='ew')
        total = tk.Label(frame2, text=get_size(sysram.total), anchor='e')
        total.grid(row=2, column=2, padx='50 0', sticky='ew')

        disp = tk.Label(frame2, anchor='w', text=' Disponible:')
        disp.grid(row=3, column=1, sticky='ew')
        self.disp = tk.Label(frame2, text=get_size(sysram.available), anchor='e')
        self.disp.grid(row=3, column=2, padx='50 0', sticky='ew')

        used = tk.Label(frame2, anchor='w', text=' Utilisé:')
        used.grid(row=4, column=1, sticky='ew')
        self.used = tk.Label(frame2, text=get_size(sysram.used), anchor='e')
        self.used.grid(row=4, column=2, padx='50 0', sticky='ew')
    
        perc = tk.Label(frame2, anchor='w', text=' Percentage:')
        perc.grid(row=5, column=1, sticky='ew')
        self.perc = tk.Label(frame2, text=f"{sysram.percent} %", anchor='e')
        self.perc.grid(row=5, column=2, padx='50 0', sticky='ew')


        # DISK
        self.nbook = ttk.Notebook(self)
        self.nbook.grid(row=2, column=1, columnspan=2, sticky='nsew', padx=5, pady=5, ipadx=5, ipady=5)


        ##########################################################################################
        
        self.dico_nbook = {}
        datas_row = psutil.disk_partitions()


        for p in [disk for disk in datas_row if 'sda' in disk.device]:

            frm1 = tk.Frame(self.nbook)

            ftype_ = tk.Label(frm1, anchor='w', text=' Type sys fichier:')
            ftype_.grid(row=1, column=1, sticky='ew', pady='10 0')
            ftype = tk.Label(frm1, text=p.fstype, anchor='e')
            ftype.grid(row=1, column=2, sticky='ew', padx='210 0', pady='10 0')

            try:
                partition_usage = psutil.disk_usage(p.mountpoint)
            except PermissionError:
                # au cas ou le disque qui n'est pas prêt
                continue

            total_ = tk.Label(frm1, anchor='w', text=' Taille total:')
            total_.grid(row=2, column=1, sticky='ew')
            total = tk.Label(frm1, text=get_size(partition_usage.total), anchor='e')
            total.grid(row=2, column=2, sticky='ew', padx='210 0')

            used_ = tk.Label(frm1, anchor='w', text=' Utilisé:')
            used_.grid(row=3, column=1, sticky='ew')
            used = tk.Label(frm1, text=get_size(partition_usage.used), anchor='e')
            used.grid(row=3, column=2, sticky='ew', padx='210 0')
        
            disp_ = tk.Label(frm1, anchor='w', text=' Disponible:')
            disp_.grid(row=4, column=1, sticky='ew')
            disp = tk.Label(frm1, text=get_size(partition_usage.free), anchor='e')
            disp.grid(row=4, column=2, sticky='ew', padx='210 0')

            perc_ = tk.Label(frm1, anchor='w', text=' Pourcentage:')
            perc_.grid(row=4, column=1, sticky='ew')
            perc = tk.Label(frm1, text=f"{partition_usage.percent} %", anchor='e')
            perc.grid(row=4, column=2, sticky='ew', padx='210 0')

            self.nbook.add(frm1, text=f'{p.device}', padding='0.1i', sticky='nsew')

            self.dico_nbook[p.device] = {
                'main': frm1,
                'used': used,
                'disp': disp,
                'perc': perc,
            }

        # Network info
        
        ip_info = {}

        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET' and 'wlp3s0' == interface_name:
                    ip_info['interface'] = interface_name
                    ip_info['ip_adresse'] = address.address
                    ip_info['netmask'] = address.netmask
                    ip_info['broadcast'] = address.broadcast
    

        net_frame = tk.LabelFrame(self)
        net_frame.grid(
            row=3,
            padx=5,
            pady=5,
            ipady=5,
            ipadx=5,
            column=1,
            columnspan=2,
            sticky='nsew'
        )

        if ip_info:
            info_net = tk.Label(net_frame, text=' Interface ')
            info_net.grid(row=1, column=1, sticky='ew')
            info_net = tk.Label(net_frame, text=' IP Adresse ')
            info_net.grid(row=1, column=2, sticky='ew')
            info_net = tk.Label(net_frame, text=' Netmask ')
            info_net.grid(row=1, column=3, sticky='ew')
            info_net = tk.Label(net_frame, text=' Broadcast ')
            info_net.grid(row=1, column=4, sticky='ew')

            info_netv = tk.Label(net_frame, text=ip_info['interface'])
            info_netv.grid(row=2, column=1, sticky='ew', ipadx=5, padx=3)
            info_netv = tk.Label(net_frame, text=ip_info['ip_adresse'])
            info_netv.grid(row=2, column=2, sticky='ew', ipadx=5, padx=3)
            info_netv = tk.Label(net_frame, text=ip_info['netmask'])
            info_netv.grid(row=2, column=3, sticky='ew', ipadx=5, padx=3)
            info_netv = tk.Label(net_frame, text=ip_info['broadcast'])
            info_netv.grid(row=2, column=4, sticky='ew', ipadx=5, padx=3)

        _info = tk.Label(net_frame, text="Use <Ctrl+clic> to exit", fg='#F50', justify='center', anchor='center')
        _info.grid(row=3, column=1, columnspan=4, sticky='ew', ipadx=5, padx=3)


        # self.master.bind('<Leave>', self.mouse_leave)
        # self.master.bind('<Motion>', self.mouse_enter)
        self.master.bind('<B1-Motion>', self.leftMove)
        self.master.bind('<Button-1>', self.leftDown)
        self.master.bind('<ButtonRelease-1>', self.leftUp)
        self.master.bind('<Control-Button-1>', self.rightDown)
        self.master.bind('<Button-3>', self.premier_plan)

        self.x = tk.IntVar(value=0)
        self.y = tk.IntVar(value=0)
        self.moving = tk.IntVar(value=0)
        self.status = tk.IntVar(value=1)

        # Refresh data after 1s
        self.changes()

    def changes(self):
        self.master.after(1000, self.changes)

        # SYSTEME
        self.cpuu.configure(text=f'{psutil.cpu_percent()} %')

        # RAM
        sysram = psutil.virtual_memory()
        self.disp.configure(text=get_size(sysram.available))
        self.used.configure(text=get_size(sysram.used))
        self.perc.configure(text=f"{sysram.percent} %")

        # Device
        datas_row = psutil.disk_partitions()
        a_conserver = []

        for p in [disk for disk in datas_row if 'sda' in disk.device]:
            try:
                partition_usage = psutil.disk_usage(p.mountpoint)
            except (PermissionError, AssertionError) as e:
                continue

            a_conserver.append(p.device)

            if self.dico_nbook.get(p.device):
                self.dico_nbook[p.device].get('used').configure(text=get_size(partition_usage.used))
                self.dico_nbook[p.device].get('disp').configure(text=get_size(partition_usage.free))
                self.dico_nbook[p.device].get('perc').configure(text=f"{partition_usage.percent} %")
            else:
                frm1 = tk.Frame(self.nbook)

                ftype_ = tk.Label(frm1, anchor='w', text=' Type sys fichier:')
                ftype_.grid(row=1, column=1, sticky='ew', pady='10 0')
                ftype = tk.Label(frm1, text=p.fstype, anchor='e')
                ftype.grid(row=1, column=2, sticky='ew', padx='210 0', pady='10 0')

                try:
                    partition_usage = psutil.disk_usage(p.mountpoint)
                except PermissionError:
                    # au cas ou le disque qui n'est pas prêt
                    continue

                total_ = tk.Label(frm1, anchor='w', text=' Taille total:')
                total_.grid(row=2, column=1, sticky='ew')
                total = tk.Label(frm1, text=get_size(partition_usage.total), anchor='e')
                total.grid(row=2, column=2, sticky='ew', padx='210 0')

                used_ = tk.Label(frm1, anchor='w', text=' Utilisé:')
                used_.grid(row=3, column=1, sticky='ew')
                used = tk.Label(frm1, text=get_size(partition_usage.used), anchor='e')
                used.grid(row=3, column=2, sticky='ew', padx='210 0')
            
                disp_ = tk.Label(frm1, anchor='w', text=' Disponible:')
                disp_.grid(row=4, column=1, sticky='ew')
                disp = tk.Label(frm1, text=get_size(partition_usage.free), anchor='e')
                disp.grid(row=4, column=2, sticky='ew', padx='210 0')

                perc_ = tk.Label(frm1, anchor='w', text=' Pourcentage:')
                perc_.grid(row=4, column=1, sticky='ew')
                perc = tk.Label(frm1, text=f"{partition_usage.percent} %", anchor='e')
                perc.grid(row=4, column=2, sticky='ew', padx='210 0')

                self.nbook.add(frm1, text=f'{p.device}')

                self.dico_nbook[p.device] = {
                    'main': frm1,
                    'used': used,
                    'disp': disp,
                    'perc': perc,
                }
        
        a_supprimer = [elm for elm in self.dico_nbook if elm not in a_conserver]
        for e in a_supprimer:
            self.nbook.forget(self.dico_nbook[e]['main'])
            del self.dico_nbook[e]


    def premier_plan(self, *_):
        al = self.master.wm_attributes('-alpha')

        if al == 0.2:
            self.master.wm_attributes('-alpha', 0.4)
        elif al == 0.4:
            self.master.wm_attributes('-alpha', 0.6)
        elif al == 0.6:
            self.master.wm_attributes('-alpha', 1.0)
        else:
            self.master.wm_attributes('-alpha', 0.2)


    # def mouse_enter(self, *_):
    #     self.master.wm_attributes('-alpha', 1)


    # def mouse_leave(self, *_):
    #     self.master.wm_attributes('-alpha', 0.8)


    def leftUp(self, event):
        # self.master.wm_attributes('-alpha',0.8)
        self.moving.set(0)


    def leftDown(self, event):
        # self.master.wm_attributes('-alpha',0.2)
        self.x.set(event.x)
        self.y.set(event.y)
        self.moving.set(1)


    def leftMove(self, event):
        if self.moving.get() == 1:
            newX = self.master.winfo_x() + (event.x - self.x.get())
            newY = self.master.winfo_y() + (event.y - self.y.get())
            self.master.geometry(f'+{int(newX)}+{int(newY)}')


    def rightDown(self, event):
        self.status.set(0)
        self.master.destroy()



if __name__ == '__main__':
    DeviceState().mainloop()
    # import doctest
    # doctest.testmod()
