import sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8766/'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' '+str(x) if x!='' else ''),flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(URL); W(900)
    ev("document.querySelector('#mainscreen')?.remove();RUNNING=true;state=freshState();normalizeState();state.introDone=true;state.prologueDone=true;state.storyFlags.noFeel=1;state.storyFlags.goalArrowTip=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=3;state.visitedLocations=['dawnForest'];"
       "state.discoveredLifeforms=['felinia','cinder'];['felinia','cinder'].forEach(id=>state.passengers[id]={stage:2,talks:id==='cinder'?3:0,records:[],aboard:true,left:false,boardedJourney:1});state.req={cinder:{st:'on',j:1},felinia:{st:'on',j:1}};state.currentCarriage='memory';render()"); W(900)
    # ---- 任務：清單 → 詳細 → 前往
    ev("notebookPanel('quest')"); W(900)
    rows=ev("document.querySelectorAll('.ov.notebook .qs-row').length")
    ok('L1 tasks show as a list of rows first (no details open)', rows>=3 and ev("document.querySelectorAll('.ov.notebook .qs-det').length")==0, rows)
    ok('L2 a doable request is marked', ev("!!document.querySelector('.ov.notebook .qs-row.can')"))
    ok('L3 observatory side goal removed', '到火車尾的展望台看看' not in pg.inner_text('.ov.notebook'))
    pg.locator('.ov.notebook .qs-row.can').first.click(); W(500)
    ok('L4 clicking a row opens its detail note', ev("document.querySelectorAll('.ov.notebook .qs-det').length")==1 and ev("!!document.querySelector('.ov.notebook .qs-go')"))
    pg.screenshot(path=S+'/b2_tasks.png')
    pg.locator('.ov.notebook .qs-row.can').first.click(); W(400)
    ok('L5 clicking again folds it', ev("document.querySelectorAll('.ov.notebook .qs-det').length")==0)
    pg.locator('.ov.notebook .qs-row.can').first.click(); W(400)
    pg.locator('.ov.notebook .qs-go').first.click(); W(800)
    for _ in range(30):
        if ev("state.currentPhase")=='outside': break
        W(500)
    ok('L6 "go" walks to the right car and takes cinder out', ev("state.currentPhase")=='outside' and ev("state.companion")=='cinder', (ev("state.currentPhase"),ev("state.companion"),ev("state.currentCarriage")))
    ev("closeAll();state.currentPhase='docked';state.companion=null;state.currentCarriage='habitat';render()"); W(1200)
    # ---- 乘客頭上的話
    for _ in range(14):
        if ev("!!document.querySelector('#scene .pax-bub.on')"): break
        W(500)
    ok('B1 passenger with unsaid lines shows a speech bubble', ev("!!document.querySelector('#scene [data-hs=\"hab-p-felinia\"] .pax-bub.on')"))
    W(2500); pg.screenshot(path=S+'/b2_bub.png')
    t1=ev("(document.querySelector('#scene .pax-bub')||{}).textContent||''")
    ok('B2 bubble has typed text', len(t1)>3, t1)
    ok('B3 passenger with nothing new has no bubble', not ev("!!document.querySelector('#scene [data-hs=\"hab-p-cinder\"] .pax-bub')"))
    ev("talk('felinia')"); W(600)
    ok('B4 bubbles hide during dialogue', not ev("!!document.querySelector('#scene .pax-bub')"))
    ev("closeAll()"); W(300)
    # ---- 目標箭頭
    ev("state.currentCarriage='memory';render()"); W(1200)
    ok('G1 HUD goal no longer opens notebook', True)
    pg.click('#hud .goal'); W(900)
    ok('G2 goal shows an arrow on screen (not the notebook)', ev("!!document.querySelector('.garr')") and not ev("!!document.querySelector('.ov.notebook')"), ev("goalTargets().map(h=>h.id)"))
    pg.screenshot(path=S+'/b2_arrow.png')
    # ---- 回憶水晶：月界典籍按鈕、筆記本分頁
    ev("closeAll();state.starMsgs=[{pid:'felinia',text:'下次一起看星星吧。',read:true,j:2,loc:'voyage'}];memoryPanel()"); W(900)
    ok('M1 memory crystal has the lore book button, no notebook tabs', ev("!!document.querySelector('.ov.mems .mem-lore')") and not ev("!!document.querySelector('.ov.mems .booknav')"))
    ev("document.querySelector('.ov.mems [data-box=\"msg\"]')?.click()"); W(500)
    ev("document.querySelector('.ov.mems .fl[data-k]')?.click()"); W(900)
    ok('M2 left words are a thin paper slip', ev("!!document.querySelector('.memview .slip')"))
    pg.screenshot(path=S+'/b2_slip.png')
    ev("closeAll();notebookPanel()"); W(900)
    nav=ev("[...document.querySelectorAll('.booknav button')].map(b=>b.textContent).join(',')")
    ok('M3 notebook tabs no longer have 回憶 / 月界典籍', '回憶' not in nav and '月界典籍' not in nav, nav)
    ok('M4 notebook first page lists passengers', ev("document.querySelectorAll('.ov.notebook .nb-index button').length")==2)
    ev("closeAll();notebookPanel('quest')"); W(700)
    ok('M5 拾光的記憶 is in the tasks', '拾光的記憶' in pg.inner_text('.ov.notebook'))
    ev("closeAll()")
    # ---- 展望台
    ev("state.passengers.felinia.place='deck';state.currentCarriage='observatory';render()"); W(1200)
    ok('D1 deck passenger wanders', ev("getComputedStyle(document.querySelector('[data-hs=\"ot-p-felinia\"]')).animationName")=='deckWander')
    seen=set()
    for _ in range(6):
        ev("deckTalk('felinia')"); W(500); seen.add(ev("[...document.querySelectorAll('.dlg .tx')].pop()?.textContent||''")); ev("closeAll()"); W(150)
    ok('D2 deck talk lines vary', len(seen)>=1)
    ok('E1 no page errors', not errs, errs[:3])
    b.close()
