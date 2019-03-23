"""
Assignment 6-7: Cost change path
"""
import telnetlib
import json
import cisco_controller

router_info = open('router_info.json', 'r')
router_info = json.loads(router_info.read())

def path_change(mode="route"):
    """
    args:
        mode => 'route' and 'clear'
            --> route : Changing cost to change routing table
            --> clear : clear cost to default

    R1#sh ip ospf interface s0/0
    Serial0/0 is up, line protocol is up 
    Internet Address 100.2.3.18/30, Area 1 
    Process ID 1, Router ID 100.2.101.1, Network Type POINT_TO_POINT, Cost: 64
    ...

    We can control path of OSPF using cost
    R1# ip ospf cost <cost>
    """
    router_log = ""
    int_flag = 1
    for router in router_info:
        traget = router_info[router]['ip']
        cisco = Cisco_router(router_info[router]['ip'],router_info[router]['username'],router_info[router]['password'],router_info[router]['en_password'])

        #Login phase
        print('[-] Traget is '+traget)
        print("[-] Connecting to ",traget)

        if cisco.get_connection():
            print("[-]",traget, "Login and Enable Complete ")

        #Get router name
        text = cisco.exec('sh running-config  | include host')
        text = text.split('\n')[1].split(' ')[1].strip()
        print("[-] ",traget, "Router name is "+text)
        cisco.set_routername(text)

        print("[-] Now flag is "+str(int_flag))
        cisco.exec("conf t")
        if int_flag == 1:
            cisco.exec("int s0/0")
        else:
            cisco.exec("int s0/1")
        int_flag = int_flag*-1

        #can choose route or clear
        if mode == "route"
            cisco.exec("ip ospf cost 1000")
        else:
            cisco.exec("no ip ospf cost")
        print("[!] OSPF PATH CHANGED!")
        cisco.exec("end")
        cisco.exec("exit")
path_change()
