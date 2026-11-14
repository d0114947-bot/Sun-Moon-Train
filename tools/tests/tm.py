from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader'])
    m=b.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True); m.add_init_script("window.ACT1_TEST=true")
    m.goto('http://127.0.0.1:8766/'); m.wait_for_timeout(800)
    m.evaluate("state=freshState();state.chapter='act1';state.act1={stage:'again',tut:5,flags:{},got:['first'],senseN:1,againN:0,passN:0,ended:false,pos:{x:0,y:8,z:0,yaw:0},cz:1800,exT:50,sinceFirst:5,lastPass:-999};save();ACT1.enter()"); m.wait_for_timeout(2500)
    print(m.evaluate("ACT1._dbg().lock"), m.evaluate("ACT1._dbg().P.y"))
    m.evaluate("(()=>{const b=document.querySelector('.a1-u');b.dispatchEvent(new PointerEvent('pointerdown',{pointerId:5,bubbles:true}));})()"); m.wait_for_timeout(2500)
    print(m.evaluate("ACT1._dbg().P.y"), m.evaluate("document.querySelector('.a1-u').className"))
