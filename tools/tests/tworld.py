from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    def drain(pick=None,n=40):
        seen=[]
        for _ in range(n):
            if ev("!!document.querySelector('.cine')"): ev("document.querySelector('.cine').click()"); W(250); continue
            if not ev("!!document.querySelector('.dlg')"): break
            seen.append(ev("document.querySelector('.dlg .tx')?.textContent||''"))
            if ev("!!document.querySelector('.dlg .chs button')"):
                bs=ev("[...document.querySelectorAll('.dlg .chs button')].map(b=>b.textContent)")
                i=next((k for k,x in enumerate(bs) if pick and pick in x),0)
                ev(f"document.querySelectorAll('.dlg .chs button')[{i}].click()"); W(1400); pick=None
            else: ev("document.querySelector('.dlg .box').click()"); W(120)
        return seen
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(300)
    P=lambda ids: ";".join(f"state.passengers.{i}={{stage:2,talks:1,records:[],aboard:true,boardedJourney:state.journeyCount}}" for i in ids)
    base="document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.journeyCount=3;state.currentLocation='dawnForest';state.visitedLocations=['dawnForest','starIslands'];state.currentPhase='docked';state.currentCarriage='habitat';"
    ev(base+P(['pyro','frost','felinia','aelis'])+";render()"); W(400)
    # ---- 1 society
    ok('1a relationships have different tendencies',ev("relOf('pyro','frost').tone")=='clash' and ev("relOf('felinia','aelis').tone")!='clash',[ev("relOf('pyro','frost').tone"),ev("relOf('felinia','aelis').tone")])
    for i in range(6): ev("socialStep(true)")
    ok('1b passengers interact on their own (logged, points)',ev("(state.relLog||[]).length")>=6 and ev("Object.values(state.rel).some(r=>r.pts>0)"))
    ok('1c not a single affection value: level + tone + firsts',ev("(()=>{const r=relOf('felinia','aelis'); return 'lv' in r&&'tone' in r&&'firsts' in r})()"))
    ok('1d player arrangement matters (same rest zone → more)',ev("(()=>{ const a='felinia',b='aelis'; const z=zoneOf(a)===zoneOf(b); return socBonus(a,b,'habitat')===(z?2:1); })()"))
    ev("relOf('pyro','frost').pts=5;relAdd('pyro','frost',1)"); ok('1e clash slowly turns into understanding',ev("relOf('pyro','frost').tone")=='understand' and ev("!!state.socPend"),ev("[relOf('pyro','frost'),state.socPend]"))
    ev("renderHUD()"); W(200); ok('1f important change → 去X看看 in the corner',ev("!!document.querySelector('[data-act=\"soc:go\"]')"))
    ev("socEventRun()"); W(700); t=drain(); ok('1g relationship event plays when you are there + shared memory',len(t)>=3 and ev("(state.sharedMem||[]).some(m=>m.id.startsWith('rel_'))"),t)
    # ---- group
    ev("state.groupLog=null;render()"); W(300); r=ev("groupCheck(true)"); W(700); t=drain(pick='一起聽')
    ok('2a three+ passengers → group event',r and len(t)>=4,t)
    ok('2b group memory records participants',ev("(state.sharedMem||[]).some(m=>m.id.startsWith('g_')&&m.who.length>=3)"))
    # ---- movement
    res=ev("(()=>{ const c={}; for(let i=0;i<60;i++){ const x=roamPick('aelis',['nature','observation']); c[x]=(c[x]||0)+1; } return c; })()")
    ok('3a sense-type passenger prefers the observation car',(res.get('observation',0))>(res.get('nature',0)),res)
    ev("relOf('aelis','felinia').lv=2;state.passengers.felinia.place='nature'")
    res2=ev("(()=>{ let n=0; for(let i=0;i<80;i++){ if(roamPick('aelis',['observation'])==='nature') n++; } return n; })()")
    ok('3b goes to where a friend is',res2>5,res2)
    ev("state.passengers.felinia.place=undefined;relOf('aelis','felinia').firsts.stars=1;state.currentPhase='voyage';state.voyage={to:'starIslands',from:'dawnForest',progress:.5,sky:{type:'meteor',at:.4,started:true,ended:false,watched:false},haps:[]};")
    ok('3c stargazed together → invite each other when a sky event comes',ev("skyInvite()") and ev("atDeck('aelis')&&atDeck('felinia')"))
    # ---- 2 constellation strategy
    ev("state.voyage=null;state.currentPhase='docked';state.passengers.aelis.place=undefined;state.passengers.felinia.place=undefined")
    ev("state.obsN=0"); k0=len(ev("voyObserve('starIslands').known")); ev("state.obsN=8"); k1=len(ev("voyObserve('starIslands').known"))
    ok('4a observation detail grows with experience (not always complete)',k0<k1 and k0<6,[k0,k1])
    m=ev("(()=>{ state.duty.obs={to:'starIslands',lv:'亂流',wall:'亂流',dust:'濃厚',plant:'活躍',anom:'高',known:['wall']}; const v={to:'starIslands'}; const out={}; ['deer','jelly','train','bell','wing','fox',null].forEach(b=>{ state.storyFlags.voyBless=b; state.currentPhase='voyage'; out[b||'none']=voyMods(v); }); state.currentPhase='docked'; state.storyFlags.voyBless=null; return out; })()")
    ok('4b each tendency changes the voyage differently',m['deer'].get('safe')==1 and m['jelly'].get('risk')==1 and m['train'].get('bloom')==1 and m['bell'].get('social')==1 and m['wing'].get('slow')==1 and m['fox'].get('clue')==1,m)
    ok('5a observation × blessing synergy (rough wall+guard, dense dust+explore, lively plants+plant)',m['deer'].get('syn')=='guard' and m['jelly'].get('syn')=='explore' and m['jelly']['xw']['x_starseed']==8 and m['train'].get('syn')=='plant')
    ev("state.duty.obs={to:'starIslands',lv:'平穩',wall:'平穩',dust:'稀薄',plant:'平靜',anom:'低',known:['wall']};state.storyFlags.voyBless='deer';state.currentPhase='voyage'"); g=ev("voyMods({to:'starIslands'})"); ev("state.currentPhase='docked';state.storyFlags.voyBless=null")
    ok('5b same blessing, calm wall → no synergy (no single right answer)',g.get('syn') is None and g.get('safe')==1,g)
    ev("state.consts=['deer'];state.clues=['clue_ring'];constRecAdd('deer','use');constRecAdd('deer','use');constRecAdd('deer','syn')")
    ok('5c long-term: records + story unlock needs exploration/clue too',ev("constDeep('deer')"))
    ev("state.clues=[];state.constRec={};constRecAdd('deer','use');constRecAdd('deer','use');constRecAdd('deer','syn')"); ok('5d repeating alone does not unlock it',not ev("constDeep('deer')"))
    # ---- home constellation event
    ev(base+"state.passengers.felinia.homeTold=0;state.xevHist={};state.currentPhase='voyage';state.voyage={to:'starIslands',from:'dawnForest',progress:.3,haps:[]};state.currentCarriage='observation';render()"); W(300)
    ok('6a home-constellation event is eligible',ev("homeStarWho()")=='felinia' or ev("!!homeStarWho()"))
    who=ev("homeStarWho()"); ev("XRUN.x_homestar({})"); W(600); t=drain()
    ok('6b passenger comes, recognises home stars → memory + record',ev(f"state.passengers['{who}'].place")=='observation' and ev(f"(state.sharedMem||[]).some(m=>m.id==='home_{who}')"),t)
    # ---- 3 resonance
    st=[ev(f"resStage({v})") for v in (5,25,40,55,75,95)]; ok('7a six resonance stages',st==[0,1,2,3,4,5],st)
    ev("state.currentPhase='docked';TAINT.set(40);RUNNING=true;resFx()"); ok('7b subtle visual class per stage',ev("document.body.classList.contains('res-2')"))
    ev("spiritPanel()"); W(400); ok('7c mirror shows the resonance stage',ev("document.querySelector('.mir-res')?.textContent||''").find('深層共鳴')>=0); ev("closeAll()")
    ev("TAINT.set(75);state.currentPhase='outside';state.companion=null;"); ok('7d serious erosion → hidden spots confused',ev("hiddenNow()") is None)
    ev("TAINT.set(95);state.currentPhase='docked';state.currentCarriage='habitat';render()"); ev("act('out','go')") ; W(500)
    ok('7e critical resonance: cannot go out',ev("state.currentPhase")=='docked'); drain()
    ev("TAINT.set(55)"); ok('7f 50+ duty rule kept (scan must re-run)',ev("DUTY_STEPS[0][2]()===false||!state.duty.scan"))
    # ---- 8 passengers/plants/vine with resonance
    ev(base+"state.passengers.sirenora={stage:2,talks:1,records:[],aboard:true,boardedJourney:3};state.resJ={};TAINT.set(40);render()"); W(300)
    ok('8a worried passenger keeps you company',ev("resReact(['sirenora'])")); W(800); drain(); ok('8a2 its company lowers taint',ev("TAINT.val()")<=37,ev("TAINT.val()"))
    ev("state.resJ={};state.passengers.vandora={stage:2,talks:1,records:[],aboard:true};"); ok('8b different passengers react differently (home memory)',ev("RES_TRAIT.vandora")=='home' and ev("RES_TRAIT.aelis")=='speak' and ev("RES_TRAIT.sirenora")=='worry')
    ev("window.STORY_TEST=1;TAINT.set(40);state.resT={};state.pods=[{p:'tidebloom',st:2},null,null,null];state.currentCarriage='nature';state.currentPhase='docked';render();resTick();window.STORY_TEST=0"); W(300)
    ok('8c moon plants show a hidden form and absorb a little taint',ev("(state.resFound||[]).includes('moonform')") and ev("TAINT.val()")==39,ev("TAINT.val()"))
    ok('8d watch-vine reads the resonance',all(len(x)>5 for x in ev("VINE_RES")) and ev("VINE_RES.length")==6)
    # ---- 9/10 explore companions
    ev(base+"TAINT.set(5);state.hiddenFound={};state.compHint={};state.currentPhase='outside';state.companion='felinia';state.passengers.felinia.past={};render()"); W(400)
    ok('9a companion points something out first',ev("compHintTry()")); W(900); t=drain(pick='跟過去')
    ok('9b follow → its own discovery (fly: canopy flower)',ev("!!(state.hiddenFound.df_canopy)"),t)
    ok('10a a place tied to its past → its own story (once)',ev("compPastTry()")); W(900); drain(); ok('10b once only',not ev("compPastTry()") and ev("(state.sharedMem||[]).some(m=>m.id==='past_felinia_dawnForest')"))
    # ---- 11/12 cross events
    picks=ev("(()=>{ const o=[]; state.currentPhase='voyage'; for(let j=1;j<=12;j++){ state.journeyCount=j; state.xevHist={}; const v={to:'starIslands'}; v.mods={}; o.push(xevPick(v)); } state.journeyCount=3; return o; })()")
    ok('11a cross events appear on some voyages, not all',any(picks) and not all(picks),picks)
    ev(base+"state.currentPhase='voyage';state.storyFlags.voyBless=null;state.blessNext=null;state.xevHist={};state.voyage={to:'starIslands',from:'dawnForest',progress:0};state.journeyCount=5;voyPlan(state.voyage)")
    ok('11b voyage still has 2–3 events',2<=ev("state.voyage.haps.length")<=3)
    ev("state.pods=[{p:'bell',st:0},{p:'stardaisy',st:1},null,null];state.materials={};state.clues=[];state.voyage.haps=[{id:'x_starseed',at:.1,on:true,done:false}];state.currentCarriage='observation';render()"); W(300)
    ev("hapRun('observation')"); W(600); drain()
    ok('12a star seed: step 2 moves to the greenhouse',ev("state.voyage.haps.some(h=>h.id==='x_starseed2'&&h.on&&!h.done)") and ev("hapActive('nature')!==null"))
    ev("state.currentCarriage='nature';render()"); W(300); ev("hapRun('nature')"); W(600); drain()
    ok('12b outcome updates plants, materials, clues, history',ev("state.pods[0].st>=1&&state.pods[1].st===2&&matCount('stardust')>=2&&state.clues.includes('clue_starseed')&&state.xevHist.x_starseed.n===1"))
    ev("state.clues=['clue_ring'];TAINT.set(25);state.voyage.haps=[{id:'x_wallecho',at:.1,on:true,done:false}];state.currentCarriage='observation';render()"); W(300); ev("hapRun('observation')"); W(600); t=drain()
    ok('12c wall echo: mirror → telescope → 曦淵 → new clue',ev("state.clues.includes('clue_echo')") and any('渡守' in x for x in t),t)
    ok('13a important event never repeats',ev("xevWeight('x_wallecho',{to:'starIslands'})")==0)
    ev("relOf('felinia','aelis').lv=3;state.passengers.felinia.place=undefined;state.passengers.aelis.place=undefined;state.companion=null;state.currentPhase='voyage';state.currentCarriage='habitat';render()")
    ok('12d trusted pair → secret event eligible',ev("!!secretPair()")); ev("XRUN.x_secret({})"); W(600); drain()
    ok('12e secret → special bond + shared memory',ev("relOf('felinia','aelis').lv")==4 and ev("(state.sharedMem||[]).some(m=>m.id.startsWith('secret_'))"))
    ok('13b same secret never twice',not ev("!!secretPair()&&secretPair()[0].join()==='aelis,felinia'"))
    n0=ev("state.sharedMem.length"); ev("shareMem('secret_aelis|felinia','x',['a'],'x')"); ok('13c shared memories not duplicated',ev("state.sharedMem.length")==n0)
    # memory panel shows shared crystals
    ev("closeAll();state.currentPhase='docked';state.currentCarriage='memory';render();memoryPanel()"); W(800)
    ok('2-6 shared crystals visible in 回憶水晶',ev("document.querySelectorAll('[data-sm]').length")>=3); ev("closeAll()")
    ev("whoPanel()"); W(300); ok('乘客 panel no longer shows 牠們之間 (by request); relations still kept',not ev("!!document.querySelector('.rel-list')") and ev("relList().length")>=1); ev("closeAll()")
    # ---- 14 save / load
    ev("save()"); pg.reload(); W(900)
    ok('14a everything restores after reload',ev("(()=>{const s=load(); return !!(s.rel&&s.rel['aelis|felinia'].lv===4&&s.sharedMem.length>=5&&s.xevHist.x_wallecho.done&&s.constRec&&s.resFound.includes('moonform')&&s.obsN>=0)})()"))
    ev("(()=>{const s=load(); ['rel','relLog','socCD','socPend','sharedMem','groupLog','constRec','obsN','resFound','resHist','resJ','resT','compHint','compEv','xevHist','xevOut'].forEach(k=>delete s[k]); localStorage.setItem(SAVE_KEY,JSON.stringify(s));})()"); pg.reload(); W(900)
    ev("state=load();RUNNING=true;document.querySelector('#mainscreen')?.remove();state.currentPhase='docked';state.currentCarriage='habitat';render();socialStep(true);whoPanel()"); W(300); ev("closeAll();memoryPanel()"); W(400); ev("closeAll()")
    ok('14b legacy save works with all new systems',not errs,errs)
    print('ALL PASS' if all(R) else 'SOME FAIL',len(R))
