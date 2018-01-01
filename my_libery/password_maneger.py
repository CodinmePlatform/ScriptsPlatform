from my_libery.imports.job import job
from my_libery.DBY import DBY_obj
from random import randint

class pass_saver_obj(job):
    def __init__(self):
        self.db = DBY_obj()
        self.type_file = '.pass'

    def help(self):
        h = '''?
            new_password(<for_what>)
            Example: new_password('email')

            get_password(<for_what>)
            Example: get_password('mom computer')

            delete_password(<for_what>)
            Example: delete_password('mom computer')
            '''
        return h

    def new_password(self, name):
        new_pass = self._password_creater()
        self.db.save('%s%s'%(name, self.type_file), new_pass)
        return 'OK password %s saved.'%new_pass
    def get_password(self, name):
        return self.db.load('%s%s'%(name, self.type_file))

    def _password_creater(self):
        password = ''
        chars = '123456890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM!@#$%&)('
        for i in range(8):
            password += chars[randint(0, len(chars))]
        return password

    def delete_password(self, name):
        return self.db.delete(name + self.type_file)

    def start(self, cmd):
        self.cmd = cmd
        return 'welcome to my password saver.'

password_maneger = pass_saver_obj()
