# 一般乘客的跨章節小故事線
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE=open('tchap.py').read().split('BASE="')[1].split('"\n')[0]
def pax(ids,st=1): return "".join([f"state.discoveredLifeforms.push('{x}');state.passengers['{x}']={{stage:{st},talks:3,records:[],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS['{x}'].zone}};" for x in ids])
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.CHAP_TEST=1;window.INFO_TEST=1")
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    def drain(ms=40000):
        t=0; seen=[]
        while t<ms:
            if ev("!!document.querySelector('#layer .cine')"): seen.append(pg.inner_text('#layer .cine')); ev("document.querySelector('#layer .cine').click()")
            elif ev("!!document.querySelector('#layer .dlg')"):
                seen.append(pg.inner_text('#layer .dlg'))
                if ev("!!document.querySelector('#layer .dlg .chs button')"): ev("[...document.querySelectorAll('#layer .dlg .chs button')].pop().click()"); W(300); continue
                ev("(document.querySelector('#layer .dlg .box')||document.querySelector('#layer .dlg'))?.click()")
            else:
                W(1500); t+=1500
                if not ev("!!document.querySelector('#layer .dlg,#layer .cine')"): return seen
            W(250); t+=250
        return seen
    J=lambda s:'|'.join(s)
    ev(BASE+pax(['aelis','strider'])+"state.journeyCount=3;state.chap={said:{},arr:{},ended:[],shown:[1],fl:[],heart:{},legacy:0,crys1:1};state.currentCarriage='habitat';save();PANO.active=null;RUNNING=true;render()"); W(600)
    ok('A1 five passengers have story lines', ev("ARC_IDS.length")==5)
    ok('A2 first part ready, passenger glows', ev("arcWait('aelis')") and ev("HSDEF.find(h=>h.id==='hab-p-aelis').imp()"))
    ok('A3 not before its chapter', not ev("arcWait('strider')"))
    ev("talk('aelis')"); s=drain()
    ok('A4 talking plays the story', '牆上那些刻紋' in J(s), J(s)[:200])
    ok('A5 next part waits for a later chapter and another trip', not ev("arcWait('aelis')"))
    ev("state.journeyCount=4;state.chap.ended=[1];save()")
    ok('A6 still waiting (needs 2 chapters)', not ev("arcWait('aelis')"))
    ev("state.chap.ended=[1,2];save()")
    ok('A7 ready after chapter 2', ev("arcWait('aelis')"))
    ok('A8 stays aboard until the story ends', ev("PASSENGERS.aelis.stay")==9999 and not ev("byeReady('aelis')"))
    ok('A9 notebook lists it as a collection item', '好像有話想說' in ev("questSection()") and '乘客的小故事' in ev("questSection()"))
    ok('A10 life book: journey story', '拓刻紋' in ev("journeyStory('aelis')"))
    # 灰角靈犬：認出荒原的草，留下種子
    ev("state.chap.arc.strider={b:1,j:2};save()"); n0=ev("seedTotal()")
    ok('S1 strider part 2 ready', ev("arcWait('strider')"))
    ev("closeAll();talk('strider')"); s=drain()
    ok('S2 recognises the grass in the seed vault, a seed is added', '荒原的草' in J(s) and ev("seedTotal()")==n0+1)
    # 說完以後就能下車
    ev("state.chap.arc.aelis={b:4,j:4};save()")
    ok('E1 after the last part, normal stay applies again', ev("PASSENGERS.aelis.stay")!=9999)
    # 固定上車
    ev("state.currentLocation='starIslands';state.chap.ended=[1];save()")
    ok('B1 pyro boards at the star islands in chapter 2', 'board_pyro' in ev("rollBoarders()"))
    ok('Z no page errors', not errs, errs)
    b.close()
print('TOTAL',sum(R),'/',len(R))
