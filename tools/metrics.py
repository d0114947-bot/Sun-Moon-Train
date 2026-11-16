# 從遊戲本身量結構數據：每個畫面的熱點數、需要注意的標記數、各類台詞長度
import json
from playwright.sync_api import sync_playwright
OUT={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); ev=pg.evaluate; W=pg.wait_for_timeout
    pg.add_init_script("window.LOCK_TEST=1"); pg.goto('http://127.0.0.1:8766/'); W(1000)
    PAX=['felinia','leviathaurora','cinder','pyro','vandora','frost']
    for stage,j,extra in [('early',3,"state.passengers={};"),('mid',8,"")]:
        base=f"document.querySelector('#mainscreen,#mainscreen-out')?.remove();closeAll();state=freshState();state.introDone=true;state.prologueDone=true;state.act3={{entered:true,canDepart:true}};state.journeyCount={j};state.currentLocation='starIslands';state.visitedLocations=['dawnForest','starIslands'];state.currentPhase='docked';state.carSeen=TRAIN.slice();state.annSeen='x';state.storyFlags.metDragon=1;"
        if stage=='mid': base+="state.grown=['dewmoss','glowcap'];state.pods=[{p:'dewmoss',st:1,j:7},{p:'glowcap',st:2,j:6},null,null];"+"".join([f"state.discoveredLifeforms.push('{x}');state.passengers['{x}']={{stage:2,talks:2,records:[{{j:1,t:'於晨曦森林登上列車'}}],aboard:true,left:false,boardedJourney:2,zone:PASSENGERS['{x}'].zone}};" for x in PAX])
        res={}
        for c in ['cab','memory','nature','habitat','observation','observatory']:
            for v in [0,1]:
                ev(base+f"state.currentCarriage='{c}';state[vKey('{c}')]={v};if('{c}'==='observation')state.oview={v};save();PANO.active=null;RUNNING=true;render()"); W(900)
                ev("closeAll();document.querySelectorAll('#layer .dlg,#layer .cine,#announce').forEach(e=>e.remove())"); W(200)
                r=ev("""(()=>{const H=[...document.querySelectorAll('#scene [data-hs]')]; return {hs:H.length, imp:H.filter(e=>e.classList.contains('st-important')||e.querySelector('.step')).length, words:H.map(e=>e.innerText.trim()).join('|').length, ids:H.map(e=>e.dataset.hs)}})()""")
                res[f'{c}{v}']=r
        OUT[stage]=res
    OUT['text']=ev("""(()=>{const L=a=>a.map(x=>Array.isArray(x)?String(x[1]||x[0]):String(x)); const st=a=>{const t=L(a); return {lines:t.length,chars:t.join('').length}};
      const out={}; try{ out.senses=Object.fromEntries(Object.entries(SENSES).map(([k,v])=>[k,st(v)])) }catch(e){out.senses=String(e)}
      try{ out.lore=DRAGON_LORE.map(x=>st(x.lines)) }catch(e){}
      try{ out.haps=Object.entries(VOY_HAPS).slice(0,40).map(([k,v])=>({k,lines:(v.lines||v.sc||[]).length})) }catch(e){out.haps=String(e)}
      try{ out.talks=Object.entries(PASSENGERS).slice(0,24).map(([k,p])=>({k,n:(p.talks||[]).length,lines:(p.talks||[]).reduce((a,t)=>a+(t.lines||[]).length,0),chars:(p.talks||[]).reduce((a,t)=>a+(t.lines||[]).join('').length,0)})) }catch(e){}
      try{ out.carIntro=Object.fromEntries(Object.entries(CAR_INTRO).map(([k,v])=>[k,st(v)])) }catch(e){}
      out.duty=DUTY_STEPS.length; out.voyMs=VOYAGE_MS; out.sigCycle=[4,2,0,4,3,4].map(i=>SIG_WHY[i].sec); out.voyN=VOY_N; out.skyWin=SKY_WIN;
      return out})()""")
    json.dump(OUT,open('metrics.json','w'),ensure_ascii=False,indent=1)
    for st in ['early','mid']:
        print(st, {k:(v['hs'],v['imp']) for k,v in OUT[st].items()})
    t=OUT['text']; print('duty',t['duty'],'voy',t['voyMs'],'sig',t['sigCycle'],'voyN',t['voyN'],'skyWin',t['skyWin'])
    print('senses',t.get('senses')); print('lore',t.get('lore')); print('talks sample',t.get('talks')[:5] if isinstance(t.get('talks'),list) else t.get('talks'))
    print('haps', (t.get('haps') or [])[:6] if isinstance(t.get('haps'),list) else t.get('haps'))
