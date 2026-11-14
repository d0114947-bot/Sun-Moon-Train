from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader']); pg=b.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8766/'); pg.wait_for_timeout(1000); pg.evaluate("startNew()"); pg.wait_for_timeout(500)
    print(pg.evaluate("[Object.keys(XEV).length, typeof VOY_HAPS.x_secret.car, resStage(40), RES.length]")); print(errs)
