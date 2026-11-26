p='/home/claude/game/src.html'; s=open(p).read()
def R(a,b,n=1):
    global s; assert s.count(a)==n,(s.count(a),a[:90]); s=s.replace(a,b)
# 一次性的隱藏訪客：晶冠的守望者（使用者 2026-11-27 給的影片；不是遺曦）
R("""  story:[['self','欄杆上，掛著一片會動的薄紗。……是一個被亂流捲進來的生命。'],""","""  story:[['self','欄杆上，掛著一片會動的薄紗。……是一個被亂流捲進來的生命。'],""")
R(""",give:['mosslight',1],gname:'光苔片 ×1'}};
Object.entries(VISITORS).forEach(""",""",give:['mosslight',1],gname:'光苔片 ×1'},
 /* 只來一次：去過寂滅虛空之後的航行。見面時播使用者給的影片（vis-seraph.mp4） */
 seraph:{name:'晶冠的守望者',type:'古老生命',realm:'星空的更高處',looks:'一層又一層白色的羽翼，羽翼上睜著許多藍色的眼睛；頭頂浮著一圈水晶。',car:'observation',at:{x:50,y:24},col:['#eef6ff','#9fc8ff'],shape:'wide',important:1,
  cond:()=>state.visitedLocations.includes('silentVoid'),why:'到過寂滅虛空之後的航行',vid:['vis-seraph.mp4','vis-seraph.jpg'],
  story:[['self','觀星車廂的玻璃頂外面，亮起了一圈水晶。'],['self','是一對又一對白色的羽翼。羽翼上，睜開了好多好多藍色的眼睛。'],['seraph','……不要怕。我只是來看看。'],
   ['seraph','很久以前，這列車經過的時候，我也在看。我數過每一節車廂的燈。'],['self','……你一直在看著這列車？'],['seraph','我看著所有還亮著的東西。……這一次，燈比上次多。'],
   ['self','中央那隻眼睛看了我很久。然後，所有的眼睛一起閉上了。'],['self','羽翼收攏，光退回星空裡。玻璃頂上，落下一片很輕的白羽。']],give:null,gname:'一片白羽'}};
Object.entries(VISITORS).forEach(""")
R("""function visitorMeet(){ const v=visHere(); if(!v) return; const V=VISITORS[v.id]; v.met=1; let sc=V.story.slice();""",
  """function visitorMeet(){ const v=visHere(); if(!v) return; const V=VISITORS[v.id]; v.met=1; let sc=V.story.slice(); if(V.vid) try{ xevVid(V.vid[0],V.vid[1]).classList.add('visvid'); }catch(e){}""")
R(""".xevvid.out{opacity:0;transition:opacity .7s ease}""",""".xevvid.out{opacity:0;transition:opacity .7s ease}
.xevvid.visvid{background:#f2f5fb}.xevvid.visvid video{object-fit:contain}""")
open(p,'w').write(s); print('ok')
