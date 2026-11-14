# 第二幕：銀河星點、穿越瀑布、第一次異常、第一次切換、自由切換、月界的沉睡之地、黑影、光痕事件、存檔恢復
import json,sys,base64
from playwright.sync_api import sync_playwright
R=[]; SNAP='--snap' in sys.argv
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
A1="stage:'free',tut:5,flags:{high:1,near:1,water:1},got:['first','water','curtain','still'],senseN:3,againN:1,passN:2,ended:true,cz:1800,exT:50,sinceFirst:200,lastPass:100"
def setup(pos,w="{location:'sleeping_land',dimension:'unresolved'}",a2="{}",a1=A1):
    return f"ACT1.active()&&ACT1.exit();state=freshState();state.chapter='act1';state.act1={{{a1},pos:{json.dumps(pos)}}};state.world={w};state.act2={a2};save();ACT1.enter()"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.ACT1_TEST=true; window.ACT1_SPEED=4")
    def until(js,ms=40000):
        try: pg.wait_for_function(js,timeout=ms); return True
        except Exception: return False
    D=lambda: ev("ACT2._dbg()"); P=lambda: ev("ACT1.api.P")
    def snap(n):
        if SNAP: pg.screenshot(path=f'a2s_{n}.png')
    pg.goto('http://127.0.0.1:8766/'); W(900)
    # ---- 第一幕未結束：沒有光點、穿越也不觸發
    ev(setup({'x':0,'y':10,'z':1780,'yaw':0},a1=A1.replace("stage:'free'","stage:'again'").replace("ended:true","ended:false"))); W(1500)
    ok('P1 act1 not ended: no galaxy path', D()['pts']==0)
    pg.keyboard.down('w'); until("ACT1.api.P.z>1830",20000); pg.keyboard.up('w'); W(1200)
    ok('P2 act1 not ended: crossing the curtain does nothing', D()['phase']=='' and not ev("state.act2.firstAnomalySeen"))
    ok('P3 curtain is reachable and passable (not receding)', P()['z']>ev("ACT1.api.cz"), (P()['z'],ev("ACT1.api.cz")))
    # ---- 第一幕結束後：光點出現、引向瀑布中段
    ev(setup({'x':300,'y':6,'z':300,'yaw':0})); W(2500)
    ok('G1 galaxy path appears after act1 ended', D()['pts']>=12)
    ok('G2 no arrows / text / quest UI', not ev("!!document.querySelector('#act1 .a1-tip.on,#act1 .a2-tip.on')"))
    ok('G3 switch button hidden before first anomaly', not ev("document.querySelector('.a2-moon').classList.contains('show')"))
    pressV=lambda: pg.keyboard.press('v')
    pressV(); W(400); ok('G4 V does nothing before the first switch', ev("state.world.dimension")=='unresolved' and D()['phase']=='')
    # ---- 在其他區段穿越：只有很淡的光影，沒有異常
    ev(setup({'x':400,'y':8,'z':1785,'yaw':0})); W(1200); pg.keyboard.down('w'); until("ACT1.api.P.z>1830",20000); pg.keyboard.up('w'); W(1500)
    ok('X1 crossing outside the guided segment: no anomaly', D()['phase']=='' and not ev("state.act2.firstAnomalySeen") and not D()['pend'])
    ok('X2 behind the curtain it is the same sea (scene still drawn, not locked)', not ev("ACT1.api.lock"))
    # ---- 在指定區段穿越（高速、稍微偏離）→ 異常
    ev(setup({'x':110,'y':40,'z':1700,'yaw':0})); W(1500); snap('approach')
    pg.keyboard.down('w'); ok('A1 crossing guided segment at speed triggers anomaly (tolerant +-120)', until("ACT2._dbg().phase==='anomaly'",30000), D()); pg.keyboard.up('w')
    ok('A2 controls locked during anomaly', ev("ACT1.api.lock"))
    until("ACT2._dbg().phase==='anomaly'&&false",2500); snap('glimpse')
    ok('A3 spirit lines', until("document.querySelector('.a1-say').textContent.includes('水的後面')",30000))
    ok('A4 then prompt: moon button appears with V hint', until("ACT2._dbg().phase==='prompt'",40000) and ev("document.querySelector('.a2-moon').classList.contains('show')") and 'V' in ev("document.querySelector('.a2-tip').textContent"))
    snap('prompt')
    ok('A5 anomaly saved once; artifact untouched', ev("state.act2.firstAnomalySeen") and ev("state.act1.got.length")==4)
    ok('A6 still unresolved (not switched automatically)', ev("state.world.dimension")=='unresolved'); W(1500)
    ok('A7 still waiting for the player', D()['phase']=='prompt')
    # ---- 第一次切換：玩家親自按 V
    pressV(); ok('F1 first switch by V: fade into moon side', until("state.act2.firstSwitchCompleted&&state.world.dimension==='moon'",20000))
    ok('F2 free switching opened right away', ev("state.act2.canSwitch") and not ev("ACT1.api.lock"))
    ok('F3 line after arrival', until("document.querySelector('.a1-say').textContent.includes('這裡是')",15000))
    ok('F4 button shows moon state', ev("document.querySelector('.a2-moon').classList.contains('moon')"))
    snap('moon')
    # ---- 自由切換：沒有冷卻、沒有次數限制；切回一定是 unresolved
    until("!ACT1.api.saying()",20000); W(300)
    n0=ev("state.act2.switchCount"); pressV(); ok('S1 switch back returns to unresolved (never sun)', until("state.world.dimension==='unresolved'&&!ACT2._dbg().trans",8000) and ev("state.world.dimension")!='sun')
    ok('S2 free-switch tutorial completes on the first own switch', ev("state.act2.freeSwitchTutorialCompleted"))
    ok('S3 button shows original state', not ev("document.querySelector('.a2-moon').classList.contains('moon')"))
    pressV(); pressV(); W(100)
    ok('S4 rapid press during transition is queued once (no overlap)', D()['trans'] and D()['queued'])
    ok('S5 queued switch runs after: ends back in unresolved', until("!ACT2._dbg().trans&&!ACT2._dbg().queued&&state.world.dimension==='unresolved'",10000), D())
    for k in range(6): pressV(); until("!ACT2._dbg().trans",6000)
    ok('S6 no cooldown, no limit; count recorded', ev("state.act2.switchCount")>=n0+8 and ev("state.world.dimension")=='unresolved', ev("state.act2.switchCount"))
    pg.click('.a2-moon'); ok('S7 mouse click on the icon uses the same switch', until("state.world.dimension==='moon'&&!ACT2._dbg().trans",8000))
    pressV(); until("!ACT2._dbg().trans",8000)
    ok('S8 artifact unchanged by switching', ev("state.act1.got.length")==4 and ev("state.act1.senseN")==3)
    # ---- 回到原本狀態：月界效果完全不殘留（逐像素）
    until("!ACT1.api.saying()",20000); W(2500)   # 穿越水幕的光影也已結束
    print('S9PRE',ev("JSON.stringify(ACT2._dbg())"))
    ev("window.ACT1_FREEZE=Math.round(ACT1.api.T+60)"); W(2500); h1=ev("document.querySelector('.a1-cv').toDataURL()")
    snapP=ev("JSON.stringify({P:ACT1.api.P,cam:ACT1.api.cam,spr:ACT1.api.spr})")
    fz=ev("window.ACT1_FREEZE"); ev("ACT1.exit()"); ev(setup({'x':0,'y':5,'z':0,'yaw':0},a2="{firstAnomalySeen:true,firstSwitchCompleted:true,canSwitch:true,freeSwitchTutorialCompleted:true,switchCount:9}")); W(800)
    ev(f"(()=>{{ const o={snapP}; ACT1._set({{P:o.P}}); Object.assign(ACT1.api.cam,o.cam); Object.assign(ACT1.api.spr,o.spr); }})()"); W(2500)
    h2=ev("document.querySelector('.a1-cv').toDataURL()"); ev("window.ACT1_FREEZE=null")
    open('s9a.png','wb').write(base64.b64decode(h1.split(',')[1])); open('s9b.png','wb').write(base64.b64decode(h2.split(',')[1])); print('S9STATE',snapP)
    ok('S9 after switching back nothing of the moon side remains (pixel-identical)', h1==h2)
    # ---- 劇情演出時 V 不反應
    until("!ACT1.api.lock",20000); W(500); ev("ACT1.api.setLock(true)"); pressV(); W(500); ok('L1 V ignored during cutscenes', ev("state.world.dimension")=='unresolved' and not D()['trans']); ev("ACT1.api.setLock(false)")
    # ---- 月界的沉睡之地：黑影
    pressV(); until("state.world.dimension==='moon'&&!ACT2._dbg().trans",8000)
    shp=ev("ACT2._shadowNow()"); pp=P()
    ok('H1 shadow spawns far away', shp and ((shp['x']-pp['x'])**2+(shp['z']-pp['z'])**2)**.5>=150)
    ok('H2 never in the screen centre', ev("(()=>{ const s=ACT2._shadowNow(); const pr=ACT1.api.proj(s.x,8,s.z); return !pr||Math.abs(pr.x-ACT1.api.W/2)>=ACT1.api.W*.18; })()"))
    # 頻率：以遊戲時間計算約 13～17 秒一次
    ev("window.__sht=[]; window.__shw=false; ACT1.hook('logic',()=>{ const s=ACT2._dbg().sh; if(s&&!__shw) __sht.push(ACT1.api.T); __shw=s; })")
    until("__sht.length>=4",160000); gaps=ev("__sht.slice(1).map((t,i)=>t-__sht[i])")
    ok('H3 roughly one shadow every ~15 s (game time)', len(gaps)>=2 and all(12.5<=g<=18 for g in gaps[1:]), gaps)
    # ---- 光痕事件
    ev("ACT1.exit()")
    tr=json.dumps([[0,8,1600+i*6] for i in range(30)])
    ev(setup({'x':0,'y':8,'z':1790,'yaw':0},w="{location:'sleeping_land',dimension:'moon'}",a2="{firstAnomalySeen:true,firstSwitchCompleted:true,canSwitch:true,freeSwitchTutorialCompleted:true,switchCount:3,trail:"+tr+"}")); W(1500)
    ev("ACT1.api.P.yaw=3.14")
    ok('T1 in moon side the flown path shows as light trail -> line', until("document.querySelector('.a1-say').textContent.includes('我剛才飛過的地方')",30000)); snap('trail')
    ok('T2 trail seen stored', ev("state.act2.trailSeen"))
    until("!ACT1.api.saying()",20000); pressV(); until("state.world.dimension==='unresolved'&&!ACT2._dbg().trans",8000)
    pg.keyboard.down('w'); W(5000); pg.keyboard.up('w'); W(800)
    ok('T3 flying in the original state records new trail', ev("state.act2.trail.length")>ev("state.act2.trailMark")+5)
    pressV(); ok('T4 back in moon side the new segment lit -> act 2 completes', until("state.act2.completed",30000) and until("document.querySelector('.a1-say').textContent.includes('這裡都看得見')",15000))
    ok('T5 no title card, free exploration continues', not ev("!!document.querySelector('.a1-title.on')") and not ev("ACT1.api.lock"))
    # ---- 存檔恢復
    ev(setup({'x':0,'y':8,'z':1810,'yaw':0},a2="{firstAnomalySeen:true}")); 
    ok('R1 left during the prompt -> prompt again, still waiting for the player', until("ACT2._dbg().phase==='prompt'",15000) and ev("state.world.dimension")=='unresolved')
    ev(setup({'x':0,'y':8,'z':1810,'yaw':0},w="{location:'sleeping_land',dimension:'moon'}",a2="{firstAnomalySeen:true,firstSwitchCompleted:true,canSwitch:true,switchCount:1}")); W(1200)
    ok('R2 saved in moon side -> resumes in moon side, button shows it', D()['dim']=='moon' and D()['mb']==1 and ev("document.querySelector('.a2-moon').classList.contains('moon')"))
    ok('R3 anomaly never replays once seen', D()['phase']!='anomaly' and D()['pts']==0)
    # ---- 手機
    m=b.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True); m.add_init_script("window.ACT1_TEST=true"); m.goto('http://127.0.0.1:8766/'); m.wait_for_timeout(900)
    m.evaluate(setup({'x':0,'y':8,'z':900,'yaw':0},a2="{firstAnomalySeen:true,firstSwitchCompleted:true,canSwitch:true,freeSwitchTutorialCompleted:true,switchCount:2}")); m.wait_for_timeout(2500)
    r=m.evaluate("(()=>{ const q=s=>document.querySelector(s).getBoundingClientRect(); const a=q('.a2-moon'),b=q('.a1-icon'),c=q('.a1-ud'),d=q('.a1-stick'),e=q('.a1-top'); return {a:[a.left,a.top,a.right,a.bottom],ok1:a.bottom<b.top&&a.bottom<c.top,ok2:a.left>e.right,w:a.width,kv:getComputedStyle(document.querySelector('.a2-moon .kv')).display}; })()")
    ok('M1 mobile: moon button top-right, no overlap, >=52px, no V hint', r['ok1'] and r['ok2'] and r['a'][2]<=390 and r['a'][1]>=0 and r['w']>=52 and r['kv']=='none', r)
    m.wait_for_function("!ACT1.api.lock",timeout=20000); m.tap('.a2-moon'); ok('M2 mobile tap switches', m.evaluate("new Promise(res=>setTimeout(()=>res(state.world.dimension),7000))")=='moon')
    if SNAP: m.screenshot(path='a2s_mobile.png')
    ok('Z no page errors', not errs, errs)
    print('ALL PASS' if all(R) else 'SOME FAIL', len(R))
