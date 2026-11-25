# 依兩萬人模擬的建議：光痕演一次、值勤逐步加入＋交給曦淵、對話精簡、停靠只亮一個、自動往前飛、左鍵拖曳轉向、自動播放提示
import json,sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
URL='http://127.0.0.1:8766/'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
A1="stage:'free',tut:6,flags:{high:1,near:1,water:1},got:['first','water'],senseN:3,againN:1,passN:2,ended:true,cz:1800,exT:50,sinceFirst:200,lastPass:100"
def setup(pos,a2="{}"):
    return f"ACT1.active()&&ACT1.exit();closeAll();state=freshState();state.chapter='act1';state.act1={{{A1},pos:{json.dumps(pos)}}};state.world={{location:'sleeping_land',dimension:'unresolved'}};state.act2={a2};save();ACT1.enter()"
BASE="document.querySelector('#mainscreen')?.remove();ACT1.active()&&ACT1.exit();RUNNING=true;state=freshState();normalizeState();state.introDone=true;state.prologueDone=true;state.storyFlags.noFeel=1;state.storyFlags.goalArrowTip=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.visitedLocations=['dawnForest'];"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.ACT1_TEST=true; window.ACT1_SPEED=3; window.XY_FAST=true")
    def until(js,ms=40000):
        try: pg.wait_for_function(js,timeout=ms); return True
        except Exception: return False
    pg.goto(URL); W(900)
    # ---- 1. 光痕：第一次切換後，看見一次就完成
    ev(setup({'x':0,'y':10,'z':300,'yaw':0})); W(800)
    ok('T1 the anomaly comes', until("ACT2._dbg().phase==='prompt'",80000), ev("ACT2._dbg()"))
    pg.keyboard.press('v')
    ok('T2 light-trail event finishes by itself after the first switch (no back-and-forth)', until("state.act2.completed",80000), ev("state.act2"))
    ok('T3 still in the moon side (did not have to switch back)', ev("state.world.dimension")=='moon')
    # ---- 5. 自動往前飛、左鍵拖曳轉向
    ev(setup({'x':300,'y':20,'z':300,'yaw':0},a2="{firstAnomalySeen:true,firstSwitchCompleted:true,canSwitch:true,completed:true,trail:[],trailSeen:true}")); until("!ACT1.api.lock",30000); W(500)
    ok('F1 auto-fly button in the corner', ev("!!document.querySelector('#act1 .a1-auto')"))
    z0=ev("ACT1.api.P.z"); pg.keyboard.press('KeyF'); W(3000); z1=ev("ACT1.api.P.z")
    ok('F2 F key: flies forward by itself', z1-z0>5 and ev("PREFS.autoFly"), (z0,z1))
    pg.keyboard.press('KeyF'); W(1500)
    y0=ev("ACT1.api.P.yaw"); pg.mouse.move(600,360); pg.mouse.down(); pg.mouse.move(800,360,steps=8); pg.mouse.up(); W(300)
    ok('F3 left-drag (trackpad) also turns', abs(ev("ACT1.api.P.yaw")-y0)>.3, (y0,ev("ACT1.api.P.yaw")))
    ev("ACT1.exit()")
    # ---- 3. 值勤逐步加入
    ev(BASE+"state.journeyCount=0;state.duty=dutyFresh();state.currentCarriage='cab';render()"); W(1500)
    ok('D1 first departure: equipment and 符牒 are taken care of; doors still open (can go out)', ev("equipAll()&&state.duty.briefing&&!state.duty.doors"))
    left=ev("DUTY_STEPS.filter(x=>!x[2]()).map(x=>x[1])")
    ok('D2 first departure only needs: 界染、廣播、報備、晶盤', len(left)<=5 and any('界染' in x for x in left) and not any('裝備' in x or '符牒' in x for x in left), left)
    ev("state.duty.mic=true"); W(1800)
    ok('D2b after the broadcast the doors are locked for you', ev("state.duty.doors"))
    ev(BASE+"state.journeyCount=1;state.duty=dutyFresh();state.spirit.equipment={tablet:false,compass:false,talisman:false};state.currentCarriage='cab';render()"); W(2500)
    ok('D3 later: equipment becomes a duty, with a note', not ev("equipAll()") and ev("state.storyFlags['dutyNew_cab-equip']")==1)
    ev(BASE+"state.journeyCount=5;state.storyFlags.dutyLearned=1;state.currentLocation='starIslands';state.duty=dutyFresh();state.currentCarriage='cab';render()"); W(1500)
    if ev("wallLv(nextStop())")=='亂流': ev("state.journeyCount=6;render()")
    away=ev("dragonAway()")
    ev("discPanel()"); W(800)
    if not away:
        ok('D4 after a few trips: 「交給曦淵」 also on the control disc', ev("!!document.querySelector('#dt-hand')"), ev("dutyAutoOk()"))
        ev("document.querySelector('#dt-hand').click()"); W(1200)
        ok('D5 one click finishes the other checks', ev("state.duty.signal&&state.duty.doors&&state.duty.briefing&&state.duty.reported&&equipAll()") and ev("!!document.querySelector('#layer .dlg')"))
    else: ok('D4 (dragon away this stop: no hand-over button)', not ev("!!document.querySelector('#dt-hand')"))
    ev("closeAll()")
    # ---- 4. 停靠：有目標時只亮一個
    n=ev("(()=>{ state.currentCarriage='nature';render(); return glowAllowed().length; })()")
    ok('G1 docked with a goal: at most one glowing hotspot', n<=1, n)
    # ---- 2. 曦淵導覽：點的次數變少、車廂自動亮
    ev("ACT1.active()&&ACT1.exit();closeAll();state=freshState();state.chapter='act1';state.act1={stage:'free',ended:true};state.world={location:'sleeping_land',dimension:'unresolved'};state.act2={completed:true};state.act3={trainSeen:true,obs:['carving'],entered:true,introduced:false,canDepart:false,inForest:true,xyCall:1};state.currentCarriage='cab';state.currentPhase='docked';state.currentLocation='dawnForest';state.introDone=true;save();RUNNING=true;render()")
    clicks=0; lit=0
    for _ in range(200):
        W(250); lit=max(lit,ev("document.querySelectorAll('.xy-map .xy-car.lit').length"))
        if ev("!!document.querySelector('#layer .dlg')"):
            ev("document.querySelector('#layer .dlg .box').click()"); W(80); ev("document.querySelector('#layer .dlg .box')?.click()"); clicks+=1
        elif ev("state.act3.introduced"): break
    ok('X1 曦淵 tour: all six cars light up on their own', lit==6, lit)
    ok('X2 far fewer lines to click (≤ 9)', clicks<=9 and ev("state.act3.introduced"), clicks)
    # ---- 2. 自動播放提示
    ev("PREFS.autoTip=0;PREFS.dlgAuto=0;dlgCtlAdd.n=0;closeAll()")
    for i in range(3):
        ev(f"dialogueScript([['self','第{i}句']])"); W(400)
        if i<2: ev("closeAll()"); W(200)
    ok('A1 third dialogue box: tip says it can be switched to auto play', ev("!!document.querySelector('.dlg-tipb')"))
    pg.screenshot(path=S+'/d1_tip.png'); ev("closeAll()")
    ok('Z no page errors', not errs, errs[:3])
    b.close()
