import os
from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad/ngar'; os.makedirs(S,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n,x if not c else '',flush=True)
    def adv(n=30):
        for _ in range(n):
            if ev("!!document.querySelector('.dlg')"):
                if ev("!!document.querySelector('.dlg .chs button')"): ev("document.querySelector('.dlg .chs button').click()"); W(1600)
                else: ev("document.querySelector('.dlg .box')?.click(); document.querySelector('.dlg:not(:has(.chs))')?.click()"); W(150)
            elif ev("!!document.querySelector('.cine')"): ev("document.querySelector('.cine').click()"); W(150)
            else: break
        W(400)
    badge=lambda: ev("[...document.querySelectorAll('#scene .step')].map(e=>e.closest('[data-hs]')?.dataset.hs+':'+e.innerText.replace(/\\n/g,''))")
    pg.goto('http://127.0.0.1:8766/'); W(900); ev("startNew()"); W(300)
    ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();document.querySelectorAll('.cine').forEach(e=>e.remove());state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.storyFlags.metDragon=1;state.currentPhase='docked';state.currentLocation='dawnForest';state.journeyCount=4;state.visitedLocations=['dawnForest','starIslands'];"
       "for(const id of ['felinia','titan']){state.discoveredLifeforms.push(id);state.passengers[id]={stage:2,talks:9,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS[id].zone}};state.req={felinia:{st:'done'},titan:{st:'on',j:1}};state.currentCarriage='nature';render()"); W(2500)
    ok('G0 seed intro dialogue once', (ev("state.storyFlags.seedTalk=0;seedIntro();1") and (W(1200) or True) and '種子' in ev("document.querySelector('.dlg')?.innerText||''")))
    for _ in range(8):
        ev("document.querySelector('.dlg .box')?.click()"); W(200)
    ev("seedAdd('bell',1);state.collectibles.push('seed_sunfern');render()"); W(800)
    ok('G1 step 1 on vault', badge()==[], badge())
    pg.screenshot(path=S+'/step1.png')
    ev("seedPanel()"); W(1500); pg.screenshot(path=S+'/vault.png')
    ok('G2 unknown rare seed shown', '未鑑定' in ev("document.querySelector('.ov').innerText")); ev("closeAll()"); W(300)
    ok('G3 step 2 vine', badge()==[], badge())
    ev("vinePanel()"); W(800); ev("document.querySelector('#vg-id').click()"); W(600); pg.screenshot(path=S+'/vine.png')
    ok('G4 identified', ev("seedKnown('sunfern')")); ev("closeAll()"); W(300)
    ok('G5 step 3 crystal', badge()==[], badge())
    ev("envPanel()"); W(500); ev("closeAll()"); W(300)
    ok('G6 step 4 plant', badge()==[], badge())
    ev("gardenPanel(0)"); W(800); pg.screenshot(path=S+'/garden_empty.png')
    ev("document.querySelector('[data-plant=\"bell\"]').click()"); W(500)
    ev("document.querySelector('[data-pk=\"1\"]').click()"); W(300); ev("document.querySelector('[data-plant=\"sunfern\"]').click()"); W(500)
    ok('G7 two pods planted', ev("state.pods[0]&&state.pods[0].p==='bell'&&state.pods[1]&&state.pods[1].p==='sunfern'"))
    ev("state.storyFlags.natureLight='moon';document.querySelector('[data-pk=\"1\"]').click()"); W(300); pg.screenshot(path=S+'/garden_grow.png')
    ok('G8 wrong light warns', '光不對' in ev("document.querySelector('.ov').innerText"))
    ev("closeAll()"); ev("gardenGrow()"); ok('G9 bell blooms, sunfern stalls (wrong light)', ev("state.pods[0].st===2&&state.pods[1].st===0"))
    ev("gardenPanel(1)"); W(500); ev("document.querySelector('#g-touch').click()"); W(400); ev("closeAll()"); ev("gardenGrow()")
    ok('G10 tending grows despite light', ev("state.pods[1].st===1"))
    ev("render()"); W(400); ok('G11 step 5 harvest', badge()==[], badge())
    ev("gardenPanel(0)"); W(500); ev("document.querySelector('#g-harvest').click()"); W(500); pg.screenshot(path=S+'/harvest.png')
    ok('G12 harvest gives plants+seeds', ev("plantN('bell')===2&&seedN('bell')===2&&state.grown.includes('bell')")); ev("closeAll()"); W(300)
    ok('G13 step 6 samples', badge()==[], badge())
    ev("samplePanel()"); W(600); ok('G14 sample shelf lists bell', '晨鈴花' in ev("document.querySelector('.ov').innerText")); ev("closeAll()"); W(300)
    
    # gift
    ev("plantAdd('dewmoss',1);state.currentCarriage='habitat';state.hview=0;render()"); W(800)
    ev("talk('titan')"); W(400)
    for _ in range(10):
        if ev("!!document.querySelector('.dlg .chs button')"): break
        ev("document.querySelector('.dlg .box')?.click()"); W(200)
    ok('G16 gift choice offered', ev("[...document.querySelectorAll('.dlg .chs button')].some(b=>b.textContent.includes('東西'))"))
    ev("[...document.querySelectorAll('.dlg .chs button')].find(b=>b.textContent.includes('東西')).click()"); W(1800); adv(3)
    pg.screenshot(path=S+'/giftpick.png')
    ev("document.querySelector('[data-gift=\"dewmoss\"]').click()"); W(700); pg.screenshot(path=S+'/gift.png'); adv()
    ok('G17 love gift recorded', ev("((state.gifts||{}).titan||[]).includes('dewmoss')"))
    # zone plant
    ev("zoneInfo('rings')"); W(500); pg.screenshot(path=S+'/zone.png'); ev("document.querySelector('[data-zp=\"bell\"]').click()"); W(400); ev("closeAll()"); W(300)
    ok('G18 pot in scene', ev("!!document.querySelector('#scene .zpot')")); pg.screenshot(path=S+'/pot.png')
    # titan request seed
    ev("reqDone('titan')"); W(300); ok('G19 titan gives dewmoss seed', ev("seedN('dewmoss')>=1&&seedKnown('dewmoss')"))
    # migration
    ev("state.gardenV=0;state.pods=null;state.culture={seed:'seed_starspore',bloomed:true};state.collectibles.push('seed_starspore');gardenSync()")
    ok('G20 old culture migrated', ev("state.pods[0].p==='starspore'&&state.pods[0].st===2"))
    ev("forageTake(0)"); 
    ok('Z no errors', not errs, errs)
    b.close()
