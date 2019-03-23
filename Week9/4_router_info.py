"""
    Assignment 4: get router infomation
"""

import telnetlib
import cisco_controller
import json

router_info = open('router_info.json', 'r')
router_info = json.loads(router_info.read())


def router_grep():
    for router in router_info:
        traget = router_info[router]['ip']
        cisco = Cisco_router(router_info[router]['ip'],router_info[router]['username'],router_info[router]['password'],router_info[router]['en_password'])
        
        router_log = "[-] Traget "+traget+"\n"
        router_log += "Username : "+router_info[router]['username']
        router_log += "Password : "+router_info[router]['password']
        router_log += "Enable Password :"+router_info[router]['en_password']
        router_log += "\n\n"

        #Login phase
        print('[-] Traget is '+traget)
        print("[-] Connecting to ",traget)

        if cisco.get_connection():
            print("[-]",traget, "Login and Enable Complete ")

        #get router name
        text = cisco.exec('sh running-config  | include host')
        text = text.split('\n')[1].split(' ')[1].strip()
        print("[-] ",traget, "router name is "+text)
        router_log += "[-] Router name is "+text+"\n"
        
        cisco.set_routername(text)
        
        #get router spec
        print("[-] Router "+router_info[router]['ip']+" Spec.")
        text = cisco.exec("show version")
        # print(text)
        router_log += "[-] Router Spec\n"
        router_log += text

        #get router interface
        print("[-] Router Interface ")
        text2 = cisco.exec("sh ip int br")
        router_log += "[-] Router Interface\n"
        router_log += text2+"\n"
        # print(text2)

        #get routing table
        print("[-] Routing table")
        text2 = cisco.exec("sh ip route")
        router_log += "[-] Routing Table\n"
        router_log += text2
        # print(text2)
        with open('router/'+cisco.get_routername()+"-"+router_info[router]['ip']+".txt", "w") as pipe:
            pipe.write(router_log)
        
        #exit
        print("[!] Exiting "+traget)
        cisco.close()
router_grep()
