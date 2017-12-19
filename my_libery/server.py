import socket, time, select
from my_libery.proj import myprosses
from my_libery.imports.EDY import EDY
from my_libery.imports.job import job

class server_obj(job):
    def __init__(self, name = '', password = '', script = myprosses):
        self.name = name
        self.password = password
        self.activ = True
        self.users = {}
        self.proj = script()
        self.port = 28
        self.cmd = None
        try:
            self.proj.load(name, password)
        except:
            self.proj.new(name, password)
        self.control = {}
        self.names = {}
        
    def run(self):
        s = socket.socket()
        s.bind(('0.0.0.0', self.port))
        s.listen(5)
        self.ed = EDY(self.password)
        ocs = []
        bay = b'goodBay'
        while self.activ:
            time.sleep(0.1)
            rlist, wlist, xlist = select.select([s] + ocs, ocs, [])
            for current_socket in rlist:
                if current_socket is s:
                    (new_socket, address) = s.accept()
                    name_and_pass = new_socket.recv(1024).decode().split(':')
                    ocs = self.connect(name_and_pass, new_socket, ocs)
                else:
                    try:
                        data = current_socket.recv(1024).decode()
                        self.users[current_socket] = self.ed.de(eval(data))
                        self.control[self.names[new_socket]].append(data)
                    except:
                        ocs = self.disconnect(current_socket, ocs)
            self.send_waiting_messages(wlist)
        s.close()
    
    def send_waiting_messages(self, wlist):
        for sock in wlist:
            if sock in self.users.keys() and self.users[sock]:
                data = self.users[sock]
                try:
                    out = eval('self.proj.' + data)
                except:
                    out = '<Error try help()>'
                if out == None:
                    out = 'None'
                sock.send(str(self.ed.en(str(out))).encode())
                self.users[sock] = ''

    def connect(self, name_and_pass, new_socket, ocs):
        wellcom = b'ok'

        if name_and_pass[0] == self.name and name_and_pass[1] == self.password:
            if not name_and_pass[2] in self.names.keys():
                ocs.append(new_socket)
                new_socket.send(wellcom)
                self.users[new_socket] = ''
                self.names[new_socket] = name_and_pass[2]
                self.control[self.names[new_socket]] = []
            else:
                new_socket.send(b'user name all ready exsist.')
                new_socket.close()
        else:
            new_socket.send(b'name or password worng')
            new_socket.close()
        return ocs

    def disconnect(self, current_socket, ocs):
        ocs.remove(current_socket)
        self.users.pop(current_socket)
        self.control.pop(self.names[current_socket])
        self.names.pop(current_socket)
        return ocs

    def set(self, name, value):
        try:
            setattr(self, name, value)
        except:
            return '*attribut error attributs: ' + str(self.__dict__)
        return '^%s -----> %s' % (str(name), str(value))

    def get(self, name):
        if name == 'all':
            return '?' + str(self.__dict__)
        try:
            return '^' + str(getattr(self, name))
        except:
            return '*error name'

    def help(self):
        h = '''^
            set(<name>, <value>)
            get(<name>)/get('all')
            run_server()
            stop_server()
            '''
        return h
    
    def start(self, cmd):
        self.cmd = cmd
        return '?wellcom to server script.'
    
    def stop_server(self):
        self.activ = False
        return '?server stopt.'

    def run_server(self):
        self.cmd.threads.new(self.name, self.run, self.stop_server)
        self.cmd.threads.start(self.name)
        return('^runing server...')
    
server = server_obj()
