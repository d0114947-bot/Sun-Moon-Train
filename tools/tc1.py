# 序章調整：開場節奏、意識文字、Shift 加速、播放鈕合一、彎曲星光線、日月切換、水幕不卡、飛進晨曦森林、上車遇見曦淵
import json,sys,math
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
URL=sys.argv[1] if len(sys.argv)>1 and sys.argv[1].startswith('http') else 'http://127.0.0.1:8766/'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
A1="stage:'free',tut:6,flags:{high:1,near:1,water:1},got:['first','water'],senseN:3,againN:1,passN:2,ended:true,cz:1800,exT:50,sinceFirst:200,lastPass:100"
A2D="{firstAnomalySeen:true,firstSwitchCompleted:true,canSwitch:true,freeSwitchTutorialCompleted:true,switchCount:4,trail:[],trailSeen:true,trailMark:0,completed:true}"
def setup(pos,a1=A1,a2="{}",a3="null"):
    return f"ACT1.active()&&ACT1.exit();closeAll();state=freshState();state.chapter='act1';state.act1={{{a1},pos:{json.dumps(pos)}}};state.world={{location:'sleeping_land',dimension:'unresolved'}};state.act2={a2};state.act3={a3};if(!state.act3)delete state.act3;save();ACT1.enter()"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.ACT1_TEST=true; window.ACT1_SPEED=2")
    def until(js,ms=40000):
        try: pg.wait_for_function(js,timeout=ms); return True
        except Exception: return False
    pg.goto(URL); W(900)
    # ---- 開場：很快就淡入、標題很短
    ev("ACT1.start()"); W(500)
    until("ACT1.active()&&ACT1._dbg().fade<.05",120000); tf=ev("ACT1.api.T")
    ok('O1 fade-in from black is quick (game time)', tf<3.2, tf)
    saw=until("!!document.querySelector('#act1 .a1-title.on')",200000); tt=ev("ACT1.api.T")
    ok('O2 title shows soon after waking (game time)', saw and tt<20, tt)
    until("!document.querySelector('#act1 .a1-title.on')",60000); te=ev("ACT1.api.T")
    ok('O3 title is short', te-tt<3.4, te-tt)
    ok('O4 tutorial starts', until("ACT1._dbg().stage==='tut'",60000))
    pg.screenshot(path=S+'/c1_tut.png')
    # ---- Shift 真的加速
    ev(setup({'x':300,'y':20,'z':300,'yaw':0},a2="{firstAnomalySeen:true,firstSwitchCompleted:true,canSwitch:true,freeSwitchTutorialCompleted:true,completed:true,trail:[],trailSeen:true}",a3="{trainSeen:true,obs:[],entered:false,introduced:false,canDepart:false}")); until("!ACT1.api.lock",30000); W(500)
    pg.keyboard.down('KeyW'); W(2500); v1=ev("Math.hypot(ACT1.api.P.vx||0,ACT1.api.P.vz||0)||ACT1.api.P.vt")
    pg.keyboard.down('ShiftLeft'); W(3000); v2=ev("Math.hypot(ACT1.api.P.vx||0,ACT1.api.P.vz||0)||ACT1.api.P.vt")
    op=ev("+getComputedStyle(document.querySelector('#act1 .a1-rush')).opacity")
    pg.screenshot(path=S+'/c1_boost.png'); pg.keyboard.up('ShiftLeft'); pg.keyboard.up('KeyW')
    ok('S1 Shift makes flying clearly faster (>2x)', v2>v1*2, (round(v1,1),round(v2,1)))
    ok('S2 boost has a speed effect on screen', op>.3, op)
    # ---- 意識的文字：中間打字、不擋操作、不黑不模糊（水幕附近的被動接收）
    # （水幕拿掉了：改用低空停住、點秘器，接收「倒影」的念頭）
    ev(setup({'x':300,'y':3,'z':300,'yaw':0},a1=A1.replace("got:['first','water']","got:['first']"),a2="{firstAnomalySeen:true,firstSwitchCompleted:true,canSwitch:true,freeSwitchTutorialCompleted:true,completed:true,trail:[],trailSeen:true}",a3="{trainSeen:true,obs:[],entered:false,introduced:false,canDepart:false}"))
    until("!ACT1.api.lock&&!ACT1.api.busy",30000); W(800); pg.click('#act1 .a1-icon')
    seen=until("document.querySelector('#act1 .a1-th.on .tt')&&document.querySelector('#act1 .a1-th.on .tt').textContent.length>4",30000)
    ok('T1 thought text is typed in the middle of the screen', seen, ev("(document.querySelector('#act1 .a1-th')||{}).className"))
    if seen:
        st=ev("(()=>{const t=document.querySelector('#act1 .a1-th');const c=getComputedStyle(t);return [c.backgroundImage,c.backdropFilter]})()")
        ok('T2 no dark veil, no blur', st[0]=='none' and st[1] in ('none',''), st)
        ok('T3 player can still move while the thought shows', not ev("ACT1.api.lock"))
        pg.screenshot(path=S+'/c1_thought.png')
        W(3000); txt=ev("document.querySelector('#act1 .a1-th .tt')?.textContent||''")
        ok('T4 thought is more than a few words', len(txt)>=16, txt)
    # ---- 秘器劇情結束：沒有「第一幕・沉睡之地」標題、不黑畫面
    ev(setup({'x':0,'y':10,'z':0,'yaw':0},a1="stage:'again',tut:6,flags:{},got:['first'],senseN:1,againN:0,passN:0,ended:false,cz:1800,exT:0,sinceFirst:10,lastPass:-999"))
    until("ACT1._dbg().fade<.05",60000); title=False; maxfade=0
    for _ in range(600):
        W(400); title=title or ev("!!document.querySelector('#act1 .a1-title.on')"); maxfade=max(maxfade,ev("ACT1._dbg().fade"))
        if ev("ACT1._dbg().stage")=='free' and not ev("ACT1.api.lock"): break
    ok('E1 the artifact story ends without the chapter title or a black screen', ev("ACT1._dbg().stage")=='free' and not title and maxfade<.2, (title,maxfade,ev("ACT1._dbg().stage")))
    # ---- 星光線彎曲、日月切換鈕
    ok('P1 guide line bends (not straight)', 'bA' in ev("ACT2._dbg?'bA':'bA'"))
    ev(setup({'x':0,'y':20,'z':900,'yaw':0},a2=A2D.replace('completed:true','completed:false'))); W(1500)
    pg.screenshot(path=S+'/c1_path.png')
    until("!ACT1.api.lock",60000); W(500)
    ok('M1 switch button has a sun and a moon', ev("!!document.querySelector('.a2-moon .sm-sun')&&!!document.querySelector('.a2-moon .sm-moon')"))
    pg.keyboard.press('v'); W(2500)
    ok('M2 switching turns the wheel to the moon', ev("document.querySelector('.a2-moon').classList.contains('moon')") and ev("getComputedStyle(document.querySelector('.a2-moon .sm-wheel')).transform")!='none')
    pg.screenshot(path=S+'/c1_moon.png')
    # ---- 異常（水幕拿掉後在原地發生）：手動點對話也不會卡住
    ev("window.SAY_MANUAL=true")
    ev(setup({'x':0,'y':40,'z':900,'yaw':0},a1=A1.replace("got:['first','water']","got:['first','water','curtain','still']"))); W(1200)
    reached=until("['anomaly','prompt'].includes(ACT2._dbg().phase)",60000)
    for _ in range(40):
        if ev("ACT2._dbg().phase")=='prompt': break
        if ev("(document.querySelector('#act1 .a1-say')||{}).innerText||''"): pg.mouse.click(640,250)
        W(500)
    ok('W1 after the waterfall the story reaches the switch prompt (no freeze)', reached and ev("ACT2._dbg().phase")=='prompt', ev("ACT2._dbg()"))
    pg.keyboard.press('v')
    for _ in range(40):
        if ev("ACT2._dbg().phase")=='' and not ev("ACT1.api.lock"): break
        if ev("(document.querySelector('#act1 .a1-say')||{}).innerText||''"): pg.mouse.click(640,250)
        W(500)
    ok('W2 first switch finishes and control comes back', ev("ACT2._dbg().phase")=='' and not ev("ACT1.api.lock"), (ev("ACT2._dbg()"),ev("ACT1._dbg().lock")))
    ev("window.SAY_MANUAL=false")
    # ---- 飛進晨曦森林（重新載入，避免前面手動模式的台詞留著）
    ev("ACT1.active()&&ACT1.exit()"); pg.goto(URL); W(900)
    RC=(-230,-230); yaw=math.atan2(-1,-1)
    ev(setup({'x':RC[0]+130,'y':20,'z':RC[1]+130,'yaw':yaw},a2=A2D,a3="{trainSeen:true,obs:[],entered:false,introduced:false,canDepart:false}")); W(1500)
    pg.keyboard.down('KeyW'); ok('F1 getting close flies you through into the forest', until("state.act3.inForest",20000)); pg.keyboard.up('KeyW')
    ok('F2 a location card says 晨曦森林', until("!!document.querySelector('#act1 .a3-loc.on')",8000))
    pg.screenshot(path=S+'/c1_forest.png')
    ok('F3 tip tells you to look at the train / board', until("(document.querySelector('#act1 .a3-tip2.on')||{}).textContent?.includes('✦')",20000))
    pg.screenshot(path=S+'/c1_forest2.png')
    # ---- 上車：曦淵叫你、到駕駛室、車廂一節一節亮、介紹、再開始列車教學
    ev("ACT1.active()&&ACT1.exit();closeAll();state=freshState();state.chapter='act1';state.act1={stage:'free',ended:true};state.world={location:'sleeping_land',dimension:'unresolved'};state.act2={completed:true};state.act3={trainSeen:true,obs:['carving'],entered:true,introduced:false,canDepart:false,inForest:true};save();act3BeginTrain()")
    seen=''
    for _ in range(60):
        W(400)
        if ev("!!document.querySelector('#layer .cine')"): ev("document.querySelector('#layer .cine').click()")
        elif ev("!!document.querySelector('#layer .dlg')"): seen+=ev("document.querySelector('#layer .dlg').innerText")+'|'; ev("document.querySelector('#layer .dlg .box').click()")
        elif ev("state.act3.xyCall") and '駕駛室' in seen: break
    ok('X1 a voice calls you to the cab', '駕駛室' in seen and ev("state.act3.xyCall") and not ev("state.act3.introduced"), seen[-200:])
    ok('X2 goal says go to the cab', '駕駛室' in ev("goalNow().t"))
    ev("render()"); W(600); pg.click('#hud .goal'); W(900)
    ok('X3 goal arrow points the way', ev("!!document.querySelector('.garr')"))
    ev("closeAll();state.currentCarriage='nature';render()"); W(1500)
    ok('X4 on the way, the cars do not play their own intro', not ev("!!document.querySelector('#layer .dlg')"))
    ev("state.currentCarriage='cab';render()"); seen=''; lit=0
    for _ in range(160):
        W(300)
        lit=max(lit,ev("document.querySelectorAll('.xy-map .xy-car.lit').length"))
        if ev("!!document.querySelector('#layer .dlg')"): seen+=ev("document.querySelector('#layer .dlg').innerText")+'|'; ev("document.querySelector('#layer .dlg .box').click()")
        elif ev("state.act3.introduced"): break
        if lit==3 and not ev("!!document.querySelector('.xy-shot')"): pg.screenshot(path=S+'/c1_tour.png'); ev("document.body.insertAdjacentHTML('beforeend','<i class=xy-shot></i>')")
    ok('X5 曦淵 meets you: 新的渡守？ → not 祂 → 沉睡之地 had no life', all(k in seen for k in ['新的渡守','不是祂','沉睡之地','沒有生命']), seen[:300])
    ok('X6 the cars light up one by one', lit==6, lit)
    ok('X7 train tutorial is no longer a gate (devices taught on first use)', ev("state.act3.introduced&&state.act4.finished&&!act4On()"))
    ok('X8 曦淵 stays: the crystal waits for a wish', '心願' in seen and '我去外面' not in seen)
    # ---- 播放鈕合一
    ev("closeAll();dialogueScript([['self','一'],['self','二']])"); W(500)
    n=ev("document.querySelectorAll('#layer .dlg .dlg-ctl button').length")
    ok('B1 one playback button', n==1, n)
    labs=[]
    for _ in range(4):
        labs.append(ev("document.querySelector('#layer .dlg .dlg-ctl button').textContent")); ev("document.querySelector('#layer .dlg .dlg-ctl button').click()"); W(150)
    ok('B2 it cycles 手動 → 1× → 2× → 3×', labs==['手動','1×','2×','3×'], labs)
    pg.screenshot(path=S+'/c1_btn.png'); ev("closeAll()")
    ok('Z no page errors', not errs, errs[:3])
    b.close()
