# 序章期間（新遊戲）不插入：隨機登車、乘客邀約、航行小事件、地球消息、列車成長事件；序章結束後恢復
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(900)
    base="document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();state=freshState();state.introDone=true;state.currentLocation='dawnForest';state.currentPhase='docked';state.visitedLocations=['dawnForest'];"
    ev(base+"state.act3={entered:true,introduced:true,canDepart:true};state.discoveredLifeforms=['sola'];state.passengers.sola={stage:2,talks:2,records:[],aboard:true,zone:'rings'};")
    ok('Q1 prologue: no random boarders', ev("proQuiet()") and ev("rollBoarders().length")==0)
    ev("state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'starIslands',progress:.2}")
    ok('Q2 prologue: no voyage mini-events on the first voyage', ev("voyPlan(state.voyage).length")==0)
    ok('Q3 prologue: passengers do not ask to go somewhere', ev("askRoll('sola')")==False)
    ev("state.prologueDone=true;state.voyage={from:'dawnForest',to:'starIslands',progress:.2}")
    ok('Q4 after the prologue: voyage mini-events are back', ev("voyPlan(state.voyage).length")>0 and not ev("proQuiet()"))
    ev("state=freshState();state.introDone=true;state.currentLocation='dawnForest';state.currentPhase='docked';state.visitedLocations=['dawnForest']")
    ok('Q5 legacy game: nothing is held back', not ev("proQuiet()") and ev("rollBoarders().length")>=0)
    ev("closeAll();state.carPol={habitat:5};state.materials={mosslight:1};state.currentCarriage='cab';render();crPanel()"); W(600)
    ev("document.querySelector('#layer [data-pur]').click()"); W(800)
    ok('Q6 purifying a carriage from the response panel: no page error', not errs and ev("state.carPol.habitat")==0, errs)
    ev("state.crisis=null;state.journeyCount=0;crStart('T01',{sev:1,real:true});window.CRISIS_TEST=true;state.crisis.stage='W4';crOutbreak()")
    ok('Q7 outbreak on journey 0 is recorded as burst', bool(ev("state.crisis.burst")) and '危機還沒處理完' in (ev("crBlockDepart()") or ''))
    print('ALL PASS' if all(R) else 'SOME FAIL', len(R))
