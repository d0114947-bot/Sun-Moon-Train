# 試玩報告的七項改善
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE="document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();state=freshState();state.introDone=true;state.prologueDone=true;state.storyFlags.metDragon=1;state.storyFlags.dutyLearned=1;state.storyFlags.sealSeen=1;state.currentPhase='docked';state.carSeen=['cab','memory','nature','habitat','observation'];state.annSeen='x';"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.LOCK_TEST=1"); pg.goto('http://127.0.0.1:8766/'); W(1000)
    clean=lambda: ev("closeAll();document.querySelectorAll('#layer .dlg,#layer .cine,.cpop').forEach(e=>e.remove())")
    def talk(ms=15000):
        t=0
        while t<ms:
            if ev("!!document.querySelector('#layer .cine')"): ev("document.querySelector('#layer .cine').click()")
            elif ev("!!document.querySelector('#layer .dlg')"): ev("document.querySelector('#layer .dlg .box')?.click();document.querySelector('#layer .dlg')?.click()")
            else:
                W(400); t+=400
                if not ev("!!document.querySelector('#layer .dlg,#layer .cine')"): return
            W(200); t+=200
    # ① 曦淵的故事
    ok('L1 four stories, the last one at journey 4', ev("DRAGON_LORE.length")==4 and ev("(state=freshState(),state.journeyCount=4,DRAGON_LORE.every(x=>x.need()))"))
    ev(BASE+"state.journeyCount=2;state.currentLocation='dawnForest';state.currentCarriage='cab';state.duty.reported=true;state.storyFlags.dragonLore=['dl_wall'];save();PANO.active=null;RUNNING=true;render()"); W(900); talk(); clean()
    ok('L2 docked after reporting: the dragon glows (story waiting)', ev("hsState(HSDEF.find(h=>h.id==='cab-dragon'))")=='important')
    ev("dragonTalk()"); talk(); ok('L3 story told while docked', 'dl_ferry' in ev("state.storyFlags.dragonLore"))
    ok('L4 goal says how to hear it', '曦淵' in ev("mainQuest().find(x=>x.k==='lore').t"))
    # ② 小目標
    ev("state.storyFlags.dragonLore=['dl_wall','dl_ferry'];state.journeyCount=2;render()"); W(400)
    ok('S1 waiting for the next story: a small goal for this trip', '小目標' in ev("goalNow().sub"), ev("JSON.stringify(goalNow())"))
    # ③ 棲息車廂
    ev(BASE+"state.journeyCount=8;state.currentLocation='starIslands';state.currentCarriage='habitat';state.hview=0;"+"".join([f"state.discoveredLifeforms.push('{x}');state.passengers['{x}']={{stage:1,talks:0,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS['{x}'].zone}};" for x in ['felinia','leviathaurora','cinder','pyro','vandora','frost']])+"save();render()"); W(1200); talk(); clean(); W(300)
    n=ev("[...document.querySelectorAll('#scene [data-hs^=hab-p-].st-important,#scene [data-hs^=rm-p-].st-important')].length")
    ok('H1 at most two passengers glow at once', n<=2, n)
    # ④ 值勤交給曦淵
    ev(BASE+"state.journeyCount=5;state.currentLocation='starIslands';state.routeNext='dawnForest';state.currentCarriage='cab';save();render()"); W(900); talk(); clean()
    if ev("wallLv(nextStop())")=='亂流': ev("state.journeyCount=6;render()")
    ev("dragonTalk()"); talk(); W(300)
    ok('D1 the dragon offers to do the duty', ev("!!document.querySelector('.cpop')"))
    ev("document.querySelector('.cpop .cpop-y').click()"); W(600); talk()
    ok('D2 one tap: all duty done', ev("state.duty.scan&&state.duty.briefing&&state.duty.signal&&state.duty.doors&&state.duty.reported"))
    ok('D3 waits shortened', ev("SIG_WHY.map(x=>x.sec).join(',')")=='10,25,20,18,0')
    # ⑤ 紀念品
    ok('K1 six keepsakes for the ending', ev("END_KEEPS")==6)
    # ⑥ 廣播延後、危機面板
    ev("document.querySelector('#announce')?.remove();ANN.q=null;dialogueScript([['self','測試']]);announceNow('測試廣播')"); W(1200); ok('A1 announcement waits for the dialogue', not ev("!!document.querySelector('#announce.on')")); talk(); W(1500); ok('A2 then plays', ev("!!document.querySelector('#announce.on')"))
    ev("state.crisis={id:'T01',stage:'W2',intel:0,acts:[],prep:{},reduce:0};"); ok('C1 first anomaly: observe / ask only', ev("crActList()")==['observe','ask'])
    ev("state.crisis=null")
    # ⑦ 天象
    ok('K2 sky window longer', ev("SKY_WIN")==0.35)
    ok('Z no page errors', not errs, errs)
    print('ALL PASS' if all(R) else 'SOME FAIL', len(R))
