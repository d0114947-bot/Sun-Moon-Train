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
            t.append(ev("document.querySelector('.dlg .tx')?.textContent||''"))
            if ev("!!document.querySelector('.dlg .chs button')"): ev("document.querySelector('.dlg .chs button').click()"); W(1300)
            else: ev("document.querySelector('.dlg .box').click()"); W(120)
        return t
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(300)
    P=lambda ids,st=2: ";".join(f"state.passengers.{i}={{stage:{st},talks:1,records:[],aboard:true,boardedJourney:state.journeyCount}}" for i in ids)
    base="document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.journeyCount=4;state.currentLocation='starIslands';state.visitedLocations=['origin','dawnForest','starIslands'];state.currentPhase='docked';state.currentCarriage='observatory';"
    ev(base+P(['sola','vandora','pyro','titan','felinia'])+";render()"); W(300)
    # 1 star messages
    ev("state.starMsgs=[];state.msgJ={};state.passengers.sola.place='deck';msgTry(true,'sola')"); 
    ok('M1 passenger leaves a message on its own',ev("(state.starMsgs||[]).length")==1)
    ev("render()"); W(400); ok('M2 rune hotspot appears on the deck (breathing)',ev("!!document.querySelector('[data-hs=\"ot-msg\"]')") and ev("document.querySelector('[data-hs=\"ot-msg\"]').className").find('rune-hs')>=0)
    ok('M3 cooldown: same passenger not again right away',ev("msgTry(true,'sola')") is None)
    styles=ev("['sola','vandora','pyro','titan','felinia'].map(id=>msgCompose(id,'daily'))"); ok('M4 different passengers, different voices',len(set(styles))==5,styles)
    ok('M4b no shared pool across 24 (unique signatures)',ev("new Set(Object.values(MSG_SIG)).size")==24)
    ev("msgRead()"); W(1200); ok('M5 reading shows text emerging from glyphs; marked read',ev("state.starMsgs[0].read") and ev("document.querySelector('.rune-txt').textContent.length")>3); ev("closeAll()"); W(300)
    ev("render()"); W(200); ok('M6 rune goes dormant when no new messages',not ev("!!document.querySelector('[data-hs=\"ot-msg\"]')"))
    ev("state.env={id:'tide',int:2,key:TAINT.key()};tideMsg()"); ok('M7 星潮中的留言: a shy/quiet passenger leaves a special one',ev("state.starMsgs.some(m=>m.kind==='tide')"))
    ev("state.passengers.sola.aboard=false;state.passengers.sola.left=true;state.currentCarriage='memory';render();casketPanel('msg')"); W(400)
    ok('M8 messages kept in 時光匣 after the passenger leaves',ev("document.querySelector('.caskov').textContent").find('已回到自己的地方')>=0); ev("closeAll()")
    # 2 gifts
    ev("state.passengers.sola.aboard=true;state.passengers.sola.left=false;state.pGifts=[];state.giftJ={};state.giftPend=null;giftTry(true)")
    g=ev("state.giftPend&&[state.giftPend.g.pid,state.giftPend.g.tier,state.giftPend.mode,state.giftPend.g.name]"); ok('G1 a passenger prepares a gift on its own',g is not None,g)
    pid,tier,mode,name=g
    ok('G2 gift fits the character (tier by relationship, own item)',(tier==2 and ev(f"GIFT2['{pid}'][0]")==name) or tier==1)
    if mode=='place':
        ev("state.currentCarriage='cab';render()"); W(300); ok('G3 placed silently at the duty spot',ev("!!document.querySelector('[data-hs=\"cab-gift\"]')")); ev("giftFound()"); W(300); ev("closeAll()")
    elif mode=='hand':
        ev(f"state.passengers['{pid}'].place=undefined;state.currentCarriage='habitat';render()"); W(300); ok('G3 handed over in person',ev("giftHandTry(hereList())")); W(900); drain()
    else:
        ev(f"talk('{pid}')"); W(500); ok('G3 pulls it out when you talk',ev("!!document.querySelector('.dlg')")); drain()
    ok('G4 collected once',ev("state.pGifts.length")==1 and ev("!state.giftPend"))
    ev("giftTry(true)"); n=ev("state.pGifts.length+(state.giftPend?1:0)"); ok('G5 same gift never given twice',ev(f"state.pGifts.filter(x=>x.pid==='{pid}'&&x.tier=={tier}).length")==1)
    ev("state.giftPend=null;state.passengers.vandora.stage=3;state.passengers.vandora.bye=null;state.passengers.pyro.bye=null")
    ev("state.passengers.vandora.bye={st:'prep',pairs:[]};byeGiftTry('vandora');state.passengers.pyro.bye={st:'prep',pairs:[]};byeGiftTry('pyro')")
    ok('G6 leaving: shy one leaves it secretly, proud one says nothing',ev("state.pGifts.some(x=>x.pid==='vandora'&&x.how==='secret')") and not ev("state.pGifts.some(x=>x.pid==='pyro'&&x.bye)"))
    ev("state.lastComp={id:'felinia',loc:'dawnForest',j:state.journeyCount};state.giftJ={};state.giftPend=null;giftTry()"); ok('G7 來自遠方的禮物: after exploring together',ev("state.giftPend&&state.giftPend.g.pid==='felinia'&&state.giftPend.g.desc.includes('晨曦森林')"))
    # 3 weather
    seen=ev("(()=>{ const o=new Set(); state.currentPhase='docked'; ['dawnForest','starIslands','origin'].forEach(l=>{ for(let j=1;j<12;j++){ state.currentLocation=l; state.journeyCount=j; state.env=null; const e=envSet('silent'); if(e.id) o.add(l+':'+e.id); } }); state.journeyCount=4; state.currentLocation='starIslands'; return [...o]; })()")
    ok('W1 different places → different phenomena',any(x.startswith('starIslands:tide') for x in seen) and any(x.startswith('dawnForest:petals') for x in seen),seen)
    ok('W1b same phenomenon, different intensity',len(set(ev("(()=>{const o=[];for(let j=1;j<20;j++){state.journeyCount=j;state.env=null;const e=envSet('silent');if(e.id==='tide')o.push(e.int);}state.journeyCount=4;return o})()")))>=2)
    ev("state.env={id:'mist',int:3,key:TAINT.key()};state.currentCarriage='habitat';render()"); W(300)
    ok('W2 carriage light changes (overlay + body class)',ev("!!document.querySelector('.env-ov.env-mist')") and ev("document.body.classList.contains('env-mist')"))
    ev("state.env={id:'silence',int:2,key:TAINT.key()};BGM.el={volume:.24};BGM.on=true;envFx()"); ok('W3 sound changes (silence ducks the music)',ev("BGM.el.volume")<0.2); ev("BGM.el=null;BGM.on=false")
    ev("state.env={id:'petals',int:2,key:TAINT.key()};state.envSeen={};state.pods=[{p:'bell',st:0},null,null,null];state.currentCarriage='nature';render()"); ok('W4 plants react (and a short bloom)',ev("envReact([])") and ev("state.pods[0].st")==1); W(600)
    ev("state.envSeen={};state.env={id:'tide',int:2,key:TAINT.key()};state.passengers.sola.place=undefined;state.currentCarriage='habitat';render()"); ok('W5 passengers react to familiar environments',ev("envReact(['sola'])")); W(800); drain()
    ev("state.currentPhase='voyage';state.voyage={to:'dawnForest',from:'starIslands',progress:0};render()"); ok('W6 environment ends when the context changes',not ev("!!envNow()") and not ev("!!document.querySelector('.env-ov')"))
    ev("state.trainEvo={repair:1};state.env={id:'mist',int:1,key:TAINT.key()};envFx()"); ok('W7 linked to train restoration (distortion while contaminated)',ev("document.body.classList.contains('env-warp')"))
    # 4 visitors
    ev("state.currentPhase='docked';state.currentLocation='starIslands';state.voyage=null;state.visitors={};state.visitorNow=null;state.env={id:'tide',int:2,key:TAINT.key()};state.trainEvo={ancient:1,repair:1};state.clues=[];")
    vids=ev("(()=>{ const o=new Set(); for(let i=0;i<30;i++){ state.visitorNow=null; state.visJ=null; const v=visitorRoll(); if(v) o.add(v.id); } return [...o]; })()")
    ok('V1 conditional visitor appears (tide → 星潮的小透明)','tidewisp' in vids,vids)
    ev("state.trainEvo={ancient:3,repair:1};state.visitorNow=null;visitorRoll()"); ok('V2 important visitor is guaranteed when its condition holds',ev("state.visitorNow&&state.visitorNow.id")=='elder')
    ev("state.currentCarriage='memory';state.mview=0;render()"); W(300); ok('V3 visitor stands in the right carriage',ev("!!document.querySelector('[data-hs=\"vis-elder\"]')"))
    ev("visitorMeet()"); W(500); t=drain(); ok('V4 its own short story + clue',any('澆花' in x for x in t) and ev("state.clues.includes('clue_moth')"),t)
    ok('V5 record kept; not repeated',ev("state.visitors.elder.n")==1 and ev("(()=>{state.visitorNow=null;const v=visitorRoll();return !v||v.id!=='elder'})()"))
    ev("state.visitorNow={id:'flicker',key:TAINT.key(),j:4};state.passengers.mnemo={stage:2,talks:1,records:[],aboard:true};"); ev("visitorMeet()"); W(500); t=drain()
    ok('V6 不曾見過的訪客: a passenger recognises it',any('熄滅的世界' in x for x in t) and ev("state.visitors.flicker.with")=='mnemo',t)
    ok('V7 missing visitors never block anything (no main-line dependency)',ev("Object.values(VISITORS).every(V=>!V.blocks)"))
    # 5 old echoes
    ev("window.STORY_TEST=1;state.oldEcho={};state.oldJ=null;state.oldJR=null;state.trainEvo={ancient:3,guard:1,nature:1,sky:1,repair:1};state.currentCarriage='habitat';render()")
    ev("state.journeyCount=9;state.oldJ=null")   # 渡守的聲音：第 8 趟以後才會出現
    ok('E0 echoes stay silent before journey 8',ev("(()=>{const j=state.journeyCount;state.journeyCount=4;const r=oldPick();state.journeyCount=j;return r===null})()"))
    ok('E1 important echo chosen by condition (not chance)',ev("oldPick()")=='origin')
    ev("oldPlay(null,true)"); W(1300); ok('E2 lights flicker, crystals glow while playing',ev("document.body.classList.contains('old-echo')")); t=drain()
    ok('E3 plays ancient voice, then train returns to normal',any('船只能載' in x for x in t) and not ev("document.body.classList.contains('old-echo')"),t)
    ok('E4 never repeats',ev("oldDone('origin')") and ev("oldPick()")!='origin'); ev("state.journeyCount=4")
    ev("state.oldJ=null;state.clues=['clue_wake'];state.oldEcho.name=null;delete state.oldEcho.name;state.oldJR=-9;oldPlay('name',true)"); W(1200); drain()
    ok('E5 partial echo stays unfinished until the guardian memory is found',ev("state.oldEcho.name.full")==0)
    ev("state.trainEvo.guard=4;oldSync()"); ok('E6 …then completes',ev("state.oldEcho.name.full")==1)
    ev("state.currentLocation='origin';state.trainEvo.sky=2;state.oldJ=null;state.currentCarriage='observatory';state.consts=['deer'];render()"); W(300)
    ok('E7 被喚醒的回聲 at the ancient ferry',ev("Object.keys(OLD).filter(id=>!oldDone(id)&&OLD[id].cond()).includes('ferry')"))
    ev("closeAll();casketPanel('echo')"); W(400); ok('E8 echoes collected (with unknown slots kept)',ev("document.querySelectorAll('.caskov .cask-list li').length")==len(ev("Object.keys(OLD)")) and ev("document.querySelectorAll('.caskov .cask-list li.unk').length")>0); ev("closeAll()")
    # save/load
    ev("save()"); pg.reload(); W(900)
    ok('S1 everything saved (messages read, gifts, env, visitors, echoes)',ev("(()=>{const s=load(); return s.starMsgs.length>=2&&s.starMsgs[0].read===true&&s.pGifts.length>=2&&s.visitors.elder&&s.oldEcho.origin&&s.envHist})()"))
    ev("(()=>{const s=load(); ['starMsgs','msgJ','pGifts','giftJ','giftPend','env','envHist','envSeen','envObs','visitors','visitorNow','visJ','oldEcho','oldJ','oldJR','lastComp'].forEach(k=>delete s[k]); localStorage.setItem(SAVE_KEY,JSON.stringify(s));})()"); pg.reload(); W(900)
    ev("state=load();RUNNING=true;document.querySelector('#mainscreen')?.remove();state.currentPhase='docked';state.currentCarriage='memory';render();casketPanel();msgTry(true);giftTry(true);envSet();visitorRoll();oldPick()"); W(500); ev("closeAll()")
    ok('S2 old save loads with all five systems',not errs,errs)
    print('ALL PASS' if all(R) else 'SOME FAIL',len(R))
