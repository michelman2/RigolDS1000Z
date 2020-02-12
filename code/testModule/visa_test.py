

import pyvisa 
from matplotlib import pyplot as plt
import inspect

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def query_points(inst):
    print("{}: {}".format(lineno(), inst.query(":acquire:averages?")))
    print("{}: {}".format(lineno(),inst.query(":acquire:mdepth?")))
    print("{}: {}".format(lineno(),inst.query(":acquire:type?")))
    print("{}: {}".format(lineno(),inst.query(":acquire:srate?")))

    print("{}: {}".format(lineno(),inst.query(":channel4:bwlimit?")))
    print("{}: {}".format(lineno(),inst.query(":channel4:coupling?")))
    print("{}: {}".format(lineno(),inst.query(":channel4:display?")))
    print("{}: {}".format(lineno(),inst.query(":channel4:invert?")))
    print("{}: {}".format(lineno(),inst.query(":channel4:offset?")))
    print("{}: {}".format(lineno(),inst.query(":channel4:range?")))
    print("{}: {}".format(lineno(),inst.query(":channel4:tcal?")))
    print("{}: {}".format(lineno(),inst.query(":channel4:scale?")))
    print("{}: {}".format(lineno(),inst.query(":channel4:probe?")))
    print("{}: {}".format(lineno(),inst.query(":channel4:units?")))
    print("{}: {}".format(lineno(),inst.query(":channel4:vernier?")))

    print("{}: {}".format(lineno(),inst.query(":cursor:mode?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:manual:type?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:manual:source?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:manual:tunit?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:manual:vunit?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:manual:ax?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:manual:bx?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:manual:ay?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:manual:by?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:manual:axvalue?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:manual:ayvalue?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:manual:bxvalue?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:manual:byvalue?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:manual:xdelta?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:manual:ixdelta?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:manual:ydelta?")))

    print("{}: {}".format(lineno(),inst.query(":cursor:track:sour1?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:track:sour2?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:track:ax?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:track:ay?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:track:bx?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:track:by?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:track:axvalue?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:track:ayvalue?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:track:bxvalue?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:track:byvalue?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:track:xdelta?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:track:ydelta?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:track:ixdelta?")))

    print("{}: {}".format(lineno(),inst.query(":cursor:auto:item?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:auto:ax?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:auto:bx?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:auto:ay?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:auto:by?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:auto:axvalue?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:auto:ayvalue?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:auto:bxvalue?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:auto:byvalue?")))
    
    print("{}: {}".format(lineno(),inst.query(":cursor:xy:ax?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:xy:bx?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:xy:ay?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:xy:by?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:xy:axvalue?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:xy:ayvalue?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:xy:bxvalue?")))
    print("{}: {}".format(lineno(),inst.query(":cursor:xy:byvalue?")))

    ## decoder commands

   
    # print("{}: {}".format(lineno(),inst.query(":display:data?")))
    print("{}: {}".format(lineno(),inst.query(":display:type?")))
    print("{}: {}".format(lineno(),inst.query(":display:grading:time?")))
    print("{}: {}".format(lineno(),inst.query(":display:wbrightness?")))
    print("{}: {}".format(lineno(),inst.query(":display:grid?")))
    print("{}: {}".format(lineno(),inst.query(":display:gbrightness?")))

    ## etable commands

    print("{}: {}".format(lineno(),inst.query(":function:wrecord:fend?")))
    print("{}: {}".format(lineno(),inst.query(":function:wrecord:fmax?")))
    print("{}: {}".format(lineno(),inst.query(":function:wrecord:finterval?")))
    print("{}: {}".format(lineno(),inst.query(":function:wrecord:prompt?")))
    print("{}: {}".format(lineno(),inst.query(":function:wrecord:operate?")))
    print("{}: {}".format(lineno(),inst.query(":function:wrecord:enable?")))
    print("{}: {}".format(lineno(),inst.query(":function:wreplay:fstart?")))
    print("{}: {}".format(lineno(),inst.query(":function:wreplay:fend?")))
    print("{}: {}".format(lineno(),inst.query(":function:wreplay:fmax?")))
    print("{}: {}".format(lineno(),inst.query(":function:wreplay:finterval?")))
    print("{}: {}".format(lineno(),inst.query(":function:wreplay:mode?")))
    print("{}: {}".format(lineno(),inst.query(":function:wreplay:direction?")))
    print("{}: {}".format(lineno(),inst.query(":function:wreplay:operate?")))
    print("{}: {}".format(lineno(),inst.query(":function:wreplay:fcurrent?")))


    print("{}: {}".format(lineno(),inst.query("*esr?")))
    print("{}: {}".format(lineno(),inst.query("*idn?")))
    print("{}: {}".format(lineno(),inst.query("*stb?")))
    print("{}: {}".format(lineno(),inst.query("*tst?")))

    ## LA commands 

    print("{}: {}".format(lineno(),inst.query(":lan:dhcp?")))
    print("{}: {}".format(lineno(),inst.query(":lan:autoip?")))
    print("{}: {}".format(lineno(),inst.query(":lan:gateway?")))
    print("{}: {}".format(lineno(),inst.query(":lan:dns?")))
    print("{}: {}".format(lineno(),inst.query(":lan:mac?")))
    print("{}: {}".format(lineno(),inst.query(":lan:manual?")))
    
    print("{}: {}".format(lineno(),inst.query(":lan:ipaddress?")))
    print("{}: {}".format(lineno(),inst.query(":lan:smask?")))
    print("{}: {}".format(lineno(),inst.query(":lan:status?")))
    print("{}: {}".format(lineno(),inst.query(":lan:visa?")))
    


    print("{}: {}".format(lineno(),inst.query(":math:display?")))
    print("{}: {}".format(lineno(),inst.query(":math:operator?")))
    print("{}: {}".format(lineno(),inst.query(":math:source1?")))
    print("{}: {}".format(lineno(),inst.query(":math:source2?")))
    print("{}: {}".format(lineno(),inst.query(":math:lsource1?")))
    print("{}: {}".format(lineno(),inst.query(":math:lsource2?")))
    print("{}: {}".format(lineno(),inst.query(":math:scale?")))
    print("{}: {}".format(lineno(),inst.query(":math:offset?")))
   
    print("{}: {}".format(lineno(),inst.query(":math:fft:source?")))
    print("{}: {}".format(lineno(),inst.query(":math:fft:window?")))
    print("{}: {}".format(lineno(),inst.query(":math:fft:split?")))
    print("{}: {}".format(lineno(),inst.query(":math:fft:unit?")))
    print("{}: {}".format(lineno(),inst.query(":math:fft:hscale?")))
    print("{}: {}".format(lineno(),inst.query(":math:fft:hcenter?")))
    print("{}: {}".format(lineno(),inst.query(":math:fft:mode?")))
    print("{}: {}".format(lineno(),inst.query(":math:filter:type?")))
    print("{}: {}".format(lineno(),inst.query(":math:filter:w1?")))
    print("{}: {}".format(lineno(),inst.query(":math:filter:w2?")))
    print("{}: {}".format(lineno(),inst.query(":math:option:start?")))
    print("{}: {}".format(lineno(),inst.query(":math:option:end?")))
    print("{}: {}".format(lineno(),inst.query(":math:option:invert?")))
    print("{}: {}".format(lineno(),inst.query(":math:option:sens?")))
    print("{}: {}".format(lineno(),inst.query(":math:option:dis?")))
    print("{}: {}".format(lineno(),inst.query(":math:option:asc?")))
    print("{}: {}".format(lineno(),inst.query(":math:option:thr1?")))
    print("{}: {}".format(lineno(),inst.query(":math:option:thr2?")))
    print("{}: {}".format(lineno(),inst.query(":math:option:fx:sour1?")))
    print("{}: {}".format(lineno(),inst.query(":math:option:fx:sour2?")))
    print("{}: {}".format(lineno(),inst.query(":math:option:fx:oper?")))


    print("{}: {}".format(lineno(),inst.query(":mask:enable?")))
    print("{}: {}".format(lineno(),inst.query(":mask:sour?")))
    print("{}: {}".format(lineno(),inst.query(":mask:oper?")))
    print("{}: {}".format(lineno(),inst.query(":mask:mdis?")))
    print("{}: {}".format(lineno(),inst.query(":mask:soo?")))
    print("{}: {}".format(lineno(),inst.query(":mask:outp?")))
    print("{}: {}".format(lineno(),inst.query(":mask:x?")))
    print("{}: {}".format(lineno(),inst.query(":mask:y?")))
    
    print("{}: {}".format(lineno(),inst.query(":mask:pass?")))
    print("{}: {}".format(lineno(),inst.query(":mask:failed?")))
    print("{}: {}".format(lineno(),inst.query(":mask:tot?")))
    


    print("{}: {}".format(lineno(),inst.query(":meas:sour?")))
    print("{}: {}".format(lineno(),inst.query(":meas:counter:sour?")))
    print("{}: {}".format(lineno(),inst.query(":meas:counter:value?")))
    
    
    print("{}: {}".format(lineno(),inst.query(":meas:adisplay?")))
    print("{}: {}".format(lineno(),inst.query(":meas:ams?")))
    print("{}: {}".format(lineno(),inst.query(":meas:setup:max?")))
    print("{}: {}".format(lineno(),inst.query(":meas:setup:mid?")))
    print("{}: {}".format(lineno(),inst.query(":meas:setup:min?")))
    print("{}: {}".format(lineno(),inst.query(":meas:setup:psa?")))
    print("{}: {}".format(lineno(),inst.query(":meas:setup:psb?")))
    print("{}: {}".format(lineno(),inst.query(":meas:setup:dsa?")))
    print("{}: {}".format(lineno(),inst.query(":meas:setup:dsb?")))
    print("{}: {}".format(lineno(),inst.query(":meas:stat:disp?")))
    print("{}: {}".format(lineno(),inst.query(":meas:stat:mode?")))
 
    # print("{}: {}".format(lineno(),inst.query(":meas:stat:item?")))
    # print("{}: {}".format(lineno(),inst.query(":meas:item?")))
    
    ## reference commands

    print("{}: {}".format(lineno(),inst.query(":source1:output1:state?")))
    print("{}: {}".format(lineno(),inst.query(":source1:output2:state?")))
    print("{}: {}".format(lineno(),inst.query(":source2:output1:state?")))
    print("{}: {}".format(lineno(),inst.query(":source2:output2:state?")))
    print("{}: {}".format(lineno(),inst.query(":source1:output1:impedance?")))
    print("{}: {}".format(lineno(),inst.query(":source1:output2:impedance?")))
    print("{}: {}".format(lineno(),inst.query(":source2:output1:impedance?")))
    print("{}: {}".format(lineno(),inst.query(":source2:output2:impedance?")))
    
    # inst.query(":source1:freq?")
    # inst.query(":source2:freq?")
    # inst.query(":source1:phase?")
    # inst.query(":source2:phase?")
    # source commands

    print("{}: {}".format(lineno(),inst.query(":storage:image:type?")))
    print("{}: {}".format(lineno(),inst.query(":storage:image:invert?")))
    print("{}: {}".format(lineno(),inst.query(":storage:image:color?")))

    print("{}: {}".format(lineno(),inst.query(":system:autoscale?")))
    print("{}: {}".format(lineno(),inst.query(":system:beep?")))
    print("{}: {}".format(lineno(),inst.query(":system:error?")))
    print("{}: {}".format(lineno(),inst.query(":system:gam?")))
    print("{}: {}".format(lineno(),inst.query(":system:lang?")))
    print("{}: {}".format(lineno(),inst.query(":system:lock?")))
    print("{}: {}".format(lineno(),inst.query(":system:pon?")))
    print("{}: {}".format(lineno(),inst.query(":system:ram?")))

    ## ascii problem
    # print("{}: {}".format(lineno(),inst.query(":SYSTem:SETup?")))


    ## trace commands

    print("{}: {}".format(lineno(),inst.query(":tim:del:enab?")))
    print("{}: {}".format(lineno(),inst.query(":tim:del:offs?")))
    print("{}: {}".format(lineno(),inst.query(":tim:del:scal?")))
    print("{}: {}".format(lineno(),inst.query(":tim:main:offs?")))
    print("{}: {}".format(lineno(),inst.query(":tim:main:scale?")))
    print("{}: {}".format(lineno(),inst.query(":tim:mode?")))
    
    
    print("{}: {}".format(lineno(),inst.query(":trig:mode?")))
    print("{}: {}".format(lineno(),inst.query(":trig:coup?")))
    print("{}: {}".format(lineno(),inst.query(":trig:stat?")))
    print("{}: {}".format(lineno(),inst.query(":trig:swe?")))
    print("{}: {}".format(lineno(),inst.query(":trig:hold?")))
    print("{}: {}".format(lineno(),inst.query(":trig:nrej?")))
    print("{}: {}".format(lineno(),inst.query(":trig:pos?")))
    print("{}: {}".format(lineno(),inst.query(":trig:edg:sour?")))
    print("{}: {}".format(lineno(),inst.query(":trig:edg:slop?")))
    ## ascii problem
    # print("{}: {}".format(lineno(),inst.query(":trig:edg:lev?")))
    print("{}: {}".format(lineno(),inst.query(":trig:puls:sour?")))
    print("{}: {}".format(lineno(),inst.query(":trig:puls:when?")))
    print("{}: {}".format(lineno(),inst.query(":trig:puls:width?")))
    print("{}: {}".format(lineno(),inst.query(":trig:puls:uwidth?")))
    print("{}: {}".format(lineno(),inst.query(":trig:puls:lwidth?")))
    print("{}: {}".format(lineno(),inst.query(":trig:puls:level?")))

    
    print("{}: {}".format(lineno(),inst.query(":trig:slop:sour?")))
    print("{}: {}".format(lineno(),inst.query(":trig:slop:when?")))
    print("{}: {}".format(lineno(),inst.query(":trig:slop:time?")))
    print("{}: {}".format(lineno(),inst.query(":trig:slop:tupper?")))
    print("{}: {}".format(lineno(),inst.query(":trig:slop:tlow?")))
    print("{}: {}".format(lineno(),inst.query(":trig:slop:wind?")))
    print("{}: {}".format(lineno(),inst.query(":trig:slop:alev?")))
    print("{}: {}".format(lineno(),inst.query(":trig:slop:blev?")))

    print("{}: {}".format(lineno(),inst.query(":trig:vid:sour?")))
    print("{}: {}".format(lineno(),inst.query(":trig:vid:pol?")))
    print("{}: {}".format(lineno(),inst.query(":trig:vid:mode?")))
    print("{}: {}".format(lineno(),inst.query(":trig:vid:line?")))
    print("{}: {}".format(lineno(),inst.query(":trig:vid:stan?")))
    print("{}: {}".format(lineno(),inst.query(":trig:vid:lev?")))

    ## ascii
    # print("{}: {}".format(lineno(),inst.query(":trig:patt:patt?")))
    print("{}: {}".format(lineno(),inst.query(":TRIGger:PATTern:LEVel? CHANnel4")))

    print("{}: {}".format(lineno(),inst.query(":trig:durat:sour?")))
    print("{}: {}".format(lineno(),inst.query(":trig:durat:typ?")))
    print("{}: {}".format(lineno(),inst.query(":trig:durat:when?")))
    print("{}: {}".format(lineno(),inst.query(":trig:durat:tupp?")))
    print("{}: {}".format(lineno(),inst.query(":trig:durat:tlow?")))

    print("{}: {}".format(lineno(),inst.query(":trig:tim:sour?")))
    print("{}: {}".format(lineno(),inst.query(":trig:tim:slop?")))
    print("{}: {}".format(lineno(),inst.query(":trig:tim:tim?")))

    print("{}: {}".format(lineno(),inst.query(":trig:runt:sour?")))
    print("{}: {}".format(lineno(),inst.query(":trig:runt:pol?")))
    print("{}: {}".format(lineno(),inst.query(":trig:runt:when?")))
    print("{}: {}".format(lineno(),inst.query(":trig:runt:wupp?")))
    print("{}: {}".format(lineno(),inst.query(":trig:runt:wlow?")))
    print("{}: {}".format(lineno(),inst.query(":trig:runt:alev?")))
    print("{}: {}".format(lineno(),inst.query(":trig:runt:blev?")))

    print("{}: {}".format(lineno(),inst.query(":trig:wind:sour?")))
    print("{}: {}".format(lineno(),inst.query(":trig:wind:slop?")))
    print("{}: {}".format(lineno(),inst.query(":trig:wind:pos?")))
    print("{}: {}".format(lineno(),inst.query(":trig:wind:tim?")))
    print("{}: {}".format(lineno(),inst.query(":trig:wind:alev?")))
    print("{}: {}".format(lineno(),inst.query(":trig:wind:blev?")))

    print("{}: {}".format(lineno(),inst.query(":trig:del:sa?")))
    print("{}: {}".format(lineno(),inst.query(":trig:del:slopa?")))
    print("{}: {}".format(lineno(),inst.query(":trig:del:sb?")))
    print("{}: {}".format(lineno(),inst.query(":trig:del:slopb?")))
    print("{}: {}".format(lineno(),inst.query(":trig:del:typ?")))
    print("{}: {}".format(lineno(),inst.query(":trig:del:tupper?")))
    print("{}: {}".format(lineno(),inst.query(":trig:del:tlower?")))

    print("{}: {}".format(lineno(),inst.query(":trig:shold:ds?")))
    print("{}: {}".format(lineno(),inst.query(":trig:shold:cs?")))
    print("{}: {}".format(lineno(),inst.query(":trig:shold:slop?")))
    print("{}: {}".format(lineno(),inst.query(":trig:shold:patt?")))
    print("{}: {}".format(lineno(),inst.query(":trig:shold:typ?")))
    print("{}: {}".format(lineno(),inst.query(":trig:shold:stim?")))
    print("{}: {}".format(lineno(),inst.query(":trig:shold:htim?")))

    print("{}: {}".format(lineno(),inst.query(":trig:nedge:sour?")))
    print("{}: {}".format(lineno(),inst.query(":trig:nedge:slop?")))
    print("{}: {}".format(lineno(),inst.query(":trig:nedge:idle?")))
    print("{}: {}".format(lineno(),inst.query(":trig:nedge:edge?")))
    print("{}: {}".format(lineno(),inst.query(":trig:nedge:lev?")))

    # print("{}: {}".format(lineno(),inst.query(":trig:rs232?")))
    # print("{}: {}".format(lineno(),inst.query(":trig:iic?")))
    # print("{}: {}".format(lineno(),inst.query(":trig:spi?")))


    print("{}: {}".format(lineno(),inst.query(":waveform:source?")))
    print("{}: {}".format(lineno(),inst.query(":waveform:mode?")))
    print("{}: {}".format(lineno(),inst.query(":waveform:format?")))
    # print("{}: {}".format(lineno(),inst.query(":waveform:data?")))
    print("{}: {}".format(lineno(),inst.query(":waveform:xincrement?")))
    print("{}: {}".format(lineno(),inst.query(":waveform:xorigin?")))
    print("{}: {}".format(lineno(),inst.query(":waveform:xreference?")))
    print("{}: {}".format(lineno(),inst.query(":waveform:yincrement?")))
    print("{}: {}".format(lineno(),inst.query(":waveform:yorigin?")))
    print("{}: {}".format(lineno(),inst.query(":waveform:yreference?")))
    print("{}: {}".format(lineno(),inst.query(":waveform:start?")))
    print("{}: {}".format(lineno(),inst.query(":waveform:stop?")))
    ## ascii problem
    # print("{}: {}".format(lineno(),inst.query(":waveform:preamble?")))
    
    



rm = pyvisa.ResourceManager()
a = rm.list_resources()
inst = rm.open_resource('TCPIP0::169.254.16.78::INSTR')
print(inst.query("*IDN?"))
inst.write(":run")

inst.write(":waveform:source 4")
inst.write(":waveform:mode normal")
inst.write(":waveform:format ASCII")
data = inst.query(":waveform:data?")

# query_points(inst)
