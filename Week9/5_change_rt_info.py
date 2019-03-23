"""
    Assingment 5: Change router infomation
"""
import telnetlib
import json
import cisco_controller

router_info = open('router_info.json', 'r')
router_info = json.loads(router_info.read())

def router_change_info():
    """
        Assignment 5: Router change name and change password
    """
    router_log = ""
    for router in router_info:
        traget = router_info[router]['ip']
        cisco = Cisco_router(router_info[router]['ip'],router_info[router]['username'],router_info[router]['password'],router_info[router]['en_password'])
        
        #Information of Router
        #Login phase
        print('[-] Traget is '+traget)
        print("[-] Connecting to ",traget)

        if cisco.get_connection():
            print("[-]",traget, "Login and Enable Complete ")

        #Get router name
        text = cisco.exec('sh running-config  | include host')
        text = text.split('\n')[1].split(' ')[1].strip()
        print("[-] ",traget, "Router name is "+text)
        router_log += "[-] Router name is "+text+"\n"
        cisco.set_routername(text)
        print("[+] Changing Router name From",cisco.get_routername(),"to",cisco.get_routername()+"s")
        router_log += "[+] Changing Router name From "+cisco.get_routername()+" to "+cisco.get_routername()+"s"+"\n"
        cisco.exec("conf t") #enter conf mode
        cisco.exec("hostname "+cisco.get_routername()+"s")
        
        #change router name
        cisco.exec("end") #back to enable mode
        text = cisco.exec('sh running-config  | include host')
        text = text.split('\n')[1].split(' ')[1].strip()
        if(text == cisco.get_routername()+"s"):
            print("[+] Changing Router name complete")
            print("[+] Now Router name is "+text)
            router_log += "[+] Changing Router name complete\n"
            router_log += "[+] Now Router name is "+text+"\n"
        else:
            print("[!] Can't change Router name !")
            router_log  += "[!] Can't change Router name !"
        #change password
        print("[+] Changing Password")
        cisco.exec("conf t")
        cisco.exec("username cisco password cisco1")
        router_info[router]["password"] = "cisco1"
        
        #exit
        cisco.close()

    #Update json
    with open("router_info.json", "w") as json2:
        router_info = json.dumps(router_info)
        json2.write(router_info)
    with open("router/router_name.txt", "w") as logz:
        logz.write(router_log)
router_change_info()
