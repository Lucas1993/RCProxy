Servidor Proxy
==============

Projeto de um servidor proxy para a disciplina de Redes de Computadores.

Instruções de execução
----------------------

O arquivo a ser chamado é o **proxy.py**.

O programa recebe dois argumentos obrigatórios e um opcional, nessa ordem:  

- O endereço de IP.
- A porta.
- Um arquivo de filtragem de urls. Pode ser considerado tanto uma blacklist (-b) quanto uma whitelist (-w)  
1. A blacklist é a opção padrão. Caso nada seja especificado (lista vazia), todas as urls são permitidas. As urls no arquivo especificado serão bloqueados.
2. Analogamente, as urls em uma whitelist serão as únicas permitidas, todas as outras serão bloqueadas.  
3. Vale lembrar que os arquivos podem conter apenas palavras chaves, que irão casar com as urls que a possuírem nos acessos.

Exemplo de uso:

`./proxy.py -i localhost -p 80 -b proibidos`

Existe também um arquivo **run.sh** que já faz uma chamada padrão ao programa, para teste.


Visão geral do projeto
----------------------

O código se divide essencialmente em 3 arquivos:  

- proxy.py
- server.py
- logger.py

###proxy.py
Esse arquivo é a "main" do programa. Ele quem lida com a passsagem de argumentos, a inicialização do servidor e a terminação do programa.  

###server.py
Esse arquivo contém a classe Server, que é o servidor proxy em si. Possui as funções start, work e stop, além de uma função valid_addr de auxílio.  
- A função **start** inicia o servidor e escuta na porta especificada. Irá disparar uma thread com a função **work** para cada conexão recebida.
- A função **work** realiza o serviço de proxy em si para a conexão, sendo o intermediário entre o cliente e o host. Realiza também a checagem de urls permitidas. 
- A função **stop** é chamada quando se deseja encerrar o proxy e gravar os logs, com o auxílio da classe Logger.

###logger.py
Arquivo que contém uma classe auxiliar que realiza o log do programa, com funções para gravar os acessos, clientes conectados, acesso à páginas bloqueadas e etc.  

Autor
-------
* Lucas de Moura Amaral 	-	11/0015690

