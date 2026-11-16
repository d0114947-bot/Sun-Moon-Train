# 資訊減量：訊息排隊、發光上限、系統跟章節開放
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE=open('tchap.py').read().split('BASE="')[1].split('"\n')[0]
PAX="".join([f"state.discoveredLifeforms.push('{x}');state.passengers['{x}']={{stage:1,talks:1,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS['{x}'].zone}};" for x in ['felinia','leviathaurora','cinder','pyro','vandora']])
CH1="state.chap={said:{},arr:{},ended:[],shown:[1],legacy:0};"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.CHAP_TEST=1;window.INFO_TEST=1;window.LOCK_TEST=1;window.__LOG=[]")
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    ev("""['dialogueScript','senseShow','toastShow'].forEach(n=>{const o=window[n];window[n]=function(){__LOG.push([n,performance.now(),JSON.stringify(arguments[0]).slice(0,60)]);return o.apply(this,arguments)}})""")
    def drain(ms=12000):
        t=0
        while t<ms:
            if ev("!!document.querySelector('#layer .cine')"): ev("document.querySelector('#layer .cine')?.click()")
            elif ev("!!document.querySelector('#layer .dlg')"): ev("(document.querySelector('#layer .dlg .box')||document.querySelector('#layer .dlg'))?.click()")
            else:
                W(1500); t+=1500
                if not ev("!!document.querySelector('#layer .dlg,#layer .cine')"): return
            W(300); t+=300
    # ① 抵達：去過的地方不再整段五感
    ev(BASE+CH1+"state.feelSeen=['dawnForest','starIslands'];state.currentLocation='dawnForest';state.currentCarriage='cab';state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'starIslands',progress:1,evt:true,sky:null};save();PANO.active=null;RUNNING=true;render()"); W(800)
    ev("__LOG.length=0;voyageArrive()"); W(2500); drain()
    dl=[x for x in ev("__LOG") if x[0]=='dialogueScript']
    ok('I1 revisiting: no five-sense dialogue on arrival', not any('星河' in x[2] for x in dl), dl)
    ev("closeAll();state.feelSeen=[];state.currentPhase='voyage';state.voyage={from:'starIslands',to:'dawnForest',progress:1,evt:true,sky:null};__LOG.length=0;voyageArrive()"); W(2500)
    n=0
    for _ in range(30):
        if ev("!!document.querySelector('#layer .dlg')"): n+=1; ev("(document.querySelector('#layer .dlg .box')||document.querySelector('#layer .dlg'))?.click()"); W(300)
        elif ev("!!document.querySelector('#layer .cine')"): ev("document.querySelector('#layer .cine').click()"); W(300)
        else: W(600)
    dl=[x for x in ev("__LOG") if x[0]=='dialogueScript']
    ok('I2 first visit: one short senses dialogue (2 lines)', len(dl)>=1 and ev("arrSenses('dawnForest').length")==2, dl)
    # ② 念頭：說話時不出現、只留最新、隔 40 秒
    ev("closeAll();HINTQ.q=[];HINTQ.busy=false;hintNext.ls=-1e9;__LOG.length=0;dialogueScript([['self','測試一下']]);sense('（舊的念頭）');sense('（新的念頭）')"); W(1500)
    ok('I3 no thought while a dialogue is open', not [x for x in ev("__LOG") if x[0]=='senseShow'])
    drain(); W(1500)
    sh=[x[2] for x in ev("__LOG") if x[0]=='senseShow']
    ok('I4 only the newest thought is shown', sh and '新的念頭' in sh[0] and not any('舊的念頭' in x for x in sh), sh)
    W(4500); ev("sense('（第三個念頭）')"); W(3000)
    ok('I5 next thought waits (40 s gap)', not any('第三' in x[2] for x in ev("__LOG") if x[0]=='senseShow'))
    # ③ 發光上限
    ev(BASE+CH1+PAX+"state.journeyCount=3;state.storyFlags.dragonLore=[];state.currentLocation='starIslands';state.currentCarriage='cab';save();render()"); W(1200); drain(); ev("closeAll();render()"); W(600)
    g=ev("[...document.querySelectorAll('#scene [data-hs].st-important')].map(e=>e.dataset.hs)")
    raw=ev("HSDEF.filter(h=>h.scene==='cab'&&(!h.show||h.show())&&hs0State(h)==='important').map(h=>h.id)")
    ok('I6 cab: at most 2 glowing', len(g)<=2, [g,raw])
    ok('I7 cab: the glow follows the goal (duty step / dragon / disc)', g and all(x in ev("goalHsIds()") for x in g), [g,ev("goalHsIds()")])
    # 棲息區域
    ev("closeAll();state.currentCarriage='habitat';state.hview=0;render()"); W(800)
    zs=ev("[...document.querySelectorAll('#scene [data-hs^=hab-]')].map(e=>e.dataset.hs).filter(x=>/^hab-(spring|rings|moss|crystal|veil|rest)$/.test(x))")
    need=ev("['spring','rings','moss','crystal','veil','rest'].filter(zoneNeeded)")
    ok('I8 habitat: rest areas only where needed', sorted(zs)==sorted('hab-'+x for x in need) and len(zs)<6, [zs,need])
    # ④ 系統跟章節開放
    ok('I9 chapter one: telescope hidden, deck door locked, no sky events', not ev("HSDEF.find(h=>h.id==='obs-scope').show()") and ev("hsState(HSDEF.find(h=>h.id==='obs-front'))")=='locked' and ev("skyForecast('starIslands')") is None)
    ok('I10 chapter one: passengers do not ask favours yet', not ev("reqGateOk()"))
    ev("state.chap.ended=[1];state.chap.said[1]=1;state.chap.shown=[1];closeAll();state.currentCarriage='cab';render();chapCheck()"); W(1200)
    ok('I11 chapter two: card shown', '渡守的圓環' in (ev("document.querySelector('#layer .cine')?.innerText")or''))
    drain(); W(2000)
    ok('I12 chapter two: the deck and telescope open, with a note', ev("HSDEF.find(h=>h.id==='obs-scope').show()") and ev("hsState(HSDEF.find(h=>h.id==='obs-front'))")!='locked' and '展望台' in ''.join(ev("BL.map?BL.map(x=>x.t||x[1]||'').join('|'):''") if False else [ev("(state.backlog||[]).map(x=>x.t).join('|')")]), ev("(state.backlog||[]).slice(-4)"))
    ok('I13 armillary waits for chapter three', not ev("HSDEF.find(h=>h.id==='mem-armillary').show()"))
    ev(BASE+"state.storyFlags.dragonLore=['dl_wall','dl_ferry','dl_dimming','dl_name'];state.clues=['clue_dragon'];delete state.chap;state.currentLocation='dawnForest';render()"); W(600)
    ok('I14 old save: everything up to its chapter is open', ev("sysOpen(2)&&sysOpen(3)&&sysOpen(4)"))
    ok('Z no page errors', not errs, errs)
    print('ALL PASS' if all(R) else 'SOME FAIL', len(R))
