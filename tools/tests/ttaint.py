from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' '+str(x) if x!='' else ''),flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(900)
    ev("document.querySelector('#mainscreen')?.remove();RUNNING=true;state=freshState();normalizeState();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=1;state.visitedLocations=['dawnForest'];state.currentCarriage='cab';render()"); W(500)
    T=lambda: ev("state.spirit.taint")
    ok('T1 new game starts pure', T()==6)
    def scan():
        ev("closeAll();state.duty.scan=false;render()"); W(300); pg.click('[data-hs="cab-scan"]'); W(500); pg.click('#sb'); W(2900)
        r=ev("[state.spirit.contamination.value,state.spirit.contamination.level,document.querySelector('#so').innerText]"); ev("closeAll()"); W(300); return r
    r=scan(); ok('T2 scan reads the real value', r[0]==6 and r[1]=='純淨' and '可以值勤' in r[2], r[:2])
    def ready(): ev("state.spirit.equipment={tablet:true,compass:true,talisman:true};Object.assign(state.duty,{briefing:true,signal:true,doors:true,mic:true});CAB.signal='green';CAB.doors='lit';render()")
    def report():
        ev("closeAll()"); W(200); ev("dragonTalk()"); W(400); lines=[]
        for _ in range(40):
            if not ev("!!document.querySelector('.dlg')"): break
            lines.append(pg.locator('.dlg .tx').last.inner_text()); pg.locator('.dlg .box').last.click(); W(140)
        return lines
    ev("state.spirit.taint=30;render()"); W(200); ok('T3 mild taint → grey-violet edge mist', ev("document.body.classList.contains('taint-mild')"))
    r=scan(); ok('T4 scan says 微染, can still depart', r[1]=='微染' and '建議盡快淨化' in r[2], r[:2])
    ev("state.spirit.taint=62;render()"); r=scan(); ready()
    ok('T5 heavy taint: scan says 重染, cannot work', r[1]=='重染' and '不得值勤' in r[2] and ev("document.body.classList.contains('taint-heavy')"))
    ok('T6 scan hotspot asks to re-measure', ev("document.querySelector('[data-hs=\"cab-scan\"]').classList.contains('st-important')"))
    L=report(); ok('T7 dragon refuses departure at 50+', any('先去淨化' in l for l in L) and ev("state.currentPhase")=='docked', L[-1:])
    # purification spots
    ev("closeAll();state.currentCarriage='nature';render()"); W(500); ev("INTERACT['nat:special']()"); W(400)
    t0=T(); pg.click('#vr'); W(300); ok('T8 守望藤 −10 once (spirit rests under the tree)', T()==t0-10 and ev("!document.querySelector('#vr')") and ev("!!document.querySelector('.vine-me.rest')"), (t0,T()))
    ev("closeAll()"); W(300); ev("INTERACT['nat:special']()"); W(300); ok('T9 same stop: already used', ev("!document.querySelector('#vr')") and '休息過了' in pg.inner_text('.vine-bub'))
    ev("closeAll();state.grown=['dewmoss'];podB()"); W(300); t0=T(); pg.click('[data-pur="plant"]'); W(300); ok('T10 淨化植株 −15', T()==t0-15)
    ev("closeAll();zoneInfo('spring')"); W(300); t0=T(); pg.click('[data-pur="spring"]'); W(300); ok('T11 靈泉 −6', T()==t0-6, T())
    ev("closeAll()"); W(300)
    t0=T(); ev("state.passengers.sirenora={stage:1,talks:0,records:[],aboard:true,left:false,boardedJourney:1};state.discoveredLifeforms.push('sirenora');talk('sirenora')"); W(500)
    for _ in range(30):
        if not ev("!!document.querySelector('.dlg')"): break
        if ev("!!document.querySelector('.dlg .chs button')"): pg.locator('.dlg .chs button').last.click(); W(1100)
        else: pg.locator('.dlg .box').last.click(); W(160)
    ok('T12 霧羽海葵龍 soothing −12', T()==max(0,t0-12), (t0,T()))
    ev("talk('sirenora')"); W(400)
    for _ in range(30):
        if not ev("!!document.querySelector('.dlg')"): break
        if ev("!!document.querySelector('.dlg .chs button')"): pg.locator('.dlg .chs button').last.click(); W(1100)
        else: pg.locator('.dlg .box').last.click(); W(160)
    ok('T13 soothing only once per stop', T()==max(0,t0-12))
    ok('T14 below 50 → re-scan allows departure', T()<50)
    ev("state.currentCarriage='cab';render()"); W(400); r=scan(); ready(); L=report()
    ev("discPanel()"); W(500); ev("document.querySelector('#dgo').click()"); W(7000)
    for _ in range(8):
        if ev("!!document.querySelector('.cine')"): ev("document.querySelector('.cine').click()"); W(300)
    ok('T15 dragon grants departure after purification', ev("state.currentPhase")=='voyage', r[:2])
    ok('T16 crossing to 月界 adds +10', abs(ev("state.spirit.taint")-(r[0]+10))<=1, (r[0],T()))
    for _ in range(8):
        if not ev("!!document.querySelector('.cine')"): break
        pg.mouse.click(640,360); W(300)
    ev("closeAll()"); W(300)
    ev("state.passengers.sola={stage:1,talks:1,records:[],aboard:true,left:false,boardedJourney:1};state.spirit.taint=20;state.voyage.to='dawnForest';voyageArrive()"); W(500)
    ok('T17 arrival in 日界: lost passenger +3, dawn light −8', T()==15, T())
    for _ in range(10):
        if not ev("!!document.querySelector('.cine,.dlg,.board')"): break
        pg.mouse.click(640,360); W(400)
    ev("closeAll()"); W(200)
    t0=T(); ev("INTERACT['obs:anomaly']()"); W(300); ok('T18 space anomaly +8', T()==t0+8); ev("closeAll()")
    ev("journeyPanel()"); W(400); ok('T19 journal tags purification', ev("document.querySelectorAll('.jlog li.lk-purify').length")>=3)
    pg.screenshot(path=S+'/taint_log.png'); ev("closeAll()")
    ev("state.spirit.taint=35;render()"); W(300); pg.screenshot(path=S+'/taint_mild.png')
    ok('T20 no errors', not errs, errs)
    b.close()
