# 危機的畫面效果：震動、搖晃、黑霧、車外視角
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE=open('tchap.py').read().split('BASE="')[1].split('"\n')[0]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.CRISIS_TEST=1")
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    ev(BASE+"state.currentCarriage='habitat';state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'starIslands',progress:.4,evt:true};save();PANO.active=null;RUNNING=true;render()"); W(500)
    # 黑霧
    ev("crStart('D04',{real:true,sev:2});state.crisis.stage='W3';save()"); W(1600)
    ok('F1 turbid crisis: fog in the affected car', ev("document.getElementById('crfog').className")=='f2')
    ev("state.crisis.stage='W4';save()"); W(1500)
    ok('F2 outbreak: fog thickest', ev("document.getElementById('crfog').className")=='f3')
    ev("state.currentCarriage='nature';render()"); W(1500)
    ok('F3 other cars: lighter fog', ev("document.getElementById('crfog').className")=='f2')
    ev("state.crisis=null;state.carPol={nature:70};save()"); W(1500)
    ok('F4 heavily polluted car keeps a thin fog', ev("document.getElementById('crfog').className")=='f1')
    ev("state.carPol={};save()"); W(1500)
    ok('F5 clean car: no fog', ev("document.getElementById('crfog').className")=='')
    # 攻擊：震動
    ev("crStart('B03',{real:true,sev:2});state.crisis.stage='W3';save();crOutbreak()"); W(700)
    ok('S1 attack: screen shakes on outbreak', ev("document.body.classList.contains('cr-shake-big')"))
    W(1500); ev("closeAll();document.querySelectorAll('#layer .dlg').forEach(d=>d.remove());state.crisis=null;save()")
    ev("crStart('A02',{real:true,sev:2});state.crisis.stage='W3';save();crOutbreak()"); W(700)
    ok('S2 turbulence: carriage sways', ev("document.body.classList.contains('cr-sway')"))
    W(1500); ev("closeAll();document.querySelectorAll('#layer .dlg').forEach(d=>d.remove());state.crisis=null;save()")
    # 故障：車外視角
    ev("crStart('C04',{real:true,sev:2});state.crisis.stage='W3';save();crOutbreak()"); W(1800)
    ok('C1 malfunction: cut to the outside of the train', ev("!!document.querySelector('.cine.crext img')") and '連接處' in ev("document.querySelector('.cine.crext').textContent+[...document.querySelectorAll('.cine.crext')].length"), ev("document.querySelector('.cine')&&document.querySelector('.cine').outerHTML.slice(0,200)"))
    for _ in range(4): ev("document.querySelector('.cine')&&document.querySelector('.cine').click()"); W(600)
    W(800)
    ok('C2 then back inside: the crisis dialogue', ev("!!document.querySelector('#layer .dlg')"))
    ok('Z no page errors', not errs, errs)
    b.close()
print('TOTAL',sum(R),'/',len(R))
