import threading
import socket
import time
import subprocess

class ProxyServer():

    """Classe que instancia e gerencia o servidor proxy. Ao ser iniciado, o servidor roda em uma thread separada.
       Ao encerrar, grava as estatísticas usando o my_logger (logger.Logger) """

    def __init__(self, domain_list, is_blacklist, my_logger, access_log_name, block_log_name, client_log_name, dire = "."):
        self.my_logger = my_logger
        self.domain_list = domain_list
        self.is_blacklist = is_blacklist
        self.access_log_name = access_log_name
        self.block_log_name = block_log_name
        self.client_log_name = client_log_name
        self.access_log = {}
        self.block_log = []
        self.client_log = {}
        self.current_sock = None
        self.dire = dire
        self._stop = False

    def valid_addr(self, addr):
        if self.is_blacklist:
            allowed = True
            for filter in self.domain_list:
                if filter in addr:
                    allowed = False
                    break
        else:
            allowed = False
            for filter in self.domain_list:
                if filter in addr:
                    allowed = True
                    break
        return allowed

    def start(self, host, port):
        self._stop = False
        soc = socket.socket(socket.AF_INET)
        self.current_sock = soc
        soc.bind((host, port))
        soc.listen(0)
        while not self._stop:
            conn, client_addr = soc.accept()
            if not self._stop:
                threading.Thread( target = self.work, args = (conn, client_addr) ).start()

    """ Função que lida com a requisição de cada conexão dos clientes. """
    def work(self, client_conn, client_addr):
        addr, port = client_addr
        buf = b''
        while not self._stop:
            buf = b''
            client_conn.settimeout(0.6)
            try:
                while True:
                    hbuf = client_conn.recv(64)
                    buf += hbuf
                    if not hbuf:
                        break
            except socket.timeout:
                pass

            if not buf:
                return
            init_time = time.time()

            sp = buf.split(b'\n')
            host = sp[1].split()[1]
            res = sp[0].split()[1]
            shost = host.decode("utf-8")
            sres = res.decode("utf-8")

            # Confere se o endereço é permitido
            if self.valid_addr(shost):
                # Realiza os logs
                if addr in self.client_log:
                    self.client_log[addr] += 1
                else:
                    self.client_log[addr] = 1

                if shost in self.access_log:
                    if res in self.access_log[shost]:
                        self.access_log[shost][sres] += 1
                    else:
                        self.access_log[shost][sres] = 1
                else:
                    self.access_log[shost] = {}

                host_soc = socket.socket(socket.AF_INET)

                # Não mostrar erros de endereços não encontrados
                try:
                    # Abre conexão com o destino, envia requisição e recebe os
                    # dados, redirecionando para o cliente
                    (_,_,_,_, address) = socket.getaddrinfo(host, 80)[0]
                    host_soc.connect(address)
                    host_soc.send(buf)
                    host_soc.settimeout(0.6)
                    buf = b''
                    host_buf = b''
                    try:
                        while True:
                            help_buf = host_soc.recv(64)
                            host_buf += help_buf
                            if not help_buf:
                                break
                    except socket.timeout:
                        pass
                    client_conn.send(host_buf)
                    host_buf = b''
                    end_time = time.time()

                    # Exibe dados da requisição na tela
                    request_log = {"ip_origem": str(addr), "port_origem": str(port), "url": res.decode("utf-8"), "ip_destino": str(address[0]),
                                "port_destino": str(address[1]), "time": str(end_time-init_time)}
                    self.my_logger.request_logger(request_log)
                except socket.gaierror:
                    pass
            else: # not valid_addr
                # Trata bloqueia e loga
                self.block_log.append({"url": host.decode("utf-8"), "client": addr})
                msg = '<html>\r\nPágina bloqueada pelo administrador da rede. Favor entrar em contato com a administração\r\n</html>'.encode()
                block_string = b'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: ' + str(len(msg)).encode() +  b'\r\n\r\n' + msg
                client_conn.send(block_string)
                down_url = (res).decode("utf-8")
                func = "wget -r " + down_url + " -P " + self.dire

                # Chama o wget pra baixar
                wget = subprocess.Popen(['/usr/bin/wget', "-r", down_url, "-P", self.dire], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                stdout, nothing = wget.communicate()
                return


    def stop(self):
        self._stop = True
        if self.current_sock != None:
            self.current_sock.close()
        self.my_logger.client_logger(self.client_log, self.client_log_name)
        self.my_logger.block_logger(self.block_log, self.block_log_name)
        self.my_logger.access_logger(self.access_log, self.access_log_name)

