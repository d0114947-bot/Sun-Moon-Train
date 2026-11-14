from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader']); pg=b.new_page(); pg.goto('http://127.0.0.1:8766/'); pg.wait_for_timeout(900); ev=pg.evaluate
    ev("window.CRISIS_TEST=1;startNew();state.introDone=true;state.trainTaint=30;state.carPol={nature:70};state.crCalm=99;state.sealed=['nature']")
    print(ev("[trainT(), (crNode('depart'),trainT()), JSON.stringify(state.carPol)]"))
    ev("state.crHist=[{id:'A01',n:'x',j:1,sev:'S2',cause:'c',signs:[],acts:[],pax:[],xi:false,res:'succ',d:0,lines:[]}]")
    ev("notebookPanel()"); pg.wait_for_timeout(700); print(ev("[...document.querySelectorAll('#layer .ov')].map(o=>o.className+':'+o.textContent.slice(0,200))"))
