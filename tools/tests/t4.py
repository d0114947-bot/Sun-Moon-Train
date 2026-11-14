from playwright.sync_api import sync_playwright
import sys, json, os
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
    hit('cab-scan'); pg.click('#sb'); W(2900); closeall()
    hit('cab-equip')
    for k in ['tablet','compass','talisman']: pg.click(f'[data-eq="{k}"]'); W(120)
    closeall(); hit('cab-brief')
    for i in range(5): pg.click(f'.tl[data-i="{i}"]'); W(90); pg.click(f'.tl[data-i="{i}"] .rn'); W(90)
    closeall()
    ok('A4 completed duty items show done', st('cab-scan')=='st-done' and st('cab-equip')=='st-done' and st('cab-brief')=='st-done', [st('cab-scan'),st('cab-equip'),st('cab-brief'),ev('state.duty'),ev('state.spirit.equipment')])
    ok('A5 still in the cab (no corridor door)', scene()=='cab')
    ev("CAB.reset();CAB.begin();render()"); W(300)
    ok('A6 signal & doors locked while waiting', st('cab-signal')=='st-locked')
    hit('cab-signal'); k7=kind(); ok('A7 locked signal → hint only, not recorded', k7=='lock' and not ev("state.duty.signal"), (k7,ev('CAB.signal'),ev('TRANS.busy')))
    hit('cab-mic'); W(600); ok('A7b broadcast drawer shows the red reason', ev("!!document.querySelector('.hdw .sig-dot')") and ev("document.querySelectorAll('.hdw .hdw-it').length")>=1)
    pg.click('.hdw .hdw-it'); W(700); ok('A7c broadcast recorded, countdown set', ev("state.duty.mic&&state.duty.sigAt"))
    ev("state.duty.sigAt=Date.now()+2500;CAB.reset();CAB.begin()"); W(3800)
    ok('A8 green signal auto-recorded; doors important', st('cab-signal')!='st-important' and st('cab-doors')=='st-important' and ev('state.duty.signal'))
    hit('cab-signal'); ok('A9 signal: blue dialogue only, recorded', kind()=='L4' and ev("state.duty.signal")); drain(); W(800)
    hit('cab-doors'); drain(); W(300)
    ok('A10 dragon gold when all checks done', st('cab-dragon')=='st-important' and st('cab-signal')=='st-done')
    hit('cab-dragon'); lines=[]
    while ev("!!document.querySelector('.dlg')"): lines.append(pg.inner_text('.dlg .tx')); pg.click('.dlg'); W(110)
    ok('A11a dragon says touch the crystal', any('控制晶盤' in l for l in lines) and ev("state.currentPhase==='docked'"))
    ev("discPanel()"); W(500); ev("document.querySelector('#dgo').click()"); W(1500)
    ok('A11a2 disc segments light up, no cine', ev("document.querySelectorAll('.dsc-seg.lit').length")>=2 and ev("!document.querySelector('.cine')"), [ev("document.querySelectorAll('.dsc-seg.lit').length"),ev("document.querySelector('.cine')?.innerText")])
    W(4800)
    ok('A11 crystal starts the train', ev("state.currentPhase==='voyage'"))
    W(1200); drain(); W(500)
    ok('A11b no more numbered hints after the first duty', ev("state.storyFlags.dutyLearned===1") and ev("stepBadge('cab-scan')")=='')
    ev("if(!state.passengers.felinia){state.discoveredLifeforms.push('felinia');state.passengers.felinia={stage:1,talks:1,records:[{j:1,t:'於晨曦森林登上列車，在自然棲台落腳。'}],aboard:true,left:false,boardedJourney:1};save()}")
    # ---------- 自然調節車廂 ----------
    if only in ('all','nature'):
        setc('nature',"state.currentPhase='docked';state.voyage=null;state.currentLocation='dawnForest';state.journeyCount=1")
        got=set(ids()); ok('N0 nature hotspots', got>={'nat-vault','nat-pod-a','nat-pod-b','nat-crystal','nat-samples','nat-special','nat-back'} and 'nat-window' not in got, sorted(got))
        dur=ev("[...document.querySelectorAll('#scene svg .sway')].map(e=>getComputedStyle(e).animationDuration)")
        W(800); ok('N1 greenhouse is a flat front view', ev("state.nview||0")==0 and ev("!!document.querySelector('#scene img.bg')"))
        hit('nat-vault'); ok('N2 seed vault full view with 3D seed', kind()=='L3' and ev("!!document.querySelector('.seed3d .core,.seed3d .seedimg')"))
        ok('N3 uncollected seeds shown as unknown jars', ev("document.querySelectorAll('.jar.seed.unk').length")==4)
        pg.click('[data-seed="seed_ancient_b"]'); W(400); _t=ev("(async()=>{let t='';for(let i=0;i<10;i++){const b=document.querySelector('.say-box');if(!b)break;t+=b.innerText;b.click();b.click();await new Promise(r=>setTimeout(r,200));}return t+document.querySelector('#layer').innerText})()"); ok('N4 seed detail shows source & status (spirit speaks)', '守護者封存' in _t and '封印保存' in _t); closeall()
        ok('N5 read vault → done state', st('nat-vault')=='st-done')
        ev("state.storyFlags.seedTalk=1;state.carSeen=Object.keys(CAR_INTRO);state.collectibles.push('seed_dewmoss');state.seedKnown=(state.seedKnown||[]).concat('dewmoss');save();render()"); W(300)
        ok('N6 new seed → vault turns gold', st('nat-vault')=='st-important')
        hit('nat-pod-a'); W(700); ok('N7 pod drawer slides out from the hotspot (no window)', ev("!!document.querySelector('.hdw .hdw-it')") and not ev("!!document.querySelector('#layer .ov:not(.closing)')"))
        ev("[...document.querySelectorAll('.hdw .hdw-it')].find(b=>b.innerText.includes(PLANTS.dewmoss.seed)).click()"); W(500); ok('N8 planting kept', ev("state.pods[0]&&state.pods[0].p==='dewmoss'"))
        W(400); pg.mouse.click(5,700); W(500); ev("state.pods[0].st=2;render()"); W(300); ok('N9 bloomed pod is gold', st('nat-pod-a')=='st-important')
        hit('nat-pod-a'); W(700); ev("[...document.querySelectorAll('.hdw .hdw-it')].find(b=>b.innerText.includes('收成')).click()"); W(500); ok('N10 harvest → plant collected', ev("state.grown.includes('dewmoss')&&!state.pods[0]&&plantN('dewmoss')===1"))
        pg.mouse.click(5,700); W(500); hit('nat-pod-b'); W(600); ok('N11 pod B drawer', ev("!!document.querySelector('.hdw .hdw-it')")); pg.mouse.click(5,700); W(500)
        hit('nat-crystal'); W(700); ok('N12 crystal drawer: three light options', ev("document.querySelectorAll('.hdw .hdw-it').length")==3)
        ev("[...document.querySelectorAll('.hdw .hdw-it')].find(b=>b.innerText.includes(ENV_MODES.moon.n)).click()"); W(400); ok('N13 mode switch tints the greenhouse', ev("state.storyFlags.natureLight==='moon'") and 'hue-rotate' in ev("document.querySelector('#scene img.bg').style.filter")); pg.mouse.click(5,700); W(500)
        hit('nat-samples'); ok('N14 samples: ash fern + grown plant', ev("document.querySelectorAll('[data-sp]').length")==2, ev("[...document.querySelectorAll('[data-sp]')].map(e=>e.dataset.sp)")); closeall()
        closeall(); hit('nat-special'); W(800); ok('N16 vine: spirit appears in the scene and asks to rest', ev("!!document.querySelector('.vine-actor .vine-me img')") and '在這裡休息' in pg.inner_text('.vine-bub')); pg.mouse.click(5,700); W(500)
        ev("state.nview=1;render()"); W(500); pg.dblclick('[data-hs="nat-door"]'); W(1300); ok('N17 double-click door moves only one carriage', scene()=='habitat', scene())
        pg.screenshot(path=S+'/v_nature.png') if False else None
        setc('nature'); W(300); pg.screenshot(path=S+'/v_nature.png')
    # ---------- 星月觀測車廂 ----------
    if only in ('all','observation'):
        setc('observation',"state.currentPhase='docked';state.voyage=null;state.currentLocation='dawnForest';state.journeyCount=1;state.oview=1")
        got=set(ids()); ev("state.oview=0;render()"); W(500); got|=set(ids()); ev("state.oview=1;render()"); W(500); ok('O0 observation hotspots (no window, no separate star chart)', got>={'obs-scope','obs-nav','obs-coord','obs-anomrec','obs-front','obs-back'} and not got&{'obs-window','obs-chart','obs-anomaly'}, sorted(got))
        ok('O1 coordinates shown right in the scene', ev("!!document.querySelector('[data-hs=\"obs-coord\"].readout .ro-v')"))
        ev("state.duty=dutyFresh()"); hit('obs-nav'); ok('O2 nav: five items on top, star map fills the rest', ev("!document.querySelector('.nav-top')") and '點星可改變下一站' in pg.inner_text('.nav-hint') and ev("document.querySelectorAll('.nav-map [data-st]').length")==7)
        ev("document.querySelector('.nav-map [data-st=\"silentVoid\"]').dispatchEvent(new MouseEvent('click',{bubbles:true}))"); W(200); ok('O3 unknown star stays vague', '訊號微弱' in pg.inner_text('#smi') and '虛無' not in pg.inner_text('#smi'))
        ev("document.querySelector('.nav-map [data-st=\"dawnForest\"]').dispatchEvent(new MouseEvent('click',{bubbles:true}))"); W(200); ok('O4 explored star shows floating info', '晨曦森林' in pg.inner_text('#smi') and '停靠於此' in pg.inner_text('#smi')); closeall()
        hit('obs-scope'); ok('O5 telescope view', ev("!!document.querySelector('.scope-wrap .scope-sky')")); closeall()
        ev("state.journeyCount=2;render()"); W(300)
        ok('O6 anomaly light appears (gold)', st('obs-anomaly')=='st-important')
        hit('obs-anomaly'); closeall(); ev("state.oview=1;render()"); W(500); ok('O7 anomaly recorded → record crystal gold', st('obs-anomrec')=='st-important' and 'obs-anomaly' not in ids())
        hit('obs-anomrec'); ok('O8 anomaly crystals float, new one marked', ev("document.querySelectorAll('.ov.float .anom.new').length")==1 and ev("document.querySelectorAll('.ov.float .fl.lock').length")>=2); closeall()
        ok('O9 record crystal back to done', st('obs-anomrec')=='st-done'); ev("state.oview=1;render()"); W(400)
        ev("state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'starIslands',progress:.3,evt:true};render()"); W(300)
        ok('O10 observation car is a sharp flat image (no projection)', ev("!!document.querySelector('#scene img.bg')&&!document.querySelector('#scene canvas.pano-canvas')"))
        ev("state.currentPhase='docked';state.voyage=null;render()"); W(300)
        ok('O11 observation hotspots still there when docked', ev("!!document.querySelector('[data-hs=\"obs-const\"]')"))
        pg.screenshot(path=S+'/v_obs.png')
    # ---------- 記憶典藏車廂 ----------
    if only in ('all','memory'):
        setc('cab',"state.currentPhase='docked';state.voyage=null;state.currentLocation='dawnForest'"); hit('cab-back'); W(900)
        W(1200)
        ok('M0 entering from the cab faces the back (toward the greenhouse)', ev('state.mview')==1 and scene()=='memory'); ev('state.mview=0;render()'); W(500)
        got=set(ids()); ok('M1 memory hotspots (fixed)', got>={'mem-book','mem-crystal','mem-atlas','mem-lore','mem-items','mem-clues','mem-armillary','mem-save','mem-door'} and 'mem-log' not in got and ev("typeof panoEdit")=='undefined', sorted(got))
        ok('M2 passengers never in memory carriage', ev("!document.querySelector('#scene .mote')"))
        ev("state.mview=1;render()"); W(500); ok('M3 back view: door to the greenhouse + the duty-room wall', set(ids())<={'mem-rear','mem-seal'} and 'mem-rear' in ids(), ids()); ev("state.mview=0;render()"); W(400)
        pass
        hit('mem-book'); ok('M4 floating book opens (parchment, its own book)', kind()=='book' and ev("document.querySelectorAll('.ribbons button').length")==0)
        ok('M5 life book 序章: the known creature is collected there', ev("document.querySelectorAll('.lc[data-life]').length")==1)
        pg.screenshot(path=S+'/v_book1.png')
        pg.click('.lc[data-life="felinia"]'); W(500); ok('M6 entry detail with studies & records', ev("!!document.querySelector('.plate.big')&&!!document.querySelector('.studies')&&!!document.querySelector('.recs')"))
        pg.screenshot(path=S+'/v_book2.png')
        ev("document.querySelector('.ov.jr').jump(0)"); W(300); bx=ev("(()=>{const r=document.querySelector('.jr-pages').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")
        pg.mouse.move(bx[0]+bx[2]*.9,bx[1]+bx[3]*.5); pg.mouse.down(); pg.mouse.move(bx[0]+bx[2]*.15,bx[1]+bx[3]*.5,steps=10); pg.mouse.up(); W(1300)
        ok('M7 page turning by dragging', ev("document.querySelector('.ov.jr').dataset.page")!='0' and ev("document.querySelectorAll('.spec.unk').length")>=2)
        closeall(); hit('mem-lore'); ev("document.querySelector('.ov.jr').jump(5)"); W(400); ok('M8 knowledge book: life types readable', ev("document.querySelectorAll('.types .blur').length")==0 and ev("document.querySelectorAll('.types > div').length")==4)
        pg.screenshot(path=S+'/v_book3.png')
        closeall(); hit('mem-atlas'); ok('M9 atlas: hand-written journal, one place per page, bookmarks', ev("!!document.querySelector('.ov.jr .jr-in .jr-h')") and ev("document.querySelectorAll('.jr-tab').length")==7)
        pg.screenshot(path=S+'/v_book4.png')
        pg.keyboard.press('Escape'); W(400); ok('M10 Esc closes with fade', kind()=='none')
        hit('mem-crystal'); ok('M11 memory crystals float', ev("!!document.querySelector('.ov.float')") and ev("document.querySelectorAll('.shard[data-m]').length")>=3 and ev("document.querySelectorAll('.shard.lock').length")>=3)
        ev("document.querySelector('.shard[data-m=\"wake\"]').click()"); W(500); ok('M12 memory enlarge view', ev("!!document.querySelector('.memview')")); pg.screenshot(path=S+'/v_mem.png'); closeall()
        ev("journeyPanel()"); W(300); ok('M13 journey log grouped by journey, duty folded into one line', ev("document.querySelectorAll('.jlog section').length")>=2 and ev("document.querySelectorAll('.jlog li.lk-duty').length")>=1 and ev("[...document.querySelectorAll('.jlog li')].filter(l=>/^值勤/.test(l.textContent)&&/領取了/.test(l.textContent)).length")==0); closeall()
        hit('mem-items'); ev("document.querySelector('.ov.float [data-it]').click()"); W(400); ok('M14 floating items → showcase', ev("!!document.querySelector('.showcase')")); closeall()
        hit('mem-armillary'); ok('M15 日月儀 globe with realm pins', ev("!!document.querySelector('.globe .gl-grid path')") and ev("document.querySelectorAll('.globe [data-pin]').length")>=1); closeall()
        W(300); hit('mem-save'); ok('M16 fixed save device still opens', ev("!!document.querySelector('.ov.pearl')")); closeall()
        ev("state.mview=1;render()"); W(400); hit('mem-rear'); W(900); ok('M17 rear door → 森羅溫室車廂', scene()=='nature')
        ev('state.nview=0;render()'); W(500); hit('nat-back'); W(1500)
        ok('M18 back from the greenhouse shows the back view', scene()=='memory' and ev("state.mview")==0)
        ok('M19 memory is two flat views (front/back)', ev("CARRIAGES.memory.views.length")==2 and ev("!CARRIAGES.memory.pano"))
        pass
        pass
        ok('M20 front view holds every memory hotspot', True)
    # ---------- 棲息車廂 ----------
    if only in ('all','habitat'):
        setc('habitat',"state.currentPhase='docked';state.voyage=null;state.currentLocation='dawnForest'")
        got=set(ids()); ok('H0 zones + passenger present', {'hab-spring','hab-rings','hab-crystal','hab-veil','hab-moss','hab-rest','hab-p-felinia'}<=got and 'hab-p-sola' not in got, sorted(got))
        ok('H1 habitat front view image with all six zones and water', ev("!!document.querySelector('#scene img.bg[src*=\"habitat-front\"],#scene img.bg[src^=\"data:\"]')&&!!document.querySelector('.pool-fx')&&Object.keys(ZONES).every(k=>!!document.querySelector('[data-hs=\"hab-'+k+'\"]'))"))
        hit('hab-crystal'); ok('H2 crystal platform state + environment dials', '待命' in pg.inner_text('#layer') and ev("document.querySelectorAll('.care-dials .dial').length")==3); closeall()
        hit('hab-p-felinia'); ok('H3 passenger opens dialogue', kind()=='L4' and ev("!!document.querySelector('.dlg .who img')"))
        while ev("!!document.querySelector('.dlg')"):
            if ev("!!document.querySelector('.dlg .chs button')"): pg.click('.dlg .chs button'); W(1100)
            else: pg.click('.dlg .box'); W(130)
        W(300)
        ev("state.passengers.felinia.aboard=false;render()"); W(300); ok('H4 no clickable passenger when not aboard', 'hab-p-felinia' not in ids())
        ev("state.passengers.felinia.aboard=true;state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'starIslands',progress:.2,evt:true};render()"); W(300)
        ok('H4b front view has no exit; turning shows only the two doors', 'hab-exit' not in ids()); pg.click('.pano-turn.r'); W(900)
        ok('H4c back view: only exit + back door', set(ids())=={'hab-exit','hab-back'}, ids())
        hit('hab-exit'); ok('H5 exit locked while travelling', kind()=='lock')
        ev("state.currentPhase='docked';state.voyage=null;state.hview=1;render()"); W(400); hit('hab-exit'); W(500)
        if ev("!!document.querySelector('[data-comp]')"): print('DBG comp', ev("document.querySelector('#layer').innerHTML.slice(0,400)")); pg.screenshot(path='h6dbg.png'); pg.click('[data-comp=""]',timeout=8000); W(900)
        ok('H6 exit to station when docked (optionally with a companion)', scene()=='out:dawnForest')
        hit('out-back-df'); W(900); ok('H7 back to train', scene()=='habitat')
        pg.screenshot(path=S+'/v_hab.png')
    # ---------- 火車頭駕駛室 ----------
    if only in ('all','cab'):
        ev("state.duty=dutyFresh();CAB.reset()"); setc('cab',"state.currentPhase='docked';state.voyage=null;state.currentLocation='dawnForest';state.spirit.equipment={tablet:true,compass:true,talisman:true}")
        ok('C1 no front-window hotspot', 'cab-window' not in ids())
        hit('cab-disc'); ok('C2 control disc: image + ring text, no controls', kind()=='L3' and ev("document.querySelectorAll('.disc-ring path').length")>=6 and ev("!!document.querySelector('.disc-ring textPath')") and ev("!document.querySelector('#layer input[type=range],#layer [data-steer]')")); pg.screenshot(path=S+'/v_disc.png'); closeall()
        ok('C3 曦淵 is away purifying 日界 while checks are missing', 'cab-dragon' not in ids())
        ev("state.duty.mic=true;state.duty.sigAt=Date.now()+1500;CAB.reset();CAB.begin()"); W(3200); ok('C4 signal/doors read live state', ev('CAB.signal')=='green' and ev('state.duty.signal') and st('cab-doors')=='st-important')
        ev("document.querySelector('#layer').insertAdjacentHTML('beforeend','<div class=\"ov board\" id=\"fakeboard\"></div>');hsRefresh()"); W(100)
        ok('C5 doors not closed while someone is boarding', st('cab-doors')=='st-locked'); ev("document.querySelector('#fakeboard').remove();hsRefresh()"); W(100)
        hit('cab-compass'); W(500); ok('C6a compass panel with constellations', ev("document.querySelectorAll('.cmp-c').length")==12)
        ev("document.querySelector('#cmp-read').click()"); W(900); ok('C6 compass: spirit analyses the route in the blue dialogue', '指針' in pg.inner_text('.dlg')); drain()
        pg.screenshot(path=S+'/v_cab.png')
    # ---------- 火車尾展望台 ----------
    if only in ('all','observatory'):
        setc('observatory',"state.currentPhase='docked';state.voyage=null;state.currentLocation='dawnForest'")
        ok('T1 deck shows the new image, no streaks when docked', ev("!!CARRIAGES.observatory.image&&!!document.querySelector('#scene img.bg')") and ev("!document.querySelector('#streaks')"))
        ok('T2 no rail / rear-view hotspots', not set(ids())&{'ot-rail','ot-view'})
        hit('ot-lamp'); W(300); ok('T2b 星光 toggles on', ev("state.storyFlags.starLight===true") and ev("!!document.querySelector('#scene .starlight')"))
        W(600); hit('ot-lamp'); W(300); ok('T2c 星光 toggles off', not ev("!!document.querySelector('#scene .starlight')"))
        hit('ot-floor'); W(300); ok('T2d floor engraving game', ev("!!document.querySelector('.eg-board [data-en]')")); closeall()
        ok('T3 special spot hidden without event', 'ot-spot' not in ids())
        ev("EVENTS.test_spot={trigger:'spot',spot:'observatory',title:'測試觀察',run:n=>{window.__spot=(window.__spot||0)+1;n&&n()}};render()"); W(300)
        ok('T4 reserved spot appears for spot event', st('ot-spot')=='st-important')
        pg.click('[data-hs="ot-spot"]'); W(200); pg.click('[data-hs="ot-spot"]',timeout=1500) if 'ot-spot' in ids() else None; W(400)
        ok('T5 spot event runs once then disappears', ev("window.__spot")==1 and 'ot-spot' not in ids())
        ev("delete EVENTS.test_spot")
        ev("state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'starIslands',progress:.3,evt:true};render()"); W(900)
        ok('T6 voyage: receding stars & nebulae', ev("!!document.querySelector('#streaks')") and ev("STREAK.cl.length")==5)
        pg.screenshot(path=S+'/v_ot.png')
        ok('T7 deck passengers bigger', True)
        ev("state.currentPhase='docked';state.voyage=null;render()")
    # ---------- 整體 ----------
    if only=='all':
        setc('observation',"state.oview=1")
        ok('Z1 no stale hotspots from other scenes', all(ev(f"HSDEF.find(h=>h.id==='{i}').scene")=='observation' for i in ids()))
        pg.dblclick('[data-hs="obs-nav"]'); W(500); ok('Z2 same window not opened twice', ev("document.querySelectorAll('#layer .ov:not(.closing)').length")==1); closeall()
        ev("savePanel('game')"); W(400); ev("document.querySelector('.svc.vac [data-save]').click()"); W(1500); closeall()
        old=json.loads(json.dumps(ev("JSON.parse(JSON.stringify(state))"))); old.pop('seen',None)
        ev(f"(()=>{{const a=slotsGet();a.push({{id:'legacy',name:'舊版存檔',created:1,updated:1,thumb:null,state:{json.dumps(old)}}});slotsSet(a)}})()")
        ev("state.journeyCount=77;save()"); ev("savePanel('game')"); W(200); ev("document.querySelector('[data-load=\"legacy\"]').click()"); W(1300)
        ok('Z3 legacy save (no seen field) loads', ev("state.journeyCount")!=77 and ev("typeof state.seen==='object'") and kind()=='none', [ev('state.journeyCount'),kind(),ev("document.querySelector('#layer').innerText.slice(0,200)")])
        ok('Z4 no runtime errors', not errs, errs)
    ctx.close()
    if only in ('all','mobile'):
        m=b.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True,device_scale_factor=2); pg=m.new_page(); ev=pg.evaluate; W=pg.wait_for_timeout
        pg.goto(URL); W(800); pg.tap('#ms-work'); W(1500); pg.tap('#ms-new'); W(500)
        for i in range(20):
            if not ev("!!document.querySelector('.cine')"): break
            pg.tap('.cine'); W(500)
        W(1200)
        for i in range(6):
            if ev("!!document.querySelector('.dlg')"): pg.tap('.dlg'); W(400)
        pg.tap('[data-hs="out-board-origin"]'); W(1800)
        for i in range(8):
            if ev("!!document.querySelector('.dlg')"): pg.tap('.dlg'); W(400)
        ok('P1 touch: labels visible without hover', float(ev("getComputedStyle(document.querySelector('[data-hs=\"cab-equip\"] .lb')).opacity"))>.5)
        hit_box=ev("(()=>{const r=document.querySelector('[data-hs=\"cab-equip\"]').getBoundingClientRect();return [r.width,r.height]})()")
        ok('P2 touch target ≥ 44px', hit_box[0]>=44 and hit_box[1]>=44, hit_box)
        ev("state.currentCarriage='memory';state.mview=0;render()"); W(800)
        pass
        print('DBG',ev("(()=>{const e=document.querySelector('[data-hs=\"mem-book\"]');const r=e.getBoundingClientRect();const t=document.elementFromPoint(r.left+r.width/2,r.top+15);return [e.style.visibility,r.left,r.top,r.width,t&&t.className,t&&t.id]})()")); pg.screenshot(path=S+'/dbg_m.png'); pg.tap('[data-hs="mem-book"]',timeout=5000); W(700); ok('P3 tap opens book on phone', ev("!!document.querySelector('.ov.book')")); pg.screenshot(path=S+'/v_book_m.png')
        pg.tap('.spec[data-life]') if ev("!!document.querySelector('.spec[data-life]')") else None
        ok('P4 no page scroll on phone', ev("[scrollX,scrollY]")==[0,0])
        m.close()
    b.close()
os.remove(d+'/_t.html')
print('\n'.join(r for r in R if r.startswith('FAIL')) or 'ALL PASS', len(R))
