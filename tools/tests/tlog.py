from playwright.sync_api import sync_playwright
S='/tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout
    pg.goto('http://127.0.0.1:8766/'); W(800)
    ev("""document.querySelector('#mainscreen')?.remove();RUNNING=true;state=freshState();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.currentPhase='docked';state.currentLocation='starIslands';state.journeyCount=2;
    state.log=[{j:0,t:'值勤量測：界染度 7/100，判定「純淨」。'},{j:0,t:'領取了星途符牒。'},{j:0,t:'領取了星軌羅盤。'},{j:0,t:'核對值勤資訊：日月 001 次，預定停靠晨曦森林。'},{j:0,t:'確認前方星光號誌：綠光，平安號誌。'},{j:0,t:'向領頭曦淵報備，取得出發許可（日月 001 次）。'},
    {j:1,t:'列車自沉睡之地出發，抵達晨曦森林。'},{j:1,t:'露米（界域生命）登上了列車。'},{j:1,t:'在古樹上發現與列車相同的圓環刻痕，留下拓印。'},
    {j:1,t:'值勤量測：界染度 9/100，判定「純淨」。'},{j:1,t:'向領頭曦淵報備，取得出發許可（日月 002 次）。'},{j:2,t:'羽貓獸（異界生命）登上了列車。'},{j:2,t:'列車自晨曦森林出發，抵達星河浮島。'},{j:2,t:'在晶體縫隙找到星塵孢子。'},{j:2,t:'值勤量測：界染度 5/100，判定「純淨」。'}];
    render(); journeyPanel()""")
    W(900); pg.screenshot(path=S+'/log.png')
    ev("closeAll();state.currentCarriage='memory';render()"); pg.wait_for_function("PANO.ready.memory===true",timeout=15000); W(500)
    names=ev("[...document.querySelectorAll('#scene [data-hs]')].map(e=>e.querySelector('.lb')&&e.querySelector('.lb').textContent)")
    print(names)
    b.close()
