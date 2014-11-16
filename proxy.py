#!/usr/bin/env python3
# encoding: utf-8

import optparse
import logger
import server
import threading

def handle_usage():
    """ Função para gerenciar uso do programa e passagem do argumentos através da linha de comando.  """

    usage = ''' usage %prog -i <ip> -p <port> -b <blacklist> -w <whitelist> -d <dir>
                    <blacklist>: Arquivo com lista de URLs a serem bloqueadas. Default.
                    <whitelist>: Arquivo com lista de URLs permitidas. Opção não pode ser passada junto com a blacklist.
                    <dir>: Diretório para se guardar as páginas bloqueadas. Padrão é o diretório atual.'''

    parser = optparse.OptionParser(usage)
    parser.add_option('-i', dest='ip', type='string', help='IP do servidor')
    parser.add_option('-p', dest='port', type='int', help='Porta a se escutar')
    parser.add_option('-b', dest='blacklist', type='string', help='Arquivo contendo URLs a serem bloqueadas')
    parser.add_option('-w', dest='whitelist', type='string', help='Arquivo contendo URLs a serem permitidas')
    parser.add_option('-d', dest='dire', type='string', help='Diretório para se baixar as páginas bloqueadas.')

    return parser

def main():
    # Recebe os argumentos por linha de comando
    parser = handle_usage()
    (options, args) = parser.parse_args()

    ip = options.ip
    port = options.port
    blacklist = options.blacklist
    whitelist = options.whitelist
    dire = options.dire

    if (ip == None) | (port == None) :
        print(parser.usage)
        return
    elif (whitelist != None) & (blacklist != None) :
        print(parser.usage)
        return
    else:
        # Classe para gerenciar os logs, gravar em arquivo e imprimir na tela as requests
        log = logger.Logger()
        # Define as variaveis de lista e tipo de bloqueio a serem passadas para o servidor
        listname = blacklist if blacklist != None else whitelist
        list_type = False if whitelist != None else True

        if dire == None:
            dire = "./"

        try:
            url_list = [line.strip() for line in open(listname)]
        except FileNotFoundError:
            url_list = []

        # Inicializa o servidor
        proxy_server = server.ProxyServer(url_list, list_type, log, "access_log.txt", "block_log.txt", "client_log.txt", dire)
        thr = threading.Thread( target = proxy_server.start, args = (ip, port) )
        thr.setDaemon(True) # Programa não espera essa thread para encerrar
        thr.start()
        # Encerra o programa caso Ctrl+D (EOF) seja inserido
        try:
            while (input()):
                pass
        except EOFError:
            proxy_server.stop()
            return

if __name__ == '__main__':
    main()
