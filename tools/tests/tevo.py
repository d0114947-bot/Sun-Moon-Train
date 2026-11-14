from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    def drain(n=40):
        t=[]
        for _ in range(n):
            if ev("!!document.querySelector('.cine')"): ev("document.querySelector('.cine').click()"); W(250); continue
            if not ev("!!document.querySelector('.dlg')"): break
            t.append(ev("document.querySelector('.dlg .tx')?.textContent||''")); ev("document.querySelector('.dlg .box').click()"); W(120)
        return t
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("window.LOCK_TEST=1;startNew()"); W(300)
    base="document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.journeyCount=1;state.currentLocation='dawnForest';state.visitedLocations=['origin'];state.currentPhase='docked';"
    ev(base+"state.trainEvo=null;state.trainUnlock=null;state.grown=[];state.consts=[];state.clues=[];state.engr=[];state.skySeen=[];evoSync()")
    ok('A1 start: every direction at stage 1',ev("EVO.every(e=>trainStage(e.k)===1)"),ev("EVO.map(e=>e.calc())"))
    ev("state.currentCarriage='nature';state.nview=0;render()"); W(400)
    ok('A2 advanced hotspots start locked (still visible)',ev("document.querySelector('[data-hs=\"nat-samples\"]')?.className||''").find('st-locked')>=0)
    ok('A3 locked look depends on kind (dormant)',ev("document.querySelector('[data-hs=\"nat-samples\"]').className").find('lk-dormant')>=0)
    ok('A4 basic functions stay open',ev("hsState(HSDEF.find(h=>h.id==='nat-pod-a'))")!='locked' and ev("hsState(HSDEF.find(h=>h.id==='nat-vault'))")!='locked')
    ev("hsClick('nat-samples',document.querySelector('[data-hs=\"nat-samples\"]'))"); W(400)
    ok('A5 clicking a locked one gives a short hint, not numbers',(ev("document.querySelector('.whisper')?.textContent||''").find('開花')>=0))
    # nature
    ev("document.querySelectorAll('.whisper').forEach(e=>e.remove());state.grown=['bell'];evoSync();render()"); W(500)
    ok('N1 first bloom → 自然萌芽 + shelf unlocked',ev("trainStage('nature')")==2 and ev("hsState(HSDEF.find(h=>h.id==='nat-samples'))")!='locked')
    ok('N2 greenhouse scene changes: plant on the empty shelf (display-shelf hotspot removed by request)',ev("document.querySelectorAll('.evo-nat img.disp').length")>=1 and not ev("!!document.querySelector('[data-hs=\"nat-display\"]')"))
    ev("state.grown=['bell','bell','bell'];evoSync()"); ok('N3 repeats of the same plant do not count',ev("new Set(state.grown).size")==1 and ev("trainStage('nature')")==2)
    ev("state.grown=['bell','sunfern','dewmoss','tidebloom','stardaisy'];evoSync();render()"); W(300)
    ok('N4 more kinds → 自然繁盛 (vines appear)',ev("trainStage('nature')")==3 and ev("!!document.querySelector('.evo-nat .vine-l')"))
    # sanctuary
    ev("state.passengers.felinia={stage:1,talks:1,records:[],aboard:true};evoSync();state.currentCarriage='habitat';state.hview=0;render()"); W(400)
    ok('S1 first companionship → 溫暖停留, lantern appears',ev("trainStage('sanct')")==2 and ev("document.querySelectorAll('.evo-sanct .lantern').length")>=1)
    ev("zoneInfo('rest')"); W(500); ok('S2 歸宿之燈 opens in the special rest area',ev("!!document.querySelector('[data-home]')")); ev("closeAll()"); W(300)
    ev("['aelis','pyro','frost','sola','titan'].forEach(i=>state.passengers[i]={stage:2,talks:2,records:[],aboard:true});state.passengers.titan.left=true;state.passengers.titan.aboard=false;evoSync();render()"); W(300)
    ok('S3 lives that found home still count (歸宿之所)',ev("trainStage('sanct')")==4 and ev("document.querySelectorAll('.evo-sanct .lantern.gone').length")>=1)
    ev("habHome()"); W(300); ok('S4 look back on every life you helped',ev("document.querySelectorAll('.growov .who-list li').length")>=6); ev("closeAll()")
    # ancient
    ev("state.currentCarriage='memory';state.mview=0;render()"); W(300)
    ok('C0 wall glyphs hidden at first',not ev("!!document.querySelector('.evo-glyph')"))
    ev("state.engr=['dawnForest'];evoSync();render()"); W(300)
    ok('C1 first carving → writing appears on the wall',ev("trainStage('ancient')")==2 and ev("!!document.querySelector('.evo-glyph.st2')") and ev("hsState(HSDEF.find(h=>h.id==='mem-wall'))")!='locked')
    ev("memWall()"); W(300); ok('C2 wall text is partly readable',ev("document.querySelectorAll('.anc-l.blur').length")==4); ev("closeAll()")
    t0=ev("trainT()"); ev("state.engr=['dawnForest','starIslands'];state.clues=['clue_ring'];evoSync();render()"); W(300)
    ok('C3 古代迴響 → ancient devices restore the train a little (once)',ev("trainStage('ancient')")==3 and ev("trainT()")<t0)
    t1=ev("trainT()"); ev("evoSync()"); ok('C4 bonus not counted twice',ev("trainT()")==t1)
    # sky
    ev("state.consts=['deer','wing'];evoSync();state.currentCarriage='observatory';render()"); W(300)
    ok('K1 constellations → 星光甦醒 + projection unlocked',ev("trainStage('sky')")==2 and ev("!!document.querySelector('.evo-proj')") and ev("hsState(HSDEF.find(h=>h.id==='ot-proj'))")!='locked')
    ev("state.consts=['deer','wing','jelly','fox'];state.skySeen=['meteor','tide'];state.projPick=['deer','wing','jelly','fox'];evoSync();render()"); W(300)
    ok('K2 constellations picked on the star disc appear in the projection',ev("trainStage('sky')")==3 and ev("document.querySelectorAll('.evo-proj .pc').length")==4)
    # repair
    ev("state.trainTaint=60;state.trainEvo.repair=1;state.currentCarriage='cab';render()"); W(300)
    ok('R1 train contamination is separate from the spirit',ev("trainT()")==60 and ev("TAINT.val()")!=60 and ev("!!document.querySelector('.tr-veil.tr-1')"))
    ev("state.materials={mosslight:2};cabCore()"); W(300); ev("document.querySelector('[data-core]').click()"); W(400)
    ok('R2 core crystal: purification light restores the train',ev("trainT()")==56 and ev("matCount('mosslight')")==1)
    ev("TAINT.purify('spring',3)"); ok('R3 spirit purification also helps a little',ev("trainT()")==55)
    ev("trainArrive('dawnForest')"); ok('R4 arrival effects (sun, plants, purity) move it',ev("trainT()")<55)
    ev("state.trainTaint=15;evoSync();render()"); W(300); ok('R5 windows & crystals clear up (能量恢復)',ev("trainStage('repair')")==3 and ev("!!document.querySelector('.tr-veil.tr-3')"))
    ev("state.trainTaint=50;evoSync()"); ok('R6 restoration never goes backwards',ev("trainStage('repair')")==3)
    # guardian
    ev("state.clues=['clue_ring','clue_wake'];evoSync();state.currentCarriage='memory';state.mview=1;render()"); W(300)
    ok('G1 memory echo: sealed door outline reacts',ev("trainStage('guard')")==2 and ev("!!document.querySelector('.evo-seal.g2')") and ev("HSDEF.find(h=>h.id==='mem-seal').lock()").find('門扉')>=0)
    ev("spiritPanel()"); W(300); ok('G2 mirror shows a stranger',ev("document.querySelector('.mirrorov').textContent").find('陌生的身影')>=0); ev("closeAll()")
    ev("state.clues=['clue_ring','clue_wake','clue_voyage','clue_dragon'];state.engr=[];evoSync()"); ok('G3 memories + readable ancient wall together open the room',ev("trainStage('guard')")==3) 
    ev("render()"); W(300); ok('G4 hidden room opens (渡守的值勤室)',ev("hsState(HSDEF.find(h=>h.id==='mem-seal'))")!='locked'); ev("guardRoom()"); W(300)
    ok('G5 room holds origin records',ev("document.querySelector('.growov').textContent").find('值勤日誌')>=0); ev("closeAll()")
    ev("state.clues=['clue_ring','clue_wake','clue_voyage','clue_dragon','clue_echo','clue_seed','clue_dimming'];state.consts=['deer','wing','jelly','fox'];evoSync();guardRoom()"); W(300)
    ok('G6 列車真相 at stage 4',ev("trainStage('guard')")==4 and ev("document.querySelector('.growov').textContent").find('願意繼續值勤')>=0); ev("closeAll()")
    # record panel
    ev("growthPanel()"); W(300); ok('P1 growth record shows six directions + changes',ev("document.querySelectorAll('.evo-row').length")==6 and ev("document.querySelectorAll('.evoov .who-list li').length")>=3); ev("closeAll()")
    # presentation
    ev("window.STORY_TEST=1;state.trainEvo.nature=3;state.grown=['bell','sunfern','dewmoss','tidebloom','stardaisy','glowcap','starbell','goldreed'];state.hybridSeen=['tidelotus'];state.currentCarriage='nature';render();evoSync()"); W(1600)
    ok('V1 unlock presentation: glow + line',ev("!!document.querySelector('.dlg')")); t=drain(); ev("window.STORY_TEST=0")
    ok('V2 nature reaches 自然共生',ev("trainStage('nature')")==4,t)
    # persistence
    ev("save()"); pg.reload(); W(900)
    ev("window.LOCK_TEST=1;state=load();RUNNING=true;document.querySelector('#mainscreen')?.remove();state.grown=[];state.currentPhase='docked';state.currentCarriage='nature';render()"); W(300)
    ok('L1 unlocked hotspots stay open after reload even if data changes',ev("hsState(HSDEF.find(h=>h.id==='nat-samples'))")!='locked' and ev("trainStage('nature')")==4)
    ok('L2 scene changes are still there after reload',ev("!!document.querySelector('.evo-nat')"))
    ev("(()=>{const s=load(); ['trainEvo','trainUnlock','trainLog','trainTaint','evoBonus'].forEach(k=>delete s[k]); s.grown=['bell','sunfern']; s.consts=['deer']; localStorage.setItem(SAVE_KEY,JSON.stringify(s));})()"); pg.reload(); W(900)
    ev("state=load();RUNNING=true;document.querySelector('#mainscreen')?.remove();window.STORY_TEST=1;evoSync()"); W(600)
    ok('L3 old save: existing progress counted, silently (no flood)',ev("trainStage('nature')")==2 and ev("(state.trainUnlock||[]).includes('nat-samples')") and not ev("!!document.querySelector('.dlg')") and ev("EVO_Q.length")==0)
    ok('Z no page errors',not errs,errs)
    print('ALL PASS' if all(R) else 'SOME FAIL',len(R))
