import pickle 
import os

class ServerData:
    def __init__(self, np_id=0, def_id=0, channel_id=0, pws='12345'):
        self.np_id = np_id
        self.def_id = def_id
        self.channel_id = channel_id
        self.pw = pws
    
    def __str__(self):
        return f'id: {self.np_id}, def_id: {self.def_id}, channel_id: {self.channel_id}, pw: {self.pw}'

TOKEN = os.environ['TOKEN']
print(TOKEN)

storage = {}
#storage = pickle.load(open('serverdata', 'rb'))

f = {}

f['sdds'] = 'dssd'
f['ss'] = '222'

ff = [1, 2, 3]
print(len('sdadsas dsds'.split()))

#pickle.dump(f, open('hists.pck','wb'))

f = {}

#f = pickle.load(open('hists.pck', 'rb'))

stt = 'assdaasd default_role dasdsa'
print(stt[stt.find('default_role')+13:])

print(f)

if 'dssd' in f:
    print("there")

if 'ss' in f:
    print("sthere")