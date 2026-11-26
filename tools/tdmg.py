# 被襲擊的車廂＋駕駛室後方
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE=open(S+'/tchap.py').read().split('BASE="')[1].split('"\n')[0]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    ev(BASE+"state.currentPhase='docked';state.currentLocation='dawnForest';state.currentCarriage='cab';save();PANO.active=null;RUNNING=true;render()"); W(800)
    bg=lambda: ev("(document.querySelector('#scene img.bg')||{}).src||''")
    fr=lambda: ev("[...document.querySelectorAll('#scene svg image')].map(i=>i.getAttribute('href')).filter(h=>/cab-frame/.test(h)).join()")
    ok('R1 cab has a turn button', ev("!!document.querySelector('#scene .pano-turn')"))
    ok('R2 front: door hotspots hidden, console hotspots shown', not ev("!!document.querySelector('#scene [data-hs=\"cab-back\"],#scene [data-hs=\"cab-exit\"]')") and ev("!!document.querySelector('#scene [data-hs=\"cab-disc\"]')"))
    ev("document.querySelector('#scene .pano-turn').click()"); W(900)
    ok('R3 turned: 駕駛室後方 picture', 'cab-rear' in bg() and 'dmg' not in bg() and 'moon' not in bg(), bg())
    ok('R4 the door leads back to 記憶典藏車廂, console hotspots hidden', ev("!!document.querySelector('#scene [data-hs=\"cab-back\"]')") and not ev("!!document.querySelector('#scene [data-hs=\"cab-disc\"]')"))
    ev("state.currentLocation='dawnForest';render()"); W(400)
    ok('R4b right door is the way out (下車) when docked', ev("!!document.querySelector('#scene [data-hs=\"cab-exit\"]')"))
    pg.screenshot(path=S+'/dmg_rear.png')
    ev("state.trainMoon=true;render()"); W(500); ok('R5 moon side', 'cab-rear-moon' in bg(), bg()); ev("state.trainMoon=false;render()"); W(300)
    W(3000); ok('R6 stays fine over time (no errors)', not errs, errs[:2])
    ev("document.querySelector('#scene [data-hs=\"cab-back\"]').click()"); W(2500)
    ok('R7 door walks to 記憶典藏車廂', ev("state.currentCarriage")=='memory')
    ev("state.currentCarriage='cab';render()"); W(500)
    ok('R8 coming back into the cab faces the console', ev("state.cview||0")==0 and 'cab-frame.webp' in fr(), fr())
    # 危機爆發
    ev("state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'starIslands',progress:.6,evt:true};crStart('B01',{real:true,sev:3});state.crisis.stage='W4';save();render()"); W(800)
    ok('D1 cab during an outbreak: damaged console', 'cab-frame-dmg' in fr(), fr())
    pg.screenshot(path=S+'/dmg_cab.png')
    want={'nature':['nature-front-dmg','nature-back-dmg'],'habitat':['habitat-front-dmg','habitat-back-dmg'],'memory':['memory-front-dmg','memory-back-dmg'],'observation':['observation-back-dmg','observation-front-dmg']}
    for car,W2 in want.items():
        got=[]
        for v in (0,1):
            ev(f"state.currentCarriage='{car}';state[vKey('{car}')]={v};render()"); W(500); got.append(bg())
        ok(f'D2 {car}: both views damaged', all(w in g for w,g in zip(W2,got)), got)
        if car=='nature': pg.screenshot(path=S+'/dmg_nature.png')
    ev("state.currentCarriage='cab';state.cview=1;render()"); W(400); ok('D3 cab rear damaged', 'cab-rear-dmg' in bg(), bg())
    ev("state.trainMoon=true;render()"); W(300); ok('D4 damage wins over the moon side', 'cab-rear-dmg' in bg(), bg()); ev("state.trainMoon=false")
    ev("state.crisis=null;state.currentCarriage='nature';state.nview=0;render()"); W(400)
    ok('D5 crisis over: back to normal', bg().endswith('nature-front.jpg'), bg())
    ev("crStart('B01',{real:true,sev:3});state.crisis.stage='W3';render()"); W(300)
    ok('D6 before the outbreak (warning signs only): still normal', bg().endswith('nature-front.jpg'), bg())
    ev("state.crisis=null;state.currentPhase='docked';state.voyage=null;render()")
    ok('Z no page errors', not errs, errs[:3])
    b.close()
