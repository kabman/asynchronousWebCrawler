import socket
from selectors import *

selector = DefaultSelector()
urls_todo = set(['/'])
urls_seen = set(['/'])
stopped = False
concurrency_achieved = 0

class Fetcher:
    def __init__(self,url):
        self.res = b''
        self.url = url
        self.sock = None
    
    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('xkcd.com,80'))
        except BlockingIOError:
            pass

        #register next callback
        selector.register(self.sock.fileno(),EVENT_WRITE,self.connected)

    def connected(self,key,mask):
        print('connected!')
        selector.unregister(key.fd)
        request = 'GET {} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'.format(self.url)
        self.sock.send(request.encode('ascii'))

        selector.register(key.fd,EVENT_READ,self.read_response)
    
    def read_response(self, key, mask):
        global stopped
        chunk = self.sock.recv(4096) # 4k chunk size.
        if chunk:
            self.res += chunk
        else:
            selector.unregister(key.fd) # Done reading.
            links = self.parse_links()
        # Python set-logic:
        for link in links.difference(urls_seen):
            urls_todo.add(link)
            Fetcher(link).fetch() # <- New Fetcher.
        urls_seen.update(links)
        urls_todo.remove(self.url)
        if not urls_todo:
            stopped = True

    def loop():
        while not stopped:
            events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback(event_key, event_mask)

    
