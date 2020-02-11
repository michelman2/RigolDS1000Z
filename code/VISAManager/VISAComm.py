import pyvisa as ps 

resource_man = ps.ResourceManager()
rsrcs = resource_man.list_resources()
id_instr = "TCPIP:169.254.16.79::INSTR"

# print(rsrcs)
 
inst = resource_man.open_resource('TCPIP:169.254.16.78::INSTR')


# print(inst.query("*IDN?"))