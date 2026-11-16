# 種子庫任務（三枚封存古種）＋月界才有的事＋望遠鏡黑影
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE="document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();state=freshState();state.introDone=true;state.prologueDone=true;state.journeyCount=9;state.clues.push('clue_dragon');state.storyFlags.sealSeen=1;state.storyFlags.metDragon=1;state.currentPhase='docked';state.carSeen=TRAIN.slice();state.annSeen='x';state.visitedLocations=['dawnForest','starIslands','reverseRealm','boundlessCorridor','timeriftSea'];"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    clean=lambda: ev("closeAll();document.querySelectorAll('#layer .dlg,#layer .cine').forEach(e=>e.remove());document.querySelectorAll('.hdw').forEach(d=>drawerClose(d))")
    def talk(ms=20000):
        t=0
        while t<ms:
            if ev("!!document.querySelector('#layer .cine')"): ev("document.querySelector('#layer .cine').click()")
            elif ev("!!document.querySelector('#layer .dlg')"): ev("document.querySelector('#layer .dlg .box')?.click();document.querySelector('#layer .dlg')?.click()")
            else:
                W(400); t+=400
                if not ev("!!document.querySelector('#layer .dlg,#layer .cine')"): return
            W(200); t+=200
    hs=lambda: ev("[...document.querySelectorAll('#scene [data-hs]')].map(e=>e.dataset.hs)")
    ev(BASE+"state.currentLocation='reverseRealm';state.currentCarriage='nature';state.nview=0;save();PANO.active=null;RUNNING=true;render()"); W(900); talk(); clean()
    ok('S0 arriving no longer unseals by itself', not ev("seedOpen('seed_ancient_a')"))
    ok('S0b goal: read the seal', '刻紋' in ev("document.querySelector('#hud .goal').innerText"))
    ev("INTERACT['nat:vault']()"); W(900); ev("document.querySelector('[data-seed=seed_ancient_a]').click()"); W(500)
    ok('A1 sealed seed: read the inscription', ev("!!document.querySelector('.sq-read')")); ev("document.querySelector('.sq-read').click()"); W(400)
    ok('A1b inscription read', ev("sq('a')")==1 and '倒著流的光' in ev("document.querySelector('#layer .ov').innerText")); clean(); talk()
    ev("state.currentCarriage='cab';render()"); W(800); talk(); clean()
    ok('A2 at 逆生之境: the cab window shows the waterfall', 'sq-win-a' in hs(), hs())
    ev("hsClick('sq-win-a',document.querySelector('[data-hs=sq-win-a]'))"); W(400); talk(); ok('A2b the seed reacts', ev("sq('a')")==2)
    ev("state.currentCarriage='nature';state.trainMoon=true;state.storyFlags.natureLight='moon';render()"); W(700); clean()
    ev("hsClick('nat-crystal',document.querySelector('[data-hs=nat-crystal]'))"); W(800)
    ok('A3 moon train: cannot use dawn light for the seed', ev("[...document.querySelectorAll('.hdw .hdw-it')].some(b=>/封存種子・甲/.test(b.innerText)&&b.disabled)")); clean()
    ev("state.trainMoon=false;state.storyFlags.natureLight='dawn';render()"); W(500); ev("hsClick('nat-crystal',document.querySelector('[data-hs=nat-crystal]'))"); W(800)
    ev("[...document.querySelectorAll('.hdw .hdw-it')].find(b=>/封存種子・甲/.test(b.innerText)).click()"); W(600); talk()
    ok('A4 sun + dawn light: 晨種 wakes', ev("seedOpen('seed_ancient_a')")); clean()
    # 潮種
    ev("state.seedQ.b=2;state.currentLocation='boundlessCorridor';state.trainMoon=false;render()"); W(500); ev("skylight()"); W(400); talk(); ok('B1 sun: tide seed does not answer', not ev("seedOpen('seed_ancient_b')"))
    ev("state.trainMoon=true;render()"); W(400); ev("skylight()"); W(400); talk(); ok('B2 moon + skylight: 潮種 wakes', ev("seedOpen('seed_ancient_b')")); clean()
    # 暮種
    ev("state.seedQ.c=2;state.currentLocation='timeriftSea';render()"); W(500); ev("hsClick('nat-crystal',document.querySelector('[data-hs=nat-crystal]'))"); W(800)
    ev("[...document.querySelectorAll('.hdw .hdw-it')].find(b=>/放在晶石上/.test(b.innerText)).click()"); W(600); clean(); W(300)
    pg.keyboard.press('KeyV'); W(2000); talk(); ok('C1 seed on the crystal + switch realm: 暮種 wakes', ev("seedOpen('seed_ancient_c')"))
    ok('C2 main quest moves to the void', '寂滅虛空' in ev("goalNow().t"))
    # 月界才有的事
    ev(BASE+"state.currentLocation='starIslands';state.currentCarriage='observatory';state.starMsgs=[{pid:'sola',t:'謝謝你',read:false,j:1}];state.trainMoon=false;save();render()"); W(800); talk(); clean()
    if 'ot-msg' in hs():
        ev("hsClick('ot-msg',document.querySelector('[data-hs=ot-msg]'))"); W(500); ok('M1 sun: message engraving too faint', '好像留著什麼字' in ev("document.querySelector('#layer .dlg')?.innerText||''")); talk(); clean()
    ev("state.currentCarriage='memory';state.mview=0;state.trainMoon=false;render()"); W(500); ok('M2 sun: no moonlight writing', 'mem-moonwrit' not in hs())
    ev("state.trainMoon=true;render()"); W(500); ok('M3 moon: moonlight writing appears', 'mem-moonwrit' in hs())
    ev("state.spirit.taint=10;TAINT.add(10)"); ok('M4 docked in the moon realm + moon train: taint rises slower', ev("TAINT.val()")==16)
    ev("state.trainMoon=false;state.spirit.taint=10;TAINT.add(10)"); ok('M5 sun look: normal', ev("TAINT.val()")==20)
    ev("state.trainMoon=false;state.currentPhase='voyage';state.voyage={to:'boundlessCorridor',from:'starIslands',progress:.27,t0:Date.now()};state.currentCarriage='habitat';render()"); W(1600)
    ok('M6 shadow segment warning', '暗影航段' in ev("document.querySelector('#layer .dlg')?.innerText||''")); talk(); clean()
    ev("Math.random=()=>0.01;state.voyage.progress=.4"); W(2600); ok('M7 sun look in the shadow segment: noticed', ev("!!state.voyage.shade.seen"))
    talk(); clean()
    # 望遠鏡
    ev(BASE+"state.currentLocation='dawnForest';state.currentCarriage='observation';save();render()"); W(700); talk(); clean()
    ev("scopePanel()"); W(900)
    n=ev("document.querySelectorAll('.scope-shadow:not(.place)').length")
    if n:
        ev("document.querySelector('.scope-shadow:not(.place)').dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}))"); W(1700)
        ok('T1 telescope: clicking the shadow reveals the creature', ev("getComputedStyle(document.querySelector('.scope-shadow:not(.place)')).filter").find('brightness(1)')>=0, ev("getComputedStyle(document.querySelector('.scope-shadow:not(.place)')).filter"))
    else: ok('T1 telescope has shadows', False)
    ok('Z no page errors', not errs, errs)
    print('ALL PASS' if all(R) else 'SOME FAIL', len(R))
