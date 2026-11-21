# 新插圖與影片：決定卡片、終幕與結局、古種解封、回憶、星河浮島第二張景、事件影片
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE=open('tchap.py').read().split('BASE="')[1].split('"\n')[0]
px="state.discoveredLifeforms.push('skywhale');state.passengers.skywhale={stage:2,talks:3,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS.skywhale.zone};"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]; bad=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('response',lambda r: bad.append(r.url) if r.status>=400 else None)
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    ev(BASE+px+"state.currentPhase='voyage';state.voyage={from:'dawnForest',to:'starIslands',progress:.4,evt:true};save();PANO.active=null;RUNNING=true;render();decideNow('ch2')"); W(1200)
    imgs=ev("[...document.querySelectorAll('.decov .dec-card .dc-art img')].map(i=>[i.getAttribute('src'),i.naturalWidth])")
    ok('A1 chapter-2 cards show their illustrations', len(imgs)==3 and all(w>0 for _,w in imgs), imgs)
    ev("closeAll()"); W(400)
    def cineimg(js):
        ev("document.querySelectorAll('#layer .cine').forEach(c=>c.remove());"+js); W(700)
        r=ev("(()=>{const i=document.querySelector('#layer .cine > img');return i?[i.getAttribute('src'),i.naturalWidth]:null})()"); return r
    for name,js,f in [('finale',"cine(FINALE,()=>{})",'end-finale'),('dawn',"cine(ENDINGS.dawn.lines,()=>{})",'end-dawn'),('return',"cine(ENDINGS.return.lines,()=>{})",'end-return'),('night',"cine(ENDINGS.night.lines,()=>{})",'end-night'),('watch',"cine(ENDINGS.watch.lines,()=>{})",'end-watch'),('unseal',"cine(['森羅溫室的方向，傳來很輕的一聲「喀」。','x'],()=>{})",'seed-unseal')]:
        r=cineimg(js); ok(f'B {name}: background illustration', r and f in r[0] and r[1]>0, r)
    ev("document.querySelectorAll('#layer .cine').forEach(c=>c.remove());state.clues=['clue_dragon'];state.trainEvo={repair:3};state.oldEcho={};save();oldPlay('lastdawn',true)"); W(1500)
    ok('C1 memory 最後一道晨曦: 拾光 and 曦淵 behind the dialogue', ev("!!document.querySelector('.xevvid.memimg img')") and ev("document.querySelector('.xevvid.memimg img').naturalWidth")>0)
    ev("document.querySelectorAll('#layer .dlg,#layer .xevvid').forEach(d=>d.remove())")
    ok('D1 星河浮島 has a second scene', 'starIslands-2' in (ev("LOC_IMG2.starIslands") or ''))
    ok('E1 five more voyage events play their videos', ev("['x_starseed','x_bloom','x_wallecho','x_homestar','x_lostlight'].every(k=>XRUN[k].toString().includes('xevVidWhenTalk'))"))
    ev("xevVidWhenTalk('assets/xev-homestar.mp4','assets/xev-homestar.jpg');dialogueScript([['self','窗外的星光特別亮。']])"); W(800)
    ok('E2 video starts once the event starts talking', ev("!!document.querySelector('.xevvid video')") and 'homestar' in ev("document.querySelector('.xevvid video').getAttribute('src')"))
    ok('Z no page errors / missing files', not errs and not [u for u in bad if 'assets/' in u], [errs,bad])
    b.close()
print('TOTAL',sum(R),'/',len(R))
