# 第三幕：遠方的異常景象 → 發現列車 → 觀察點 → 進入列車 → 接上列車遊戲
import json,sys,math
from playwright.sync_api import sync_playwright
R=[]; SNAP='--snap' in sys.argv
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
A1="stage:'free',tut:5,flags:{high:1,near:1,water:1},got:['first','water','curtain','still'],senseN:3,againN:1,passN:2,ended:true,cz:1800,exT:50,sinceFirst:200,lastPass:100"
A2D="{firstAnomalySeen:true,firstSwitchCompleted:true,canSwitch:true,freeSwitchTutorialCompleted:true,switchCount:4,trail:[],trailSeen:true,trailMark:0,completed:%s}"
YAW=math.atan2(-1,-1)
def setup(pos,done=True,a3="null",dim='unresolved'):
    return f"ACT1.active()&&ACT1.exit();closeAll();state=freshState();state.chapter='act1';state.act1={{{A1},pos:{json.dumps(pos)}}};state.world={{location:'sleeping_land',dimension:'{dim}'}};state.act2={A2D%('true' if done else 'false')};state.act3={a3};if(!state.act3)delete state.act3;save();ACT1.enter()"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.ACT1_TEST=true; window.ACT1_SPEED=4")
    def until(js,ms=40000):
        try: pg.wait_for_function(js,timeout=ms); return True
        except Exception: return False
    D=lambda: ev("ACT3._dbg()")
    def snap(n):
        if SNAP: pg.screenshot(path=f'a3s_{n}.png')
    def adv(js,ms=60000):
        t=0
        while t<ms:
            if ev(js): return True
            ev("(()=>{const d=document.querySelector('#layer .cine')||document.querySelector('#layer .dlg');if(d)d.click();})()"); W(700); t+=700
        return False
    def tele(q,yaw=None):
        ev(f"ACT1._set({{P:{{x:{q[0]},y:{q[1]},z:{q[2]}{',yaw:'+str(yaw) if yaw is not None else ''},vx:0,vy:0,vz:0}}}})")
    pg.goto('http://127.0.0.1:8766/'); W(900)
    # ---- 第二幕未完成：第三幕不出現
    ev(setup({'x':-250,'y':22,'z':-250,'yaw':YAW},done=False)); W(3000)
    ok('N1 act2 not completed: nothing of act3', not D()['act'] and D()['ap']==0 and not ev("state.act3.trainSeen"))
    # ---- 第二幕完成：遠方的星光逐漸變密、縫隙出現
    ev(setup({'x':0,'y':8,'z':0,'yaw':YAW})); W(1500)
    ok('N2 act2 completed: act3 active', D()['act'])
    ok('N3 rifts fade in (from the far view)', until("ACT3._dbg().ap>=.99",30000)); snap('far')
    ok('N4 not seen from far away yet', not ev("state.act3.trainSeen"))
    # ---- 場景一：發現列車
    ev(setup({'x':-250,'y':22,'z':-250,'yaw':YAW})); W(1200)
    ok('T1 approaching the rift: spirit stops and sees the train', until("state.act3.trainSeen",30000) and ev("ACT1.api.lock"))
    ok('T2 line 「那是……列車？」', until("document.querySelector('.a1-say').textContent.includes('列車')",20000)); snap('seen')
    ok('T3 control returns', until("!ACT1.api.lock",30000))
    ok('T4 train does not react (no state change besides seen)', ev("state.act3.obs.length")==0 and not ev("state.act3.entered"))
    # ---- 車門：還沒觀察 → 不能進
    q=ev("ACT3.spot('door')"); tele([q[0]+6*0.7071,q[1],q[2]+6*0.7071],YAW); W(2500)
    ok('E1 door before any observation: no enter button', not D()['btn'])
    ok('E2 gentle line instead', until("document.querySelector('.a1-say').textContent.includes('看看四周')",20000))
    # ---- 觀察點
    until("!ACT1.api.saying()",20000)
    q=ev("ACT3.spot('carving')"); tele([q[0]+8*0.7071,q[1],q[2]+8*0.7071],YAW); W(1800); snap('carving')
    ok('O1 near a spot: 觀察 button', until("ACT3._dbg().btn&&ACT3._dbg().near==='carving'",20000) and '觀察' in ev("document.querySelector('.a3-act').textContent"))
    pg.keyboard.press('Enter'); ok('O2 observed and recorded', until("state.act3.obs.includes('carving')",10000))
    ok('O3 observation thought', until("document.querySelector('.a1-say').textContent.includes('紋路')",20000))
    ok('O4 observed spot no longer offered', until("!ACT1.api.saying()",20000) and (W(1200) or True) and D()['near']!='carving')
    for k in ['texture','shard','struct']:
        q=ev(f"ACT3.spot('{k}')"); tele([q[0]+7*0.7071,q[1],q[2]+7*0.7071],YAW); W(1500)
        if until(f"ACT3._dbg().near==='{k}'",15000): pg.click('.a3-act')
        until("!ACT1.api.saying()",20000)
    ok('O5 all four spots, each once', sorted(ev("state.act3.obs"))==['carving','shard','struct','texture'], ev("state.act3.obs"))
    # ---- 存檔恢復：還沒進列車
    ev("ACT1.api.persist()"); st=ev("JSON.stringify(state)"); ev("ACT1.exit()"); ev(f"loadGame(JSON.parse({json.dumps(st)}),'t')"); W(2500)
    ok('R1 resume before entering: back in the sleeping land, no replay', ev("ACT1.active()") and ev("state.act3.trainSeen") and not ev("ACT1.api.lock") and len(ev("state.act3.obs"))==4)
    # ---- 進入列車
    q=ev("ACT3.spot('door')"); tele([q[0]+6*0.7071,q[1],q[2]+6*0.7071],YAW); W(1500); snap('door')
    ok('I1 door after observing: 進入 button', until("ACT3._dbg().near==='door'",15000) and '進入' in ev("document.querySelector('.a3-act').textContent"))
    pg.keyboard.press('Enter'); ok('I2 fade and enter the train', until("!ACT1.active()&&state.introDone",20000))
    ok('I3 train game starts in the habitat carriage, docked at the rift', ev("state.currentCarriage")=='habitat' and ev("state.currentPhase")=='docked' and ev("LOCATIONS.origin.name")=='世界縫隙')
    ok('I4 line 「這裡……竟然有這麼大的空間。」', until("(document.querySelector('#layer .dlg')||{}).textContent&&document.querySelector('#layer .dlg').textContent.includes('這麼大的空間')",20000)); snap('inside')
    ok('I5 ancient inscription introduces the train', adv("!!document.querySelector('#layer .cine')&&document.querySelector('#layer .cine').textContent.includes('移動庇護所')"))
    snap('cine')
    ok('I6 introduction finished, then the habitat introduction', adv("state.act3.introduced&&!!document.querySelector('#layer .dlg')&&document.querySelector('#layer .dlg').textContent.includes('棲息車廂')"))
    adv("!document.querySelector('#layer .dlg,#layer .cine')",40000)
    ok('I7 observations kept in the journal', sum(1 for e in ev("state.log") if '觀察紀錄' in e['t'])==4)
    ok('I8 opening log rewritten (no "train woke up")', '世界縫隙' in ev("state.log[0].t") and '甦醒' not in ev("state.log[0].t"))
    ok('I9 guardian clue count unchanged from the old opening (clue_wake only)', ev("state.clues")==['clue_wake'], ev("state.clues"))
    ok('D1 control disc stays asleep (cannot depart yet)', '沉睡' in (ev("crBlockDepart()") or ''))
    ok('D2 cannot get off here', ev("LOCATIONS.origin.name")=='世界縫隙')
    # ---- 存檔恢復：進了列車、刻文還沒讀完
    ev("state.act3.introduced=false;save()"); st=ev("JSON.stringify(state)"); ev(f"closeAll();loadGame(JSON.parse({json.dumps(st)}),'t')"); W(1500)
    ok('R2 resume mid-introduction replays the inscription once', adv("state.act3.introduced",60000) and not ev("ACT1.active()"))
    adv("!document.querySelector('#layer .dlg,#layer .cine')",40000)
    # ---- 舊開場：?legacy 流程不受影響
    ev("closeAll();state=freshState();save()")
    ok('L1 legacy/new-game without act3: origin is still the sleeping land', ev("LOCATIONS.origin.name")=='沉睡之地' and ev("crBlockDepart()")!='水晶沒有回應。……它還在沉睡。')
    ok('L2 memory entry unchanged for legacy', ev("MEMORIES.find(m=>m.id==='wake').title")=='甦醒')
    ok('Z no page errors', not errs, errs)
    print('ALL PASS' if all(R) else 'SOME FAIL', len(R))
