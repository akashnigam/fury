from swpag_client import Team
import json
t = Team("http://actf0.cse545.rev.fish/", "IeaL1xdIryga0Ubazn2Zi2Sh3Gf47RdN")
print(t.game_url)
#print(t.get_vm())
print(t.get_game_status())
print(t.get_service_list())
#t.get_targets(service_id)
services = t.get_service_list()
print('services:',services)
print()
for service in services:
    print('SERVICE NAME:',service)
    #serviceObj = json.loads(service)
    targets = t.get_targets(service['service_id'])
    #targets = t.get_targets(10001)
    for target in targets:
        print('TARGET NAME:',target)

