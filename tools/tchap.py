# 劇情章節
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE="document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();state=freshState();state.introDone=true;state.prologueDone=true;state.storyFlags.metDragon=1;state.storyFlags.dutyLearned=1;state.storyFlags.sealSeen=1;state.currentPhase='docked';state.carSeen=['cab','memory','nature','habitat','observation'];state.annSeen='x';state.visitedLocations=['dawnForest','starIslands'];state.discoveredLifeforms=['sola'];state.passengers.sola={stage:2,talks:3,records:[],aboard:false,left:true};"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)+' '+str(e.stack)[:300]))
    pg.add_init_script("window.CHAP_TEST=1"); pg.goto('http://127.0.0.1:8766/'); W(1000)
    def cinetext():
        return pg.inner_text('#layer .cine') if ev("!!document.querySelector('#layer .cine')") else ''
    def drain(ms=20000):
        t=0; seen=[]
        while t<ms:
            if ev("!!document.querySelector('#layer .cine')"): seen.append(cinetext()); ev("document.querySelector('#layer .cine').click()")
            elif ev("!!document.querySelector('#layer .dlg')"):
                tx=pg.inner_text('#layer .dlg'); seen.append(tx)
                if seen.count(tx)>3: ev("document.querySelector('#layer .dlg').remove()"); continue
                ev("document.querySelector('#layer .dlg .box')?.click();document.querySelector('#layer .dlg')?.click()")
            elif ev("!!document.querySelector('#layer .board')"): ev("document.querySelector('#layer .board #hi')?.click()")
            else:
                W(500); t+=500
                if not ev("!!document.querySelector('#layer .dlg,#layer .cine,#layer .board')"): W(1200); t+=1200
                if not ev("!!document.querySelector('#layer .dlg,#layer .cine,#layer .board')"): return seen
            W(150); t+=150
        return seen
    ev(BASE+"state.currentLocation='starIslands';state.currentCarriage='cab';save();PANO.active=null;RUNNING=true;render()"); W(1500)
    ok('C1 chapter one title card', '界壁的另一邊' in cinetext() and '第一章' in cinetext(), cinetext())
    drain()
    ok('C2 goal names the chapter', '第一章' in ev("goalNow().sub") and '晨曦森林' in ev("goalNow().t"), ev("JSON.stringify(goalNow())"))
    ok('C3 only the first story is ready', ev("loreNext()&&loreNext().id")=='dl_wall')
    x4=ev("Array.from({length:40},()=>rollBoarders()).flat()");ok('C4 heroes never board at random', all(not x.startswith('board_treeling') for x in x4), x4)
    # 航行：聽故事
    ev("state.currentPhase='voyage';state.voyage={from:'starIslands',to:'dawnForest',progress:.4,evt:true,sky:null};render()"); W(400)
    ok('C5 during the voyage the goal is the dragon story', '曦淵' in ev("goalNow().t+goalNow().sub"), ev("JSON.stringify(goalNow())"))
    ev("dragonTalk()"); drain()
    ok('C6 story heard', 'dl_wall' in ev("state.storyFlags.dragonLore"))
    ev("state.voyage.progress=1;voyageArrive()"); drain()
    ok('C7 arrival: the chapter hero waits to board', ev("state.chap.arr[1]===1") and 'chb_1' in ev("state.boardQ||[]"), ev("JSON.stringify([state.chap,state.boardQ])"))
    ev("closeAll();state.currentCarriage='habitat';state.hview=0;render();checkCarriageEvents()"); W(800); seen=drain(); seen0=seen
    ok('C8 the hero boards with the chapter line', ev("aboard('treeling')") and any('老樹' in x for x in seen), seen[:2])
    ok('C9 the hero glows', ev("hsState(HSDEF.find(h=>h.id==='hab-p-treeling'))")=='important')
    seen=drain()
    ok('C10 hero tells the chapter story', any('界壁' in x for x in seen0) and ev("state.chap.said[1]===1"), seen[:3])
    W(1500); seen=seen0+drain()
    ok('C11 chapter end card, then chapter two card', any('第一章・完' in x for x in seen) and any('渡守的圓環' in x for x in seen), seen)
    ok('C12 the end of chapter one: ancient stage 2', ev("trainStage('ancient')")>=2)
    ok('C13 the next story opens', ev("loreNext()&&loreNext().id")=='dl_ferry')
    ok('C14 notebook lists the chapters', ev("(()=>{const m=questCats().find(x=>x.k==='main');return m.L[0].st==='done'&&m.L[0].t.includes('第一章')&&m.L.some(x=>x.t.includes('第二章'))&&m.L[m.L.length-1].st==='lock';})()"))
    # 舊存檔
    ev(BASE+"state.currentLocation='dawnForest';state.currentCarriage='cab';state.storyFlags.dragonLore=['dl_wall','dl_ferry','dl_dimming','dl_name'];state.clues=['clue_dragon'];state.unlockedLocations.push('reverseRealm','boundlessCorridor');delete state.chap;save();render()"); W(1500)
    ok('C15 old save: chapters 1–3 already done, no end cards', ev("JSON.stringify(state.chap.ended)")=='[1,2,3]' and '第三章・完' not in cinetext(), ev("JSON.stringify(state.chap)"))
    ok('C16 old save: lands on chapter four or five', ev("chapCur()") in (4,5) and ('第四章' in cinetext() or '第五章' in cinetext()), cinetext())
    drain()
    ok('C17 chapter four: read the seal first', '甲' in ev("goalNow().t") or ev("chapCur()")==5, ev("JSON.stringify(goalNow())"))
    ok('C18 parallel chapter: boundless picks chapter five', ev("(()=>{state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'boundlessCorridor',progress:.2};const c=chapCur();state.currentPhase='docked';state.voyage=null;return c;})()")==5)
    # 第四章：逆生之境
    ev("closeAll();state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'reverseRealm',progress:1,evt:true,sky:null};sqSet('a',1);voyageArrive()"); drain()
    ok('C19 arriving at reverseRealm: titan waits', 'chb_4' in ev("state.boardQ||[]") and ev("state.chap.arr[4]===1"), ev("JSON.stringify([state.boardQ,state.chap])"))
    ev("closeAll();state.currentCarriage='habitat';render();checkCarriageEvents()"); W(800); seen=drain()
    ok('C20 titan tells about the reversed light', any('倒著流的光' in x for x in seen) and ev("state.chap.said[4]===1"))
    ok('C21 goal now: wake the seed', '晨光' in ev("goalNow().t") or '窗' in ev("goalNow().t"), ev("JSON.stringify(goalNow())"))
    ev("state.seedOpen=(state.seedOpen||[]).concat('seed_ancient_a');render()"); W(1500); seen=drain()
    ok('C22 chapter four ends; nature grows', any('第四章・完' in x for x in seen) and ev("trainStage('nature')")>=2, seen[:3])
    ok('Z no page errors', not errs, errs)
    print('ALL PASS' if all(R) else 'SOME FAIL', len(R))
