# 新玩家容易卡住的地方：星途符牒的確認方式、序章第一次出發的號誌等待、主畫面
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(900)
    ev("document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();state=freshState();state.introDone=true;state.currentCarriage='cab';state.spirit.equipment.tablet=true;save();RUNNING=true;render();briefPanel()"); W(600)
    ok('B1 first time: how-to line in the panel', '再輕觸一次' in ev("document.querySelector('#layer .ov').innerText"))
    W(4500)
    for i in range(5): ev(f"document.querySelector('.tl[data-i=\"{i}\"] .k').click()"); W(150)
    ok('B2 tapping a revealed row again confirms it (no need to hit the small circle)', ev("state.duty.briefing"))
    ev("closeAll();state.duty.briefing=false;briefPanel()"); W(300)
    ok('B3 hint gone once learned', '再輕觸一次' not in ev("document.querySelector('#layer .ov').innerText"))
    ev("closeAll()")
    # 號誌：序章第一次出發（亂流）只等一下
    ev("state.currentLocation='dawnForest';state.routeNext='starIslands'"); print('wall',ev("[nextStop(),wallLv(nextStop())]"))
    ev("state.act3={trainSeen:true,obs:['carving'],entered:true,introduced:true,canDepart:true};state.prologueDone=false;state.journeyCount=0")
    ok('S1 prologue first departure: short wait', ev("sigWhy().k")=='wall' and ev("sigWhy().sec")<=10)
    ev("state.prologueDone=true"); ok('S2 after the prologue: normal wait', ev("sigWhy().sec")==50)
    ev("delete state.act3;state.prologueDone=false"); ok('S3 legacy: normal wait', ev("sigWhy().sec")==50)
    ok('S4 SIG_WHY table unchanged', ev("SIG_WHY[1].sec")==50)
    ok('Z no page errors', not errs, errs)
    print('ALL PASS' if all(R) else 'SOME FAIL', len(R))
