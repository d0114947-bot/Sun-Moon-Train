from playwright.sync_api import sync_playwright
import sys
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' '+str(x) if x!='' else ''),flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(1500)
    ok('U1 silent before any tap', ev("!TRAINSFX.out && !(BGM.el&&!BGM.el.paused)"))
    pg.click('#ms-work'); W(800)
    ok('U2 tap on main screen starts train sound', ev("!!TRAINSFX.out && SFX.ctx.state==='running' && !!TRAINSFX.timer"))
    pg.click('#ms-snd'); W(300); ok('U3 main-screen ♪ turns it off', ev("!TRAINSFX.out && PREFS.sound===false"))
    pg.click('#ms-snd'); W(300); ok('U4 ♪ turns it back on', ev("!!TRAINSFX.out && PREFS.sound!==false"))
    pg.click('#ms-new'); W(2500)
    st=ev("[!!TRAINSFX.out, BGM.on, BGM.el&&!BGM.el.paused, BGM.el&&BGM.el.currentTime, BGM.el&&BGM.el.src.split('/').pop(), BGM.el&&BGM.el.volume]")
    ok('U5 new game: train sound stops, music auto-plays', st[0] is False and st[1] and st[2] and st[3]>0.5 and st[4].startswith('bgm-'), st)
    seen=[st[4]]
    for i in range(12):
        ev("BGM.el.dispatchEvent(new Event('ended'))"); W(700); seen.append(ev("BGM.el.src.split('/').pop()"))
    ok('U6 first 10 tracks are all different (shuffled)', len(set(seen[:10]))==10, seen)
    ok('U7 never repeats the same track back-to-back', all(seen[i]!=seen[i+1] for i in range(len(seen)-1)))
    ok('U8 next track actually playing', ev("!BGM.el.paused") and ev("BGM.el.readyState")>=2)
    ev("closeAll()"); W(300)
    pg.click('.snd[data-act="sound:toggle"]') if ev("!!document.querySelector('.snd[data-act=\"sound:toggle\"]')") else ev("document.querySelector('.hud .snd').click()")
    W(900); ok('U9 HUD ♪ off stops music', ev("BGM.el.paused || BGM.el.volume<.05") and not ev("BGM.on"))
    ev("document.querySelector('.snd[data-act=\"sound:toggle\"]').click()"); W(2200); ok('U10 HUD ♪ on resumes music', ev("BGM.on && !BGM.el.paused && BGM.el.volume>.2"), ev("[BGM.on,BGM.el.paused,BGM.el.volume]"))
    ev("showMain()"); W(1600)
    ok('U11 back to main screen: music fades out, train sound plays', ev("!BGM.on && (BGM.el.paused||BGM.el.volume<.1) && !!TRAINSFX.out"), ev("[BGM.on,BGM.el.paused,BGM.el.volume,!!TRAINSFX.out]"))
    ok('U12 no errors', not errs, errs)
    b.close()
