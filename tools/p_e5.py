p='/home/claude/game/src.html'; s=open(p).read()
def R(a,b,n=1):
    global s; assert s.count(a)==n,(s.count(a),a[:90]); s=s.replace(a,b)
# 再加三位一次性的隱藏訪客（使用者 2026-11-27 給的三段影片）。都只來一次；各自在去過某個界域之後的航行出現
R("""gname:'一片白羽'}};""","""gname:'一片白羽'},
 thorneye:{name:'荊纏的眼',type:'古老生命',realm:'無界迴廊的盡頭',looks:'六片褐色的羽翼，圍著一隻被黑色荊棘纏住的大眼睛；羽翼上也有小小的眼睛。',car:'memory',at:{x:50,y:26},col:['#e8d6b8','#8a6a48'],shape:'wide',important:1,
  cond:()=>state.visitedLocations.includes('boundlessCorridor'),why:'到過無界迴廊之後的航行',vid:['vis-thorneye.mp4','vis-thorneye.jpg'],
  story:[['self','典藏車廂的燈下，停著一團褐色的羽翼。中間，是一圈黑色的荊棘。'],['self','荊棘裡面……有一隻眼睛，閉著。'],['thorneye','……迴廊太長了。看太多，會迷路。所以我把眼睛纏起來。'],
   ['thorneye','可是我聽說，有一列車，把迷路的東西一個一個載回家。'],['self','荊棘鬆開了一點。那隻眼睛，慢慢睜開了。'],['thorneye','……原來，是這個樣子的光。'],
   ['self','羽翼合起來，飄出了車窗。書架上，多了一小段乾掉的荊枝。']],give:null,gname:'一小段荊枝'},
 wheeleye:{name:'輪中之眼',type:'古老生命',realm:'時隙之海的上方',looks:'好幾圈互相穿過的金色圓環，環上刻滿了細細的眼睛；正中央，是一隻藍色的大眼睛。',car:'observatory',at:{x:50,y:26},col:['#ffe6b0','#c8a85e'],shape:'round',important:1,
  cond:()=>state.visitedLocations.includes('timeriftSea'),why:'到過時隙之海之後的航行',vid:['vis-wheeleye.mp4','vis-wheeleye.jpg'],
  story:[['self','展望台的欄杆外，有好幾圈金色的環，一直在轉。'],['self','環的正中央，是一隻很大的藍眼睛。牠在看列車開過來的那條路。'],['wheeleye','……你們走過的每一段時間，我都看著。'],
   ['wheeleye','有的時間走得很快，有的很慢。可是只要還在轉，就還沒有結束。'],['self','……那你會停下來嗎？'],['wheeleye','等所有的光都到家了，再停。'],
   ['self','圓環轉了最後一圈，變成一粒很小的金色光點，掉進了欄杆的縫裡。']],give:null,gname:'一粒會轉的金光'},
 shardwing:{name:'碎羽的守望者',type:'古老生命',realm:'逆生之境的倒影裡',looks:'一層一層像碎紙片一樣的白色羽毛，身上排著一列藍色的小眼睛，正中間是一張安靜的臉。',car:'nature',at:{x:50,y:24},col:['#fbeef0','#c9a8b8'],shape:'wide',important:1,
  cond:()=>state.visitedLocations.includes('reverseRealm'),why:'到過逆生之境之後的航行',vid:['vis-shardwing.mp4','vis-shardwing.jpg'],
  story:[['self','溫室的天窗下，飄著好多白色的碎羽。碎羽拼成了一個生命的樣子。'],['shardwing','……倒影的那一邊，什麼都是反的。我的羽毛，也是一片一片拼回來的。'],
   ['shardwing','我在找一個地方，可以讓我好好地，用正的樣子停一下。'],['self','……這裡可以。花會開，燈會亮。'],['self','碎羽在培育艙上停了很久。每一片羽毛，都慢慢合在一起。'],
   ['self','牠飛走的時候，留下了一片完整的羽毛。']],give:null,gname:'一片完整的羽毛'}};""")
open(p,'w').write(s); print('ok')
