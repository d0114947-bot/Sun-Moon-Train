import json,math,sys
from playwright.sync_api import sync_playwright
A1="stage:'free',tut:5,flags:{high:1,near:1,water:1},got:['first','water','curtain','still'],senseN:3,againN:1,passN:2,ended:true,cz:1800,exT:50,sinceFirst:200,lastPass:100"
A2="{firstAnomalySeen:true,firstSwitchCompleted:true,canSwitch:true,freeSwitchTutorialCompleted:true,switchCount:4,trail:[],trailSeen:true,trailMark:0,completed:true}"
Y=math.atan2(-1,-1); SQ=0.7071
def setup(x,y,z,yaw,dim='unresolved',seen='true',vw=(1280,720)):
    return f"ACT1.active()&&ACT1.exit();state=freshState();state.chapter='act1';state.act1={{{A1},pos:{json.dumps({'x':x,'y':y,'z':z,'yaw':yaw})}}};state.world={{location:'sleeping_land',dimension:'{dim}'}};state.act2={A2};state.act3={{trainSeen:{seen},obs:[]}};save();ACT1.enter()"
shots=[('far',0,10,0,Y,'unresolved'),('farmoon',-150,14,-150,Y,'moon'),('near',-460+95*SQ+30*SQ,22,-460+95*SQ-30*SQ,Y,'unresolved'),('side',-460+45*SQ+5*SQ,17,-460+45*SQ-5*SQ,Y,'moon'),('loco',-460+40*SQ+40*SQ,24,-460+40*SQ-40*SQ,Y-0.6,'unresolved')]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); pg.add_init_script("window.ACT1_TEST=true;window.ACT1_SPEED=4")
    pg.goto('http://127.0.0.1:8766/'); pg.wait_for_timeout(900)
    for n,x,y,z,yaw,d in shots:
        pg.evaluate(setup(x,y,z,yaw,d)); pg.wait_for_timeout(7000); pg.screenshot(path=f'a3v_{n}.png')
