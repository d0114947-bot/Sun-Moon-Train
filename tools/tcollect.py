# 必做與收藏、拿掉完成度、速寫影響深度、星塵接上危機
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE=open('tchap.py').read().split('BASE="')[1].split('"\n')[0]
def pax(ids,st=1): return "".join([f"state.discoveredLifeforms.push('{x}');state.passengers['{x}']={{stage:{st},talks:1,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS['{x}'].zone}};" for x in ids])
CH="state.chap={said:{1:1,2:1},arr:{1:1,2:1},ended:[1,2],shown:[1,2,3],fl:[],heart:{},legacy:0,crys1:1,deep:{treeling:2}};"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.CHAP_TEST=1;window.INFO_TEST=1;window.LOCK_TEST=1")
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    ev(BASE+pax(['treeling','felinia'])+CH+"state.sketches={};state.currentCarriage='habitat';save();PANO.active=null;RUNNING=true;render()"); W(800)
    # 必做／收藏
    C=ev("questCats().map(c=>[c.k,!!c.req,!!c.col])")
    ok('Q1 required (main) comes first, rest are collection', C[0][0]=='main' and C[0][1] and all(c[2] for c in C if c[0] not in ('main','daily')), C)
    ev("closeAll();notebookPanel('quest')"); W(700)
    html=ev("[...document.querySelectorAll('.ov.notebook .jr-in')].map(x=>x.innerHTML).join('')+questSection()")
    ok('Q2 notebook says collection is optional', '不用全部完成' in html)
    # 速寫的閘門
    ok('S1 3rd deep story waits for a sketch', ev("deepWait('treeling')")==False and ev("deepSketchWait().includes('treeling')"))
    ok('S2 collection lists the sketch hint', '先畫一張牠的速寫' in ev("questSection()"))
    ev("closeAll();state.sketches={treeling:[0]};save()")
    ok('S3 after a sketch the story is ready', ev("deepWait('treeling')")==True)
    # 速寫提升相遇程度
    ev("state.passengers.felinia.stage=0;sketchBond('felinia');sketchBond('felinia');sketchBond('felinia')")
    ok('S4 sketches raise bond, capped at 熟悉', ev("state.passengers.felinia.stage")==2)
    # 完成度數字
    ev("closeAll();openBook('life')"); W(700)
    t=ev("document.querySelector('.ov.jr').textContent")
    ok('C1 life book: no 尚待相遇 / 完整紀錄', '尚待相遇' not in t and '完整紀錄' not in t and '已遇見' in t, t[:200])
    src=ev("document.documentElement.outerHTML")
    ok('C2 no x/2 sketch counters in code paths', '速寫 ${sketchesOf' not in src and 'sketchesOf(id).length}/2' not in src)
    # 星塵
    ok('D1 meteor hotspot gone', ev("HSDEF.find(h=>h.id==='ot-dust').show()")==False)
    ev("closeAll();crStart('A01',{real:true,sev:2});state.crisis.intel=2;save()")
    L=ev("crActList().map(a=>a.k)")
    ok('D2 crisis offers 接住星塵', 'stardust' in L, L)
    r0=ev("state.crisis.reduce||0"); d0=ev("matCount('stardust')")
    ev("crDo('stardust')"); W(2200)
    ok('D3 dust game opens', ev("!!document.querySelector('.dustgame')"))
    for _ in range(40):
        ev("document.querySelectorAll('.dustgame .dg-mote:not(.got)').forEach(d=>d.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true})))"); W(250)
    W(3500)
    ok('D4 catching ≥5 lowers the crisis and gives stardust', ev("state.crisis.reduce||0")==r0+1 and ev("matCount('stardust')")>d0, [ev("state.crisis.reduce"),r0])
    ok('D5 only once per crisis', ev("crActList().find(a=>a.k==='stardust').why")=='已經接過了')
    ok('Z no page errors', not errs, errs)
    b.close()
print('TOTAL',sum(R),'/',len(R))
