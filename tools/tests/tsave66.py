from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(c); print(('PASS ' if c else 'FAIL ')+n,x if not c else '')
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(300)
    ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();state.introDone=true;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=4;state.duty=dutyFresh();state.duty.mic=1;state.duty.sigAt=Date.now()+40000;")
    ev("state.delay={key:stopKey(),k:'life',st:'on'};state.snailFriend=1;state.platSeen=['x'];state.voyage=null;state.passengers.felinia={stage:2,talks:0,records:[],aboard:true};state.passengers.felinia.askDone=2;state.passengers.felinia.packing=5;save()")
    sf0=ev("state.snailFriend"); ev("delayDone('t');delayDone('t')"); ok('S1 delayDone is idempotent',ev("state.delay.st")=='done')
    ok('S2 finished delay hides its hotspot',not ev("delayOn('life')"))
    ev("delayTick()"); ok('S3 delayTick does not recreate a finished delay at the same stop',ev("state.delay.st")=='done')
    ev("save()"); pg.reload(); W(900)
    st=ev("(()=>{const s=load(); return [s.delay&&s.delay.st,s.delay&&s.delay.k,s.snailFriend,s.platSeen.length,s.passengers.felinia.askDone,s.passengers.felinia.packing]})()")
    ok('S4 new fields survive save/load',st==['done','life',1,1,2,5],st)
    # mid-voyage asks
    ev("state=load();RUNNING=true;state.currentPhase='voyage';state.voyage={to:'starIslands',asks:[{id:'felinia',type:'deck',st:'on'}],haps:[],fin:null};save()"); pg.reload(); W(900)
    ok('S5 voyage asks survive reload',ev("load().voyage.asks[0].st")=='on')
    # legacy save: strip new fields
    ev("(()=>{const s=load(); delete s.delay; delete s.snailFriend; delete s.platSeen; delete s.voyage; s.currentPhase='docked'; for(const k in s.passengers){ delete s.passengers[k].askDone; delete s.passengers[k].packing; delete s.passengers[k].leftJ;} localStorage.setItem(SAVE_KEY,JSON.stringify(s));})()")
    pg.reload(); W(900)
    ev("state=load();RUNNING=true;document.querySelector('#mainscreen')?.remove();state.currentCarriage='habitat';render()"); W(500)
    ok('S6 legacy save: delay helpers work',ev("delayOn()")==False and ev("(delayTick(),true)"))
    ev("whoPanel()"); W(300); ok('S7 legacy save: who panel opens',ev("!!document.querySelector('.whoov')")); ev("closeAll()")
    ev("prepPanel()"); W(300); ok('S8 legacy save: prep panel opens',ev("!!document.querySelector('.prepov')")); ev("closeAll()")
    ev("state.currentCarriage='cab';render()"); W(400); ok('S9 cab-scan still opens the 淨界晶環 (not prep)',(ev("act('prep','scan'),!!document.querySelector('.scanov')")))
    ok('S10 no page errors',not errs,errs)
    print('ALL PASS' if all(R) else 'SOME FAIL',len(R))
