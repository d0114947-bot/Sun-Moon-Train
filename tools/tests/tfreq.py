from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader']); pg=b.new_page(); pg.goto('http://127.0.0.1:8766/'); pg.wait_for_timeout(900); ev=pg.evaluate
    ev("window.CRISIS_TEST=1;startNew();state.introDone=true")
    out=ev("""(()=>{ const runs=[]; for(let r=0;r<200;r++){ state=freshState(); state.introDone=true; const L=[]; for(let j=0;j<30;j++){ state.journeyCount=j;
      for(const ph of ['depart','arrive']){ const had=!!state.crisis; crNode(ph); const C=state.crisis; if(C&&!had) L.push([j,C.sevN,C.real]); if(C&&C.stage==='W4'){ state.crisis.acts=['observe']; crResolve(); state.repairs=[]; state.trainSt=null; } } }
     runs.push(L); } const per=runs.map(L=>L.length); const early=runs.map(L=>L.filter(x=>x[0]<6).length); const gaps=[]; runs.forEach(L=>{ for(let i=1;i<L.length;i++) gaps.push(L[i][0]-L[i-1][0]); });
     const sev={}; runs.forEach(L=>L.forEach(x=>{ sev[(x[0]<3?'j0-2':x[0]<7?'j3-6':x[0]<12?'j7-11':'j12+')+':S'+x[1]]=(sev[(x[0]<3?'j0-2':x[0]<7?'j3-6':x[0]<12?'j7-11':'j12+')+':S'+x[1]]||0)+1; }));
     return {avgPer30:per.reduce((a,b)=>a+b,0)/runs.length, avgFirst6:early.reduce((a,b)=>a+b,0)/runs.length, avgGap:gaps.reduce((a,b)=>a+b,0)/gaps.length, gap0:gaps.filter(g=>g===0).length/gaps.length, sev}; })()""")
    print(out)
