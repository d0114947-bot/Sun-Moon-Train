from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' '+str(x) if x!='' else ''),flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(900)
    bad=ev("""Object.entries(NOTES).flatMap(([id,N])=>N.list.filter(x=>!PASSENGERS[id].talks.some(t=>t.lines.some(l=>l.includes(x.p)))).map(x=>id+':'+x.p))""")
    ok('N1 every glowing phrase exists in its passenger lines', not bad, bad)
    cover=ev("""Object.entries(NOTES).flatMap(([id,N])=>N.secs.filter(k=>!N.list.some(x=>x.k===k)).map(k=>id+':'+k))""")
    ok('N2 every codex section can be learned', not cover, cover)
    ev("document.querySelector('#mainscreen')?.remove();RUNNING=true;state=freshState();normalizeState();state.req=Object.fromEntries(Object.keys(REQ).map(k=>[k,{st:'done',j:0}]));state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=2;state.visitedLocations=['dawnForest'];"
       "state.care={felinia:{t:1,l:1},vandora:{l:0,h:2}};state.discoveredLifeforms=['felinia'];state.passengers.felinia={stage:1,talks:0,records:[],aboard:true,left:false,boardedJourney:2};state.currentCarriage='habitat';render()"); W(600)
    def run_dialog(mark_all=True, pick=0):
        for _ in range(40):
            if not ev("!!document.querySelector('.dlg')"): return
            if mark_all:
                for m in pg.locator('.dlg mark.hl:not(.got)').all():
                    m.click(); W(150)
            if ev("!!document.querySelector('.dlg .chs button')"): pg.locator('.dlg .chs button').nth(pick).click(); W(1100)
            else: pg.locator('.dlg .box').last.click(); W(160)
    ev("talk('felinia')"); W(500); pg.locator('.dlg .box').last.click(); W(250); pg.screenshot(path=S+'/hl.png')
    ok('N3 key phrases glow in the dialogue', ev("document.querySelectorAll('.dlg mark.hl').length")>=1)
    pg.locator('.dlg .box').last.click(); W(300)
    ok('N3b forgetting a glowing phrase shows a reminder box', ev("!!document.querySelector('.dlg .hl-tip')") and '雲霧會繞著老樹' in pg.locator('.dlg .tx').last.inner_text())
    pg.screenshot(path=S+'/tip.png')
    pg.locator('.dlg mark.hl').first.click(); W(200); ok('N3c noting it removes the reminder', ev("!document.querySelector('.dlg .hl-tip')"))
    run_dialog()
    ok('N4 tapping a glowing phrase writes a note', len(ev("state.notes.felinia"))==2, ev("state.notes.felinia"))
    ok('N5 nothing is auto-written into the codex', ev("JSON.stringify(state.filed||{})")=='{}')
    ev("talk('felinia')"); W(500); run_dialog(); ev("talk('felinia')"); W(500); run_dialog()
    ok('N6 notebook never fills (all 5 glowing phrases kept)', len(ev("state.notes.felinia"))==5, ev("state.notes.felinia"))
    # notebook panel
    pg.click('[data-act="notes:open"]'); W(500); ok('N7 🗒️ opens the notebook', ev("!!document.querySelector('.ov.notebook .nb-list')") and ev("document.querySelectorAll('.nb-who .nb-list li').length")==5)
    pg.screenshot(path=S+'/nb.png')
    pg.click('[data-erase="felinia:4"]'); W(300); ok('N8 erase a note frees a page', len(ev("state.notes.felinia"))==4); ev("closeAll()"); W(300)
    # codex filing
    ev("openBook('life','felinia')"); W(1200)
    ok('N9 codex sections start blank with note slots', ev("document.querySelectorAll('.file-slot').length")==4 and '崖壁縫隙' not in pg.inner_text('.ov.jr'))
    pg.screenshot(path=S+'/cx0.png')
    pg.click('.file-slot[data-sec="habitat"] [data-file]'); W(300)
    ok('N10 slot lists the notes', ev("document.querySelectorAll('.file-slot [data-pick]').length")==4)
    pg.screenshot(path=S+'/cx1.png')
    pg.click('.file-slot [data-pick$=":3"]'); W(400); ok('N11 wrong note does not fit', ev("!(state.filed&&state.filed.felinia&&state.filed.felinia.habitat!==undefined)"))
    pg.click('.file-slot [data-pick$=":0"]'); W(900); ok('N12 right note reveals the full text', ev("state.filed.felinia.habitat")==0 and '崖壁縫隙' in pg.inner_text('.ov.jr'))
    ok('N12b sketches start blank in the codex', ev("document.querySelectorAll('.studies .sk.blank').length")==2)
    for sec,i in [('habits',1),('abilities',2),('bio',3)]:
        pg.click(f'.file-slot[data-sec="{sec}"] [data-file]'); W(300); pg.click(f'.file-slot [data-pick="felinia:{sec}:{i}"]'); W(900)
    ok('N13 sections filed but no sketches → not complete yet', ev("noteDone('felinia')") and not ev("fullDone('felinia')") and '完整紀錄' not in pg.inner_text('.ov.jr'))
    ev("closeAll()"); W(400)
    ok('N13b passenger stays while sketches are missing', not ev("readyToLeave('felinia')"))
    ev("state.currentCarriage='habitat';render()"); W(500)
    ok('S0 no sketch button in the HUD', not ev("!!document.querySelector('#hud [data-act=\"sketch:open\"]')"))
    ev("talk('felinia')"); W(500)
    ok('S1 talking to a passenger shows ✍️ 觀察速寫', ev("!!document.querySelector('.dlg .dsk')"))
    pg.click('.dlg .dsk'); W(900)
    def draw_one():
        for _ in range(400):
            inz=ev("(()=>{const b=document.querySelector('.sk-bar');if(!b)return null;const z=b.querySelector('.zone'),p=b.querySelector('.ptr');const a=parseFloat(z.style.left),w=parseFloat(z.style.width),x=parseFloat(p.style.left);if(x>=a+w*.3&&x<=a+w*.7){document.querySelector('#skgo').click();return true}return false})()")
            if inz is None: return False
            if inz: W(1800); return True
            W(40)
        return False
    ok('S2 drawing at the right moment captures a sketch', draw_one() and len(ev("state.sketches.felinia"))==1)
    pg.screenshot(path=S+'/sk.png')
    n0=len(ev("state.sketches.felinia"))
    for _ in range(300):
        if ev("(()=>{const b=document.querySelector('.sk-bar'),z=b.querySelector('.zone'),p=b.querySelector('.ptr');const a=parseFloat(z.style.left),w=parseFloat(z.style.width),x=parseFloat(p.style.left);if(x<a-12||x>a+w+12){document.querySelector('#skgo').click();return true}return false})()"): break
        W(30)
    W(300)
    ok('S3 missing the moment does not count', len(ev("state.sketches.felinia"))==n0 and '歪掉' in pg.inner_text('#skm'))
    draw_one(); ok('S4 two sketches done', len(ev("state.sketches.felinia"))==2 and ev("fullDone('felinia')") and ev("state.log.some(l=>/圖鑑整理完成/.test(l.t))"))
    ev("closeAll()"); W(400); ev("openBook('life','felinia')"); W(1200)
    ok('N13c codex shows sketches and complete seal', ev("document.querySelectorAll('.studies .sk.blank').length")==0 and '完整紀錄' in pg.inner_text('.ov.jr'))
    pg.screenshot(path=S+'/cx2.png'); ev("closeAll()"); W(400)
    ok('N13d now ready to leave', ev("readyToLeave('felinia')"))
    # replay when a section is still missing (vandora, all talks already heard, no notes)
    ev("state.discoveredLifeforms.push('vandora');state.passengers.vandora={stage:2,talks:3,records:[],aboard:true,left:false,boardedJourney:2};talk('vandora')"); W(500)
    for _ in range(6):
        if ev("!!document.querySelector('.dlg .chs button')"): break
        pg.locator('.dlg .box').last.click(); W(160)
    ok('N14 can ask a passenger to tell it again', '再跟我說一次' in pg.inner_text('.dlg .chs'))
    pg.locator('.dlg .chs button').first.click(); W(1100)
    for _ in range(3): pg.locator('.dlg .box').last.click(); W(200)
    ok('N15 replayed story has glowing phrases', ev("document.querySelectorAll('.dlg mark.hl').length")>=1, pg.inner_text('.dlg .tx'))
    run_dialog()
    # farewell thanks
    ev("closeAll()"); W(300); ev("farewell('felinia',()=>{})"); W(400); L=[]
    for _ in range(8):
        if not ev("!!document.querySelector('.dlg')"): break
        L.append(pg.locator('.dlg .tx').last.inner_text()); pg.locator('.dlg .box').last.click(); W(160)
    ok('N16 completed codex → passenger thanks you when leaving', any('山上的風' in l for l in L), L)
    ok('N17 no errors', not errs, errs)
    b.close()
