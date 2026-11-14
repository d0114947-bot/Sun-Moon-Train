from playwright.sync_api import sync_playwright
import sys, json, os, time
T0=time.time()
def TT(m): print('%.1f'%(time.time()-T0),m,flush=True)
S=sys.argv[1]; only=sys.argv[2] if len(sys.argv)>2 else 'all'; d='/home/claude/game'
html=open(d+'/index.html').read()
open(d+'/_t.html','w').write('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">'+html)
URL='http://127.0.0.1:8765/_t.html'
R=[]
def ok(n,c,x=''):
    R.append(('PASS ' if c else 'FAIL ')+n+(' '+str(x) if x!='' and (not c or len(str(x))<90) else '')); print(R[-1],flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    ctx=b.new_context(viewport={'width':1280,'height':720}); pg=ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    ev=pg.evaluate; W=pg.wait_for_timeout
    def scene(): return ev("HS_SCENE()")
    def ids(): return ev("[...document.querySelectorAll('#scene [data-hs]')].map(e=>e.dataset.hs)")
    def st(i): return ev(f"(()=>{{const e=document.querySelector('[data-hs=\"{i}\"]');return e?[...e.classList].find(c=>c.startsWith('st-')):null}})()")
    def face(i): ev(f"panoFace('{i}')"); W(350)
    def hit(i):
        if ev("!!PANO.active"): face(i)
        pg.click(f'[data-hs="{i}"]',force=True); W(420)
    def drain():
        for _ in range(12):
            if not ev("!!document.querySelector('#layer .dlg')"): break
            pg.locator('#layer .dlg').last.click(); W(160)
    def closeall():
        while ev("!!document.querySelector('#layer .ov:not(.closing)')"):
            ev("closeOv([...document.querySelectorAll('#layer .ov:not(.closing)')].pop())"); W(330)
        W(120)
    def kind():
        return ev("(()=>{const o=[...document.querySelectorAll('#layer .ov:not(.closing)')].pop(); if(o) return o.classList.contains('small')?'L2':o.classList.contains('book')?'book':'L3'; if(document.querySelector('.whisper')) return document.querySelector('.whisper.lock')?'lock':'L1'; if(document.querySelector('#layer .dlg')) return 'L4'; return 'none'})()")
    def setc(car,extra=''):
        ev(f"{extra};state.boardQ=[];closeAll();state.currentCarriage='{car}';state.currentPhase=state.currentPhase==='outside'?'docked':state.currentPhase;render()"); W(500)

    pg.goto(URL); W(800); ev("window.rollBoarders=()=>[]")
    # ---------- A. main flow (regression of the duty system) ----------
    pg.click('#ms-work'); W(1500); pg.click('#ms-new'); W(600)
    for i in range(6): pg.click('.cine'); W(260)
    W(1200); drain(); W(300)
    ok('A0 opening ends on the 沉睡之地 platform with a boarding hotspot', scene()=='out:origin' and 'out-board-origin' in ids(), (scene(),ids()))
    hit('out-board-origin'); W(1600); drain(); W(300)
    ok('A1 opening → duty prep happens in the cab', scene()=='cab')
    ok('A1b hint badge shows number only and the hotspot pulses', ev("!document.querySelector('.step i')") and ev("!!document.querySelector('.hs.stepcur')"))
    ok('A2 no prep corridor on the walking path', ev("TRAIN.indexOf('prep')")==-1 and ev("neighbors('cab').back")=='memory')
    ok('A3 duty hotspots important', st('cab-scan')=='st-important' and st('cab-equip')=='st-important')
    TT('a');hit('cab-scan');TT('b'); pg.click('#sb');TT('c'); W(2900); closeall();TT('d')
    hit('cab-equip');TT('e')
    for k in ['tablet','compass','talisman']: pg.click(f'[data-eq="{k}"]'); W(120)
    closeall(); hit('cab-brief');TT('f')
    for i in range(5): pg.click(f'.tl[data-i="{i}"]'); W(90); pg.click(f'.tl[data-i="{i}"] .rn'); W(90)
    closeall()
    TT('g'); b.close()
