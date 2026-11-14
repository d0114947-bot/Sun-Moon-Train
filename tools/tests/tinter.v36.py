from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' '+str(x) if x!='' else ''),flush=True)
PAIRS=[('int_lumi_felinia','lumi','felinia',''),('int_sola_levi','sola','leviathaurora',''),('int_cinder_pyro','cinder','pyro',''),('int_pyro_frost','pyro','frost',''),
       ('int_felinia_aelis','felinia','aelis',''),('int_vandora_aelis','vandora','aelis','voyage'),('int_sirenora_pyro','sirenora','pyro',''),('int_sirenora_levi','sirenora','leviathaurora',''),('int_titan_lumi','lumi','titan',''),('int_frost_lynx','lynx','frost',''),('int_cinder_strider','strider','cinder','')]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(900)
    ok('I0 eleven interactions, each with a memory crystal', ev("Object.keys(EVENTS).filter(k=>k.startsWith('int_')).length")==11 and ev("Object.keys(EVENTS).filter(k=>k.startsWith('int_')).every(k=>MEMORIES.some(m=>m.id===k))"))
    shot=False
    for eid,a,c,cond in PAIRS:
        ev("document.querySelector('#mainscreen')?.remove();RUNNING=true;state=freshState();normalizeState();state.introDone=true;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.storyFlags.noteTip=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=3;state.visitedLocations=['dawnForest'];"
           f"for(const id of ['{a}','{c}']){{state.discoveredLifeforms.push(id);state.passengers[id]={{stage:1,talks:0,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS[id].zone}}}}state.currentCarriage='observation';render()"); W(300)
        if cond=='voyage':
            ev("state.currentCarriage='habitat';render();checkCarriageEvents()"); W(300)
            ok(f'{eid}: not while docked', not ev(f"state.pendingEvents.includes('{eid}')"))
            ev("state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'starIslands',progress:.2,evt:true}")
        ev("state.currentCarriage='habitat';render();checkCarriageEvents()"); W(400)
        ok(f'{eid}: appears in the habitat', ev(f"state.pendingEvents.includes('{eid}')") and ev(f"!!document.querySelector('[data-act=\"event:{eid}\"]')"))
        pg.click(f'[data-act="event:{eid}"]'); W(500)
        L=ev("[...document.querySelectorAll('.dlg .who')].map(w=>w.style.left)")
        n=0
        while ev("!!document.querySelector('.dlg')") and n<30:
            if not shot and n==2: pg.screenshot(path=S+'/inter.png'); shot=True
            pg.locator('.dlg').last.click(); W(140); n+=1
        W(500)
        ok(f'{eid}: plays, logs, crystal, records', n>=6 and ev(f"MEMORIES.find(m=>m.id==='{eid}').have()") and ev("state.log.some(l=>l.k==='life')") and ev(f"state.passengers['{a}'].records.length")>=1, n)
    # same-zone condition
    ev("state=freshState();normalizeState();state.introDone=true;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=3;for(const id of ['cinder','pyro']){state.discoveredLifeforms.push(id);state.passengers[id]={stage:1,talks:0,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS[id].zone}};state.passengers.pyro.zone='rest';state.currentCarriage='habitat';render();checkCarriageEvents()"); W(300)
    ok('I9 燼風帆獸×燼角巨獸 only when they share a zone', not ev("state.pendingEvents.includes('int_cinder_pyro')"))
    ok('I10 no errors', not errs, errs)
    b.close()
