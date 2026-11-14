from playwright.sync_api import sync_playwright
import os,sys
d=sys.argv[1]; html=open(d+'/index.html').read()
page_html='<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">'+html
open(d+'/_t.html','w').write(page_html)
out=sys.argv[2]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
    pg=b.new_page(viewport={'width':1280,'height':720})
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8765/_t.html'); pg.wait_for_timeout(800)
    pg.click('#st')
    for i in range(6): pg.click('.cine'); pg.wait_for_timeout(500)
    pg.wait_for_timeout(1200)
    # boarding cine
    pg.click('.cine'); pg.wait_for_timeout(1800)
    pg.screenshot(path=out+'/s1.png')
    pg.click('#hi'); pg.wait_for_timeout(400)
    pg.click('.dlg .box'); pg.wait_for_timeout(200); pg.click('.dlg .chs button'); pg.wait_for_timeout(1200)
    pg.screenshot(path=out+'/s2.png')
    pg.click('.dlg .box'); pg.wait_for_timeout(300)
    pg.wait_for_timeout(700)
    pg.screenshot(path=out+'/s3.png')
    pg.click('[data-act="go:nature"]'); pg.wait_for_timeout(1200); pg.screenshot(path=out+'/s4.png')
    pg.click('[data-act="go:habitat"]'); pg.wait_for_timeout(1200); pg.screenshot(path=out+'/s5.png')
    pg.click('[data-act="go:memory"]'); pg.wait_for_timeout(1200); pg.screenshot(path=out+'/s6.png')
    print(errs)
    b.close()
os.remove(d+'/_t.html')
