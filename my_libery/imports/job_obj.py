
class job_obj(object):
    def __init__(self, name, account_fun):
        self.name = name
        self.account_fun = account_fun
        self.back_job = []

    def set_job(self, new_name):
        self.back_job.append(self.name)
        self.name = new_name

    def back(self):
        if self.back_job:
            self.name = self.back_job.pop()
            self.account_fun = None
            return self.name
        else:
            return None

    def get_account(self):
        if self.account_fun:
            return self.account_fun()
        else:
            return ''
    def set_account(self, fun):
        self.account_fun = fun

    def get_job(self):
        return self.name + self.get_account()
    def get_name(self):
        return self.name
