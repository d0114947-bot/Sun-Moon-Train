# 第二幕前置作業：存檔結構、相容性、掛勾點
import json
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
A1="{stage:'free',tut:5,flags:{high:1,near:1,water:1},got:['first','water'],senseN:3,againN:1,passN:1,ended:true,pos:{x:4,y:9,z:33,yaw:.2},cz:1800,exT:50,sinceFirst:90,lastPass:30}"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.ACT1_TEST=true")
    pg.goto('http://127.0.0.1:8766/'); W(900)
    # 1 new game
    pg.click('#ms-work'); W(1500); pg.click('#ms-new'); W(800)
    ok('W1 new game: world created as unresolved sleeping land', ev("JSON.stringify(state.world)")=='{"location":"sleeping_land","dimension":"unresolved"}', ev("JSON.stringify(state.world)"))
    ok('W2 new game: act2 defaults', ev("JSON.stringify({a:state.act2.firstAnomalySeen,b:state.act2.firstSwitchCompleted,c:state.act2.canSwitch,d:state.act2.freeSwitchTutorialCompleted,e:state.act2.switchCount})")=='{"a":false,"b":false,"c":false,"d":false,"e":0}')
    ok('W3 sceneVariant not stored, derived from dimension', ev("!('sceneVariant' in state.world) && sceneVariantOf('unresolved')==='original' && sceneVariantOf('moon')==='moon'"))
    ok('W4 chapter routing unchanged (act1)', ev("state.chapter")=='act1' and not ev("state.introDone"))
    ev("ACT1.exit()")
    # 2 old act1 save (no world/act2)
    ev(f"state=freshState();state.chapter='act1';state.act1={A1};delete state.world;delete state.act2;save()")
    before=ev("JSON.stringify(load().act1)")
    ev("state=load();ACT1.enter()"); W(800)
    ok('C1 old act1 save loads and gets safe defaults', ev("state.world.dimension")=='unresolved' and ev("state.act2.firstAnomalySeen")==False)
    after=ev("JSON.stringify(Object.assign({},state.act1,{pos:load().act1.pos}))")
    ok('C2 act1 progress untouched', json.loads(before)==json.loads(ev("JSON.stringify(Object.assign({},state.act1,{pos:"+json.dumps(json.loads(before)['pos'])+"}))")), (before,after))
    ok('C3 resumes in free exploration (no Act 2 playback)', ev("ACT1._dbg().stage")=='free' and not ev("state.act2.firstAnomalySeen"))
    ev("ACT1.api.persist()"); ok('C4 world/act2 saved', ev("!!load().world&&!!load().act2"))
    ev("ACT1.exit()")
    # 3 sanitising
    def norm(w,a2):
        ev(f"state=freshState();state.chapter='act1';state.act1={A1};state.world={w};state.act2={a2};ACT1.enter()"); W(300)
        r=ev("({w:state.world,a:state.act2})"); ev("ACT1.exit()"); return r
    r=norm("{location:'sleeping_land',dimension:'moon'}","{firstSwitchCompleted:false}")
    ok('S1 not switched yet -> cannot be in moon', r['w']['dimension']=='unresolved' and r['a']['canSwitch']==False)
    r=norm("{location:'sleeping_land',dimension:'moon'}","{firstAnomalySeen:true,firstSwitchCompleted:true,canSwitch:false,switchCount:3}")
    ok('S2 first switch done -> canSwitch true, moon kept', r['w']['dimension']=='moon' and r['a']['canSwitch']==True and r['a']['switchCount']==3)
    r=norm("{location:'sleeping_land',dimension:'sun'}","{firstSwitchCompleted:true}")
    ok('S3 sun never appears in sleeping land yet -> unresolved', r['w']['dimension']=='unresolved')
    r=norm("{dimension:'xyz',sceneVariant:'moon'}","{switchCount:'-3'}")
    ok('S4 bad values cleaned; stored sceneVariant removed', r['w']['dimension']=='unresolved' and 'sceneVariant' not in r['w'] and r['a']['switchCount']==0 and r['w']['location']=='sleeping_land')
    r=norm("{location:'sleeping_land',dimension:'unresolved'}","{firstAnomalySeen:true}")
    ok('S5 progress flags kept as saved (never auto-advanced)', r['a']['firstAnomalySeen']==True and r['a']['firstSwitchCompleted']==False)
    # 4 hooks
    ok('H1 hook API: known hooks only', ev("(()=>{ try{ ACT1.hook('nope',()=>{}); return false; }catch(e){ return true; } })()"))
    ev(f"window.ACT1_FREEZE=6.5;state=freshState();state.chapter='act1';state.act1={A1};state.act2={{firstAnomalySeen:true,firstSwitchCompleted:true,canSwitch:true}};ACT1.enter()"); W(2500)
    cap=lambda: ev("document.querySelector('.a1-cv').toDataURL()")
    pg.wait_for_function("(()=>{ const c=document.querySelector('.a1-cv'); if(!c) return false; const d=c.getContext('2d').getImageData(c.width/2|0,c.height*.3|0,1,1).data; return d[0]+d[1]+d[2]>30; })()",timeout=30000)   # 畫面真的畫出來了
    h0=cap()
    for _ in range(10):   # 等圖片、材質都載入完成、畫面穩定下來
        W(1000); hx=cap()
        if hx==h0: break
        h0=hx
    ev("window.__hk={pre:0,post:0,logic:0,enter:0,exit:0};ACT1.hook('drawPre',()=>__hk.pre++);ACT1.hook('drawPost',()=>__hk.post++);ACT1.hook('logic',()=>__hk.logic++);ACT1.hook('enter',()=>__hk.enter++);ACT1.hook('exit',()=>__hk.exit++);"); W(2000)
    h1=ev("document.querySelector('.a1-cv').toDataURL()")
    import hashlib; hh=lambda d: hashlib.md5(d.encode()).hexdigest()[:8]
    seq=[hh(h0),hh(h1)]
    for _ in range(3): W(800); seq.append(hh(cap()))
    import base64; open('h0.png','wb').write(base64.b64decode(h0.split(',')[1])); open('h1.png','wb').write(base64.b64decode(h1.split(',')[1]))
    print('SEQ',seq, ev("JSON.stringify({P:ACT1.api.P,cam:ACT1.api.cam,T:ACT1.api.T,spr:ACT1.api.spr,cz:state.act1.cz,frz:window.ACT1_FREEZE})"))
    ok('H2 empty hooks do not change a single pixel', h0==h1)
    ok('H3 draw hooks run every frame', ev("__hk.pre>0&&__hk.post>0"))
    ev("ACT1.exit();window.ACT1_FREEZE=null;ACT1.enter()"); W(1500)
    ok('H4 enter/exit/logic hooks fire', ev("__hk.enter>=1&&__hk.exit>=1&&__hk.logic>0"))
    t0=ev("ACT1.api.T"); W(800); ok('H5 freeze is off by default: time runs', ev("ACT1.api.T")>t0)
    ok('H6 api is read-only view (P, cam, lock)', ev("typeof ACT1.api.P.x==='number'&&typeof ACT1.api.lock==='boolean'"))
    ev("ACT1.exit()")
    # 5 train game untouched
    ev("startNew()"); W(400)
    ok('T1 legacy opening: no world/act2 in train state', ev("!('world' in state)&&!('act2' in state)"))
    ev("(()=>{const s=freshState(); s.introDone=true; s.currentPhase='docked'; s.currentLocation='dawnForest'; localStorage.setItem(SAVE_KEY,JSON.stringify(s));})()")
    pg.reload(); W(900); pg.click('#ms-work'); W(1500); pg.click('#ms-cont'); W(800); pg.click('[data-load="auto"]'); W(1200)
    ok('T2 old train save loads into the train game, no world added', ev("!document.querySelector('#act1')&&RUNNING&&!('world' in state)"))
    ok('Z no page errors', not errs, errs)
    print('ALL PASS' if all(R) else 'SOME FAIL', len(R))
