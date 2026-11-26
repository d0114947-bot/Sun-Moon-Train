p='/home/claude/game/src.html'; s=open(p).read()
def R(a,b,n=1):
    global s; assert s.count(a)==n,(s.count(a),a[:90]); s=s.replace(a,b)
# 1. 被襲擊的車廂（危機爆發到處理完之前）＋駕駛室後方
R("""const tImg=src=>state&&state.trainMoon&&MOON_IMG[src]||src;""",
"""/* 危機爆發（W4）到處理完之前：車廂換成被襲擊的樣子（比月界優先；值勤室沒有被襲擊的圖，照常） */
const DMG_IMG={'nature-front.jpg':'nature-front-dmg.jpg','nature-back.jpg':'nature-back-dmg.jpg','memory-front.jpg':'memory-front-dmg.jpg','memory-back.jpg':'memory-back-dmg.jpg',
 'habitat-front.jpg':'habitat-front-dmg.jpg','habitat-back.jpg':'habitat-back-dmg.jpg','observation-front.jpg':'observation-front-dmg.jpg','observation-back.jpg':'observation-back-dmg.jpg','cab-rear.jpg':'cab-rear-dmg.jpg'};
MOON_IMG['cab-rear.jpg']='cab-rear-moon.jpg';
const tImg=src=>crDmg()&&DMG_IMG[src]||state&&state.trainMoon&&MOON_IMG[src]||src;""")
R("""function trmSync(){""","""function crDmg(){ const C=state&&state.crisis; return !!(C&&C.real&&!C.done&&C.stage==='W4'&&state.currentPhase!=='outside'); }
function trmSync(){""")
R("""const CAB_IMG={frame:'cab-frame.webp',moon:'cab-frame-moon.webp',space:'cab-space.webp'}""","""const CAB_IMG={frame:'cab-frame.webp',moon:'cab-frame-moon.webp',dmg:'cab-frame-dmg.webp',space:'cab-space.webp',rear:'cab-rear.jpg'}""")
R("""<image href="${state.trainMoon?CAB_IMG.moon:CAB_IMG.frame}" x="0" y="0" width="1600" height="900" preserveAspectRatio="none"/>""",
  """<image href="${crDmg()?CAB_IMG.dmg:state.trainMoon?CAB_IMG.moon:CAB_IMG.frame}" x="0" y="0" width="1600" height="900" preserveAspectRatio="none"/>""")
# 2. 駕駛室後方：駕駛室也可以轉身（0＝操控台，1＝往後看：通往記憶典藏車廂的門）
R("""const vKey=c=>c==='observation'?'oview':""","""const vKey=c=>c==='cab'?'cview':c==='observation'?'oview':""")
R("""  if(c!=='memory') state.gRoom=0;\n""","""  if(c!=='memory') state.gRoom=0;\n  if(c!=='cab') state.cview=0;\n""")
R("""  h += C.views? `<img class="bg" src="${tImg(C.views[state[vKey(c)]||0])}" alt="${C.name}">` :""","""  h += c==='cab'&&state.cview===1? `<img class="bg" src="${tImg(CAB_IMG.rear)}" alt="駕駛室後方">` : C.views? `<img class="bg" src="${tImg(C.views[state[vKey(c)]||0])}" alt="${C.name}">` :""")
R("""  if(c==='habitat'&&!(state.hview||0)) h+=POOL_FX+zonePots();
  if(c==='nature'&&!(state.nview||0)) h+=podScene();
  if(C.views) h+=""","""  if(c==='habitat'&&!(state.hview||0)) h+=(crDmg()?'':POOL_FX)+zonePots();
  if(c==='nature'&&!(state.nview||0)&&!crDmg()) h+=podScene();
  if(C.views||c==='cab') h+=""")
R("""{id:'cab-back',scene:'cab',name:'返回記憶典藏車廂',shape:'back',at:{x:7,y:94},show:()=>false,act:'go:memory'},""","""{id:'cab-back',scene:'cab',name:'返回記憶典藏車廂',shape:'back',at:{x:49.5,y:56},act:'go:memory'},   /* 駕駛室後方（轉身）的門 */""")
R("""const VIEW_BACK=['hab-exit',""","""const VIEW_BACK=['cab-back','hab-exit',""")
R("""const hsView=h=>{ const C=CARRIAGES[h.scene]; if(!C||!C.views||VIEW_BOTH.includes(h.id)) return true;""","""const hsView=h=>{ const C=CARRIAGES[h.scene]; if(!C||(!C.views&&h.scene!=='cab')||VIEW_BOTH.includes(h.id)) return true;""")
open(p,'w').write(s); print('ok')
