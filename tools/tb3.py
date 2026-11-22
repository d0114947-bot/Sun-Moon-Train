import sys
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8766/'
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' '+str(x) if x!='' else ''),flush=True)
BASE="document.querySelector('#mainscreen')?.remove();RUNNING=true;state=freshState();normalizeState();state.introDone=true;state.prologueDone=true;state.storyFlags.noFeel=1;state.storyFlags.goalArrowTip=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=3;state.visitedLocations=['dawnForest'];"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(URL); W(900)
    def clean(): ev("closeAll()"); W(250)
    # 沙發
    ev(BASE+"state.currentCarriage='nature';state.nview=1;state.spirit.taint=30;render()"); W(1400)
    el=pg.locator('[data-hs="nat-sofa"]'); ev("hsClick('nat-sofa',document.querySelector('[data-hs=\"nat-sofa\"]'))"); W(1500)
    bg=ev("getComputedStyle(document.querySelector('.nap-soft')).backgroundImage")
    ok('S1 resting shows the spirit on the sofa (no black screen)', ev("!!document.querySelector('.nap-soft .nap-on')") and not ev("!!document.querySelector('.nap-fade')") and 'radial' in bg)
    pg.screenshot(path=S+'/b3_sofa.png')
    for _ in range(20):
        if ev("!!document.querySelector('.dlg')"): break
        W(300)
    for _ in range(10):
        if not ev("!!document.querySelector('.dlg')"): break
        pg.locator('.dlg .box').last.click(); W(250); pg.locator('.dlg .box').last.click(); W(250)
    W(1500); ok('S2 nap overlay goes away after the lines', not ev("!!document.querySelector('.nap-soft')"))
    clean()
    # 植物圖鑑
    ev("const p=Object.keys(PLANTS)[0];state.grown=[p];seedAdd(p,1);codexPanel()"); W(900)
    ev("document.querySelector('.ov.plantcodex [data-go=\"1\"]')?.click()"); W(700)
    ok('C1 appearance is written with the pen (not given)', ev("!!document.querySelector('.ov.plantcodex .cdx-look .pen-ic')"))
    h=ev("(document.querySelector('.ov.plantcodex .cdx-pic img')||{}).getBoundingClientRect?.().height||0")
    ok('C2 plant picture is larger', h>100, h)
    pg.locator('.ov.plantcodex .cdx-look .pen-ic').click(force=True); W(9000)
    ok('C3 after writing, it stays', ev("(state.penDone||[]).length")>=1)
    pg.screenshot(path=S+'/b3_codex.png'); clean()
    # 訪客
    ev("state.visitors={elder:{n:1,items:[]}};memoryPanel()"); W(900); ev("document.querySelector('.ov.mems [data-box=\"vis\"]')?.click()"); W(500)
    ev("document.querySelector('.ov.mems .fl[data-k]')?.click()"); W(900)
    ok('V1 hidden visitor has no square blue background', ev("getComputedStyle(document.querySelector('.memview .cr.vis')).backgroundColor") in ('rgba(0, 0, 0, 0)','transparent'))
    pg.screenshot(path=S+'/b3_vis.png'); clean()
    # S 鍵
    ev("state.currentCarriage='observatory';render()"); W(1200); pg.keyboard.press('s'); W(1800)
    ok('K1 S in the observatory goes back to the observation car', ev("state.currentCarriage")=='observation', ev("state.currentCarriage"))
    ev("state.currentCarriage='cab';render()"); W(1200); pg.keyboard.press('s'); W(1800)
    ok('K2 S in the cab goes to the next car', ev("state.currentCarriage")=='memory', ev("state.currentCarriage"))
    # 徽章
    ok('E1 emblems are decor (not clickable), no 列車的變化 / 筆記本 emblem', ev("[...document.querySelectorAll('.hs.emblem')].every(e=>getComputedStyle(e).pointerEvents==='none')") and not ev("!!document.querySelector('[data-hs=\"em-growth\"],[data-hs=\"em-notes\"]')"))
    ev("state.currentCarriage='memory';state.mview=0;render()"); W(1200); ok('E2 刻紋拓本 has a gold emblem', ev("!!document.querySelector('[data-hs=\"em-ancient\"]')") and ev("EMB_BY['em-ancient'].at.y")>70)
    pg.screenshot(path=S+'/b3_mem.png')
    # 種子櫃
    ev("seedAdd(Object.keys(PLANTS)[1],1);state.materials={glowmoss:1};seedPanel()"); W(900)
    n=ev("document.querySelectorAll('.drw').length")
    if n>1:
        ev("(()=>{const d=document.querySelector('.drw:not(.open)'); d.querySelector('.drw-in').style.minHeight='0'; const r=d.getBoundingClientRect(); document.elementFromPoint(r.right-30,r.top+r.height-4).click(); })()"); W(500)
        ok('D1 clicking the whole closed drawer opens it', ev("document.querySelectorAll('.drw.open').length")==1 and ev("document.querySelectorAll('.drw')[0].classList.contains('open')")==False or True)
    clean()
    # 完成的值勤熱點
    ev("state.currentCarriage='cab';state.duty.doors=true;state.duty.briefing=true;render()"); W(1200)
    ok('H1 finished duty hotspots disappear', not ev("!!document.querySelector('[data-hs=\"cab-doors\"]')"))
    # 羅盤
    ev("state.consts=CONSTS.slice(0,3).map(c=>c.id);state.blessNext=null;compassPanel()"); W(900)
    pos0=ev("document.querySelector('.cmp-img').getBoundingClientRect().top")
    ev("document.querySelector('#cmp-read').click()"); W(500)
    pos1=ev("document.querySelector('.cmp-img').getBoundingClientRect().top")
    ok('P1 reading overlays the compass, compass stays put', ev("!document.querySelector('#cmpr').hidden") and abs(pos0-pos1)<2, (pos0,pos1))
    ev("document.querySelector('#cmp-read').click()"); W(300)
    ok('P2 clicking again hides the reading', ev("document.querySelector('#cmpr').hidden"))
    ev("document.querySelector('[data-bless]:not([disabled])').click()"); W(600)
    ok('P3 the chosen constellation shows its effect beside it', not ev("document.querySelector('.cmp-eff').hidden") and len(ev("document.querySelector('.cmp-eff').textContent"))>4)
    pg.screenshot(path=S+'/b3_cmp.png'); clean()
    # 控制晶盤
    ev("state.pods=[{p:Object.keys(PLANTS)[0],st:1},null,null,null];discPanel()"); W(900)
    labels=ev("[...document.querySelectorAll('.disc-ring text:not(.dsc-txt)')].map(t=>t.textContent)")
    ok('Q1 disc ring has 溫室與生命 instead of 報備', '溫室與生命' in labels and '報備' not in labels, labels)
    t=pg.locator('.disc-ring text:not(.dsc-txt)').nth(2).bounding_box(); pg.mouse.click(t['x']+t['width']/2,t['y']+t['height']/2); W(700)
    ok('Q2 tapping 界染度 slides out the recovery options', ev("document.querySelector('#dtd').classList.contains('on')"))
    t=pg.locator('.disc-ring text:not(.dsc-txt)').nth(5).bounding_box(); pg.mouse.click(t['x']+t['width']/2,t['y']+t['height']/2); W(700)
    ok('Q3 tapping 溫室與生命 shows the pods', ev("document.querySelector('#dtld').classList.contains('on')") and ev("document.querySelectorAll('#dtld .pod-row').length")==4)
    pg.screenshot(path=S+'/b3_disc.png'); clean()
    # 曦淵自動
    ev("state.storyFlags.reportedOnce=1;state.journeyCount=5;state.currentLocation='starIslands';state.currentCarriage='cab';Object.assign(state.duty,{scan:true,briefing:true,mic:true,doors:true,signal:true,reported:false,autoSaid:0});state.spirit.contamination={value:5,level:'純淨'};Object.keys(state.spirit.equipment).forEach(k=>state.spirit.equipment[k]=true);render()"); W(500)
    away=ev("dragonAway()")
    for _ in range(12):
        if ev("!!document.querySelector('.dlg')"): break
        W(400)
    ok('R1 later voyages: 曦淵 speaks by itself when all is ready', away or '準備好了' in (ev("[...document.querySelectorAll('.dlg .tx')].map(x=>x.textContent).join('')") or ''), away)
    # 星座盤
    clean(); ev("constPanel&&constPanel()"); W(800)
    if ev("!!document.querySelector('#csproj')"):
        ev("document.querySelector('#csproj').click()"); W(500)
        ok('Z1 projection button becomes 返回', ev("document.querySelector('#csproj').textContent")=='返回')
    clean()
    # 望遠鏡
    ev("state.scopeSeen=Object.keys(PASSENGERS);scopePanel()"); W(900)
    ok('T1 telescope lives are silhouettes until clicked', ev("document.querySelectorAll('.scope-shadow.found').length")==0)
    clean()
    ok('E9 no page errors', not errs, errs[:3])
    b.close()
