from playwright.sync_api import sync_playwright
import sys
S=sys.argv[1]
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' '+str(x) if x!='' else ''),flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    for vw,vh,tag,block in [(1280,720,'d',0),(390,844,'m',0),(844,390,'l',0),(1440,900,'w',0),(390,844,'mb',1),(390,844,'mc',2)]:
        ctx=b.new_context(viewport={'width':vw,'height':vh}); pg=ctx.new_page(); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
        if block==1: pg.route('**/*.mp4',lambda r:r.abort())
        if block==2: pg.add_init_script("HTMLMediaElement.prototype.play=function(){return Promise.reject(new DOMException('blocked','NotAllowedError'))};new MutationObserver(()=>document.querySelectorAll('video[autoplay]').forEach(v=>{v.removeAttribute('autoplay');v.autoplay=false;v.pause()})).observe(document,{childList:true,subtree:true})")
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('http://127.0.0.1:8766/'); W(3200)
        r=ev("(()=>{const r=document.querySelector('#mst').getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]})()")
        ok(tag+' train covers screen', r[0]<=0.5 and r[1]<=0.5 and r[2]>=vw-0.5 and r[3]>=vh-0.5, [round(x) for x in r])
        if block: ok(tag+' fallback animated image', ev("(()=>{const i=document.querySelector('#mst img.ms-anim');return !!i&&i.complete&&i.naturalWidth===864&&!document.querySelector('#mst video')})()"))
        else:
            v=ev("(()=>{const v=document.querySelector('#mst video');return v&&[v.readyState,v.paused,v.currentTime]})()")
            ok(tag+' video playing', v and v[0]>=2 and not v[1] and v[2]>0.3, v)
        pg.screenshot(path=f'{S}/ms_{tag}0.png')
        pg.click('#ms-work'); W(1600); pg.screenshot(path=f'{S}/ms_{tag}1.png')
        rs=ev("['#ms-new','#ms-cont','#ms-work','.ms-logo .logo','#ms-note','.ms-logo .en'].map(s=>{const r=document.querySelector(s).getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom)]})")
        inside=all(a[0]>=0 and a[2]<=vw and a[1]>=0 and a[3]<=vh for a in rs[:3])
        ov=lambda a,c: not(a[2]<=c[0] or c[2]<=a[0] or a[3]<=c[1] or c[3]<=a[1])
        ok(tag+' buttons on screen, no overlap', inside and not ov(rs[0],rs[1]) and not ov(rs[0],rs[3]) and not ov(rs[1],rs[3]) and not ov(rs[0],rs[5]) and not ov(rs[1],rs[5]) and not ov(rs[2],rs[4]), rs)
        pg.click('#ms-new'); W(800); ok(tag+' new game starts', ev("!document.querySelector('#mainscreen')") and not errs, errs)
        ctx.close()
    b.close()
