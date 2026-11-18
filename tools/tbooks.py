# 兩本書：筆記本與生命誌的分頁、熱點收合
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=''): R.append(bool(c)); print(('PASS ' if c else 'FAIL ')+n,'' if c else x,flush=True)
BASE=open('tchap.py').read().split('BASE="')[1].split('"\n')[0]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); W(1000)
    ev(BASE+"state.currentCarriage='memory';state.storyFlags.guardRead={0:1};state.clues=state.clues||[];save();PANO.active=null;RUNNING=true;render()"); W(800)
    ids=ev("[...document.querySelectorAll('[data-hs]')].map(e=>e.dataset.hs)")
    ok('B1 mem-lore/mem-atlas/mem-clues hidden', not any(i in ids for i in ['mem-lore','mem-atlas','mem-clues']), ids)
    ok('B2 mem-book named 生命誌', ev("HSDEF.find(h=>h.id==='mem-book').name")=='生命誌')
    ev("closeAll();openBook('life')"); W(600)
    nav=ev("[...document.querySelectorAll('.booknav button')].map(b=>b.textContent)")
    ok('B3 life book tabs', nav[:3]==['生命','界域地誌','植物'], nav)
    ev("[...document.querySelectorAll('.booknav button')].find(b=>b.textContent==='界域地誌').click()"); W(800)
    ok('B4 tab switches to atlas', ev("!!document.querySelector('.ov.atlas .booknav button.on')") and ev("document.querySelectorAll('#layer .ov:not(.closing)').length")==1)
    ev("closeAll();notebookPanel()"); W(600)
    nav=ev("[...document.querySelectorAll('.booknav button')].map(b=>b.textContent)")
    ok('B5 notebook tabs incl. 月界典籍 & 值勤室紀錄', '月界典籍' in nav and '值勤室紀錄' in nav, nav)
    ev("[...document.querySelectorAll('.booknav button')].find(b=>b.textContent==='值勤室紀錄').click()"); W(800)
    ok('B6 guard book opens with read record', ev("!!document.querySelector('.ov.guardbook')") and ev("document.querySelector('.ov.guardbook').textContent.includes('值勤日誌')"))
    ev("[...document.querySelectorAll('.booknav button')].find(b=>b.textContent==='月界典籍').click()"); W(800)
    ok('B7 lore opens from notebook', ev("!!document.querySelector('.ov.book .booknav button.on')") and ev("document.querySelector('.booknav button.on').textContent")=='月界典籍')
    ok('B8 no page errors', not errs, errs)
    b.close()
print('TOTAL',sum(R),'/',len(R))
