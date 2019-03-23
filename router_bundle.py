"""
        Router 1 config
        100.2.101.1
"""
import getpass
import telnetlib
import subprocess
import json
import threading
import time


Device = "10.30.7.45"

# Import router_info

router_info = open('router_info.json', 'r')
router_info = json.loads(router_info.read())

subnet_info = {
    'sub_a': router_info['r1']['ip'][:-1]+'1',
    'sub_b': router_info['r2']['ip'][:-1]+'1',
    'sub_a_dat' : router_info['r3']['ip'][:-1]+'1',
    'sub_b_dat' : router_info['r4']['ip'][:-1]+'1',
    'sub_a_dat_dat' : router_info['r5']['ip'][:-1]+'1',
    'sub_b_dat_dat' : router_info['r6']['ip'][:-1]+'1'
}

class Cisco_router:
    def __init__(self, router_ip,username,password,en_password):
        self.router_ip = router_ip
        self.username = username
        self.password = password
        self.en_password = en_password
        self.router_name = ""

    def get_connection(self):
        self.telnet = telnetlib.Telnet(self.router_ip,timeout = 1)
        self.telnet.read_until(b"Username: ")
        self.telnet.write(self.username.encode('ascii') + b"\n")
        self.telnet.write(self.password.encode('ascii') + b"\n")
        self.telnet.read_until(b">")
        self.telnet.write('ena'.encode('ascii') + b"\n")
        self.telnet.read_until(b"Password:")
        self.telnet.write(self.en_password.encode('ascii') + b"\n")
        self.telnet.read_until(b"#")
        return True

    def set_routername(self,rt_name):
        self.router_name = rt_name
    def get_routername(self):
        return self.router_name
    def exec(self,cmd):
        self.telnet.write(cmd.encode('ascii')+b'\n')
        text = self.telnet.read_until((self.router_name+"#").encode('ascii'), 5).decode('utf-8')
        # text = text.split('\r\n')
        return text
    def close(self):
        self.exec('end')
        self.exec('exit')

def exec(cmd):
    text = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines='\r\n')
    return text.stdout

def traceroute():
    """ Do traceroute"""
    for subnet in subnet_info:
        text = exec('ping -c 1 '+subnet_info[subnet])
        print(text)
        if ' 0%' in str(text):
            print('[-] Ping '+subnet_info[subnet]+'Complete')
            print('[-] Traceroute ',subnet,subnet_info[subnet])
            trace_result = exec('tracert '+subnet_info[subnet])
            saveoutput = open('traceroute/'+subnet+'-'+subnet_info[subnet]+'.txt',"w")
            saveoutput.write(str(trace_result))
            saveoutput.close()
        else:
            print("[!] Ping "+subnet_info[subnet]+' is failed!')
# traceroute()

def router_grep():
    """
        Assignment 4: get router infomation
    """

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
        #Disable screen line bug  
        cisco.exec("terminal length 0")
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
# router_grep()

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

        #Disable screen line bug  
        cisco.exec("terminal length 0")

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
        cisco.exec("end")
        cisco.exec("exit")

    with open("router_info.json", "w") as json2:
        router_info = json.dumps(router_info)
        json2.write(router_info)
    with open("router/router_name.txt", "w") as logz:
        logz.write(router_log)
# router_change_info()


def path_change():
    """
    Assignment 6-7: Cost change path

    R1#sh ip ospf interface s0/0 
    Serial0/0 is up, line protocol is up 
    Internet Address 100.2.3.18/30, Area 1 
    Process ID 1, Router ID 100.2.101.1, Network Type POINT_TO_POINT, Cost: 64
    Transmit Delay is 1 sec, State POINT_TO_POINT
    Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5
        oob-resync timeout 40
        Hello due in 00:00:00
    Supports Link-local Signaling (LLS)
    Index 1/1, flood queue length 0
    Next 0x0(0)/0x0(0)
    Last flood scan length is 1, maximum is 2
    Last flood scan time is 0 msec, maximum is 4 msec
    Neighbor Count is 1, Adjacent neighbor count is 1 
        Adjacent with neighbor 100.2.102.1
    Suppress hello for 0 neighbor(s)

    We can control path of OSPF using cost
    R1# ip ospf cost <cost>

    """
    router_log = ""
    int_flag = 1
    for router in router_info:
        traget = router_info[router]['ip']
        cisco = Cisco_router(router_info[router]['ip'],router_info[router]['username'],router_info[router]['password'],router_info[router]['en_password'])
        
        #Information of Router
        
 
        #Login phase
        print('[-] Traget is '+traget)
        print("[-] Connecting to ",traget)

        if cisco.get_connection():
            print("[-]",traget, "Login and Enable Complete ")

        #Disable screen line bug  
        cisco.exec("terminal length 0")

        #Get router name
        text = cisco.exec('sh running-config  | include host')
        text = text.split('\n')[1].split(' ')[1].strip()
        print("[-] ",traget, "Router name is "+text)
        router_log += "[-] Router name is "+text+"\n"
        cisco.set_routername(text)

        print("[-] Now flag is "+str(int_flag))
        cisco.exec("conf t")
        if int_flag == 1:
            cisco.exec("int s0/0")
        else:
            cisco.exec("int s0/1")
        int_flag = int_flag*-1
        #can choose route or clear
        cisco.exec("no ip ospf cost")
        # cisco.exec("ip ospf cost 1000")
        print("[!] OSPF PATH CHANGED!")
        cisco.exec("end")
        cisco.exec("exit")
