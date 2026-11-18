# 主角的深層故事、渡守的稱呼、曦淵的試探、生命誌、設定改寫、彩蛋
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
exec(open('theart.py').read().split('with sync_playwright')[0].split("R=[]")[1].split("def ok")[0]) if False else None
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
                seen.append(pg.inner_text('#layer .dlg'))
                if ev("!!document.querySelector('#layer .dlg .chs button')"): ev("[...document.querySelectorAll('#layer .dlg .chs button')].pop().click()"); W(300); continue
                ev("(document.querySelector('#layer .dlg .box')||document.querySelector('#layer .dlg'))?.click()")
            else:
                W(1500); t+=1500
                if not ev("!!document.querySelector('#layer .dlg,#layer .cine')"): return seen
            W(250); t+=250
        return seen
    J=lambda s:'|'.join(s)
    def go(js,w=900): ev("closeAll();document.querySelectorAll('#layer .dlg,#layer .cine').forEach(e=>e.remove());"+js); W(w)
    # 設定改寫
    ok('S1 the dragon names the last ferryman: 拾光, back to the sleeping land', ev("DRAGON_LORE.find(x=>x.id==='dl_name').lines.map(x=>x[1]).join('')").count('拾光')>=1 and '沉睡之地' in ev("DRAGON_LORE.find(x=>x.id==='dl_name').lines.map(x=>x[1]).join('')"))
    ok('S2 return ending: back to sleep, a new spirit will wake', '回到沉睡之地' in ''.join(ev("ENDINGS.return.lines")))
    ok('S3 yixi cannot tell the light apart', '分辨不出來' in ev("PASSENGERS.yixi.field.abilities[0][1]"))
    # 深層故事
    go(BASE+chap('[1,2,3,4,5]','{1:1,2:1,3:1,4:1,5:1}')+LORE+pax(['treeling','grinfox','mnemo'])+"state.currentLocation='dawnForest';state.currentCarriage='habitat';state.hview=0;save();PANO.active=null;RUNNING=true;render()",1500); drain()
    ok('D1 a hero with its heart given has a story waiting (glows)', ev("deepWait('treeling')") and ev("hsState(HSDEF.find(h=>h.id==='hab-p-treeling'))")=='important')
    ev("talk('treeling')"); s=drain(); ok('D2 first story: the humming child', '哼歌的孩子' in J(s) and ev("state.chap.nick.treeling===1"), [x[:14] for x in s])
    ok('D3 notebook: the ferryman page lists the nickname', ev("(()=>{const c=questCats().find(x=>x.k==='ferry');return !!c&&c.L.some(x=>x.t.includes('哼歌的孩子'))&&c.L[0].t.includes('拾光')})()"))
    ev("talk('treeling')"); s=drain(); ok('D4 second story: hid as a tree', '最後一班' in J(s))
    ok('D4b third story waits for a sketch', not ev("deepWait('treeling')")); ev("state.sketches=Object.assign({},state.sketches,{treeling:[0]});save()")
    ev("talk('treeling')"); s=drain(); ok('D5 third story: it was not wrong', '沒有躲錯' in J(s) and not ev("deepWait('treeling')"))
    ok('D6 life book shows the journey story (3 parts)', ev("journeyStory('treeling')").count('<p>')==3)
    ev("talk('mnemo')"); s=drain(); ok('D7 mnemo has not given its heart yet: no deep story', '說話的人' not in J(s))
    # 墜飾
    go(BASE+chap('[1,2,3,4,5,6]','{1:1,2:1,3:1,4:1,5:1,6:1}',",deep:{mnemo:3},bye7:{mnemo:1,grinfox:1}")+LORE+pax(['grinfox','mnemo'])+"state.currentLocation='dawnForest';state.currentCarriage='habitat';save();render()",1200); drain()
    ev("talk('mnemo')"); s=drain(); ok('D8 the pendant memory: the girl got on the train; the fox laughs', '牠上車了' in J(s) and '嘻嘻' in J(s) and ev("state.chap.pendant===1"), [x[:14] for x in s])
    ok('D9 after chapter six + mnemo nickname: all names are one person', ev("(()=>{state.chap.nick={mnemo:1};const c=questCats().find(x=>x.k==='ferry');return c.L.some(x=>x.t.includes('同一個人'))})()"))
    # 曦淵的試探
    go(BASE+chap('[1,2]','{1:1,2:1,3:1}')+LORE+"state.currentLocation='dawnForest';state.currentCarriage='cab';state.duty.reported=true;save();render()",1200); drain()
    ev("dragonTalk()"); s=drain(); ok('H1 the dragon tests you once (latest chapter)', '揮手' in J(s) and ev("state.chap.hunch[2]===1"), [x[:14] for x in s])
    ev("dragonTalk()"); s=drain(); ok('H2 then the earlier one', '手勢' in J(s))
    # 彩蛋
    ok('E1 dawn ending: Sola waves from her island', '浮島' in ''.join(ev("(state.discoveredLifeforms.push('sola'),ENDINGS.dawn.lines)")) and '歡迎回來' in ''.join(ev("ENDINGS.dawn.lines")))
    ok('Z no page errors', not errs, errs)
    print('ALL PASS' if all(R) else 'SOME FAIL', len(R))
