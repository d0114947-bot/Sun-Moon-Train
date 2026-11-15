# 列車部分的玩家：只點畫面上看得到的東西
TR0=time.time(); log('=== 列車部分開始')
stuck={'n':0,'last':''}
JS_VIS="""(()=>{ const vis=e=>{ const r=e.getBoundingClientRect(), s=getComputedStyle(e); return r.width>0&&r.height>0&&s.visibility!=='hidden'&&s.display!=='none'&&r.right>0&&r.left<innerWidth&&r.bottom>0&&r.top<innerHeight; };
 const hs=[...document.querySelectorAll('#scene [data-hs],#scene [data-hid]')].filter(vis);
 const steps=[...document.querySelectorAll('#scene .step')].filter(vis).map(e=>{ const h=e.closest('[data-hs],[data-hid]'); return h?(h.dataset.hs||h.dataset.hid):null; }).filter(Boolean);
 return {n:hs.length, labels:hs.map(e=>(e.innerText||'').trim()).filter(Boolean), steps, hud:[...document.querySelectorAll('#hud button,.right button,.snd')].filter(vis).map(b=>b.innerText.trim()).filter(Boolean),
  ann:!!document.querySelector('#announce.on'), toasts:[...document.querySelectorAll('.toast')].filter(vis).length, a5:!!document.querySelector('.a5-cur') }; })()"""
def clickEl(sel):
    r=ev(f"""(()=>{{ const e=document.querySelector({json.dumps(sel)}); if(!e) return null; e.scrollIntoView&&0; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2,r.width]; }})()""")
    if not r or r[2]==0: return False
    pg.mouse.click(r[0],r[1]); return True
def clickHs(id):
    r=ev(f"""(()=>{{ const L=[...document.querySelectorAll('#scene [data-hs="{id}"],#scene [data-hid="{id}"]')].filter(e=>{{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&s.visibility!=='hidden'&&r.right>0&&r.left<innerWidth;}}); const e=L[0]; if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]; }})()""")
    if not r: return False
    pg.mouse.click(r[0],r[1]); return True
def turn():
    if clickEl('#scene .pano-turn.r'): W(1600); return True
    return False
def scene(): return ev("HS_SCENE()")
def go_to(car,maxs=40):
    for _ in range(maxs):
        cur=ev("state.currentPhase==='outside'?'out':state.currentCarriage")
        if cur==car: return True
        if busy(): handle(); continue
        T=ev("TRAIN"); i,j=T.index(cur),T.index(car); nxt=T[i+(1 if j>i else -1)]
        did=False
        for h in ev(f"HSDEF.filter(h=>h.scene==='{cur}'&&h.act==='go:{nxt}').map(h=>h.id)"):
            if clickHs(h): did=True; log('  click door',h); break
        if not did:
            if not turn(): log('  cannot find door to',nxt); return False
            continue
        for _ in range(30):
            W(400)
            if ev(f"state.currentCarriage==='{nxt}'&&!TRANS.busy"): break
        W(700); watch()
    return ev("state.currentCarriage")==car
