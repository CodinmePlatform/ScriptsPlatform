from threading import Thread

class threads(object):
    def __init__(self):
        self.threads = {}

    def new(self, name, fun, stop_fun):
        new_thread = Thread(target = fun)
        self.threads[name] = (new_thread, stop_fun)

    def stop(self, name):
        exsist = self.exsist(name)
        if not exsist:
            return
        self.threads[name][1]()
        
        return '^thread remove.'

    def start(self, name):
        exsist = self.exsist(name)
        if not exsist:
            return exsist

        try:
            self.threads[name][0].start()
        except:
            return '*thread is all raedy started.'

    def close(self):
        for i in self.threads.keys():
            self.stop(i)
        return '?threads closed.'

    def exsist(self, name):
        if not name in self.threads.keys():
            return False
        return True
        

