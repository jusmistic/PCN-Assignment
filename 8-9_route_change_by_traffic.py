"""
    Assignment 8-9: Select path via traffic
"""
import telnetlib
import json
import cisco_controller

router_info = open('router_info.json', 'r')
router_info = json.loads(router_info.read())

def traffic_control():
    """
    Control trafic from A-->A'
        if small traffic on B-->A (R2 S0/0):
            normal route
        if large taffic: # RSBX on S0/0 > 30000 bits/sec
            change cost:
                R1(S0/0) cost 1000
                R2(s0/1) cost 1000
        traffic = {
            "RXBS": rx rate (bits/sec) int
            "RXPS": rx rate (pkts/sec) int
            "TXBS": tx rate (bits/sec) int
            "TXPS": tx rate (pkts/sec) int
        }
            
    """

    #Setup Connection on R1
    r1 = Cisco_router(router_info['r1']['ip'],router_info['r1']['username'],router_info['r1']['password'],router_info['r1']['en_password'])
    if r1.get_connection():
        print("[-]",r1.router_ip, "Login and Enable Complete ")
    text = r1.exec('sh running-config  | include host')
    text = text.split('\n')[1].split(' ')[1].strip()
    print("[-]",r1.router_ip, "Router name is", text)
    r1.set_routername(text)

    #Setup Connection on R2
    r2 = Cisco_router(router_info['r2']['ip'],router_info['r2']['username'],router_info['r2']['password'],router_info['r2']['en_password'])
    traffic = {}
    print("[-] Connecting to ",r2.router_ip)
    if r2.get_connection():
        print("[-]",r2.router_ip, "Login and Enable Complete ")
    text = r2.exec('sh running-config  | include host')
    text = text.split('\n')[1].split(' ')[1].strip()
    print("[-]", r2.router_ip, "Router name is",text)
    r2.set_routername(text)


    #R2 monitoring
    while True:
        time.sleep(5)
        text = r2.exec('sh int s0/0 summary | b Interface')
        text = text.split('\n')[3]
        text = text.split()
        traffic['RXBS'] = int(text[6])
        traffic['RXPS'] = int(text[7])
        traffic['TXBS'] = int(text[8])
        traffic['TXPS'] = int(text[9])
        print("[-] Debug traffic", traffic)
        text = r2.exec('sh ip ospf interface s0/1 | section include Cost').split(',')
        text = text[3].split("\r")[0].strip()
        text = int(text[5:])
        
        #if int s0/1 on R2 cost is 64 == normal route
        if text == 64:
            # print("[-] Debug Routing Normal route ")
            #large traffic
            if traffic['RXBS'] > 30000:
                large_traffic_config(r1, r2)
            continue #pass checking small traffic
        else:
            #int s0/0 cost != 64 (large cost redirect)
            #check should change to normal route
            if traffic['RXBS'] <= 30000:
               small_traffic_config(r1,r2)
        
def large_traffic_config(r1, r2):
    """
        Change routing when incomming traffic to int s0/0 on R2 too large
        if large taffic: # RSBX on S0/0 > 10000 bits/sec
        change cost:
            R1(S0/0) cost 1000
            R2(s0/1) cost 1000
    """
    print("[!] Large Traffic Detected!")
    print("[!] Change route path!")

    #r1 Change path
    print("[-] R1",r1.router_ip,"Login and Enable Complete ")
    r1.exec("conf t")
    r1.exec("int s0/0")
    r1.exec("ip ospf cost 1337")
    r1.exec("end")
    text = r1.exec('sh ip ospf interface s0/0 | section include Cost')

    # print(text)
    if "1337" in text:
        print("[/] R1 Change int s0/0 cost to 1337 Complete!")

    #r2 Change path
    print("[-] R2",r2.router_ip,"Login and Enable Complete ")
    r2.exec("conf t")
    r2.exec("int s0/1")
    r2.exec("ip ospf cost 1337")
    r2.exec("end")
    text = r2.exec('sh ip ospf interface s0/1 | section include Cost')
    # print(text)
    if "1337" in text:
        print("[/] R2 Change int s0/1 cost to 1337 Complete!")

def small_traffic_config(r1,r2):
    """
        Change route path
    """
    print("[!] Traffic Decrease")
    print("[!] Changing route path to Normal route!")

    #r1 Change path
    print("[-] R1",r1.router_ip,"Login and Enable Complete ")
    r1.exec("conf t")
    r1.exec("int s0/0")
    r1.exec("no ip ospf cost 1337")
    r1.exec('end')
    text = r1.exec('sh ip ospf interface s0/0 | section include Cost')
    # print(text)
    if "64" in text:
        print("[/] R1 Change int s0/0 cost to 64 Complete! [Notmal route]")

    #r2 Change path
    print("[-] R2",r2.router_ip,"Login and Enable Complete ")
    r2.exec("conf t")
    r2.exec("int s0/1")
    r2.exec("no ip ospf cost 1337")
    r2.exec('end')
    text = r2.exec('sh ip ospf interface s0/1 | section include Cost')
    # print(text)
    if "64" in text:
        print("[/] R2 Change int s0/1 cost to 64 Complete! [Notmal route]")
    
traffic_control()