# path_change()


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

    rt = Cisco_router(router_info['r2']['ip'],router_info['r2']['username'],router_info['r2']['password'],router_info['r2']['en_password'])
    traffic = {}
    print("[-] Connecting to ",rt.router_ip)
    traget = rt.router_ip
    if rt.get_connection():
        print("[-]",traget, "Login and Enable Complete ")

    #Disable screen line bug  
    rt.exec("terminal length 0")

    #Get router name
    text = rt.exec('sh running-config  | include host')
    text = text.split('\n')[1].split(' ')[1].strip()
    print("[-]",traget, "Router name is "+text)
    rt.set_routername(text)

    r1 = Cisco_router(router_info['r1']['ip'],router_info['r1']['username'],router_info['r1']['password'],router_info['r1']['en_password'])
    r1.get_connection()
    r1.exec("teminal len 0")
    text = r1.exec('sh running-config  | include host')
    text = text.split('\n')[1].split(' ')[1].strip()
    print("[-]",r1.router_ip, "Router name is "+text)
    r1.set_routername(text)

    #Start monitoring
    while True:
        time.sleep(5)
        text = rt.exec('sh int s0/0 summary | b Interface')
        text = text.split('\n')[3]
        text = text.split()
        traffic['RXBS'] = int(text[6])
        traffic['RXPS'] = int(text[7])
        traffic['TXBS'] = int(text[8])
        traffic['TXPS'] = int(text[9])
        print("[-] Debug traffic", traffic)
        text = rt.exec('sh ip ospf interface s0/1 | section include Cost').split(',')
        text = text[3].split("\r")[0].strip()
        text = int(text[5:])
        
        #if int s0/1 on R2 cost is 64 == normal route
        if text == 64:
            print("[-] Debug Routing Normal route ")
            #large traffic
            if traffic['RXBS'] > 30000:
                """
                    if large taffic: # RSBX on S0/0 > 10000 bits/sec
                    change cost:
                        R1(S0/0) cost 1000
                        R2(s0/1) cost 1000
                """
                print("[!] Large Traffic Detected!")
                print("[!] Change route path!")
                r1 = r1
                r2 = rt

                #r1 Change path
                print("[-] R1",r1.router_ip,"Login and Enable Complete ")
                r1.exec("conf t")
                r1.exec("int s0/0")
                r1.exec("ip ospf cost 1337")
                r1.exec("end")
                text = r1.exec('sh ip ospf interface s0/0 | section include Cost')
                # print(text)
                if "1337" in text:
                    print("[//] R1 Change int s0/0 cost to 1337 Complete!")

                #r2 Change path
                print("[-] R2",r2.router_ip,"Login and Enable Complete ")
                r2.exec("conf t")
                r2.exec("int s0/1")
                r2.exec("ip ospf cost 1337")
                r2.exec("end")
                text = r2.exec('sh ip ospf interface s0/1 | section include Cost')
                # print(text)
                if "1337" in text:
                    print("[//] R2 Change int s0/1 cost to 1337 Complete!")
            continue #pass checking small traffic
        else:
            #int s0/0 cost != 64 (large cost redirect)
            #check should change to normal route
            if traffic['RXBS'] <= 30000:
                print("[!] Traffic Decrease")
                print("[!] Changing route path to Normal route!")
                r1 = r1
                r2 = rt

                #r1 Change path
                print("[-] R1",r1.router_ip,"Login and Enable Complete ")
                r1.exec("conf t")
                r1.exec("int s0/0")
                r1.exec("no ip ospf cost 1337")
                r1.exec('end')
                text = r1.exec('sh ip ospf interface s0/0 | section include Cost')
                # print(text)
                if "64" in text:
                    print("[//] R1 Change int s0/0 cost to 64 Complete! [Notmal route]")

                #r2 Change path
                print("[-] R2",r2.router_ip,"Login and Enable Complete ")
                r2.exec("conf t")
                r2.exec("int s0/1")
                r2.exec("no ip ospf cost 1337")
                r2.exec('end')
                text = r2.exec('sh ip ospf interface s0/1 | section include Cost')
                # print(text)
                if "64" in text:
                    print("[//] R2 Change int s0/1 cost to 64 Complete! [Notmal route]")


        
traffic_control()
"""
Testing 
root@UbuntuDockerGuest-6:~# iperf3 -c 100.2.102.2 -b 1M -t 300
"""