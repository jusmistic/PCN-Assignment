import telnetlib
import subprocess
import json
import threading
import cisco_controller

"""
    Assigment 3: Traceroute on router
"""
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

traceroute()