def busy(): return ev("!!document.querySelector('#layer .dlg,#layer .cine,#layer .board,#layer .ov:not(.closing),.hdw,#layer .pop,.cpop')")
def handle():
    watch()
    k=ev("""(()=>{ const L=document.querySelector('#layer'); if(L.querySelector('.cine')) return 'cine'; if(L.querySelector('.ov.board')) return 'board'; if(L.querySelector('.dlg')) return 'dlg';
      const o=[...L.querySelectorAll('.ov:not(.closing)')].pop(); if(o){ return 'ov:'+o.className+'|'+((o.querySelector('h2')||{}).innerText||''); } if(document.querySelector('.cpop')) return 'cpop'; if(document.querySelector('.hdw')) return 'hdw:'+document.querySelector('.hdw').dataset.hs; if(L.querySelector('.pop')) return 'pop'; return ''; })()""")
    if not k: return False
    if k=='cine': clickEl('#layer .cine'); W(700); return True
    if k=='board': W(1500); shot('board'); clickEl('#hi'); W(1200); return True
    if k=='dlg':
        # 發光的字（玩家會點）
        if ev("!!document.querySelector('#layer .dlg mark.hl:not(.got)')"): clickEl('#layer .dlg mark.hl:not(.got)'); log('  tap glowing words'); W(600); return True
        if ev("!!document.querySelector('#layer .dlg .chs button')"):
            t=ev("[...document.querySelectorAll('#layer .dlg .chs button')].map(b=>b.innerText)"); log('  choices',t); clickEl('#layer .dlg .chs button'); W(1200); return True
        if not clickEl('#layer .dlg .box'): ev("document.querySelector('#layer .dlg .box')?.click()")
        log('   dlg click') if ev("!!document.querySelector('#layer .ov:not(.closing)')") else None
        W(500); return True
    if k=='cpop':
        log('  confirm:', ev("document.querySelector('.cpop').innerText.replace(/\\n/g,' ').slice(0,90)")); clickEl('.cpop-y'); W(900); return True
    if k=='pop':
        log('  confirm pop', ev("document.querySelector('#layer .pop').innerText.slice(0,80)")); clickEl('#layer .pop .btn:not(.ghost)') or clickEl('#layer .pop button'); W(800); return True
    if k.startswith('hdw:'):
        hs=k[4:]; log('  drawer',hs, ev("document.querySelector('.hdw').innerText.replace(/\\n/g,' ').slice(0,100)"))
        if hs.startswith('hab-'):
            z=hs[4:]
            if ev(f"aboard('sola')&&zoneOf('sola')==='{z}'&&!careOk('sola')"):
                for d in ['t','l','h']:
                    v=ev(f"CARE.sola['{d}']")
                    if v is not None: clickEl(f'.hdw [data-dk="{d}"][data-dv="{v}"]'); W(500)
                log('  adjusted zone for sola, ok=',ev("careOk('sola')"))
            W(800)
        elif hs=='nat-crystal' and not ev("state.storyFlags.gt_light"):
            clickEl('.hdw .hdw-it:not(.on)'); W(800)
        else:
            if ev("!!document.querySelector('.hdw .hdw-it:not(.on):not([disabled])')"): clickEl('.hdw .hdw-it:not(.on):not([disabled])'); W(900)
            if not ev("!!document.querySelector('.hdw')"): return True
        pg.mouse.click(640,690); W(700); return True
    # 面板
    cls,h2=k[3:].split('|',1); log('  panel',h2,'(',cls,')')
    W(900);
    if ev("!!document.querySelector('#layer .ov [data-dk]')"):
        r=ev("(document.querySelector('#layer .a5-react')||{}).innerText||''")
        if r: log('   panel hint:',r)
        for _ in range(4):
            m=ev("aboard('sola')&&!careOk('sola')&&document.querySelector('#layer .a5-react')?mismatch('sola',zoneOf('sola')):null")
            if not m: break
            v=ev("CARE.sola['%s']"%m['k']); clickEl('#layer .ov [data-dk="%s"][data-dv="%s"]'%(m['k'],v)); W(900)
            r=ev("(document.querySelector('#layer .a5-react')||{}).innerText||''"); log('   adjusted',m['k'],'->',v,'| hint now:',r)
    if 'crov' in cls:
        if ev("!!document.querySelector('#layer [data-cr-go]')"):
            for sel in ['#layer [data-pax="sola"]:not([disabled])','#layer [data-cr="calm"]:not([disabled])','#layer [data-cr="purify"]:not([disabled])']:
                if ev(f"!!document.querySelector('{sel}')"): clickEl(sel); W(400); log('   ',sel, ev("(document.querySelector('#layer .cr-msg')||{}).innerText")); W(2600); return True
            shot('crisis_panel'); log('   acts:',ev("state.crisis&&state.crisis.acts"),'pax:',ev("state.crisis&&state.crisis.pax.map(p=>p.id+':'+p.k)")); clickEl('#layer [data-cr-go]'); W(1200); return True
        if ev("state.act6&&state.act6.said.mind&&!state.act6.said.calmed"): clickEl('#layer .ov:not(.closing) .close'); W(800); go_to('habitat'); return True
        for sel in ['#layer [data-cr="observe"]:not([disabled])','#layer [data-cr="ask"]:not([disabled])','#layer [data-pur]']:
            if ev(f"!!document.querySelector('{sel}')") and not (sel.endswith('observe"]:not([disabled])') and ev("state.crisis&&state.crisis.intel>=3")):
                clickEl(sel); W(400); log('   ',sel, ev("(document.querySelector('#layer .cr-msg')||{}).innerText")); W(2400); return True
    if 'savep' in cls:
        if not ev("/已存檔/.test(document.querySelector('#layer .ov').innerText)") and ev("!!document.querySelector('#layer [data-save]')"):
            clickEl('#layer [data-save]'); W(1500); shot('saved');
    if 'briefov' in cls:
        for i in range(8):
            if not clickEl('#layer .ov .tl:not(.ok) .rn'): break
            W(1300)
        log('   brief rows checked:',ev("document.querySelectorAll('#layer .ov .tl.ok').length"))
    if 'eqov' in cls:
        log('   equip hint:',ev("(document.querySelector('#layer .hint1')||{}).innerText||'(none)'"))
        for k in ['tablet','compass','talisman']:
            clickEl(f'#layer [data-eq="{k}"]:not(.got)'); W(900)
    if 'lifebook' in cls:
        W(800)
        if not ev("!!document.querySelector('#layer [data-file]')"): clickEl('#layer [data-life="sola"]'); W(1000); log('   open her page')
        if ev("!!document.querySelector('#layer [data-file]')"):
            log('   slot marked:',ev("!!document.querySelector('#layer .a5-slot')")); clickEl('#layer [data-file]'); W(900)
            opts=ev("[...document.querySelectorAll('#layer .pick')].map(b=>b.innerText)"); log('   file options',opts)
            if ev("(()=>{const b=[...document.querySelectorAll('#layer .pick')].find(b=>b.innerText.includes('浮島')); if(b){b.click(); return true;} return false;})()"): W(1200); shot('filed'); log('   filed bio=',ev("filedOf('sola').bio"))
    if '要邀請誰' in h2:
        if clickEl('#layer [data-comp="sola"]'): log('   with sola'); W(1500); return True
    # 其他面板：先試主要按鈕（值勤用），再關掉
    if any(x in h2 for x in ['淨界晶環','裝備','星途符牒','領取','量測','控制晶盤','啟動']) or 'prep' in cls:
        b2=ev("[...document.querySelectorAll('#layer .ov:not(.closing) button.btn:not(.ghost):not([disabled]),#layer .ov:not(.closing) #dgo')].map(b=>b.innerText.trim())")
        log('   buttons',b2)
        if b2: clickEl('#layer .ov:not(.closing) #dgo') or clickEl('#layer .ov:not(.closing) button.btn:not(.ghost):not([disabled])'); W(1500); return True
    W(1200); shot('panel_'+(h2[:8] or 'x'))
    if not clickEl('#layer .ov:not(.closing) .close'): ev("closeAll()"); log('   (no close button, closeAll)')
    W(800); return True
