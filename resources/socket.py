import  socket, ssl

def open_socket(dst, port, secure=False):
  s = None
  res = socket.getaddrinfo(dst, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
  af, socktype, proto, canonname, sockaddr = res[0]
  skt = socket.socket(af, socktype, proto)
  if secure:
    s = ssl.wrap_socket(skt, ssl_version=ssl.PROTOCOL_TLSv1_2, ciphers="ADH-AES128-SHA256") #ADH-AES128-SHA256
  else:
    s = skt
  s.connect(sockaddr)
  return s