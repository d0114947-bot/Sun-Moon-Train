from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' '+str(x) if x!='' else ''),flush=True)
ids=['frost','sirenora','cinder','felinia','pyro','aelis']
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(900)
    ev("document.querySelector('#mainscreen')?.remove();RUNNING=true;state=freshState();normalizeState();state.homeConsts=Object.keys(HOME_C);state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'starIslands',progress:.3,evt:true};state.currentLocation='dawnForest';state.journeyCount=3;state.visitedLocations=['dawnForest'];"
       f"for(const id of {ids}){{state.discoveredLifeforms.push(id);state.passengers[id]={{stage:id==='aelis'?1:2,talks:1,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS[id].zone}}}}state.currentCarriage='observatory';render()"); W(800)
    ok('D1 invite spot on the deck', ev("!!document.querySelector('[data-hs=\"ot-invite\"]')"))
    def inv(i):
        ev("closeAll()"); W(200); ev("deckInvite()"); W(400); pg.click(f"[data-inv=\"{i}\"]",force=True); W(400)
        for _ in range(8):   # 邀請時多了一句「一起看什麼」的台詞
            if ev("!!document.querySelector('.dlg')"): pg.locator('.dlg').last.click(); W(300)
        W(400)
    inv('aelis'); ok('D2 not close enough yet → polite no', not ev("atDeck('aelis')"))
    for i in ['frost','sirenora','cinder','felinia']: inv(i)
    ok('D3 familiar passengers come to the deck', all(ev(f"atDeck('{i}')") for i in ['frost','sirenora','cinder','felinia']))
    ok('D4 they appear on the deck', ev("['frost','sirenora','cinder','felinia'].every(id=>!!document.querySelector(`[data-hs=\"ot-p-${id}\"]`))"))
    pg.screenshot(path=S+'/deck.png')
    inv('pyro'); ok('D5 deck holds four at most', not ev("atDeck('pyro')"))
    ev("closeAll();state.currentCarriage='habitat';render()"); W(600)
    ok('D6 deck passengers are not in the habitat at the same time', not ev("!!document.querySelector('[data-hs=\"hab-p-frost\"]')") and ev("!!document.querySelector('[data-hs=\"hab-p-pyro\"]')"))
    ev("closeAll();state.currentCarriage='observatory';render()"); W(600); ev("deckTalk('frost')"); W(400); t=pg.locator('.dlg .tx').last.inner_text()
    pg.locator('.dlg .box').last.click(); W(250); t2=pg.locator('.dlg .tx').last.inner_text()
    ok('D7 stargazing line (voyage)', '冰原的夜' in t2, t2)
    pg.locator('.dlg .chs button').nth(1).click(); W(1200); pg.locator('.dlg .box').last.click(); W(500)
    ok('D8 can send it back to the habitat; journal + record', not ev("atDeck('frost')") and ev("state.log.some(l=>/展望台一起看了天空/.test(l.t))") and ev("state.passengers.frost.records.length")>=1)
    ok('D9 memory carriage still never shows passengers', (ev("closeAll();state.currentCarriage='memory';render()") or True) and not ev("!!document.querySelector('#scene .mote')"))
    ok('D10 no errors', not errs, errs)
    b.close()