def follow_badge():
    info=ev(JS_VIS)
    if info['a5']: log('  click glowing notebook'); clickEl('.a5-cur'); W(1200); return True
    for sid in info['steps']:
        log('  badge ->',sid, '| hotspots on screen:',info['n']); clickHs(sid); W(1200); return True
    return False
def snapshot_density(tag):
    info=ev(JS_VIS); log('  [畫面資訊]',tag,'熱點',info['n'],'徽章',info['steps'],'HUD',info['hud'],'廣播' if info['ann'] else '','toast',info['toasts'])
ph_last=''
for it in range(900):
    a=ev("({a4:state.act4&&state.act4.finished, a5:state.act5&&state.act5.done, a6:state.act6&&state.act6.done, epi:state.epi&&state.epi.done, car:state.currentCarriage, ph:state.currentPhase, loc:state.currentLocation, prog:state.voyage&&+state.voyage.progress.toFixed(2)})")
    phase='a4' if not a['a4'] else 'a5' if not a['a5'] else 'a6' if not a['a6'] else 'epi' if not a['epi'] else 'done'
    if phase!=ph_last: ckpt(phase); log('=== 進入',phase,'%.0fs'%(time.time()-TR0)); ph_last=phase; shot('phase_'+phase); snapshot_density(phase)
    if phase=='done': break
    if busy(): handle(); continue
    if follow_badge(): continue
    # 沒有徽章：依剛才精靈說的話去找
    if not turn() or follow_badge()==False:
        pass
    if follow_badge(): continue
    want=None
    if phase=='a4':
        d=ev("state.act4.done"); want=[c for c in ['habitat','nature','observation','memory'] if not d.get(c)]
        want=want[0] if want else None
    elif phase=='a5':
        if ev("aboard('sola')") and not ev("careOk('sola')"): want='habitat'
        elif ev("state.act5.nb") and ev("filedOf('sola').bio===undefined"): want='memory'
        elif not ev("notesOf('sola').length"): want='habitat'
    elif phase=='a6':
        if not ev("state.act6.woke"): want='cab'
        elif a['ph']=='docked': want='cab'
        else:
            C=ev("state.crisis&&{st:state.crisis.stage,intel:state.crisis.intel}")
            if C and C['intel']<3: want='observation'
            elif ev("state.act6.said.mind&&!state.act6.said.calmed"): want='habitat'
            elif ev("(state.carPol||{}).habitat>0&&state.act6.resolved"): want='cab'
            elif ev("state.crisis&&state.crisis.burst&&!state.crisis.done"): want='cab'
    elif phase=='epi':
        if a['ph']=='outside':
            if ev("(state.places||[]).includes('sola')"):
                for h in ev("HSDEF.filter(h=>h.scene===HS_SCENE()&&(h.act==='back:'||h.shape==='back')).map(h=>h.id)"):
                    if clickHs(h): log('  back to train'); break
                W(2500); continue
        elif a['ph']=='docked' and a['loc']=='starIslands': want='habitat'
    if want and a['car']!=want and a['ph']!='outside': log('  go to',want); go_to(want); continue
    W(1500); watch()
    stuck['n']+=1
    if stuck['n']%20==0: shot('idle'); snapshot_density('idle'); log('  ...idle', a, ev("({busy:act4Busy(),a6:state.act6,pol:state.carPol,cr:!!state.crisis,lay:[...document.querySelectorAll('#layer > *')].map(e=>e.className)})"))
log('=== 序章完成 列車部分 %.0fs'%(time.time()-TR0))
shot('end')
log('errors',errs)
