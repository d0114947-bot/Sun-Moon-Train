from playwright.sync_api import sync_playwright
import sys, json
d='/home/claude/game'; S=sys.argv[1]
html=open(d+'/index.html').read()
open(d+'/_t.html','w').write('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">'+html)
seed={"v":1,"introDone":True,"currentCarriage":"memory","currentLocation":"dawnForest","completedEvents":["board_lumi"],"storyFlags":{"natureLight":"dawn"}}
R=[]
def ok(name,cond,extra=''): R.append(('PASS' if cond else 'FAIL')+' '+name+(' '+str(extra) if extra else ''))
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    ctx=b.new_context(viewport={'width':1280,'height':720})
    ctx.add_init_script("if(!sessionStorage.getItem('seeded')){localStorage.setItem('riyue-save-v1',%s);sessionStorage.setItem('seeded','1')}"%json.dumps(json.dumps(seed)))
    pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: m.type=='warning' and errs.append(m.text))
    pg.goto('http://127.0.0.1:8765/_t.html'); pg.wait_for_timeout(500); pg.click('#st'); pg.wait_for_function('PANO.ready.memory===true',timeout=15000); pg.wait_for_timeout(300)
    ok('pano canvas present', pg.evaluate("!!document.querySelector('#pano canvas') && PANO.ready.memory===true"))
    ok('webgl active', pg.evaluate("!!PANO.gl"))
    pg.screenshot(path=S+'/p1.png')
    face=lambda hid:(pg.evaluate(f"(()=>{{const o=PANO.list.find(x=>x.hotspotId==='{hid}');PANO.tLon=PANO.lon=o.yaw;PANO.tLat=PANO.lat=0;PANO.need=true}})()"),pg.wait_for_timeout(400))
    pos=lambda hid: pg.evaluate(f"(()=>{{const e=document.querySelector('[data-hid=\"{hid}\"]');return e.style.visibility==='visible'?[parseFloat(e.style.left),parseFloat(e.style.top)]:null}})()")
    a=pos('mem-door-habitat'); lon0=pg.evaluate('PANO.tLon')
    # drag left 300px
    pg.mouse.move(640,400); pg.mouse.down(); pg.mouse.move(500,400,steps=8); pg.mouse.move(340,400,steps=8); pg.mouse.up(); pg.wait_for_timeout(500)
    b2=pos('mem-door-habitat')
    ok('hotspot follows scene on drag', a and b2 and abs((a[0]-b2[0])-300)<12, (a,b2))
    pg.screenshot(path=S+'/p2.png')
    # full 360 by repeated drags
    k=pg.evaluate('PANO.fov/PANO.h'); per=360/k; steps=int(per//600)+1; each=per/steps
    start=pg.evaluate('PANO.tLon'); x=1100
    for i in range(steps):
        pg.mouse.move(1150,400); pg.mouse.down(); pg.mouse.move(1150-each,400,steps=15); pg.mouse.up(); pg.wait_for_timeout(120)
    pg.wait_for_timeout(500); end=pg.evaluate('PANO.lon')
    ok('full 360 rotation returns to start', abs(((end-start)%360+360)%360 - 0)<0.5 or abs(((end-start)%360+360)%360-360)<0.5, (start,end))
    c=pos('mem-door-habitat'); ok('hotspot same place after 360', c and b2 and abs(c[0]-b2[0])<3, (b2,c))
    # vertical clamp
    pg.mouse.move(640,200); pg.mouse.down(); pg.mouse.move(640,700,steps=10); pg.mouse.up(); pg.wait_for_timeout(400)
    lat,mx=pg.evaluate('[PANO.lat,PANO.maxLat]'); ok('vertical clamped', abs(lat-mx)<0.01 and mx<30, (lat,mx))
    pg.mouse.move(640,700); pg.mouse.down(); pg.mouse.move(640,450,steps=10); pg.mouse.up(); pg.wait_for_timeout(400)
    # drag beginning on a hotspot shouldn't open it
    face('mem-log')
    h=pos('mem-log'); pg.mouse.move(h[0],h[1]); pg.mouse.down(); pg.mouse.move(h[0]-120,h[1],steps=8); pg.mouse.up(); pg.wait_for_timeout(300)
    ok('drag from hotspot does not open panel', pg.evaluate("!document.querySelector('.ov')"))
    face('mem-log')
    h=pos('mem-log'); pg.mouse.click(h[0],h[1]); pg.wait_for_timeout(400)
    ok('click hotspot opens panel', pg.evaluate("!!document.querySelector('.ov') && document.querySelector('.ov h2').textContent.includes('旅程紀錄')"))
    pg.click('.ov .close'); pg.wait_for_timeout(200)
    # edit mode
    pg.click('.pano-edit-btn'); pg.wait_for_timeout(300); face('mem-log')
    ok('edit mode on', pg.evaluate("PANO.edit && !!document.querySelector('.pe-bar') && document.querySelector('#hud').hidden"))
    h=pos('mem-log'); before=pg.evaluate("JSON.stringify(PANO.list.find(x=>x.hotspotId==='mem-log'))")
    pg.mouse.move(h[0],h[1]); pg.mouse.down(); pg.mouse.move(h[0]+150,h[1]+60,steps=10); pg.mouse.up(); pg.wait_for_timeout(300)
    h2=pos('mem-log'); ok('hotspot dragged to pointer', h2 and abs(h2[0]-(h[0]+150))<3 and abs(h2[1]-(h[1]+60))<3, (h,h2))
    ok('no panel opened in edit', pg.evaluate("!document.querySelector('.ov')"))
    ok('form shows selected', pg.evaluate("document.querySelector('#pe-name').value==='旅程之書'"))
    pg.fill('#pe-name','旅程之書（測試）'); R.append('before add '+str(pg.evaluate('PANO.list.length'))+' '+pg.evaluate('document.querySelector("#pedit").innerText.slice(0,80)')); pg.click('#pe-add'); pg.wait_for_timeout(200)
    n=pg.evaluate("PANO.list.length"); ok('add hotspot', n==8, n)
    pg.fill('#pe-name','測試熱點'); pg.select_option('#pe-type','note'); pg.fill('#pe-note','這是測試說明')
    pg.screenshot(path=S+'/p3.png')
    pg.click('#pe-save'); pg.wait_for_timeout(200)
    saved=pg.evaluate("JSON.parse(localStorage.getItem('riyue-hotspots-v1')).memory")
    ok('saved to storage', len(saved)==8 and any(x['name']=='旅程之書（測試）' for x in saved))
    # delete new one
    pg.click('#pe-del'); pg.click('#pe-d-yes'); ok('delete', pg.evaluate("PANO.list.length")==7)
    pg.click('#pe-exit'); pg.wait_for_timeout(200)
    ok('exit asks when unsaved', pg.evaluate("!!document.querySelector('#pe-x-save')"))
    pg.click('#pe-x-drop'); pg.wait_for_timeout(300)
    ok('discard restores saved (8)', pg.evaluate("PANO.list.length")==8 and pg.evaluate("!PANO.edit && !document.querySelector('#hud').hidden"))
    # reload persistence
    moved=pg.evaluate("JSON.stringify(PANO.list.find(x=>x.hotspotId==='mem-log'))")
    pg.reload(); pg.wait_for_timeout(500); pg.click('#st'); pg.wait_for_timeout(1200)
    ok('positions persist after reload', pg.evaluate("JSON.stringify(PANO.list.find(x=>x.hotspotId==='mem-log'))")==moved and moved!=before)
    ok('view orientation restored', pg.evaluate("Math.abs(PANO.tLon-PANO.list.find(x=>x.hotspotId==='mem-log').yaw)<40"))
    # note hotspot in game mode
    nid=pg.evaluate("PANO.list.find(x=>x.type==='note').hotspotId"); pg.evaluate(f"(()=>{{const o=PANO.list.find(x=>x.hotspotId==='{nid}');PANO.tLon=PANO.lon=o.yaw;PANO.tLat=PANO.lat=0;PANO.need=true}})()"); pg.wait_for_timeout(600)
    h=pos(nid); pg.mouse.click(h[0],h[1]); pg.wait_for_timeout(300)
    ok('note hotspot opens text', pg.evaluate("document.querySelector('.ov p')?.textContent==='這是測試說明'")); pg.click('.ov .close')
    # door
    pg.evaluate("PANO.tLon=PANO.lon=180;PANO.tLat=PANO.lat=0;PANO.need=true"); pg.wait_for_timeout(500)
    h=pos('mem-door-habitat'); pg.mouse.click(h[0],h[1]); pg.wait_for_timeout(1500)
    ok('door to habitat', pg.evaluate("state.currentCarriage==='habitat' && !document.querySelector('#pano') && PANO.active===null"))
    pg.screenshot(path=S+'/p4.png')
    pg.click('[data-act="go:memory"]'); pg.wait_for_timeout(1500)
    ok('back into pano', pg.evaluate("PANO.active==='memory' && !!document.querySelector('#pano canvas')"))
    pg.click('[data-hid="mem-system"]') if pos('mem-system') else None
    ok('errors', not errs, errs)
    ctx.close()
    # mobile touch
    m=b.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True,device_scale_factor=2)
    m.add_init_script("localStorage.setItem('riyue-save-v1',%s)"%json.dumps(json.dumps(seed)))
    pg=m.new_page(); pg.goto('http://127.0.0.1:8765/_t.html'); pg.wait_for_timeout(500); pg.tap('#st'); pg.wait_for_timeout(1500)
    pg.screenshot(path=S+'/m1.png')
    cdp=m.new_cdp_session(pg); l0=pg.evaluate('PANO.tLon'); sx0=pg.evaluate('[scrollX,scrollY,document.querySelector("#viewport").scrollLeft]')
    def touch(t,x,y): cdp.send('Input.dispatchTouchEvent',{'type':t,'touchPoints':([] if t=='touchEnd' else [{'x':x,'y':y}])})
    touch('touchStart',300,420)
    for i in range(1,16): touch('touchMove',300-i*14,420); pg.wait_for_timeout(16)
    touch('touchEnd',0,0); pg.wait_for_timeout(500)
    l1=pg.evaluate('PANO.tLon'); sx1=pg.evaluate('[scrollX,scrollY,document.querySelector("#viewport").scrollLeft]')
    R.append(f'mobile stage: {pg.evaluate("[PANO.w,PANO.h,PANO.fov.toFixed(1),PANO.maxLat.toFixed(1)]")}')
    ok('touch swipe rotates', abs(l1-l0)>20, (l0,l1)); ok('no page scroll', sx0==sx1, (sx0,sx1))
    pg.screenshot(path=S+'/m2.png')
    h=pos('mem-door-habitat') or None
    pg.evaluate("PANO.tLon=PANO.lon=180;PANO.tLat=PANO.lat=0;PANO.need=true"); pg.wait_for_timeout(500); h=pos('mem-door-habitat')
    pg.tap(f'[data-hid="mem-door-habitat"]'); pg.wait_for_timeout(1500)
    ok('tap hotspot on mobile', pg.evaluate("state.currentCarriage==='habitat'"))
    b.close()
import os; os.remove(d+'/_t.html')
print('\n'.join(R))
