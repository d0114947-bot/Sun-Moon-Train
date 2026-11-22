# 車廂裡的金色徽章（UI 圖標）
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE=open('tchap.py').read().split('BASE="')[1].split('"\n')[0]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]; bad=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('response',lambda r: bad.append(r.url) if r.status>=400 else None)
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    ev(BASE+"state.trainEvo={ancient:3,guard:1};save();PANO.active=null;RUNNING=true;")
    exp={'cab':['em-repair','em-prep'],'memory':['em-ancient','em-guard'],'nature':['em-nature'],'habitat':['em-sanct','em-pax'],'observatory':['em-sky']}
    for c,ids in exp.items():
        ev(f"state.currentCarriage='{c}';render()"); W(900)
        got=ev("[...document.querySelectorAll('.hs.emblem')].map(e=>[e.dataset.hs,e.querySelector('img').naturalWidth])")
        ok(f'E1 {c}: emblems on the walls/floor', sorted(g[0] for g in got)==sorted(ids) and all(w>0 for _,w in got), got)
    ev("state.currentCarriage='memory';render()"); W(800)
    o=ev("['em-ancient','em-guard'].map(id=>+document.querySelector(`[data-hs=${id}]`).style.getPropertyValue('--eo'))")
    ok('E2 brighter as the line grows', o[0]>o[1], o)
    ry=ev("[document.querySelector('[data-hs=em-ancient]').style.getPropertyValue('--ry'),document.querySelector('[data-hs=em-guard]').style.getPropertyValue('--ry')]")
    ok('E3 刻紋拓本 emblem lies on the floor, 渡守 emblem on the wall', ry==['0deg','-52deg'] and ev("document.querySelector('[data-hs=em-ancient]').classList.contains('floor')"), ry)
    pg.mouse.move(100,300); W(300); a=ev("document.querySelector('[data-hs=em-ancient]').style.getPropertyValue('--dry')"); pg.mouse.move(1200,300); W(300); c2=ev("document.querySelector('[data-hs=em-ancient]').style.getPropertyValue('--dry')")
    ok('E4 tilt changes as you look around', a!=c2 and a and c2, [a,c2])
    ev("document.querySelector('[data-hs=em-guard]').click()"); W(700)
    ok('E5 emblems are decor only (clicking does nothing)', ev("getComputedStyle(document.querySelector('[data-hs=em-guard]')).pointerEvents")=='none')
    ok('Z no page errors / missing files', not errs and not [u for u in bad if 'assets/' in u], [errs,bad])
    b.close()
print('TOTAL',sum(R),'/',len(R))
