from playwright.sync_api import sync_playwright
import sys, json, re
S=sys.argv[1]; d='/home/claude/game'
html=open(d+'/index.html').read()
open(d+'/_t.html','w').write('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">'+html)
INTRO=json.loads(open(S+'/intro_lines_before.txt').read().replace("'",'"'))
R=[]
def ok(n,c,x=''): R.append(('PASS ' if c else 'FAIL ')+n+(' '+str(x) if x!='' else ''))
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
    ctx=b.new_context(viewport={'width':1280,'height':720}); pg=ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8765/_t.html'); pg.wait_for_timeout(900)
    ok('1 main screen shows train', pg.evaluate("!!document.querySelector('#mainscreen .ms-train svg')"))
    pg.screenshot(path=S+'/n0.png')
    pg.click('#ms-work'); pg.wait_for_timeout(1500)
    ok('2 branch menu opens', pg.evaluate("document.querySelector('#mst').classList.contains('open') && getComputedStyle(document.querySelector('#ms-new')).opacity>0.9"))
    pg.screenshot(path=S+'/n1.png')
    pg.click('#ms-cont'); pg.wait_for_timeout(200)
    ok('   continue disabled w/o saves', '尚無可接續' in pg.inner_text('#ms-note'))
    pg.click('#ms-new'); pg.wait_for_timeout(700)
    seen=[]
    for i in range(len(INTRO)):
        seen.append(pg.inner_text('.cine .txt')); pg.click('.cine'); pg.wait_for_timeout(250)
    ok('3/4 original opening played unchanged', seen==INTRO, seen if seen!=INTRO else '')
    pg.wait_for_timeout(600)
    ok('5 duty prep only after opening', pg.evaluate("state.introDone && state.currentCarriage==='prep' && document.querySelector('.cine .txt').textContent.includes('值勤準備') && !state.passengers.lumi"))
    pg.click('.cine'); pg.wait_for_timeout(900)
    pg.screenshot(path=S+'/n2.png')
    # gate
    pg.click('[data-act="go:cab"]'); pg.wait_for_timeout(300)
    ok('   cab locked before prep', pg.evaluate("state.currentCarriage==='prep' && document.querySelector('.ov h2').textContent.includes('尚未完成')")); pg.click('.ov .close')
    # scan
    pg.click('[data-act="prep:scan"]'); pg.wait_for_timeout(200); pg.click('#sb'); pg.wait_for_timeout(2900)
    ok('6 contamination measured & recorded', pg.evaluate("state.duty.scan && state.spirit.contamination.level==='純淨' && state.spirit.contaminationLog.length===1"), pg.evaluate("JSON.stringify(state.spirit.contamination)"))
    pg.screenshot(path=S+'/n3.png'); pg.click('.ov .close'); pg.wait_for_timeout(200)
    pg.click('[data-act="prep:equip"]'); pg.wait_for_timeout(200)
    for k in ['tablet','compass','talisman']: pg.click(f'[data-eq="{k}"]'); pg.wait_for_timeout(150)
    ok('7 equipment received', pg.evaluate("equipAll()")); pg.click('.ov .close'); pg.wait_for_timeout(200)
    pg.click('[data-act="prep:brief"]'); pg.wait_for_timeout(200)
    pg.screenshot(path=S+'/n4.png')
    for i in range(5): pg.click(f'.tl[data-i="{i}"]'); pg.wait_for_timeout(100)
    ok('   briefing checked', pg.evaluate("state.duty.briefing")); pg.click('.ov .close'); pg.wait_for_timeout(300)
    pg.click('[data-act="go:cab"]'); pg.wait_for_timeout(1000)
    ok('8 cab entered', pg.evaluate("state.currentCarriage==='cab'"))
    pg.click('[data-act="cab:signal"]'); pg.wait_for_timeout(200)
    ok('9a signal not green yet → not recorded', pg.evaluate("!state.duty.signal")); pg.click('.ov .close')
    pg.click('[data-act="cab:dragon"]'); pg.wait_for_timeout(300)
    lines=[]
    while pg.query_selector('.dlg'):
        lines.append(pg.inner_text('.dlg .tx')); pg.click('.dlg'); pg.wait_for_timeout(120)
    ok('10 dragon refuses when checks missing', any('還沒有確認' in l for l in lines) and pg.evaluate("state.currentPhase==='docked' && !state.duty.reported"), lines[-3:])
    pg.wait_for_timeout(4500); pg.screenshot(path=S+'/n5.png')
    pg.click('[data-act="cab:signal"]'); pg.wait_for_timeout(200); pg.click('.ov .close')
    pg.click('[data-act="cab:doors"]'); pg.wait_for_timeout(200); pg.click('.ov .close')
    ok('9b signal & doors confirmed', pg.evaluate("state.duty.signal && state.duty.doors"))
    pg.click('[data-act="cab:dragon"]'); pg.wait_for_timeout(300)
    lines=[]; shot=False
    while pg.query_selector('.dlg'):
        t=pg.inner_text('.dlg .tx'); lines.append(t)
        if '准許出發' in t and not shot: pg.screenshot(path=S+'/n6.png'); shot=True
        pg.click('.dlg'); pg.wait_for_timeout(120)
    ok('11 report → permission', '確認完成。前方航道平安，列車狀態正常。' in lines and '准許出發。' in lines)
    pg.wait_for_timeout(300)
    ok('12 auto departure starts', pg.evaluate("state.currentPhase==='voyage' && state.voyage.to==='dawnForest' && !!document.querySelector('.cine img')"))
    for i in range(4): pg.click('.cine'); pg.wait_for_timeout(250)
    pg.wait_for_timeout(1200); p0=pg.evaluate("state.voyage.progress"); pg.wait_for_timeout(1500); p1=pg.evaluate("state.voyage.progress")
    ok('   voyage runs by itself', p1>p0, (p0,p1))
    # walk to observatory during voyage
    for c in ['prep','observation','nature','habitat','memory','observatory']:
        pg.click(f'[data-act="go:{c}"]') if c!='observatory' else pg.evaluate("act('go','observatory')"); pg.wait_for_timeout(1100)
    ok('17 observatory reachable', pg.evaluate("state.currentCarriage==='observatory' && !!document.querySelector('#streaks')"))
    pg.wait_for_timeout(600); pg.screenshot(path=S+'/n7.png')
    ok('18a observatory voyage view animates', pg.evaluate("(()=>{const c=document.querySelector('#streaks');const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let n=0;for(let i=3;i<d.length;i+=4*50) if(d[i]>0) n++;return n>20})()"))
    pg.evaluate("state.voyage.progress=0.98"); pg.wait_for_timeout(800)
    # voyage event cine then arrival title
    guard=0
    while not pg.evaluate("state.currentPhase==='docked'") and guard<20:
        if pg.query_selector('.cine'): pg.click('.cine')
        pg.wait_for_timeout(400); guard+=1
    ok('   arrives automatically, journeyCount=1', pg.evaluate("state.currentLocation==='dawnForest' && state.journeyCount===1 && !state.duty.signal"))
    # arrival title + boarding
    guard=0
    while not pg.query_selector('#hi') and guard<20:
        if pg.query_selector('.cine'): pg.click('.cine')
        pg.wait_for_timeout(500); guard+=1
    ok('13 first stop → Lumi boards (original story)', pg.evaluate("state.passengers.lumi && state.passengers.lumi.aboard"))
    pg.click('#hi'); pg.wait_for_timeout(300)
    while pg.query_selector('.dlg'):
        if pg.query_selector('.dlg .chs button'): pg.click('.dlg .chs button'); pg.wait_for_timeout(1100)
        else: pg.click('.dlg .box'); pg.wait_for_timeout(150)
    pg.wait_for_timeout(800); pg.screenshot(path=S+'/n8.png')
    ok('18b observatory docked shows station', pg.evaluate("state.currentCarriage==='observatory' && !document.querySelector('#streaks')"))
    # memory crystal save
    pg.click('[data-act="go:memory"]'); pg.wait_for_function("PANO.active==='memory' && PANO.ready.memory===true", timeout=15000); pg.wait_for_timeout(400)
    ok('   rear door hotspot in pano', pg.evaluate("PANO.list.some(o=>o.action==='go:observatory') && !PANO.list.some(o=>o.action==='mem:system')"))
    pg.evaluate("(()=>{const o=PANO.list.find(x=>x.hotspotId==='mem-save');PANO.tLon=PANO.lon=o.yaw;PANO.tLat=PANO.lat=PANO.maxLat;PANO.need=true})()"); pg.wait_for_timeout(500)
    pg.click('[data-hid="mem-save"]'); pg.wait_for_timeout(300)
    ok('   save UI opens from memory crystal', pg.evaluate("!!document.querySelector('.ov.pearl #sl-new')"))
    pg.click('#sl-new'); pg.wait_for_timeout(1500)
    sl=pg.evaluate("slotsGet()")
    ok('14 slot created with thumbnail', len(sl)==1 and (sl[0]['thumb'] or '').startswith('data:image/jpeg') and len(sl[0]['thumb'])>3000, len(sl[0]['thumb'] or ''))
    open(S+'/thumb1.txt','w').write(sl[0]['thumb'] or '')
    pg.fill('#sl-name','森林第一站'); pg.click('#sl-ren'); pg.wait_for_timeout(200)
    ok('   rename', pg.evaluate("slotsGet()[0].name")=='森林第一站')
    pg.screenshot(path=S+'/n9.png'); pg.click('.ov .close'); pg.wait_for_timeout(200)
    # change state then load
    pg.click('[data-hid="mem-door-habitat"]') if pg.evaluate("(()=>{const o=PANO.list.find(x=>x.hotspotId==='mem-door-habitat');PANO.tLon=PANO.lon=o.yaw;PANO.tLat=PANO.lat=0;PANO.need=true;return 1})()") else None
    pg.wait_for_timeout(1300)
    ok('   moved to habitat', pg.evaluate("state.currentCarriage==='habitat'"))
    pg.evaluate("state.journeyCount=99; save()")
    pg.click('[data-act="go:memory"]'); pg.wait_for_timeout(1300)
    pg.evaluate("savePanel('game')"); pg.wait_for_timeout(200)
    pg.click('.slot[data-id]'); pg.wait_for_timeout(200); pg.click('#sl-load'); pg.click('#cf-y'); pg.wait_for_timeout(1200)
    ok('15 load restores state', pg.evaluate("state.journeyCount===1 && state.currentCarriage==='memory' && state.passengers.lumi.aboard && state.currentLocation==='dawnForest'"))
    # second slot then delete with double confirm
    pg.evaluate("savePanel('game')"); pg.wait_for_timeout(200); pg.click('#sl-new'); pg.wait_for_timeout(1200)
    pg.click('#sl-del'); pg.click('#cf-y'); pg.wait_for_timeout(150)
    ok('   delete asks twice', pg.evaluate("slotsGet().length")==2 and pg.query_selector('#cf-y2') is not None)
    pg.click('#cf-y2'); pg.wait_for_timeout(200); ok('   deleted', pg.evaluate("slotsGet().length")==1)
    pg.click('.ov .close')
    # reload
    pg.reload(); pg.wait_for_timeout(1000)
    ok('16 saves persist after reload', pg.evaluate("slotsGet().length")==1 and pg.query_selector('#mainscreen') is not None)
    pg.click('#ms-work'); pg.wait_for_timeout(1400); pg.click('#ms-cont'); pg.wait_for_timeout(400)
    ok('   continue lists auto + slot thumbnails', pg.evaluate("document.querySelectorAll('.ov.pearl .slot[data-id]').length===2 && document.querySelectorAll('.ov.pearl .slot img').length>=1"))
    pg.screenshot(path=S+'/n10.png')
    pg.click('.slot[data-id^="s"]'); pg.wait_for_timeout(200); pg.click('#sl-load'); pg.click('#cf-y'); pg.wait_for_timeout(1200)
    ok('   continue loads without opening', pg.evaluate("!document.querySelector('#mainscreen') && !document.querySelector('.cine') && state.journeyCount===1 && RUNNING"))
    ok('19 errors', not errs, errs)
    ctx.close()
    m=b.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True,device_scale_factor=2); pg=m.new_page()
    pg.goto('http://127.0.0.1:8765/_t.html'); pg.wait_for_timeout(900); pg.tap('#ms-work'); pg.wait_for_timeout(1500); pg.screenshot(path=S+'/m3.png')
    pg.tap('#ms-new'); pg.wait_for_timeout(500)
    for i in range(7): pg.tap('.cine'); pg.wait_for_timeout(300)
    pg.wait_for_timeout(800); pg.screenshot(path=S+'/m4.png')
    b.close()
import os; os.remove(d+'/_t.html')
print('\n'.join(R))
