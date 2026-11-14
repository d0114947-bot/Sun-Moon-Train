# 第一幕逐像素基準：python3 pix.py save|check
import sys, json, hashlib, base64
from playwright.sync_api import sync_playwright
MODE=sys.argv[1]; OUT='pix_base.json'
CASES=[
 ('start',  {'x':0,'y':3,'z':0,'yaw':0},     'free',{}, 2.0),
 ('high',   {'x':0,'y':140,'z':0,'yaw':0},   'free',{}, 7.3),
 ('curtain',{'x':12,'y':20,'z':1560,'yaw':0},'free',{}, 11.1),
 ('water',  {'x':-30,'y':1.6,'z':40,'yaw':0},'free',{}, 4.4),
 ('turn',   {'x':5,'y':12,'z':80,'yaw':2.4}, 'free',{}, 9.9),
 ('back',   {'x':0,'y':30,'z':300,'yaw':3.14},'free',{}, 13.7),
 ('held',   {'x':0,'y':8,'z':20,'yaw':.6},   'held',{}, 5.5),
 ('far',    {'x':1500,'y':25,'z':900,'yaw':-.8},'free',{}, 21.2)]
res={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    for vw in [(1280,720),(390,844)]:
        pg=b.new_page(viewport={'width':vw[0],'height':vw[1]}); ev=pg.evaluate
        pg.add_init_script("window.ACT1_TEST=true")
        pg.goto('http://127.0.0.1:8766/'); pg.wait_for_timeout(900)
        for name,pos,stage,_,t in CASES:
            ev(f"ACT1.active()&&ACT1.exit(); window.ACT1_FREEZE={t}")
            ev(f"state=freshState();state.chapter='act1';state.act1={{stage:'{stage}',tut:5,flags:{{high:1,near:1,water:1}},got:['first'],senseN:1,againN:1,passN:1,ended:true,pos:{json.dumps(pos)},cz:1800,exT:50,sinceFirst:5,lastPass:-999}};state.world={{location:'sleeping_land',dimension:'unresolved'}};state.act2={{firstAnomalySeen:true,firstSwitchCompleted:true,canSwitch:true,freeSwitchTutorialCompleted:true,switchCount:2}};save();ACT1.enter()")
            pg.wait_for_timeout(2500)   # 凍結狀態下進入：物理、邏輯都不跑，只畫指定時刻
            d=ev("document.querySelector('.a1-cv').toDataURL('image/png')")
            h=hashlib.sha256(base64.b64decode(d.split(',')[1])).hexdigest()
            key=f"{vw[0]}x{vw[1]}:{name}"; res[key]=h
            if MODE=='save': open(f'pixbase_{vw[0]}_{name}.png','wb').write(base64.b64decode(d.split(',')[1]))
        pg.close()
if MODE=='save':
    json.dump(res,open(OUT,'w'),indent=1); print('saved',len(res))
else:
    base=json.load(open(OUT)); bad=[k for k in base if base[k]!=res.get(k)]
    print('PIXEL IDENTICAL' if not bad else 'PIXEL DIFF '+', '.join(bad), len(base))
