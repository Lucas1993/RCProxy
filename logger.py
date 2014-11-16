class Logger():

    """Classe para controlar o log, gravar em arquivos e imprimir na tela
       Cada uma das funções pode receber um objeto ou uma lista de objetos
       e jogá-lo no log adequado (arquivo ou stdout)"""

    def client_logger(self, clients, file_name = "client_log.txt"):
        if (clients == {}) | (clients == None):
            return
        l_str = ""
        client_list = list(clients.items())
        client_list.sort(reverse=True)
        for (k,v) in client_list:
            l_str += k + " - Acessos: " + str(v) + "\n"
        with open(file_name, mode='w', encoding='utf-8') as a_file:
            a_file.write(l_str)
        return

    def block_logger(self, blocks, file_name = "block_log.txt"):
        if (blocks == []) | (blocks == None):
            return
        l_str = "Cliente : Página\n"
        for b in blocks:
            l_str += b["url"] + " : " + b["client"] + "\n"
        with open(file_name, mode='w', encoding='utf-8') as a_file:
            a_file.write(l_str)
        return

    def request_logger(self, request):
        l_str = (request["ip_origem"] + ":")
        l_str += (request["port_origem"] + "\n")
        l_str += (request["url"] + " /  ")
        l_str += (request["ip_destino"] + ":")
        l_str += (request["port_destino"] + "\n")
        l_str += ("Tempo gasto: " + request["time"] + "\n")
        print(l_str)
        return

    def access_logger(self, access_dict, file_name = "access_log.txt"):
        if (access_dict == {}) | (access_dict == None):
            return
        reduced_dict = {}
        for k,v in access_dict.items():
            acc = 0
            for sub, local in v.items():
                acc += local
            reduced_dict[k] = acc
        sorted_access = sorted(reduced_dict.items(), key = lambda x: x[1], reverse=True)
        log_str = ""
        for (k, _) in sorted_access:
            log_str += "Domínio:\n" + k + "(" + str(reduced_dict[k]) + ")" + "\nAcessos:\n"
            for req, amnt in access_dict[k].items():
                log_str += req + " - " + str(amnt) + " acessos.\n"
            log_str += "\n"
        with open(file_name, mode='w', encoding='utf-8') as a_file:
            a_file.write(log_str)
        return

