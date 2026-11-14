from playwright.sync_api import sync_playwright
import sys,time
S=sys.argv[1]; d='/home/claude/game'
open(d+'/_t.html','w').write('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'+open(d+'/index.html').read())
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate
    pg.goto('http://127.0.0.1:8765/_t.html'); pg.wait_for_timeout(600)
    ev("startNew()"); pg.wait_for_timeout(300); ev("closeAll();state.introDone=true;state.storyFlags.noFeel=1;state.carSeen=Object.keys(CAR_INTRO);state.storyFlags.seedTalk=1;state.discoveredLifeforms=['lumi','sola'];state.passengers.lumi={stage:2,talks:2,records:[{j:1,t:'於晨曦森林登上列車，在自然棲台落腳。'},{j:1,t:'關係：認識'},{j:2,t:'留下了晨露苔種。'}],aboard:true,left:false};state.passengers.sola={stage:1,talks:1,records:[{j:2,t:'於星河浮島登上列車。'}],aboard:true};state.visitedLocations=['dawnForest','starIslands'];state.currentLocation='starIslands';state.journeyCount=2;render()")
    for ch,sub,n in [('life',None,'b1'),('life','lumi','b2'),('lore',None,'b3'),('atlas',None,'b4')]:
        ev(f"openBook('{ch}',{('\"'+sub+'\"') if sub else 'undefined'})"); t=time.time(); pg.wait_for_timeout(1600)
        print(n, ev("[...document.querySelectorAll('.spread .page')].map(p=>getComputedStyle(p).opacity+'/'+p.innerText.length)"))
        pg.screenshot(path=f'{S}/{n}.png')
    b.close()
import os; os.remove(d+'/_t.html')
