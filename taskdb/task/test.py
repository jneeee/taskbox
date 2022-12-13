class Abc():
    def __init__(self):
        self.asd = None
        pass

    def func1(self):
        pass

class inh():
    pass

a = inh()

Abc.register(inh)

