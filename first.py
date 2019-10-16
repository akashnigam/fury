from swpag_client import Team
import json

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
    print('SERVICE NAME:',service)
    print('SERVICE ID:',service['service_id'])
    service_id = service['service_id']
    targets = t.get_targets(service_id)
    for target in targets:
        print('TARGET NAME:',target)#,netcat(target,''))
	print(netcat(target))
