from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(300)
    ok('F0 every hidden reward id exists',ev("HID_ALL.every(h=>h.give.every(([m])=>m.startsWith('sd:')?!!PLANTS[m.slice(3)]:!!(MATS[m]||COLLECTIBLES[m])))"))
    ok('F0b 24 passengers each have exactly one skill',ev("Object.keys(PASSENGERS).every(id=>Object.values(FORAGE_SKILL).filter(k=>k.ids.includes(id)).length===1)"),ev("Object.keys(PASSENGERS).filter(id=>Object.values(FORAGE_SKILL).filter(k=>k.ids.includes(id)).length!==1)"))
    base="document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.currentLocation='dawnForest';state.visitedLocations=['dawnForest','starIslands'];state.journeyCount=3;state.currentPhase='outside';state.exitFrom='habitat';"
    hs=lambda: ev("[...document.querySelectorAll('#scene [data-hs]')].map(e=>e.dataset.hs)")
    ev(base+"state.companion=null;state.forage=null;state.materials={};render()"); W(500)
    ok('A1 no companion: three fixed spots, no hidden spot',sorted([h for h in hs() if h.startswith('out-f') or h.startswith('out-hid')])==['out-f0-df','out-f1-df','out-f2-df'],hs())
    for i in range(3): ev(f"forageTake({i})"); W(150)
    ev("render()"); W(300)
    ok('A2 taken spots stay gone this stop (no instant respawn)',not [h for h in hs() if h.startswith('out-f')] and ev("!!state.forage.doneAt"),hs())
    ok('A3 forage log written',ev("state.forageLog.dawnForest.found.length")>=1)
    got=[]
    for k in range(3):
        ev("state.forage.doneAt=Date.now()-130000;render()"); W(300)
        vis=[h for h in hs() if h.startswith('out-f')]; got.append((len(vis),ev("state.forage.spots.filter(s=>!s.taken).map(s=>s.m)")))
        if vis: ev(f"forageTake({vis[0][5]})"); W(150)
    ok('C1 regen gives one common material at a time, max twice per stop',[g[0] for g in got]==[1,1,0] and all(all(m in ('dew','mosslight') for m in g[1]) for g in got),got)
    # companions → different hidden spots at the same place
    res={}
    for cid in ['felinia','vandora','treeling','sola','aelis']:
        ev(base+f"state.passengers.{cid}={{stage:2,talks:0,records:[],aboard:true}};state.companion='{cid}';render()"); W(300)
        res[cid]=ev("hiddenNow()&&hiddenNow().id")
    ok('B1 same forest, different companion → different hidden spot',res=={'felinia':'df_canopy','vandora':'df_hollow','treeling':'df_bloom','sola':'df_spring','aelis':'df_glow'},res)
    ev(base+"state.companion='felinia';render()"); W(300)
    ok('B2 hidden spot glows as an important hotspot','out-hid-df' in hs() and ev("document.querySelector('[data-hs=\"out-hid-df\"]').className").find('important')>=0, ev("document.querySelector('[data-hs=\"out-hid-df\"]')?.className"))
    s0=ev("seedN('emberkern')"); ev("hiddenOpen()"); W(400)
    ok('B3 reward + record + journal',ev("seedN('emberkern')")==s0+1 and ev("matCount('pollen')")>=2 and ev("state.hiddenFound.df_canopy.who")=='felinia' and 'df_canopy' in ev("JSON.stringify(state.passengers.felinia.records)+''") or ev("state.passengers.felinia.records.some(r=>r.t.includes('樹冠上的花'))"))
    ev("closeAll();render()"); W(300)
    ok('B4 found once → gone',ev("hiddenNow()") is None and 'out-hid-df' not in hs())
    ev("hiddenOpen()"); ok('B5 no double reward',ev("seedN('emberkern')")==s0+1)
    ok('B6 memory crystal + atlas entry',ev("memsHave().some(m=>m.id==='hid_df_canopy')") and '樹冠上的花' in ev("atlasPages().join('')"))
    ev("state.forage=null;forageTake(3)"); W(200); ok('B7 fly companion 4th spot brings pollen',ev("state.forage.spots[3].m")=='pollen',ev("state.forage.spots[3]"))
    # ancient carving with/without mosslight
    ev(base+"state.passengers.titan={stage:2,talks:0,records:[],aboard:true};state.companion='titan';state.materials.mosslight=0;TAINT.set(30);render()"); W(300)
    ev("hiddenOpen()"); W(400); ok('D1 carving without moss-light: only "just look"',ev("document.querySelectorAll('[data-carve]').length")==1)
    ev("document.querySelector('[data-carve=\"0\"]').click()"); W(300)
    ok('D2 found, unlit, no hotspot until moss-light',ev("state.hiddenFound.df_carving.lit")==0 and ev("hiddenNow()") is None)
    ev("closeAll();state.materials.mosslight=2;render()"); W(300); ml=ev("matCount('mosslight')")
    ok('D3 with moss-light the carving glows again',ev("hiddenNow()&&hiddenNow().id")=='df_carving')
    ev("hiddenOpen()"); W(400); ev("document.querySelector('[data-carve=\"1\"]').click()"); W(300)
    ok('D4 lit: uses 1 moss-light, taint -3, no second item reward',ev("state.hiddenFound.df_carving.lit")==1 and ev("matCount('mosslight')")==ml-1 and ev("TAINT.val()")==27,[ev("matCount('mosslight')"),ev("TAINT.val()")])
    # non-companion conditions
    ev(base+"closeAll();state.companion=null;state.scopeAt=stopKey();render()"); W(300)
    ok('E1 telescope this stop → hidden spot',ev("hiddenNow()&&hiddenNow().id")=='df_scope')
    ev("state.scopeAt=null;TAINT.set(45);render()"); ok('E2 taint ≥40 → shadow path',ev("hiddenNow()&&hiddenNow().id")=='df_shadow')
    ev("TAINT.set(0);state.currentLocation='starIslands';state.skyAt={j:state.journeyCount,type:'tide'};render()"); ok('E3 tide on the way → sandbar',ev("hiddenNow()&&hiddenNow().id")=='si_tide')
    ev("state.skyAt=null;state.collectibles=state.collectibles.filter(x=>x!=='seed_tidebloom');state.passengers.sola={stage:2,talks:0,records:[],aboard:true};state.companion='sola';render()"); ev("hiddenOpen()"); W(300)
    ok('E4 tide pool gives the rare tidebloom seed once',ev("state.collectibles.includes('seed_tidebloom')"))
    # exit chooser
    ev("closeAll();state.currentPhase='docked';state.currentLocation='dawnForest';state.currentCarriage='habitat';state.companion=null;render();exitChooser(()=>{})"); W(400)
    t=ev("document.querySelector('.zask').innerText"); ok('X1 exit chooser shows skills and ✦',('飛行' in t or '夜行' in t) and '✦' in t,t)
    ev("closeAll()")
    # save/load
    ev("save()"); pg.reload(); W(900)
    ok('S1 found spots, log, lit state survive reload',ev("(()=>{const s=load(); return !!(s.hiddenFound.df_canopy&&s.hiddenFound.df_carving.lit===1&&s.forageLog.dawnForest)})()"))
    ev("(()=>{const s=load(); delete s.hiddenFound; delete s.forageLog; delete s.scopeAt; delete s.skyAt; s.forage={key:'x',spots:[]}; localStorage.setItem(SAVE_KEY,JSON.stringify(s));})()"); pg.reload(); W(900)
    ev("state=load();RUNNING=true;document.querySelector('#mainscreen')?.remove();state.currentPhase='outside';state.currentLocation='dawnForest';state.companion=null;render()"); W(400)
    ok('S2 legacy save loads: forage + atlas + memories fine',ev("!!forageNow()&&hiddenNow()===null&&atlasPages().length>0&&memsHave().length>=0"))
    ok('Z no page errors',not errs,errs)
    print('ALL PASS' if all(R) else 'SOME FAIL',len(R))
