from playwright.sync_api import sync_playwright
import sys,os
S=sys.argv[1]; d='/home/claude/game'
CSP='<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src \'unsafe-inline\'; style-src \'unsafe-inline\' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src data: blob:; media-src data: blob:">'
open(d+'/_c.html','w').write('<!doctype html><meta charset=utf-8>'+CSP+'<meta name=viewport content="width=device-width,initial-scale=1">'+open(d+'/index.html').read())
def okimg(ev,sel): return ev(f"(()=>{{const i=document.querySelector('{sel}');return !!i&&i.complete&&i.naturalWidth>0}})()")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; bad=[]
    pg.on('console',lambda m: ('Content Security' in m.text or 'Refused' in m.text or 'violates' in m.text) and bad.append(m.text[:100]))
    pg.goto('http://127.0.0.1:8765/_c.html'); W(800)
    ev("startNew()"); W(200)
    ev("closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.discoveredLifeforms=['felinia'];state.passengers.felinia={stage:1,talks:1,records:[{j:0,t:'於航行途中登上列車'}],aboard:true,left:false,boardedJourney:0};state.currentCarriage='memory';render()")
    pg.wait_for_function("PANO.ready.memory===true",timeout=15000); W(500)
    print('1 環景載入：',ev("PANO.ready.memory===true and !document.querySelector('.pano-fail')".replace(' and ','&&')))
    pg.screenshot(path=S+'/c_pano.png')
    ev("state.currentCarriage='habitat';render()"); W(1500)
    print('2 棲息車廂羽貓獸動畫：',okimg(ev,'[data-hs=\"hab-p-felinia\"] img'))
    pg.screenshot(path=S+'/c_hab.png')
    ev("talk('felinia')"); W(800); print('3 對話立繪：',okimg(ev,'.dlg .who img')); pg.screenshot(path=S+'/c_dlg.png'); ev("closeAll()")
    ev("openBook('life','felinia')"); W(1200); print('4 圖鑑靜態立繪與速寫：',okimg(ev,'.plate.big img') and okimg(ev,'.studies img')); ev("closeAll()")
    ev("cine(['測試'],null,CARRIAGES.memory.image)"); W(400); ev("closeAll()")
    ev("startDeparture()"); W(800); print('5 航行過場圖：',okimg(ev,'.cine img')); pg.screenshot(path=S+'/c_cine.png'); ev("closeAll()")
    ev("CARRIAGES.memory.pano=null;state.currentCarriage='memory';render()"); W(800); print('6 平面備援典藏圖：',okimg(ev,'#scene img.bg'))
    print('7 被安全政策擋下的資源：',len(bad),bad[:3])
    b.close()
os.remove(d+'/_c.html')
