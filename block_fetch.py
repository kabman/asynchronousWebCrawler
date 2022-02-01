import socket
import re

def fetch(url):
    sock = socket.socket()
    sock.connect(('xkcd.com',80))
    req = 'GET {} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'.format(url)
    sock.send(req.encode('ascii'))
    res = b''
    chunk = sock.recv(4096)
    while chunk:
        res+=chunk
        chunk = sock.recv(4096)
    
    urls = set(re.findall(r'''(?i)href=["']?([^\s"'<>]+)''',
                   res.split(b'\r\n\r\n', 1)[1].decode('utf-8')))
    print(urls)

if __name__ == "__main__":
    fetch("/")