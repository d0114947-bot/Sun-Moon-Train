from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(200)
    ev("closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.journeyCount=8;state.currentLocation='dawnForest';state.discoveredLifeforms=['lumi','titan'];for(const id of ['lumi','titan']) state.passengers[id]={stage:2,talks:3,records:[],aboard:true,left:false,boardedJourney:2};state.currentCarriage='habitat';render()"); W(2500)
    for _ in range(40):
        if ev("!!document.querySelector('.dlg')"):
            if ev("!!document.querySelector('.dlg .chs button')"): pg.click('.dlg .chs button')
            else: pg.click('.dlg .box')
        W(300)
    print('int done',ev("done('int_titan_lumi')"),'mem',ev("MEMORIES.find(m=>m.id==='int_titan_lumi').have()"))
    print('care',ev("CARE.titan&&suits('titan','moss')"), ev("zoneEnv('moss')"))
    print('idle',ev("idleLine?idleLine('titan'):''") if ev("typeof idleLine==='function'") else '-')
    print('deck',ev("DECK_LINE.titan.length"),'comp',ev("Object.keys(COMP_LINE.titan)"))
    print(errs); b.close()
