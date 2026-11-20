# 當下要決定：卡片、三種傾向、曦淵的暗示、傾向決定結局
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE=open('tchap.py').read().split('BASE="')[1].split('"\n')[0]
def pax(ids,st=2): return "".join([f"state.discoveredLifeforms.push('{x}');state.passengers['{x}']={{stage:{st},talks:3,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS['{x}'].zone}};" for x in ids])
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.CHAP_TEST=1;window.INFO_TEST=1")
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    ev(BASE+pax(['treeling'])+"state.chap={said:{},arr:{},ended:[],shown:[1],fl:[],heart:{},legacy:0,crys1:1};state.currentPhase='voyage';state.voyage={from:'origin',to:'dawnForest',progress:.4,evt:true};save();PANO.active=null;RUNNING=true;render()"); W(500)
    # 卡片
    ev("decideNow('ch1')"); W(600)
    C=ev("[...document.querySelectorAll('.decov .dec-card')].map(c=>[c.dataset.dec,c.className,c.querySelector('.dc-t')&&c.querySelector('.dc-t').textContent])")
    ok('K1 three cards, one per leaning', len(C)==3 and {c[1].split('t-')[1] for c in C}=={'self','let','all'}, C)
    ok('K2 each card shows its leaning with a small icon', all(c[2] in ('自己伸手','放手','交給大家') for c in C) and ev("document.querySelectorAll('.decov .dec-card .dc-t svg').length")==3)
    ev("document.querySelector('.decov .dec-card.t-all').click()"); W(400)
    ok('K3 picked card is marked; leaning recorded', ev("!!document.querySelector('.dec-card.picked.t-all')") and ev("state.lean.all")==1)
    ev("closeAll()"); W(400)
    # 主角不在：也有「交給大家」
    ev("state.passengers.treeling.aboard=false;"+pax(['felinia'],1)+"state.chap.dec={};save();decideNow('ch1')"); W(600)
    t=ev("document.querySelector('.decov .dec-card.t-all').textContent")
    ok('K4 hero absent: a familiar passenger offers to help', '羽貓獸' in t, t)
    n0=ev("seedTotal()"); ev("document.querySelector('.decov .dec-card.t-all').click()"); W(300)
    ok('K5 that card also brings a seed', ev("seedTotal()")==n0+1)
    ev("closeAll()"); W(400)
    # 沒有決定：算一點點「放手」
    l0=ev("state.lean.let"); ev("decideNow('frag')"); W(300); ev("closeAll()"); W(900)
    ok('K6 letting the timer run out counts as a little letting go', abs(ev("state.lean.let")-l0-.5)<1e-6)
    # 曦淵的暗示
    ev("window.DEC_TEST=1;state.lean={self:0,all:2,let:.5};save();decideNow('lights')"); W(300)
    ev("document.querySelector('.decov [data-dec=\"slow\"]').click()"); W(200); ev("closeAll()"); W(300)
    ev("state.lean.all=2;save();decideNow('frag')"); W(300); ev("document.querySelector('.decov .dec-card.t-all')?document.querySelector('.decov .dec-card.t-all').click():decLean({t:'all'})"); W(200); ev("closeAll()")
    if ev("state.lean.all")<3: ev("decLean({t:'all'})")
    seen=False
    for _ in range(12):
        W(500)
        if ev("!!document.querySelector('#layer .dlg')"): seen='熱鬧' in pg.inner_text('#layer .dlg'); break
    ok('H1 曦淵 hints at the leaning, without numbers', seen)
    ev("document.querySelectorAll('#layer .dlg').forEach(d=>d.remove());window.DEC_TEST=0")
    # 結局
    ev("state.storyFlags.departTaint=10;state.chap.ended=[1,2,3,4];state.collectibles=state.collectibles.concat(['keep_sola','keep_aelis']);save()")
    def end(lean): return ev(f"(()=>{{state.lean={lean};return endingType()}})()")
    ok('E1 mostly 交給大家 → 晨曦', end("{all:5,self:1,let:1}")=='dawn')
    ok('E2 mostly 自己伸手 → 歸光', end("{all:1,self:5,let:1}")=='return')
    ok('E3 mostly 放手 → 守望', end("{all:1,self:1,let:5}")=='watch')
    ev("state.storyFlags.departTaint=40;save()")
    ok('E4 not enough light → 長夜 whatever the leaning', end("{all:5,self:0,let:0}")=='night')
    ev("state.storyFlags.departTaint=10;state.chap.ended=[];state.collectibles=state.collectibles.filter(x=>!x.startsWith('keep_'));save()")
    ok('E5 too few keepsakes and hearts → 長夜', end("{all:5,self:0,let:0}")=='night')
    ok('E6 守望 ending exists with its own lines', ev("ENDINGS.watch.title")=='守望' and len(ev("ENDINGS.watch.lines"))>=5)
    ev("state.chap.ended=[1,2,3,4];state.lean={all:0,self:0,let:4};save()")
    ok('E7 finale reflects the leaning', any('離開' in x for x in ev("finaleExtra()")))
    ev("playFinale()"); W(500)
    for _ in range(60):
        if ev("!!document.querySelector('#layer .ov h2')"): break
        ev("document.querySelector('#layer .cine')&&document.querySelector('#layer .cine').click()"); W(550)
    ok('E8 watch ending plays through to its own end page', ev("document.querySelector('#layer .ov h2')&&document.querySelector('#layer .ov h2').textContent")=='守望' and ev("state.ending")=='watch')
    ok('Z no page errors', not errs, errs)
    b.close()
print('TOTAL',sum(R),'/',len(R))
