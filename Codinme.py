import os
from sys import argv
import socket
from random import randint

from my_libery.imports.EDY import EDY
from my_libery.imports.job_obj import job_obj
from my_libery.imports.threads import threads
from my_libery.imports.connections import connections

###global code
__import__ = {}

__folders__ = open(r'my_libery\settings\load_folders.plt', 'r').read().split(',')

for j in __folders__:
    __mylibery__ = os.listdir(j)
    for i in __mylibery__:
        if '.py' in i:
            i = i.replace('.py', '')
            exec('from %s.%s import %s'%(j, i, i))
            __import__[i] = eval(i).__class__
###global code

class cmd(object):
    def __init__(self):
        self.job = job_obj('main_plt', eval('main_plt').account)
        self.threads = threads()
        self.my_con = connections()
        self.exit = False
        self.sicret = False
        self.functions = [packeg.update]
        self.imports = __import__

    def is_connect(self):
        return self.my_con.is_connect()

    def start_packeg(self, file):
        file = file.replace('.pack', '')
        file = file.split('\\')[-1]
        self.run_commend('set_job("packeg")', True)
        self.run_commend('load("%s")'%file, False)

    def run(self, info = []):
        if len(info) > 1:
            if '.pack' in info[1]:
                self.start_packeg(info[1])
        while not self.exit:
            if self.is_connect():
                name = self.my_con.get_name()
            else:
                name = self.job.get_job()
            user_input = input('%s >>> '%(name))

            if not user_input:
                continue
            self.inp_control(user_input)
            if self.exit:
                break
            self.run_commend(user_input)

        self.close()

    def run_commend(self, user_input = '', progrem = False):
        if not progrem:
            if self.is_connect():
                re = self.my_con.send(self.my_con.get_name(), user_input)
                print('\n### '+user_input+' ###')
                self.smart_print(re, user_input)
                print('### '+user_input+' ###\n')
            else:
                re = self.inp(user_input)
                print('\n### '+user_input+' ###')
                self.smart_print(re)
                print('### '+user_input+' ###\n')

            for i in self.functions:
                try:
                    i(user_input, re)
                except:
                    pass
        else:
            if self.is_connect():
                re = self.my_con.send(self.my_con.get_name(), user_input)
                self.smart_print(re)
            else:
                re = self.inp_test(user_input)
                self.smart_print(re)

    def close(self):
        self.my_con.close()
        self.threads.close()
        exit()

    def smart_print(self, data, user_input = ''):
        hade = ''
        try:
            if data[0] == '*':
                hade = '[-] '
            elif data[0] == '^':
                hade = '[+] '
            elif data[0] == '?':
                hade = '[?] '
            else:
                hade = '[t] '
                data = ' ' + data
            for i in data[1:].split('\n'):
                print(hade + i)
        except:
            print(data)
                
    def inp(self, user_input):
        if user_input == 'help':
            return '*For help enter help()'
        try:
            return eval(('%s.'%self.job.get_name()) + user_input)
        except Exception as E1:
            if type(E1) != AttributeError:
                return E1
        try:
            return(eval('self.' + user_input))
        except Exception as E:
            return('*' + str(E))

    def inp_control(self, user_input):
        if user_input == 'end()' or user_input == 'exit()':
            self.exit = True
            self.threads.close()
            self.my_con.close()
        elif user_input == 'back()':
            if self.is_connect():
                self.my_con.sockets[self.my_con.get_name()]['s'].close()
                self.my_con.sockets[self.my_con.get_name()]['con'] = False
                
        

    def inp_test(self, user_input):
        try:
            return eval('self.' + user_input)
        except AttributeError:
            return eval(self.job.get_name() + '.' + user_input)
        except SyntaxError:
            return '*Syntax error try help()'

    def back(self):
        self.job.back()
        return '?back'

    def set_job(self, name):
        try:
            res = eval(name).start(self) + '\n'
            res += eval(name).help()
            self.job.set_job(name)
            self.job.set_account(eval(name).account)
            return res
        except:
            return('*' + name + ' is not a job')

    def make_list(self, lis):
        st = '^'
        for i in lis:
            st += '             ' + i + '\n'
        return st

    def cls(self):
        os.system('cls')
        return '^your windowe is empty.'

    def sicret_fun(self):
        msg = '''?
            welcome to my sicret function
            this function open for you more options in scripts.
            '''
        self.sicret = True
        return msg

my_cmd = cmd()

def wellcom():
    num = randint(1, len(os.listdir('my_libery\settings\wellcom')))
    print(open(r'my_libery\settings\wellcom\wellcom%s.plt'%str(num), 'r').read())

def info():
    print('')
    my_cmd.smart_print(open(r'my_libery\settings\start_info.plt', 'r').read())
    print('')

def main():
    wellcom()
    info()
    main_plt.start(my_cmd)
    my_cmd.run(argv)
main()
