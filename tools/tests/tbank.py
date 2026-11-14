from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]; pg.on('pageerror',lambda e:errs.append(str(e.stack)[:300]))
    def drain(pick=None,n=40):
        t=[]
        for _ in range(n):
            if ev("!!document.querySelector('.cine')"): ev("document.querySelector('.cine').click()"); W(250); continue
            if not ev("!!document.querySelector('.dlg')"): break
            t.append(ev("document.querySelector('.dlg .tx')?.textContent||''"))
            if ev("!!document.querySelector('.dlg .chs button')"):
                bs=ev("[...document.querySelectorAll('.dlg .chs button')].map(b=>b.textContent)"); i=next((k for k,x in enumerate(bs) if pick and pick in x),0)
                ev(f"document.querySelectorAll('.dlg .chs button')[{i}].click()"); W(1300)
            else: ev("document.querySelector('.dlg .box').click()"); W(120)
        return t
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(300)
    base="document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.journeyCount=2;state.currentLocation='dawnForest';state.visitedLocations=['origin','dawnForest','starIslands'];state.currentPhase='docked';"
    ev(base+"state.bank=null;state.seedBag={bell:3,stardaisy:2,tidebloom:2,sunfern:1};state.grown=[];state.currentCarriage='nature';state.nview=1;render()"); W(500)
    hs=ev("[...document.querySelectorAll('#scene [data-hs]')].map(e=>e.dataset.hs)")
    ok('A1 back view: exactly two new hotspots (守望藤, 植物生命圖鑑)', 'nat-vine-b' in hs and 'nat-codex' in hs and all(h in ['nat-vine-b','nat-codex','nat-door','nature-mirror','hap-nature'] for h in hs),hs)
    ev("state.nview=0;render()"); W(300); ok('A2 front view has none of them',not any(h in ev("[...document.querySelectorAll('#scene [data-hs]')].map(e=>e.dataset.hs)") for h in ['nat-vine-b','nat-codex']))
    ok('S1 stage 1 at start',ev("bank().stage")==1)
    ev("codexPanel()"); W(500); t=ev("document.querySelector('.plantcodex').textContent")
    ok('S1b codex: basic fields only (later ones hidden)','保存需求' in t and '？？？' in t and '保存狀態' in t,t[:200]); ev("closeAll()")
    ev("seedPanel()"); W(400); ev("document.querySelector('[data-cs=\"bell\"]').click()"); W(300); ok('S1c vault shows no preservation yet',not ev("!!document.querySelector('.keep-row')")); ev("closeAll()")
    ev("vinePanel('nat-vine-b')"); W(500); ev("document.querySelector('#vt')?.click()"); W(200); ok('S1d vine opens from the back view; only basic topics',ev("[...document.querySelectorAll('[data-vt]')].map(b=>b.dataset.vt)")==['grow']); ev("document.querySelector('.vine-actor')?._bye()"); W(400)
    # stage 2 : seed loses vitality
    ev("state.journeyCount=3;state.grown=['bell'];bankArrive()"); ok('E1 a seed loses vitality (real event)',ev("!!bank().ev.lost") and ev("bank().pend")=='lost')
    lost=ev("bank().ev.lost.p"); ev("state.nview=0;render();meetHere()"); W(800); t=drain()
    ok('E1b vine explains → 認識保存',ev("bank().stage")==2 and any('種子也是活的' in x for x in t),t)
    ev("seedPanel()"); W(400); ev("document.querySelector('[data-cs=\"bell\"]').click()"); W(300); ok('S2 vault shows need + status',ev("!!document.querySelector('.keep-row')")); ev("closeAll()")
    ev("state.storyFlags.natureLight='dawn';bank().vit={};bankKeepTick()"); ok('S2b right light → better; wrong light → weaker (never lost)',ev("vitOf('bell')")==3 and ev("vitOf('tidebloom')")==1)
    ev("bankKeepTick();bankKeepTick()"); ok('S2c weakest is 衰弱, seed not destroyed',ev("vitOf('tidebloom')")==1 and ev("seedN('tidebloom')")>=1)
    ev("state.pods=[null,null,null,null];state.pods[0]={p:'tidebloom',st:0,j:3,...(bankOn(2)&&vitOf('tidebloom')<=1?{slow:1}:{})};gardenGrow()"); ok('S2d a weak seed takes one more trip to sprout',ev("state.pods[0].st")==0 and not ev("state.pods[0].slow"))
    ev("vinePanel()"); W(500); ev("document.querySelector('#vt')?.click()"); W(200); ok('S2e vine now gives preservation advice',ev("[...document.querySelectorAll('[data-vt]')].map(b=>b.dataset.vt)").count('keep')==1); ev("document.querySelector('[data-vt=\"keep\"]').click()"); W(200); ok('S2f advice is specific',ev("document.querySelector('.vine-say').textContent").find('月輝')>=0); ev("document.querySelector('.vine-actor')?._bye()"); W(400)
    # stage 3 : passenger recognises lost home plant
    ev("state.passengers.leviathaurora={stage:2,talks:2,records:[],aboard:true};state.currentCarriage='habitat';render()"); W(300)
    ok('E2 passenger recognises a vanished home plant',ev("bankHomeTry(['leviathaurora'])")); W(900); t=drain()
    ok('E2b → 跨界連結',ev("bank().stage")==3 and any('已經沒有了' in x for x in t),t)
    ev("codexPanel()"); W(500); t=ev("document.querySelector('.plantcodex').textContent"); ok('S3 codex: native environment & receivers open; delivery still hidden','原生環境' in t); ev("closeAll()")
    # stage 4 : receivers outside (existing hotspots)
    ev("state.currentPhase='outside';state.currentLocation='dawnForest';state.companion=null;render()"); W(400)
    ok('E3 古樹 glows as a possible receiver',ev("document.querySelector('[data-hs=\"out-tree\"]').className").find('st-important')>=0)
    ev("rcvAct('tree')"); W(600); t=drain(); ok('E3b first contact → commission in the notebook → 生命傳遞',ev("bank().stage")==4 and ev("bank().comm.length")==1,t)
    want=ev("bank().comm[0].p"); ev("closeAll();notebookPanel()"); W(500); ok('S4 notebook holds the commission',ev("document.querySelector('.notebook').textContent").find('植物的旅程')>=0); ev("closeAll()")
    ev(f"seedAdd('{want}',0);plantAdd('{want}',-plantN('{want}'));bank().vit['{want}']=1;state.seedBag['{want}']=1;"); ev("rcvAct('tree')"); W(500); t=drain(); ok('S4b cannot hand over a weak seed; must prepare',ev("bank().comm[0].st")=='on',t)
    ev(f"plantAdd('{want}',1);rcvAct('tree')"); W(500); ev("document.querySelector('[data-give=\"1\"]').click()"); W(900); drain()
    ok('S4c delivered in person (plant used)',ev("bank().comm[0].st")=='done' and ev(f"plantN('{want}')")==0 and ev("bank().deliv.length")==1)
    ev("state.journeyCount+=2;bankArrive()"); ok('S4d restoration news arrives later',ev("!!bank().deliv[0].news") and ev("bank().deliv[0].newsT").find('晨曦森林')>=0)
    ok('S4e world changes: plant now grows at that place',want in ev("bank().world.dawnForest") and ev(f"bankForagePool('dawnForest',[]).some(x=>x[0]==='sd:{want}')"))
    ok('S4f atlas records the restoration',ev("atlasPages().join('')").find('重新長了出來')>=0)
    # stage 5
    ev("state.currentLocation='starIslands';rcvAct('river')"); W(500); drain(); p2=ev("bank().comm[1].p"); ev(f"plantAdd('{p2}',1);rcvAct('river')"); W(500); ev("document.querySelector('[data-give=\"1\"]').click()"); W(900); drain()
    ev("bank().deliv.push({rcv:'home_felinia',loc:'dawnForest',p:'bell',j:state.journeyCount,newsJ:state.journeyCount,how:'bye'});state.journeyCount+=2;bankArrive()")
    ok('E5 ark event queued after deliveries come alive',ev("bank().pend")=='ark')
    ev("state.currentPhase='docked';state.currentCarriage='nature';state.nview=1;render();meetHere()"); W(800); t=drain(); ok('E5b → 生命方舟',ev("bank().stage")==5 and any('方舟' in x for x in t),t)
    ok('S5 endangered plants become requestable',ev("ENDANGER.length")>0 and ev("rcvWant('tree')") is not None)
    ev("codexPanel()"); W(500); t=ev("document.querySelector('.plantcodex').textContent"); ok('S5b codex shows restoration results',('復育成果' in t) and ('還沒有消息' in t or '新葉' in t)); ev("closeAll()")
    # save/load
    ev("save()"); pg.reload(); W(900); ok('P1 everything persists',ev("(()=>{const s=load(); return s.bank.stage===5&&s.bank.deliv.length>=3&&s.bank.comm.length>=2&&Object.keys(s.bank.vit).length>0})()"))
    ev("(()=>{const s=load(); delete s.bank; localStorage.setItem(SAVE_KEY,JSON.stringify(s));})()"); pg.reload(); W(900)
    ev("state=load();RUNNING=true;document.querySelector('#mainscreen')?.remove();state.currentPhase='docked';state.currentCarriage='nature';state.nview=1;render();codexPanel()"); W(400); ev("closeAll();notebookPanel()"); W(300); ev("closeAll()")
    ok('P2 old save: starts at stage 1, nothing appears early',ev("bank().stage")==1 and not errs,errs)
    print('ALL PASS' if all(R) else 'SOME FAIL',len(R))
