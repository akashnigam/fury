from swpag_client import Team
t = Team("http://actf0.cse545.rev.fish/", "IeaL1xdIryga0Ubazn2Zi2Sh3Gf47RdN")
print(t.game_url)
print(t.get_vm())
print(t.get_game_status())
print(t.get_service_list())
#t.get_targets(service_id)
services = t.get_service_list()
print('services:',services)
for service_id in services:
    print('SERVICE NAME:',service_id)
    targets = t.get_targets(service_id)
    for target in targets:
        print('TARGET NAME:',target)

