import requests
import datetime
import time
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import threading
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

global r1,r
global headers,tkid
data = ''
waitingtime = ''

class communicator:
    def __init__(self):
        self.__stop = False
    def __runSender(self,val):
        while not self.__stop:
            process()
            time.sleep(val)
            #print "stopped sender"
    def start(self,val):
        senderThread = threading.Thread(target=self.__runSender,args=[val])
        senderThread.start()
    def stop(self):
        self.__stop = True

def send(link):
    global r,headers,logid,pswrd,data
    try:
        r = requests.get('https://leninfarm.ru'+link,headers=headers,allow_redirects=False)
        if 'Location' in r.headers:
            r1 = requests.get('https://leninfarm.ru'+r.headers['Location'],headers=headers)
            data = r1.text
            process()
        else:
            data = r.text
            process()
    except ConnectionError as e:
        print(e)

def process():
    global data
    soup = BeautifulSoup(data,"html.parser")
    x = datetime.datetime.now()
    print(len(data))
    for link in soup.findAll('a'):
        print(link.get('href'));print(str(link.contents))
        if '/?get_prize=' in str(link.get('href')) and 'gen_code=' in str(link.get('href')):
            print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))
            return send(link.get('href'))
        if 'mycellar/put_all?ok' in str(link.get('href')):
            print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))
            return send(link.get('href'))
        if 'mypool/incubator_all?ok' in str(link.get('href')):
            print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))
            return send(link.get('href'))
        if '?coca_get=' in str(link.get('href')):
            print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))
            return send(link.get('href'))
        if '[\u0417\u0410\u0411\u0420\u0410\u0422\u042c]' in repr(data): #prize
            if '[\u0417\u0410\u0411\u0420\u0410\u0422\u042c]' in str(link.contents):
                print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#pick up
                return send(link.get('href'))
        else:
            if '\u0417\u0430\u0431\u0440\u0430\u0442\u044c \u043f\u0440\u0438\u0437' in str(link.contents):
                print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#collect prize
                return send(link.get('href'))

        if '\u041e\u0441\u0432\u043e\u0431\u043e\u0434\u0438\u0442\u044c \u043f\u043e\u043b\u043a\u0438' in repr(data):#cellar
            if '\u0417\u0430\u0433\u043e\u0442\u043e\u0432\u0438\u0442\u044c \u0432\u0441\u0451' in str(link.contents) or 'To apply' in str(link.contents):
                print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#prepare
                return send(link.get('href'))
            if '>\u0417\u0430\u043a\u0438\u043d\u0443\u0442\u044c \u0443\u0434\u043e\u0447\u043a\u0443</' in str(link.contents) or 'Raise' in str(link.contents):
                print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#throw rod
                return send(link.get('href'))

        if '/mypool/clean_pools' in repr(data):#ponds
            if '\u0420\u0430\u0437\u0432\u043e\u0434\u0438\u0442\u044c' in str(link.contents) or 'To apply' in str(link.contents):
                print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#prepare
                return send(link.get('href'))
            if '>\u0417\u0430\u043a\u0438\u043d\u0443\u0442\u044c \u0443\u0434\u043e\u0447\u043a\u0443</' in str(link.contents) or 'Raise' in str(link.contents):
                print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#throw rod
                return send(link.get('href'))
            if '\u041f\u0440\u043e\u0434\u0430\u0442\u044c' in str(link.contents):
                print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#sell all
                return send(link.get('href'))

        if '/myfarm/change_plant' in data:
            if '\u0423\u0434\u043e\u0431\u0440\u0438\u0442\u044c' in str(link.contents) or '\u0421\u043e\u0431\u0440\u0430\u0442\u044c' in str(link.contents):
                print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#fertilize,Collect
                return send(link.get('href'))
            if '\u0417\u0430\u0441\u0435\u044f\u0442\u044c' in str(link.contents) or '\u0421\u043e\u0431\u0440\u0430\u0442\u044c' in str(link.contents):
                print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#Sow
                return send(link.get('href'))
            if '\u0421\u043e\u0431\u0440\u0430\u0442\u044c \u0443\u0440\u043e\u0436\u0430\u0439' in str(link.contents) or '\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c' in str(link.contents):
                print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#harvest,apply
                return send(link.get('href'))
            if '\u0412\u0441\u043a\u043e\u043f\u0430\u0442\u044c' in str(link.contents) or '\u041f\u043e\u043b\u0438\u0442\u044c' in str(link.contents).encode('utf8'):
                print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#dig up,pour out
                return send(link.get('href'))
            if '\u041f\u043e\u0441\u0430\u0434\u0438\u0442\u044c' in str(link.contents):
                print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#plant seed
                return send(link.get('href'))

        if '\u0418\u0441\u043a\u0430\u0442\u044c \u041d\u0435\u0444\u0442\u044c' in str(link.contents) or '\u041f\u0440\u043e\u0432\u0435\u0440\u0438\u0442\u044c \u0441\u043a\u0432\u0430\u0436\u0438\u043d\u0443' in str(link.contents):
            print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#search oil check well
            return send(link.get('href'))

        if '>\u0417\u0430\u0431\u0440\u0430\u0442\u044c \u043d\u0430\u0445\u043e\u0434\u043a\u0443!</font>' in str(link.contents):
            print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#pick up mine
            return send(link.get('href'))

        if '>\u0421\u043f\u0443\u0441\u0442\u0438\u0442\u044c\u0441\u044f \u0432\u043d\u0438\u0437</font>' in str(link.contents):
            print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#go down mine
            return send(link.get('href'))

        if '\u041d\u0430 \u041e\u0437\u0435\u0440\u0435' in repr(data):#fishing
            if '>\u0412\u044b\u0442\u0430\u0449\u0438\u0442\u044c \u0443\u0434\u043e\u0447\u043a\u0443 </' in str(link.contents) or 'To apply' in str(link.contents):
                print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#pull out rod
                return send(link.get('href'))
            if '>\u0417\u0430\u043a\u0438\u043d\u0443\u0442\u044c \u0443\u0434\u043e\u0447\u043a\u0443</' in str(link.contents) or 'Raise' in str(link.contents):
                print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#throw rod
                return send(link.get('href'))

        if '\u041f\u0440\u043e\u0434\u0430\u0442\u044c' in str(link.contents):
            print(link.get('href')+' = '+str(link.contents)+' ='+x.strftime("%I:%M:%S %p"))#sell pet
            return send(link.get('href'))

    if '>\u0428\u0430\u0445\u0442\u0430   <font color=' in repr(data):
        return send('/shahta')
    if '>\u0428\u0430\u0445\u0442\u0430 <span class="title">' in repr(data):
        return send('/shahta')
    if '>\u041f\u0440\u0438\u0438\u0441\u043a <span class="title">' in repr(data):
        return send('/priisk')

    for link1 in soup.findAll('li'):
        #print(str(link1.contents))
        if '>\u041f\u0440\u0443\u0434\u044b</a>' in str(link1.contents) and '<span class="title">(' in str(link1.contents):
            return send('/mypool')
        """
        if '>\u0420\u044b\u0431\u0430\u043b\u043a\u0430</a>' in str(link1.contents) and '<span class="title">' in str(link1.contents):
            return send('/fishing/lake')
        """
        if '>\u041f\u043e\u0433\u0440\u0435\u0431</a>' in str(link1.contents) and '<span class="title">' in str(link1.contents):
            return send('/mycellar')
        if '>\u0413\u0440\u044f\u0434\u043a\u0438 </a>' in str(link1.contents) and '<span class="title">(' in str(link1.contents):
            return send('/myfarm')

    global waitingtime
    if bool(waitingtime) == False:
        waitingtime = time.time()
    if (time.time() - waitingtime) > 120:
        waitingtime='';send('/myfarm')

def post():
    global r1,headers,sess,logid,pswrd,data
    pload = {'loginForm_loginForm_hf_0':'','login':'thakur','password':'bainchod'}
    r1 = requests.post('https://leninfarm.ru/autorization',data=pload,allow_redirects=False)
    print(r1.status_code)
    #print(r1.headers)
    if 'Set-Cookie' in r1.headers:
        logid=r1.cookies['id']
        pswrd=r1.cookies['pass']
        headers = {'Cookie': 'SESS='+r1.cookies['SESS']+'; log_id='+logid+'; pass='+pswrd,
                   "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-J700F Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36"}
        send('/myfarm')
        join()

def join():
    c = communicator()
    c.start(5)

post()