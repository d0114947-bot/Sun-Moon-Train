# 展望台分流、植物精簡、進化線三條、當下決定接主線與種子
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
    ev(BASE+pax(['skywhale'])+"state.chap={said:{1:1},arr:{1:1},ended:[1],shown:[1,2],fl:[1],heart:{},legacy:0,crys1:1};state.trainEvo={repair:1,nature:1,sanct:1,ancient:2,guard:1,sky:2};save();PANO.active=null;RUNNING=true;render()"); W(600)
    # 展望台
    S=ev("['hap-observatory','ot-spot','res-light','ot-cross'].map(id=>{const h=HSDEF.find(x=>x.id===id);return [h.at.x,h.at.y,typeof h.name==='function'?h.name():h.name]})")
    ok('O1 sky happenings share one spot', len({(a,b) for a,b,_ in S})==1 and S[0][2]=='天空裡的動靜', S)
    ok('O2 at most one shows at a time', ev("(()=>{ const ids=['hap-observatory','ot-spot','res-light','ot-cross']; return ids.filter(id=>HSDEF.find(h=>h.id===id).show()).length<=1 })()"))
    ev("state.currentCarriage='observation';render();constPanel()"); W(700)
    ok('O3 star projection now lives in the constellation dial', ev("!!document.querySelector('.ov.csov .cs-otproj')"))
    ev("document.querySelector('.cs-otproj').click()"); W(900)
    ok('O4 projection opens', ev("document.querySelectorAll('#layer .ov:not(.closing)').length")>=1 and not errs, errs)
    ev("closeAll()"); W(400)
    # 植物
    ok('P1 three plant families', ev("traitOf('starspore')")=='moon' and ev("['dawn','moon','calm'].includes(traitOf('glowcap'))") and ev("new Set(Object.keys(PLANTS).map(traitOf)).size")<=3, ev("[...new Set(Object.keys(PLANTS).map(traitOf))]"))
    ok('P2 no more hybrids / sky blooming', ev("Object.keys(HYB).length")==0 and ev("Object.values(SKY_BLOOM).every(a=>!a.length)"))
    ok('P3 sample shelf moved into the life book', ev("HSDEF.find(h=>h.id==='nat-samples').show()")==False)
    ev("state.grown=['bell'];save();openBook('life')"); W(600)
    ok('P4 life book has 植物樣本 tab', '植物樣本' in ev("[...document.querySelectorAll('.booknav button')].map(b=>b.textContent).join('|')"))
    ev("closeAll()"); W(300)
    # 進化線
    ok('E1 three lines', ev("evoToast('sky')").startswith('✦ 列車的變化・拾光的記憶') and ev("evoToast('sanct')").startswith('✦ 列車的變化・溫室與生命') and ev("evoToast('repair')").startswith('✦ 列車的變化・列車修復'))
    ok('E2 merged stage rises with sub-lines', ev("evoLineStage(EVO_LINE[2])")==2)
    # 當下決定：主線
    ev("state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'starIslands',progress:.4,evt:true};save()")
    ok('C1 chapter decision first', ev("decPick()")=='ch2', [ev("chapCur()"),ev("decPick()")])
    ev("decideNow()"); W(500)
    t=ev("document.querySelector('.decov').textContent")
    ok('C2 card names the chapter and offers the hero option', '雲海' in t and '第 2 章' in t and '請雲海巨鯨龍唱歌' in t, t[:200])
    n0=ev("seedTotal()")
    ev("document.querySelector('.decov [data-dec=\"hero\"]').click()"); W(400)
    ok('C3 hero option gives a seed from a lost world', ev("seedTotal()")==n0+1 and ev("Object.values(state.decSeedFrom).some(v=>v.includes('小雲鯨'))"))
    ok('C4 written into the hero journey story', '唱了歌' in ev("journeyStory('skywhale')"))
    ok('C5 chapter decision only once', ev("decPick()")!='ch2')
    ev("closeAll()"); W(300)
    ok('C6 seed origin shows in the plant entry', '小雲鯨' in (ev("plantOrigin(Object.keys(state.decSeedFrom)[0])") or ''))
    # 一般的決定也會留下種子
    n0=ev("seedTotal()"); ev("decideNow('sos')"); W(300); ev("document.querySelector('.decov [data-dec=\"go\"]').click()"); W(300)
    ok('G1 rescuing the glimmer brings a seed', ev("seedTotal()")==n0+1)
    ev("closeAll()"); W(300)
    ok('Z no page errors', not errs, errs)
    b.close()
print('TOTAL',sum(R),'/',len(R))
