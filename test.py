class Kls(object):
    def __init__(self, data):
        self.data = data
    def printd(self):
        print(self.data)
    @staticmethod
    def smethod():
        print('Static:')
    @classmethod
    def cmethod(*arg):
        print('Class:', arg)
    def dd(self):
        b()

def b():
    print 'b'

def a():
    b()

ik = Kls(23)
ik.printd()
ik.smethod()
Kls.smethod()
ik.cmethod()
Kls.cmethod()
ik.dd()
a()