from playwright.sync_api import sync_playwright
import sys
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(800); ev("startNew()"); W(200)
    ids=['lumi','sola','felinia','leviathaurora','cinder','aelis','pyro','vandora','frost','sirenora','titan','lynx','strider']
    ev("document.querySelector('#mainscreen')?.remove();closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.journeyCount=9;state.currentLocation='dawnForest';state.storyFlags.panoHintDone=1;state.discoveredLifeforms=%s;for(const id of %s) state.passengers[id]={stage:1,talks:1,records:[],aboard:true,left:false,boardedJourney:2};state.currentCarriage='habitat';render()"%(ids,ids)); W(2500)
    for i,lon in enumerate([260,180,100]):
        ev(f"PANO.tLon=PANO.lon=panoClamp({lon});PANO.need=true"); W(700); pg.screenshot(path=f'hab{i}.png')
    print('pan range', ev("[panoClamp(0),panoClamp(359),PANO.dw,PANO.w]"))
    ev("closeAll();state.currentCarriage='observation';render()"); W(2500)
    for i,lon in enumerate([260,100]):
        ev(f"PANO.tLon=PANO.lon=panoClamp({lon});PANO.need=true"); W(700); pg.screenshot(path=f'obs{i}.png')
    for d in ['state.passengers.felinia.place=\"deck\";state.passengers.cinder.place=\"deck\";state.passengers.titan.place=\"deck\";state.passengers.lynx.place=\"deck\"']:
        ev(d)
    ev("closeAll();state.currentCarriage='observatory';render()"); W(2000); pg.screenshot(path='deck0.png')
    print(errs); b.close()
