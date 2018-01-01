from my_libery.imports import EDY, job
from my_libery.server import server_obj
import os

class DBY_obj(job.job):
    def __init__(self, password = ''):
        self.fileType = '.db'
        self.db_virtual = None
        self.password = password
        self.ed = None
        if password:
            self.en_de = EDY.EDY(password)
        else:
            self.en_de = None
        self.path = r'my_libery\DB'

    def reset(self):
        self.en_de = None
        self.password = ''
    
    def save(self, file, data, password = ''):
        if not '.' in file:
            file += self.fileType
        if password:
            self.en_de = EDY.EDY(password)
        
        if self.en_de:
            open(self.path + '\%s'%(file), 'w').write(str(self.en_de.en(data)))
        else:
            open(self.path + '\%s'%(file), 'w').write(data)
        return '?OK saved.'

    def load(self, file, password = ''):
        if not '.' in file:
            file += self.fileType
        if password:
            self.en_de = EDY.EDY(password)

        if self.en_de:
            try:
                data = self.en_de.de(eval(open(self.path + '\%s'%(file), 'r').read()))
            except:
                data = "*file name or password worng!"
        else:
            data = open(self.path + '\%s'%(file), 'r').read()
        return data

    def show_all_files(self):
        return self.cmd.make_list(os.listdir(self.path))

    def delete(self, file):
        lis = os.listdir(self.path)
        for i in lis:
            if file in i:
                name = i
                break
        try:
            os.system('del %s\%s' % (self.path, name))
            return '?OK %s delete.' % name
        except:
            return '*file not found.'

    def run_server_db(self, name, password = ''):
        self.server = server_obj(name, password, self._protocol)
        if self.server:
            self.cmd.threads.new(name, self.server.run, self.stop_server_db)
            self.cmd.threads.start(name)
            return('^runing server...')
        else:
            return('*<create new_group() first>')
    def stop_server_db(self):
        self.server.stop_server()
    def _protocol(self, sock, users):
        if sock in users.keys() and users[sock]:
            data = users[sock]
            try:
                to_run = "self.%s" % data
                out = eval(to_run)
            except Exception as e:
                out = str(e)
            if out == None:
                out = 'None'
            sock.send(out.encode())

    def connect_db(self, ip, name, password = ''):
        self.cmd.my_con.new_socket(name, password)
        self.cmd.my_con.connect(name, (ip, 28))
        self.cmd.my_con.sockets[name]['s'].send((name+':'+password+':'+'username').encode())
        ans = self.cmd.my_con.sockets[name]['s'].recv(1024).decode()
        if ans == 'ok':
            self.cmd.set_job(name)
            return '?ok you connected.'
        else:
            return ans

    def help(self):
        h = '''^
                save(file, data, *<password>)

                load(file, *<password>)

                delete(file)
                reset()//password

                show_all_files()

                run_server_db(<name>, *<password>)
                stop_server_db()
                connect_db(<ip>, <name>, *<password>)
            '''
        return h

    def start(self, cmd):
        self.cmd = cmd
        return "?wellcome to my data base tool for help enter help()."
DBY = DBY_obj()
