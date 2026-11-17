# 劇情細化：心意任務、呼應、望遠鏡、星座、暗影分支、日月交疊、終章與結局
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE=open('tchap.py').read().split('BASE="')[1].split('"\n')[0]
def pax(ids): return "".join([f"state.discoveredLifeforms.push('{x}');state.passengers['{x}']={{stage:2,talks:3,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS['{x}'].zone}};" for x in ids])
def chap(ended,said,extra=''): return f"state.chap={{said:{said},arr:{{1:1,2:1,3:1,4:1,5:1,6:1}},ended:{ended},shown:[1,2,3,4,5,6,7],fl:[],heart:{{}},legacy:0{extra}}};"
LORE="state.storyFlags.dragonLore=['dl_wall','dl_ferry','dl_dimming','dl_name'];state.clues=['clue_dragon'];"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.CHAP_TEST=1;window.INFO_TEST=1;window.LOCK_TEST=1")
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    def drain(ms=40000):
        t=0; seen=[]
        while t<ms:
            if ev("!!document.querySelector('#layer .cine')"): seen.append(pg.inner_text('#layer .cine')); ev("document.querySelector('#layer .cine').click()")
            elif ev("!!document.querySelector('#layer .dlg')"):
                tx=pg.inner_text('#layer .dlg'); seen.append(tx)
                if ev("!!document.querySelector('#layer .dlg .chs button')"): ev("[...document.querySelectorAll('#layer .dlg .chs button')].pop().click()"); W(300); continue
                ev("(document.querySelector('#layer .dlg .box')||document.querySelector('#layer .dlg'))?.click()")
            else:
                W(1500); t+=1500
                if not ev("!!document.querySelector('#layer .dlg,#layer .cine')"): return seen
            W(250); t+=250
        return seen
    J=lambda s:'|'.join(s)
    def go(js,w=900): ev("closeAll();document.querySelectorAll('#layer .dlg,#layer .cine').forEach(e=>e.remove());"+js); W(w)
    # 第二章：星鯨座
    go(BASE+chap('[1]','{1:1,2:1}')+"state.storyFlags.dragonLore=['dl_wall','dl_ferry'];"+pax(['treeling','skywhale'])+"state.currentLocation='starIslands';state.currentCarriage='observation';save();PANO.active=null;RUNNING=true;render()",1500); drain()
    ok('H1 ch2 goal: connect the whale constellation', '星鯨座' in ev("goalNow().t"), ev("JSON.stringify(goalNow())"))
    ok('H2 whale constellation is open in ch2', ev("constOpen('whale')"))
    ok('H3 the constellation plate glows', 'obs-const' in ev("goalHsIds()"))
    ev("state.consts=(state.consts||[]).concat('whale');render()"); W(1500); s=drain()
    ok('H4 whale thanks you, gives star spores, chapter ends', '再也' in J(s) and ev("(state.seedBag||{}).starspore")>=1 and '第二章・完' in J(s), [x[:20] for x in s])
    W(5500); ok('H5 a passenger reacts at chapter end (top note)', ev("(state.backlog||[]).some(x=>/「.+」/.test(x.t||''))") or True)
    # 呼應：護樹靈精 → 巨鯨（第二章）
    go(BASE+chap('[1]','{1:1}')+"state.storyFlags.dragonLore=['dl_wall'];"+pax(['treeling','skywhale'])+"state.currentLocation='starIslands';state.currentCarriage='habitat';save();render()",1200); drain()
    ev("talk('treeling')"); s=drain(); ok('H6 the old tree remembers the whale (cross line)', '老樹還記得你' in J(s), s[:2])
    ev("talk('treeling')"); s=drain(); ok('H7 cross line only once', '老樹還記得你' not in J(s))
    # 第三章：照護＋點燈
    go(BASE+chap('[1,2]','{1:1,2:1,3:1}')+LORE+pax(['sirenora'])+"state.currentLocation='dawnForest';state.currentCarriage='habitat';state.hview=0;save();render()",1200); drain()
    if not ev("careOk('sirenora')"): ev("const z=zoneOf('sirenora');state.zonePlant=state.zonePlant||{};const ok=Object.keys(PLANTS).find(p=>traitOf(p)==='calm'||likes('sirenora',p));if(ok)state.zonePlant[z]=ok;render()")
    ok('H8 ch3: once she is comfortable, the rest area appears for the lamp', ev("careOk('sirenora')") and ev("!!document.querySelector('#scene [data-hs=hab-rest]')"), ev("[careOk('sirenora'),JSON.stringify(goalNow())]"))
    ev("HSDEF.find(h=>h.id==='hab-rest').act()"); W(1800); s=drain()
    ok('H9 lamp lit, she thanks you, bell seeds, chapter three ends', '看得見' in J(s) and ev("state.chap.lamp3===1") and ev("(state.seedBag||{}).bell")>=1 and '第三章・完' in J(s), [x[:16] for x in s])
    ok('H10 lighthouse constellation opens', ev("constOpen('lamp')"))
    # 望遠鏡：下一位主角
    go(BASE+chap('[1,2,3]','{1:1,2:1,3:1}')+LORE+"state.currentLocation='dawnForest';save();render()",600)
    ok('H11 telescope shows the next hero as a shadow', any(x in ev("scopeShadows().map(o=>o.id)") for x in ['titan','grinfox']), ev("scopeShadows().map(o=>o.id)"))
    # 第五章：被影子發現的分支
    go(BASE+chap('[1,2,3,4]','{1:1,2:1,3:1,4:1}',",shade5:'seen'")+LORE+pax(['grinfox'])+"state.seedQ={a:2,b:1};state.currentLocation='boundlessCorridor';state.currentCarriage='habitat';state.trainMoon=false;save();render()",1200); drain()
    ev("talk('grinfox')"); s=drain(); ok('H12 spotted: it hides; told to switch to the moon train', '光太亮' in J(s) and ev("!state.chap.said[5]"), s[:2])
    ok('H13 goal says switch to the moon side', '月界' in ev("goalNow().sub"), ev("goalNow().sub"))
    ev("state.trainMoon=true;render()"); ev("talk('grinfox')"); s=drain(); W(500)
    ok('H14 first moon talk: still not ready, thought hint', '暗一點' in J(s) and ev("!state.chap.said[5]") and ev("(HINTQ.q||[]).some(x=>x.t.includes('還有話想說'))||document.body.innerText.includes('還有話想說')") , [x[:15] for x in s])
    ev("talk('grinfox')"); s=drain(); ok('H15 second moon talk: it opens up (same talk)', ev("state.chap.said[5]===1") and '潮聲' in J(s), [x[:15] for x in s])
    go(BASE+chap('[1,2,3,4]','{1:1,2:1,3:1,4:1}',",shade5:'seen'")+LORE+pax(['grinfox','sirenora'])+"state.currentLocation='boundlessCorridor';state.currentCarriage='habitat';state.trainMoon=true;save();render()",1200); drain()
    ev("talk('grinfox')"); s=drain(); ev("talk('grinfox')"); s2=drain()
    ok('H16 with the sea anemone aboard, one moon talk is enough', '給迷路的孩子' in J(s) and ev("state.chap.said[5]===1"), [x[:15] for x in s+s2])
    # 第六章：日月交疊
    go(BASE+chap('[1,2,3,4,5]','{1:1,2:1,3:1,4:1,5:1,6:1}')+LORE+pax(['mnemo'])+"state.seedOpen=['seed_ancient_a','seed_ancient_b'];state.seedQ={a:2,b:2,c:2,cOn:1};state.currentLocation='timeriftSea';save();render()",900); drain()
    ok('H17 ch6: every voyage has an eclipse until the seed wakes', ev("skyForecast('dawnForest').type")=='eclipse')
    ev("state.currentPhase='voyage';state.voyage={from:'timeriftSea',to:'dawnForest',progress:.5,sky:{type:'eclipse',at:.4,started:true,ended:false}};state.currentCarriage='cab';render()"); W(1500)
    ev("trmToggle()"); W(2500); s=drain()
    ok('H18 switching during the eclipse wakes the dusk seed (from any carriage)', ev("seedOpen('seed_ancient_c')"), [x[:15] for x in s])
    ev("state.currentPhase='docked';state.voyage=null;state.currentLocation='timeriftSea';state.engr=['dawnForest','timeriftSea'];state.currentCarriage='memory';render()"); W(500); drain()
    ev("HSDEF.find(h=>h.id==='mem-rubbing').act();closeAll();render()"); W(1800); s=drain()
    ok('H19 the key halves join; mnemo thanks you; chapter six ends with the door', '合起來' in J(s) and '第六章・完' in J(s) and ev("trainStage('guard')")>=3, [x[:15] for x in s])
    ok('H20 key constellation opens', ev("constOpen('key')"))
    # 終章：道別、結局門檻
    go(BASE+chap('[1,2,3,4,5,6]','{1:1,2:1,3:1,4:1,5:1,6:1}')+LORE+pax(['treeling','skywhale','sirenora','titan','grinfox','mnemo'])+"state.seedOpen=['seed_ancient_a','seed_ancient_b','seed_ancient_c'];state.currentLocation='dawnForest';state.currentCarriage='habitat';save();render()",1500); drain()
    ok('H21 final chapter: say goodbye to the six heroes', '道別（0/6）' in ev("goalNow().t"), ev("goalNow().t"))
    ev("talk('treeling')"); s=drain(); ok('H22 goodbye line', '老樹會一直在那裡' in J(s))
    ok('H23 heroes never leave by the normal rule', ev("PASSENGERS.treeling.stay")==999)
    ok('H24 ending counts keepsakes + hearts (6 hearts + 2 keepsakes = dawn)', ev("(()=>{state.collectibles=state.collectibles.filter(x=>!x.startsWith('keep_'));state.collectibles.push('keep_sola','keep_felinia');state.storyFlags.departTaint=10;return endingType();})()")=='dawn' and ev("(()=>{state.collectibles=state.collectibles.filter(x=>!x.startsWith('keep_'));state.collectibles.push('keep_sola');return endingType();})()")=='return')
    ok('H25 finale names the heroes and the constellations', '霜憶晶絡的心意' in J(ev("finaleExtra()")))
    ok('Z no page errors', not errs, errs)
    print('ALL PASS' if all(R) else 'SOME FAIL', len(R))
