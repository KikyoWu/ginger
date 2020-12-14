class Kikyo():
    name='kikyo'
    age=18

    def __init__(self):
        self.gender='female'

    def keys(self):
        return ('name','age','gender')

    def __getitem__(self, item):
        return getattr(self,item)

k=Kikyo()
print(dict(k))
