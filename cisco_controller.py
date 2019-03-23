"""
    Cisco router Controller
"""
import telnetlib

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
        self.telnet.write("terminal length 0")
        return True

    def set_routername(self,rt_name):
        self.router_name = rt_name

    def get_routername(self):
        return self.router_name

    def exec(self,cmd):
        self.telnet.write(cmd.encode('ascii')+b'\n')
        text = self.telnet.read_until((self.router_name+"#").encode('ascii'), 5).decode('utf-8')
        return text
    def close(self):
        self.exec('end')
        self.exec('exit')
