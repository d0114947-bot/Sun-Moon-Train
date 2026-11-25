# 沉睡之地：新的操作、教學、自動開始的劇情、引路
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.SAY_MANUAL=1")
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    ev("localStorage.clear();ACT1.start();window.ACT1_SPEED=6"); 
    for _ in range(80):
        W(300)
        if ev("!!document.querySelector('.a1-say.on')"): break
    ok('S1 spirit speaks in a bottom dialogue box', ev("!!document.querySelector('.a1-say.on .tx')"))
    ev("ACT1.api.say(['這是一句很長很長很長很長很長很長很長很長很長很長很長很長的話，用來測試點一下就顯示完。'])")
    for _ in range(60):
        if '很長' in ev("document.querySelector('.a1-say .tx').textContent"): break
        if ev("!!document.querySelector('.a1-say.on')"): ev("document.querySelector('.a1-say').click()")
        W(150)
    W(60); ev("document.querySelector('.a1-say').click()"); W(80)
    full=ev("[...document.querySelectorAll('.a1-say .tc')].every(x=>x.classList.contains('on'))")
    ok('S2 click shows the whole line at once', full)
    W(4000); ok('S3 does not disappear by itself', ev("!!document.querySelector('.a1-say.on')"))
    ok('S4 one playback button on the box', ev("document.querySelectorAll('.a1-say .dlg-ctl button').length")==1)
    for _ in range(40):
        if ev("ACT1._dbg().stage")=='tut': break
        if ev("!!document.querySelector('.a1-say.on')"): ev("document.querySelector('.a1-say').click()")
        W(400)
    ok('T0 tutorial starts', ev("ACT1._dbg().stage")=='tut', ev("ACT1._dbg().stage"))
    tips=ev("document.querySelector('.a1-tip').innerHTML")
    ok('T1 first tip: W/S', 'W' in tips)
    # 跳到轉視角那一步
    ev("state.act1.tut=2;"); ev("ACT1.exit();ACT1.enter()"); W(2500)
    tips=ev("document.querySelector('.a1-tip').innerHTML")
    ok('T2 rotate-view tip mentions right mouse button', '滑鼠右鍵' in tips, tips)
    ok('T3 no space / Q / E in tips', '空白' not in tips and 'Q' not in tips)
    y0=ev("ACT1._dbg().P.yaw")
    pg.mouse.move(600,360); pg.mouse.down(button='right'); pg.mouse.move(900,250,steps=12); pg.mouse.up(button='right'); W(400)
    ok('C1 right-drag turns the view', abs(ev("ACT1._dbg().P.yaw")-y0)>.5)
    ok('C2 right-drag also tilts up/down', abs(ev("ACT1.api.P.pitch"))>.1)
    W(2500); ok('T4 step done after turning both ways', ev("state.act1.tut")>=3, ev("state.act1.tut"))
    ev("ACT1.api.P.pitch=.6"); pg.keyboard.down('KeyW'); W(2500); pg.keyboard.up('KeyW'); W(300)
    ok('C3 look up + W climbs', ev("ACT1._dbg().P.y")>8, ev("ACT1._dbg().P.y"))
    W(2000)
    ev("ACT1.api.P.pitch=0"); pg.keyboard.down('KeyW'); W(600); v1=ev("ACT1._dbg().P.vt"); pg.keyboard.down('ShiftLeft'); W(1500); v2=ev("ACT1._dbg().P.vt"); pg.keyboard.up('ShiftLeft'); pg.keyboard.up('KeyW')
    ok('C4 Shift = speed boost', v2>v1*1.4, [v1,v2])
    # 教學結束 → 劇情自動開始
    ev("state.act1.tut=5;ACT1.exit();ACT1.enter()"); W(2500)
    pg.keyboard.down('KeyW'); W(800); pg.keyboard.up('KeyW')
    for _ in range(30):
        W(400)
        if ev("ACT1._dbg().stage")!='tut': break
    st=[]
    for _ in range(160):
        s=ev("ACT1._dbg().stage"); st.append(s)
        if ev("!!document.querySelector('.a1-say.on')"): ev("document.querySelector('.a1-say').click()")
        if s=='free' and not ev("ACT1._dbg().busy"): break
        W(400)
    ok('F1 story runs by itself to the end of act 1', 'notice' in st and 'free' in st, sorted(set(st)))
    try: pg.wait_for_function("['anomaly','prompt'].includes(ACT2._dbg().phase)",timeout=60000); got=True
    except Exception: got=False
    ok('F2 no waterfall: the anomaly comes by itself after the artifact story', got, ev("ACT2._dbg()"))
    ok('F3 no 瀑布 tip', '瀑布' not in (ev("(document.querySelector('.a2-tip.on')||{}).textContent||''") or ''))
    ok('Z no page errors', not errs, errs)
    b.close()
print('TOTAL',sum(R),'/',len(R))
