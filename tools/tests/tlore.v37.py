from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' '+str(x) if x!='' else ''),flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(900)
    ev("document.querySelector('#mainscreen')?.remove();RUNNING=true;state=freshState();normalizeState();state.introDone=true;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=3;state.visitedLocations=['dawnForest','starIslands'];state.clues=['clue_wake'];state.currentCarriage='memory';render()"); W(500)
    ev("BOOK.lp=0;openBook('lore')"); W(800)
    ok('L1 world book opens on 序・日與月 + 起源', '序・日與月' in pg.inner_text('.spread') and '第一道晨曦' in pg.inner_text('.spread'))
    pg.screenshot(path=S+'/lore1.png')
    pg.click('[data-lp="1"]'); W(600); t=pg.inner_text('.spread')
    ok('L2 turning the page: 界壁・渡口・星河 and 渡守', '界壁・渡口・星河' in t and '渡守' in t)
    ok('L3 guardian history is still blurred without clues', ev("document.querySelectorAll('.spread .blur').length")>=2)
    pg.screenshot(path=S+'/lore2.png')
    ev("state.clues.push('clue_ring','clue_sola_legend','clue_dimming');openBook('lore')"); W(600)
    t=pg.inner_text('.spread'); ok('L4 clues make the ink appear', '建造列車的人' in t and '很久以前，無數領域' in t and '熄滅之前' in t)
    pg.screenshot(path=S+'/lore3.png')
    pg.click('[data-lp="2"]'); W(500); ok('L5 last spread: 曦淵 page + 四類生命', '曦淵與值勤精靈' in pg.inner_text('.spread') and '四類生命' in pg.inner_text('.spread'))
    ev("closeAll();atlasBook()"); W(700); t=ev("atlasPages().join('')")
    ok('L6 atlas: visited places tell their history', '渡口樹' in t and '熄滅的世界剝落下來的碎片' in t and '０・００・００' in t)
    pg.screenshot(path=S+'/atlas.png'); ev("closeAll()")
    # dragon stories during voyages
    ev("state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'starIslands',progress:.3,evt:true,sky:null};state.currentCarriage='cab';render()"); W(500)
    def talk():
        ev("dragonTalk()"); W(300); L=[]
        for _ in range(20):
            if not ev("!!document.querySelector('.dlg')"): break
            L.append(pg.locator('.dlg .tx').last.inner_text()); pg.locator('.dlg').last.click(); W(120)
        return L
    l1=talk(); l2=talk(); l3=talk()
    ok('L7 dragon tells one story per talk, in order', any('界染' in x for x in l1) and any('渡守' in x for x in l2) and any('航道很穩' in x for x in l3), (l1[:1],l2[:1],l3[:1]))
    ok('L8 the 渡守 story gives a guardian clue', ev("state.clues.includes('clue_ferrykeepers')"))
    ev("state.journeyCount=7"); talk(); talk(); ok('L9 later journeys unlock 大熄滅 and the dragon name', ev("state.clues.includes('clue_dragon')"))
    ev("state.currentPhase='docked';state.voyage=null;closeAll();samplePanel()"); W(300); ok('L10 ash-fern specimen → clue', ev("state.clues.includes('clue_ash')")); ev("closeAll()")
    n=ev("state.clues.length"); ev("state.clues.push('clue_voyage','clue_seed');INTERACT['mem:save']()"); W(500)
    ok('L11 enough clues → the save crystal reveals the rest of the message', ev("state.clues.includes('clue_wake2')"), n)
    ok('L12 no errors', not errs, errs)
    b.close()
