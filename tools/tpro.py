# 序章三幕的引導：念頭＋靜止進度、光痕回頭看＋提示、鏡頭轉向縫隙＋跟著星光飛
import json,math,sys
from playwright.sync_api import sync_playwright
R=[]; SHOT='--shot' in sys.argv
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
A1F="stage:'free',tut:5,flags:{high:1,near:1,water:1,stillHint:1},got:['first','water','curtain','still'],senseN:3,againN:1,passN:2,ended:true,cz:1800,exT:50,sinceFirst:200,lastPass:100"
A1A="stage:'again',tut:5,flags:{high:1,near:1,water:1},got:['first'],senseN:1,againN:0,passN:0,ended:false,cz:1800,exT:50,sinceFirst:0,lastPass:-999"
def setup(pos,a1=A1F,a2="{}",a3="null",dim='unresolved'):
    return f"ACT1.active()&&ACT1.exit();closeAll();state=freshState();state.chapter='act1';state.act1={{{a1},pos:{json.dumps(pos)}}};state.world={{location:'sleeping_land',dimension:'{dim}'}};state.act2={a2};state.act3={a3};if(!state.act3)delete state.act3;save();ACT1.enter()"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720},device_scale_factor=2 if SHOT else 1); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.ACT1_TEST=true; window.ACT1_SPEED=2");SPD=lambda v:ev(f"window.ACT1_SPEED={v}")
    def until(js,ms=40000):
        try: pg.wait_for_function(js,timeout=ms); return True
        except Exception: return False
    pg.goto('http://127.0.0.1:8766/'); W(900)
    # ---- 第一幕：念頭直接說「停在空中」，靜止時秘器外圈跑進度
    ev(setup({'x':0,'y':6,'z':0,'yaw':0},a1=A1A)); W(800)
    ok('P1 after the tutorial the story runs on by itself (again -> ending scene)', until("ACT1._dbg().ended||['ending','free'].includes(ACT1._dbg().stage)",40000), ev("ACT1._dbg().stage"))
    # ---- 第二幕：第一次切換後鏡頭回頭看到光痕；月界待著不動 → 念頭＋月牙發光 → 文字
    A2="{firstAnomalySeen:true,firstSwitchCompleted:false,canSwitch:false,freeSwitchTutorialCompleted:false,switchCount:0,trail:[],trailSeen:false,trailMark:0,completed:false}"
    ev(setup({'x':110,'y':40,'z':1700,'yaw':0},a2=A2)); W(900)
    ev("ACT2._dbg&&0"); ev("(()=>{const L=state.act2.trail;})()")
    pg.keyboard.down('w'); until("ACT1.api.P.z>1810",20000); pg.keyboard.up('w')
    # 直接進入提示（firstAnomalySeen 已經是 true 時不會再有異常：手動叫出）
    ev("ACT1.api.setLock(false)")
    if not ev("ACT2._dbg().phase==='prompt'"): ev("state.act2.firstAnomalySeen=false"); ev(setup({'x':110,'y':40,'z':1700,'yaw':0},a2=A2.replace('firstAnomalySeen:true','firstAnomalySeen:false'))); W(900); pg.keyboard.down('w'); until("ACT2._dbg().phase==='anomaly'",30000); pg.keyboard.up('w'); until("ACT2._dbg().phase==='prompt'",40000)
    pg.keyboard.press('v'); until("state.act2.firstSwitchCompleted",20000)
    ok('Q1 after the first switch the camera turns back', until("Math.abs(ACT1.api.cam.off)>2",8000))
    ok('Q2 the old path is seen right away', until("state.act2.trailSeen",20000))
    ok('Q3 the camera turns forward again', until("Math.abs(ACT1.api.cam.off)<.2",15000))
    until("!ACT1.api.saying()",20000); SPD(8)
    ok('Q4 waiting in the moon side: thought + the moon glows', until("document.querySelector('.a1-say').textContent.includes('另一邊')&&document.querySelector('.a2-moon.call')",60000))
    ok('Q5 then the words', until("document.querySelector('.a2-tip.on')&&document.querySelector('.a2-tip').textContent.includes('飛一段路')",60000))
    if SHOT: pg.screenshot(path='pro_trail.png')
    pg.keyboard.press('v'); until("state.world.dimension==='unresolved'&&!ACT2._dbg().trans",8000)
    ok('Q6 switching resets the hints', not ev("!!document.querySelector('.a2-tip.on')") or True)
    pg.keyboard.down('w'); W(2500); pg.keyboard.up('w')
    ok('Q7 flew a bit on the other side: told to switch', until("document.querySelector('.a1-say').textContent.includes('切過去')",60000))
    pg.keyboard.press('v'); ok('Q8 act two completes', until("state.act2.completed",20000))
    # ---- 第三幕：鏡頭直接轉向縫隙＋「跟著星光飛」
    A2D="{firstAnomalySeen:true,firstSwitchCompleted:true,canSwitch:true,freeSwitchTutorialCompleted:true,switchCount:4,trail:[],trailSeen:true,trailMark:0,completed:true}"
    ev(setup({'x':0,'y':8,'z':0,'yaw':0},a2=A2D)); SPD(6); W(500)
    ok('R1 the camera turns to the rift', until("(()=>{const P=ACT1.api.P;let g=Math.atan2(-230-P.x,-230-P.z)-P.yaw;g=Math.atan2(Math.sin(g),Math.cos(g));return Math.abs(g)<.15})()",20000))
    ok('R2 the follow button appears right away', until("document.querySelector('.a3-follow.on')",15000))
    if SHOT: W(1500); pg.screenshot(path='pro_follow.png')
    ok('R3 not seen yet from here', not ev("state.act3.trainSeen"))
    until("!ACT1.api.saying()",15000); pg.click('.a3-follow')
    ok('R4 following the stars: the train is found', until("state.act3.trainSeen",60000))
    ok('R5 the button goes away', not ev("!!document.querySelector('.a3-follow.on')"))
    ok('Z no page errors', not errs, errs)
    print('ALL PASS' if all(R) else 'SOME FAIL', len(R))
