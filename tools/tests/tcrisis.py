from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    def drain(n=30):
        t=[]
        for _ in range(n):
            if not ev("!!document.querySelector('.dlg')"): break
            t.append(ev("document.querySelector('.dlg .tx')?.textContent||''")); ev("document.querySelector('.dlg .box').click()"); W(120)
        return t
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("window.CRISIS_TEST=1;startNew()"); W(300)
    base="document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.journeyCount=8;state.currentLocation='dawnForest';state.currentPhase='docked';state.currentCarriage='cab';state.duty=dutyFresh();state.trainTaint=30;state.energy=80;state.crisis=null;state.crHist=[];state.crLast={};state.crCalm=null;state.crChain=[];state.repairs=[];state.trainSt=null;state.sealed=[];state.carPol={};state.disaster=null;state.materials={mosslight:3,stardust:3,dew:3,sand:3,pollen:3};"
    P=lambda d: ";".join(f"state.passengers.{i}={{stage:{s},talks:1,records:[],aboard:true}}" for i,s in d.items())
    ok('D0 database: 20 events, one shared format',ev("Object.keys(CRISES).length")==20 and ev("Object.values(CRISES).every(E=>E.n&&E.cat&&E.sev&&E.prev&&E.eff&&E.out&&E.dmg&&E.pax&&'lead' in E&&E.cd)"))
    # 1 storm avoided by observation
    ev(base+P({'aelis':2})+";render();crStart('A01',{real:true,sev:2})"); 
    ok('1a W1: only a subtle feeling, no hotspot/name',ev("state.crisis.stage")=='W1' and not ev("crVisible()"))
    ev("crNode('arrive')"); ok('1b next node → W2: sign appears in the observation car',ev("state.crisis.stage")=='W2' and ev("crVisible()") and ev("HSDEF.find(h=>h.id==='cr-observation').show()"))
    acts=ev("crActList().map(a=>a.k)"); ok('1c judgement unclear → only general options shown',('core' not in acts) and ('route' in acts))
    ev("crDo('observe')"); ev("crDo('ask')"); ok('1d investigation + passenger intel identifies it',ev("state.crisis.intel")==3)
    t0=ev("trainT()"); r=ev("crDo('route')"); ok('1e change route → storm avoided, no damage',ev("state.crisis")==None and ev("trainT()")==t0 and ev("state.crHist.slice(-1)[0].res")=='avoid' and ev("trainStatus().run")=='normal',r)
    # 2 ignore predator signs → attacked
    ev(base+P({'frost':2,'pyro':2})+";crStart('B01',{real:true,sev:3});crNode('arrive');crNode('depart');crNode('arrive')")
    ok('2a ignored warnings escalate to W4',ev("state.crisis.stage")=='W4')
    ev("state.currentPhase='voyage';state.voyage={to:'starIslands',from:'dawnForest',progress:.6,haps:[]};crVoyTick(state.voyage)"); W(600); drain()
    ok('2b outbreak during the voyage; voyage cannot finish until handled',ev("!!state.crisis.burst") and ev("voyTasksLeft(state.voyage)"))
    t0=ev("trainT()"); res=ev("crResolve()"); ok('2c doing nothing → real damage (taint up, train hurt)',res['res'] in ('fail','part') and ev("trainT()")>t0 and len(res['lines'])>0,res); ev("closeAll()")
    # 3 check core early → no stop
    ev(base+"crStart('C01',{real:true,sev:2});crNode('arrive')"); ev("crDo('observe');crDo('observe')"); m0=ev("matCount('mosslight')")
    r=ev("crDo('core')"); ok('3 checked the energy core in time → avoided, train keeps running (uses moss-light)',ev("state.crisis")==None and ev("trainStatus().run")=='normal' and ev("matCount('mosslight')")==m0-1,r)
    # 4 missed pollution spreads
    ev(base+"state.pods=[{p:'bell',st:1},{p:'sunfern',st:0},null,null];crStart('D02',{real:true,sev:2});crNode('arrive');crNode('depart');crNode('arrive');")
    ok('4a unnoticed plant contamination breaks out on its own',ev("!!state.crisis.burst")); W(400); drain(); res=ev("crResolve()")
    ok('4b local pollution recorded separately from global',ev("(state.carPol.nature||0)")>0 and ev("trainT()")!=ev("state.carPol.nature"),[ev("state.carPol"),ev("trainT()")])
    ev("state.carPol.nature=70;state.crCalm=99;state.sealed=[]"); g0=ev("trainT()"); ev("crNode('depart')"); ok('4c heavy local pollution spreads (global + neighbours)',ev("trainT()")>g0 and ev("(state.carPol.memory||0)+(state.carPol.habitat||0)")>0)
    ok('4d plants damaged but not wiped out',ev("state.pods.filter(Boolean).length")==2); ev("closeAll()")
    # 5 passenger proactive report
    ev(base+P({'aelis':2})+";crStart('A02',{real:true,sev:2});state.currentCarriage='habitat';render()")
    ok('5 passenger brings intel on its own',ev("crPaxReport(['aelis'])") and ev("state.crisis.intel")>=2); W(800); drain()
    # 6 passenger refuses
    ev(base+P({'frost':2,'pyro':3})+";state.journeyCount=9;crStart('B05',{real:true,sev:3});")
    r=ev("crAskPax('frost')"); ok('6 a frightened passenger refuses — no relationship penalty',r['k']=='refuse' and ev("state.passengers.frost.stage")==2,r)
    r=ev("crAskPax('pyro')"); ok('6b a trusting fighter steps in',r['k'] in ('active','agree'),r)
    # 7 xiyuan
    ok('7a 曦淵 available for a major attack',ev("crActList().some(a=>a.k==='xiyuan'&&!a.why)"))
    s0=ev("crScore()"); ev("crDo('xiyuan')"); ok('7b 曦淵 helps but is not an instant win',ev("crScore()")>s0 and ev("crScore()")<ev("2+state.crisis.sevN*1.5")+6)
    res=ev("crResolve()"); ev(base+"state.crXiJ=state.journeyCount;crStart('B05',{real:true,sev:3})"); ok('7c afterwards 曦淵 needs to recover (cannot every time)',ev("crActList().find(a=>a.k==='xiyuan').why")!=None)
    # 8 stopped train repaired
    ev(base+"crStart('C01',{real:true,sev:3});state.crisis.stage='W4';state.crisis.burst=1;"); res=ev("crResolve()")
    ok('8a failure → emergency stop, departure blocked',ev("trainStatus().run")=='stop' and ev("!!crBlockDepart()"),res)
    n=ev("state.repairs.length"); ok('8b aftermath list (needs real actions & materials)',n>=1)
    for i in range(n): ev(f"crRepair({i})")
    ok('8c repairs done → normal running again',ev("trainStatus().run")=='normal' and not ev("crBlockDepart()"))
    # 9 100% disaster
    ev(base+P({'aelis':2,'treeling':2})+";state.trainTaint=100;state.carPol={nature:80,memory:50};crNode('arrive')"); W(700); drain()
    ok('9a 100% → rescue state, not game over',ev("state.disaster&&state.disaster.st")==1 and ev("trainStatus().run")=='stop' and ev("state.passengers.aelis.aboard"))
    ev("crDisAct('go')"); ev("crDisAct('go')"); ev("crDisAct('go')")
    ok('9b staged rescue with passengers (find → purify → stabilise)',ev("state.disaster.st")==4 and ev("trainT()")<100)
    for i in range(ev("state.repairs.length")): ev(f"state.materials.pollen=3;crRepair({i})")
    ok('9c after repairs the emergency ends',ev("!state.disaster") and ev("trainStatus().run")=='normal')
    # 10/11 calm + no repeat
    ev(base+"crStart('A04',{real:true,sev:1});state.crisis.stage='W4';state.crisis.burst=1;crResolve();")
    ok('10 after a crisis, normal travel resumes',ev("state.crisis")==None)
    ok('11 same event not rolled again inside its cooldown',ev("(()=>{ for(let i=0;i<200;i++){ if(crPick('depart')==='A04') return false; } return true; })()"))
    ev(base+"state.crisis=null;state.crLast={S2:8};"); ok('11b severity gap respected',ev("(()=>{ for(let i=0;i<200;i++){ const id=crPick('depart'); if(id&&crSevOf(CRISES[id])===2) return false; } return true; })()"))
    # false alarm
    ev(base+"crStart('D02',{real:false});crNode('arrive');crDo('observe');crDo('observe')"); ok('F misleading sign: cheap investigation reveals a natural phenomenon',ev("state.crisis")==None and ev("state.crHist.slice(-1)[0].res")=='false')
    # disabled options with reasons, sealed car
    ev(base+"state.materials={};crStart('C05',{real:true,sev:2});crNode('arrive');crDo('observe');crDo('observe')")
    a=ev("crActList().find(a=>a.k==='regulate')"); ok('O inapplicable action shown disabled with reason',a and a['why'],a)
    ev("crDo('isolate')"); ev("state.currentCarriage='nature';state.nview=0;render()"); W(300)
    ev("state.carPol={nature:70};state.sealed=['nature'];state.crCalm=99;crNode('depart')"); ok('S0 sealing a car stops its pollution from spreading to neighbours',not ev("(state.carPol.memory||0)+(state.carPol.habitat||0)"))
    ev("state.carPol={nature:20};state.crCalm=null")
    ok('S sealed carriage: functions paused with a message',ev("hsState(HSDEF.find(h=>h.id==='nat-pod-a'))")=='locked' and '封鎖' in ev("HSDEF.find(h=>h.id==='nat-pod-a').lock()"))
    ev("closeAll();state.currentCarriage='cab';render();cabCore()"); W(500); ok('UI crisis panel opens from the existing core crystal',ev("!!document.querySelector('.crov')")); ev("closeAll()")
    W(500); ev("crRecord('part',['溫室暫時封鎖'],4)"); ev("notebookPanel()"); W(800); print('DBG',ev("[state.crHist.length,[...document.querySelectorAll('#layer .ov')].map(o=>o.className).join('|')]")); ok('N history lives in the notebook',ev("document.querySelector('.notebook')?.textContent||document.body.textContent").find('危機紀錄')>=0); ev("closeAll()")
    # 12 reload
    ev("save()"); pg.reload(); W(900)
    print('DBG12',ev("(()=>{const s=load(); return [s.crisis&&s.crisis.id,s.crisis&&s.crisis.intel,s.sealed,s.crHist&&s.crHist.length]})()"))
    ok('12 crisis state survives reload',ev("(()=>{const s=load(); return s.crisis&&s.crisis.id==='C05'&&s.crisis.intel>=2&&s.sealed.includes('nature')&&s.crHist.length>=1&&s.crHist[0].acts.length>=2})()"))
    ev("(()=>{const s=load(); ['crisis','crHist','crLast','crCalm','crChain','repairs','trainSt','sealed','carPol','disaster','energy','crXiJ','crS4ok'].forEach(k=>delete s[k]); localStorage.setItem(SAVE_KEY,JSON.stringify(s));})()"); pg.reload(); W(900)
    ev("window.CRISIS_TEST=1;state=load();RUNNING=true;document.querySelector('#mainscreen')?.remove();state.currentPhase='docked';state.currentCarriage='cab';render();cabCore();crNode('arrive')"); W(400); ev("closeAll()")
    ok('L old save loads with the crisis system',not errs,errs)
    print('ALL PASS' if all(R) else 'SOME FAIL',len(R))
