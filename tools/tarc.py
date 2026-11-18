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
    ok('A8 can leave mid-story (normal stay)', ev("PASSENGERS.aelis.stay")!=9999)
    ok('A9 notebook lists it as a collection item', '好像有話想說' in ev("questSection()") and '乘客的小故事' in ev("questSection()"))
    ok('A10 life book: journey story', '拓刻紋' in ev("journeyStory('aelis')"))
    # 灰角靈犬：認出荒原的草，留下種子
    ev("state.chap.arc.strider={b:1,j:2};save()"); n0=ev("seedTotal()")
    ok('S1 strider part 2 ready', ev("arcWait('strider')"))
    ev("closeAll();talk('strider')"); s=drain()
    ok('S2 recognises the grass in the seed vault, a seed is added', '荒原的草' in J(s) and ev("seedTotal()")==n0+1)
    # 要下車了：最後一段在整理行李時說完
    ev("closeAll();state.chap.arc.aelis={b:1,j:4};state.passengers.aelis.bye={st:'prep',j:4,pairs:[]};save()")
    ok('E1 packing to leave: the last part is ready right away', ev("arcWait('aelis')"))
    ev("talk('aelis')"); s=drain()
    ok('E2 plays the final part (not part 2)', '風開始唱歌了' in J(s) and '耳朵就會癢' not in J(s), J(s)[:200])
    ok('E3 story marked finished; life book shows told parts only', ev("arcAt('aelis')")==4 and '傳的是' not in ev("journeyStory('aelis')") and '抄成了一本書' in ev("journeyStory('aelis')") and '渡口' not in ev("journeyStory('aelis')"))
    # 道別時才說
    ev("closeAll();"+pax(['vandora'])+"state.chap.arc.vandora={b:1,j:3};save();farewell('vandora',()=>{window._fw=1})"); s=drain()
    ok('E4 farewell: final part first, then goodbye', '外面的光，不可怕' in J(s) and ev("arcAt('vandora')")==4, J(s)[:300])
    # 曦淵的近照
    ev("closeAll();dialogueScript([['dragon','一'],['dragon','二']])"); W(500)
    a=ev("document.querySelector('.dlg .who img').getAttribute('src')"); bt=ev("[Math.round(document.querySelector('.dlg .who img').getBoundingClientRect().bottom),Math.round(document.querySelector('.dlg .box').getBoundingClientRect().top)]")
    ev("document.querySelector('.dlg .box').click()"); W(500); c=ev("document.querySelector('.dlg .who img').getAttribute('src')")
    ok('X1 two close-ups alternate', a!=c and 'xiyuan-face' in a and 'xiyuan-face' in c, [a,c])
    ok('X2 close-up sits on the dialogue box', abs(bt[0]-bt[1])<=3, bt)
    ev("document.querySelector('.dlg .box').click()"); W(400)
    # 同行者的秘密：影片
    ev("closeAll();xevVid('xev-secret.mp4','xev-secret.jpg');dialogueScript([['aelis','……這件事，我沒有跟別人說過。']])"); W(900)
    ok('V0 secret event is wired to the video', 'xev-secret.mp4' in ev("XRUN.x_secret.toString()"))
    ok('V1 secret event plays the video behind the dialogue', ev("!!document.querySelector('.xevvid video')") and ev("!!document.querySelector('#layer .dlg')"))
    drain(); W(1500)
    ok('V2 video goes away after the talk', not ev("!!document.querySelector('.xevvid')"))
    # 固定上車
    ev("state.currentLocation='starIslands';state.chap.ended=[1];save()")
    ok('B1 pyro boards at the star islands in chapter 2', 'board_pyro' in ev("rollBoarders()"))
    ok('Z no page errors', not errs, errs)
    b.close()
print('TOTAL',sum(R),'/',len(R))
