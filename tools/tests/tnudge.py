from playwright.sync_api import sync_playwright
A1="stage:'free',tut:5,flags:{high:1,near:1,water:1},got:['first','water','curtain','still'],senseN:3,againN:1,passN:2,ended:true,cz:1800,exT:50,sinceFirst:200,lastPass:100"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.ACT1_TEST=true"); pg.goto('http://127.0.0.1:8766/'); W(900)
    # 第二幕剛完成：在水幕前，面向水幕（縫隙在背後）
    ev("state=freshState();state.chapter='act1';state.act1={"+A1+",pos:{x:0,y:30,z:1750,yaw:0}};state.world={location:'sleeping_land',dimension:'unresolved'};state.act2={firstAnomalySeen:true,firstSwitchCompleted:true,canSwitch:true,freeSwitchTutorialCompleted:true,switchCount:4,trail:[],trailSeen:true,trailMark:0,completed:false};save();ACT1.enter()"); W(3000)
    ev("state.act2.completed=true"); 
    got=''
    for _ in range(40):
        W(500); got=ev("document.querySelector('.a1-say').textContent")
        if '星光' in got: break
    print('NUDGE:',got, errs)
