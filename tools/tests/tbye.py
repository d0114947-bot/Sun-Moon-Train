from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    def drain(pick=None,n=40):
        seen=[]
        for _ in range(n):
            if ev("!!document.querySelector('.cine')"): ev("document.querySelector('.cine').click()"); W(250); continue
            if not ev("!!document.querySelector('.dlg')"): break
            t=ev("document.querySelector('.dlg .tx')?.textContent||''"); seen.append(t)
            if ev("!!document.querySelector('.dlg .chs button')"):
                bs=ev("[...document.querySelectorAll('.dlg .chs button')].map(b=>b.textContent)")
                i=next((k for k,x in enumerate(bs) if pick and pick in x),len(bs)-1)
                ev(f"document.querySelectorAll('.dlg .chs button')[{i}].click()"); W(1400); pick=None
            else: ev("document.querySelector('.dlg .box').click()"); W(120)
        return seen
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(300)
    base="document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.visitedLocations=['dawnForest','starIslands'];state.carSeen=Object.keys(CAR_INTRO);window.readyToLeave=()=>true;"
    ev(base+"state.journeyCount=1;state.currentLocation='dawnForest';state.currentPhase='docked';state.currentCarriage='habitat';"
       "state.passengers.felinia={stage:2,talks:PASSENGERS.felinia.talks.length,records:[],aboard:true,boardedJourney:0,outings:['dawnForest']};"
       "state.passengers.aelis={stage:2,talks:PASSENGERS.aelis.talks.length,records:[],aboard:true,boardedJourney:0};render()"); W(400)
    ok('O1 near leaving: signs start (no progress bar)',ev("nearLeave('felinia')") and ev("omenTry('felinia')"))
    W(800); t=drain(); ok('O2 sign is personal (asks about next stop / home)',any('山' in x or '下一站' in x for x in t),t)
    ok('O3 at most one sign per journey',not ev("omenTry('felinia')"))
    ok('O4 different passengers, different signs',ev("OMEN.felinia.m!==OMEN.aelis.m&&Object.keys(OMEN).length===23"))
    # ready but at a stop that is not hers
    ev("state.journeyCount=2;state.currentLocation='starIslands';state.hiddenFound={df_canopy:{j:1,loc:'dawnForest',who:'felinia'}};byeSync();render()"); W(300)
    ok('P1 ready → homeward prep state',ev("state.passengers.felinia.bye&&state.passengers.felinia.bye.st")=='prep')
    ok('P2 not her place → no farewell queued here',not ev("leaveOKAt('felinia','starIslands')") and ev("leaveOKAt('felinia','dawnForest')"))
    ev("packTry('felinia')"); W(800); t=drain(); ok('P3 packing scene mentions her keepsake',any('浮羽' in x for x in t),t)
    ev("talk('felinia')"); W(600); t=drain(pick='回憶水晶')
    ok('P4 last talk recaps real records (rides, outing, hidden spot)',any('趟車' in x for x in t) and any('樹冠上的花' in x for x in t),t)
    ok('P5 memory crystal prepared',ev("state.passengers.felinia.bye.mem===1&&memsHave().some(m=>m.id==='trip_felinia')"))
    ev("plantAdd('bell',1);talk('felinia')"); W(600); drain(pick='植物'); W(500)
    ev("document.querySelector('[data-bg]')&&document.querySelector('[data-bg]').click()"); W(700); drain()
    ok('P6 gift a plant (optional)',ev("state.passengers.felinia.bye.gift")=='bell')
    ev("talk('felinia')"); W(600); drain(pick='界域地誌'); ok('P7 written into the atlas',ev("state.passengers.felinia.bye.atlas")==1)
    ev("talk('felinia')"); W(600); drain(pick='展望台'); W(300)
    ok('P8 stars: she goes to the deck',ev("state.passengers.felinia.place")=='deck')
    ev("state.currentCarriage='observatory';render()"); W(300); ev("meetHere()"); W(900); t=drain()
    ok('P9 last starry sky together',ev("state.passengers.felinia.bye.stars")==1,t)
    ev("state.passengers.felinia.place=undefined;state.currentCarriage='habitat';complete('int_felinia_aelis');render()"); W(300)
    ok('C1 bond-based goodbye between passengers',ev("pairByeTry('felinia')")); W(800); t=drain()
    ok('C2 their own words',any('地下的心跳' in x for x in t) and ev("state.passengers.felinia.bye.pairs.includes('aelis')"),t)
    ok('C3 no bond → no pair goodbye',ev("bondsOf('felinia').length")==1 and not ev("pairByeTry('felinia')"))
    # reload in the middle of leaving
    ev("state.currentLocation='dawnForest';state.journeyCount=3;save();farewell('felinia')"); W(500); pg.reload(); W(900)
    ok('R1 refresh mid-farewell: she is still aboard',ev("(()=>{const s=load(); return s.passengers.felinia.aboard&&!s.passengers.felinia.left})()"))
    ev("state=load();RUNNING=true;"+base+"state.currentPhase='docked';state.currentCarriage='habitat';state.passengers.aelis.boardedJourney=3;render();arrivalChecks()"); W(900)
    t=drain(n=80)
    ok('F1 farewell plays at her place',ev("state.passengers.felinia.left&&state.passengers.felinia.leftAt==='dawnForest'"),t[:6])
    ok('F2 farewell flow: arrival → door → her words → prepared details → friend sees off → reflection',all(any(k in x for x in t) for k in ['列車停在','車門前','山','鈴','回憶水晶','界域地誌','星星','羽貓獸的位置']),t)
    ok('F3 keepsake kept',ev("state.collectibles.includes('keep_felinia')"))
    ok('F4 codex / records / notes kept, stage 3',ev("state.passengers.felinia.records.length>5&&state.passengers.felinia.stage===3&&state.discoveredLifeforms!==undefined"))
    ok('F5 farewell memory crystal + replay button',ev("memsHave().some(m=>m.id==='bye_felinia')") and 'data-replay' in ev("MEMORIES.find(m=>m.id==='bye_felinia').text"))
    ev("document.body.insertAdjacentHTML('beforeend','<button id=rp data-replay=felinia>x</button>');document.getElementById('rp').click()"); W(700)
    ok('F6 replay plays the saved farewell',ev("!!document.querySelector('.dlg')")); drain(n=80); ev("document.getElementById('rp').remove()")
    ok('F7 atlas page records the goodbye',('在這裡道別' in ev("atlasPages().join('')")))
    ok('F8 zone trace left behind',ev("zoneTraces(PASSENGERS.felinia.zone)").find('絨羽')>=0)
    ok('F9 one-time: no second farewell',not ev("byeReady('felinia')"))
    # echoes
    ev("state.journeyCount=4;state.currentLocation='starIslands';state.echoJ=null"); ok('E1 no sign echo away from her stop',ev("echoSign()") is None)
    ev("state.journeyCount=5;state.currentLocation='dawnForest';state.echoJ=null"); f=ev("!!echoSign()"); ok('E2 sign echo at her stop, once',f and ev("echoSign()") is None)
    ev("state.journeyCount=6;state.echoJ=null;state.currentCarriage='habitat';render()"); W(300)
    ok('E3 friend mentions her',ev("echoFriend(hereList())")); W(800); t=drain(); ok('E3b',any('羽貓獸現在' in x for x in t),t)
    ok('E4 at most one echo per journey',not ev("echoFriend(hereList())"))
    ev("state.journeyCount=7;state.echoJ=null;state.currentPhase='voyage';state.voyage={to:'starIslands',haps:[],progress:.3};state.currentCarriage='observation';"); ok('E5 star echo while voyaging',ev("echoStar()"))
    ev("state.journeyCount=8;state.echoJ=null;state.currentPhase='outside';state.currentLocation='dawnForest';state.companion=null;render()"); ok('E6 trace echo where you found a place together',ev("echoTrace()"))
    # late fallback & legacy
    ev("state.passengers.pyro={stage:2,talks:9,records:[],aboard:true,boardedJourney:0};state.journeyCount=4"); ok('L1 not stuck: after stay+3 rides any stop works',not ev("leaveOKAt('pyro','starIslands',2)") and ev("leaveOKAt('pyro','starIslands',5)"))
    ev("state.passengers.sola={stage:3,talks:3,records:[],aboard:false,left:true}"); ok('L2 legacy farewell (no saved script) still viewable',ev("byeLines('sola').length")==3 and 'data-replay' in ev("MEMORIES.find(m=>m.id==='bye_sola').text"))
    ev("save()"); pg.reload(); W(900)
    ok('S1 bye state survives reload',ev("(()=>{const s=load(),B=s.passengers.felinia.bye; return B.st==='gone'&&B.gift==='bell'&&B.script.length>8&&s.storyFlags.echo_sign_felinia===1})()"))
    ok('Z no page errors',not errs,errs)
    print('ALL PASS' if all(R) else 'SOME FAIL',len(R))
