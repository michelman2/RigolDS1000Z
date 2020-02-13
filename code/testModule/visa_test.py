

import pyvisa 
from matplotlib import pyplot as plt
import inspect

f = open("malfunc" , "w")


def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def write_to_file(command): 
    # print(command)
    f.write(command)

def query_points(inst):
    write_to_file("{}: {}".format(lineno(), inst.query(":acquire:averages?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":acquire:mdepth?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":acquire:type?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":acquire:srate?")))

    write_to_file("{}: {}".format(lineno(),inst.query(":channel4:bwlimit?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":channel4:coupling?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":channel4:display?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":channel4:invert?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":channel4:offset?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":channel4:range?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":channel4:tcal?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":channel4:scale?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":channel4:probe?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":channel4:units?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":channel4:vernier?")))

    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:mode?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:manual:type?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:manual:source?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:manual:tunit?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:manual:vunit?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:manual:ax?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:manual:bx?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:manual:ay?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:manual:by?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:manual:axvalue?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:manual:ayvalue?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:manual:bxvalue?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:manual:byvalue?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:manual:xdelta?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:manual:ixdelta?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:manual:ydelta?")))

    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:track:sour1?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:track:sour2?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:track:ax?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:track:ay?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:track:bx?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:track:by?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:track:axvalue?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:track:ayvalue?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:track:bxvalue?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:track:byvalue?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:track:xdelta?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:track:ydelta?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:track:ixdelta?")))

    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:auto:item?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:auto:ax?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:auto:bx?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:auto:ay?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:auto:by?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:auto:axvalue?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:auto:ayvalue?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:auto:bxvalue?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:auto:byvalue?")))
    
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:xy:ax?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:xy:bx?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:xy:ay?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:xy:by?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:xy:axvalue?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:xy:ayvalue?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:xy:bxvalue?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":cursor:xy:byvalue?")))

    ## decoder commands

   
    # write_to_file("{}: {}".format(lineno(),inst.query(":display:data?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":display:type?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":display:grading:time?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":display:wbrightness?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":display:grid?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":display:gbrightness?")))

    ## etable commands

    write_to_file("{}: {}".format(lineno(),inst.query(":function:wrecord:fend?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":function:wrecord:fmax?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":function:wrecord:finterval?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":function:wrecord:prompt?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":function:wrecord:operate?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":function:wrecord:enable?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":function:wreplay:fstart?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":function:wreplay:fend?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":function:wreplay:fmax?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":function:wreplay:finterval?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":function:wreplay:mode?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":function:wreplay:direction?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":function:wreplay:operate?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":function:wreplay:fcurrent?")))


    write_to_file("{}: {}".format(lineno(),inst.query("*esr?")))
    write_to_file("{}: {}".format(lineno(),inst.query("*idn?")))
    write_to_file("{}: {}".format(lineno(),inst.query("*stb?")))
    write_to_file("{}: {}".format(lineno(),inst.query("*tst?")))

    ## LA commands 

    write_to_file("{}: {}".format(lineno(),inst.query(":lan:dhcp?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":lan:autoip?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":lan:gateway?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":lan:dns?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":lan:mac?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":lan:manual?")))
    
    write_to_file("{}: {}".format(lineno(),inst.query(":lan:ipaddress?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":lan:smask?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":lan:status?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":lan:visa?")))
    


    write_to_file("{}: {}".format(lineno(),inst.query(":math:display?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:operator?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:source1?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:source2?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:lsource1?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:lsource2?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:scale?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:offset?")))
   
    write_to_file("{}: {}".format(lineno(),inst.query(":math:fft:source?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:fft:window?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:fft:split?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:fft:unit?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:fft:hscale?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:fft:hcenter?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:fft:mode?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:filter:type?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:filter:w1?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:filter:w2?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:option:start?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:option:end?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:option:invert?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:option:sens?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:option:dis?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:option:asc?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:option:thr1?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:option:thr2?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:option:fx:sour1?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:option:fx:sour2?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":math:option:fx:oper?")))


    write_to_file("{}: {}".format(lineno(),inst.query(":mask:enable?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":mask:sour?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":mask:oper?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":mask:mdis?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":mask:soo?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":mask:outp?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":mask:x?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":mask:y?")))
    
    write_to_file("{}: {}".format(lineno(),inst.query(":mask:pass?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":mask:failed?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":mask:tot?")))
    


    write_to_file("{}: {}".format(lineno(),inst.query(":meas:sour?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":meas:counter:sour?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":meas:counter:value?")))
    
    
    write_to_file("{}: {}".format(lineno(),inst.query(":meas:adisplay?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":meas:ams?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":meas:setup:max?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":meas:setup:mid?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":meas:setup:min?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":meas:setup:psa?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":meas:setup:psb?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":meas:setup:dsa?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":meas:setup:dsb?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":meas:stat:disp?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":meas:stat:mode?")))
 
    # write_to_file("{}: {}".format(lineno(),inst.query(":meas:stat:item?")))
    # write_to_file("{}: {}".format(lineno(),inst.query(":meas:item?")))
    
    ## reference commands

    write_to_file("{}: {}".format(lineno(),inst.query(":source1:output1:state?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":source1:output2:state?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":source2:output1:state?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":source2:output2:state?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":source1:output1:impedance?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":source1:output2:impedance?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":source2:output1:impedance?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":source2:output2:impedance?")))
    
    # inst.query(":source1:freq?")
    # inst.query(":source2:freq?")
    # inst.query(":source1:phase?")
    # inst.query(":source2:phase?")
    # source commands

    write_to_file("{}: {}".format(lineno(),inst.query(":storage:image:type?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":storage:image:invert?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":storage:image:color?")))

    write_to_file("{}: {}".format(lineno(),inst.query(":system:autoscale?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":system:beep?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":system:error?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":system:gam?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":system:lang?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":system:lock?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":system:pon?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":system:ram?")))

    
    inst.write(":system:setup?")
    write_to_file("{}: {}".format(lineno(),inst.read_raw()))


    ## trace commands

    write_to_file("{}: {}".format(lineno(),inst.query(":tim:del:enab?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":tim:del:offs?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":tim:del:scal?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":tim:main:offs?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":tim:main:scale?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":tim:mode?")))
    
    
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:mode?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:coup?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:stat?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:swe?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:hold?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:nrej?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:pos?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:edg:sour?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:edg:slop?")))
    
    inst.write("trig:edg:lev?")
    write_to_file("{}: {}".format(lineno(),inst.read_raw()))

    write_to_file("{}: {}".format(lineno(),inst.query(":trig:puls:sour?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:puls:when?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:puls:width?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:puls:uwidth?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:puls:lwidth?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:puls:level?")))

    
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:slop:sour?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:slop:when?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:slop:time?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:slop:tupper?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:slop:tlow?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:slop:wind?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:slop:alev?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:slop:blev?")))

    write_to_file("{}: {}".format(lineno(),inst.query(":trig:vid:sour?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:vid:pol?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:vid:mode?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:vid:line?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:vid:stan?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:vid:lev?")))

    inst.write(":trig:patt:patt?")
    write_to_file("{}: {}".format(lineno(),inst.read_raw()))
    
    write_to_file("{}: {}".format(lineno(),inst.query(":TRIGger:PATTern:LEVel? CHANnel4")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:durat:sour?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:durat:typ?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:durat:when?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:durat:tupp?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:durat:tlow?")))

    write_to_file("{}: {}".format(lineno(),inst.query(":trig:tim:sour?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:tim:slop?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:tim:tim?")))

    write_to_file("{}: {}".format(lineno(),inst.query(":trig:runt:sour?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:runt:pol?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:runt:when?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:runt:wupp?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:runt:wlow?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:runt:alev?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:runt:blev?")))

    write_to_file("{}: {}".format(lineno(),inst.query(":trig:wind:sour?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:wind:slop?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:wind:pos?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:wind:tim?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:wind:alev?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:wind:blev?")))

    write_to_file("{}: {}".format(lineno(),inst.query(":trig:del:sa?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:del:slopa?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:del:sb?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:del:slopb?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:del:typ?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:del:tupper?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:del:tlower?")))

    write_to_file("{}: {}".format(lineno(),inst.query(":trig:shold:ds?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:shold:cs?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:shold:slop?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:shold:patt?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:shold:typ?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:shold:stim?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:shold:htim?")))

    write_to_file("{}: {}".format(lineno(),inst.query(":trig:nedge:sour?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:nedge:slop?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:nedge:idle?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:nedge:edge?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":trig:nedge:lev?")))

    # write_to_file("{}: {}".format(lineno(),inst.query(":trig:rs232?")))
    # write_to_file("{}: {}".format(lineno(),inst.query(":trig:iic?")))
    # write_to_file("{}: {}".format(lineno(),inst.query(":trig:spi?")))


    write_to_file("{}: {}".format(lineno(),inst.query(":waveform:source?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":waveform:mode?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":waveform:format?")))
    # write_to_file("{}: {}".format(lineno(),inst.query(":waveform:data?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":waveform:xincrement?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":waveform:xorigin?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":waveform:xreference?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":waveform:yincrement?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":waveform:yorigin?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":waveform:yreference?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":waveform:start?")))
    write_to_file("{}: {}".format(lineno(),inst.query(":waveform:stop?")))

    inst.write(":waveform:preamble?")
    write_to_file("{}: {}".format(lineno(),inst.read_raw()))
    
    



rm = pyvisa.ResourceManager()
a = rm.list_resources()
inst = rm.open_resource('TCPIP0::169.254.16.78::INSTR')
print(inst.query("*IDN?"))
inst.write(":run")

inst.write(":waveform:source channel4")
inst.write(":waveform:mode normal")
inst.write(":waveform:format ASCII")
data = inst.query(":waveform:data?").split(",")



query_points(inst)

f.close()

inst.close()

float_data = [float(x) for x in data[3:len(data)-3]]
plt.plot(range(0 , len(float_data)) , float_data)
plt.show()