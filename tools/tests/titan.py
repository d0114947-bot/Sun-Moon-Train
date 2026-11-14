import re
P='/home/claude/game/src.html'
s=open(P,encoding='utf-8').read()
def ins_before(anchor,text,start=0):
    global s
    i=s.index(anchor,start); s=s[:i]+text+s[i:]
def ins_after(anchor,text):
    global s
    i=s.index(anchor)+len(anchor); s=s[:i]+text+s[i:]

ENTRY=r""",
 titan:{name:'苔淵巨靈',type:'other',species:'Mossbound Titan',zone:'moss',spot:{x:12,y:66},spriteH:27,ar:'340/300',color:'radial-gradient(circle,#e3f0c8,#5d7a45)',
  image:'titan.webp',still:'titan-still.webp',studies:['titan-s1.webp','titan-s2.webp'],land:true,sprite:true,art:()=>ART.portrait.unknown(),
  homeText:'深邃而古老的原始紅木森林・霧氣瀰漫的溫帶雨林深處',
  intro:'列車停靠時，森林邊緣一座長滿苔蘚的小山，緩緩動了起來。牠的肩上長著蕨類，鬍鬚像垂下的枯木鬚根，每一次沉重的呼吸，都帶起一陣帶有草木清香的晨霧。',
  bio:'在古老林海的深處，苔淵巨靈如同一座移動的小山般緩步前行。牠每一次沉重的呼吸，都會帶起陣陣帶有草木清香的晨霧。森林裡的精靈與走獸從不畏懼牠的存在，反而視牠為行走的庇護所——因為在巨靈經過的足跡上，總會滋養出最豐饒的生命與最清澈的泉水。',
  field:{alias:'行走的森林、大地之錨、沉睡古民',
   cls:'遠古巨獸 / 森林巨人類',
   danger:'中',
   rarity:'稀有',
   looks:'擁有如千年古樹般粗壯厚重的軀體，皮膚表面佈滿粗糙的樹皮紋理與深綠色的厚重苔蘚。雙肩與背脊上常年覆蓋著蕨類植物與微型地被灌木。頭部輪廓深邃，面容宛如風化嚴重的岩石，垂下如枯木鬚根般的長鬍鬚，雙手巨大而有力。',
   habitat:'深邃而古老的原始紅木森林、霧氣瀰漫的溫帶雨林深處。',
   habits:[['活動時間','極度緩慢，通常以數十年甚至數百年為一個行動與沉睡的週期。'],['飲食','以吸收土壤養分、地脈靈氣以及雨水為主，偶爾攝取少量的礦物質。'],['性格與群居','個性溫和、孤獨且極度沉穩，通常獨來獨往。對外界事物不理不睬，除非棲息地遭受嚴重破壞，否則不會主動展現攻擊性。']],
   abilities:[['自然偽裝','具備完美的自然偽裝能力，靜止時與周遭環境無異'],['承載生態','其龐大的身軀能承載並調節一片微型生態系，行走時震動地面能促進周遭植物的生長與地脈循環。']]},
  stay:2,
  talks:[
   {lines:['（自然棲台的角落，多了一座長滿苔蘚的小山。你走近了，才發現那座山有一張像岩石一樣的臉。）','……嗯。','……我……睡著了，一下子。','一下子……是從你出生之前，到剛剛。','我住的地方……樹很老，很高。紅木森林的深處，霧不會散。'],choices:[{t:'你睡了多久？',r:'……很久嗎？對我來說，只是翻了一個身。'},{t:'（安靜地等牠說下去）',r:'……你很有耐心。森林裡的小東西，也是這樣等我的。'}]},
   {lines:['（牠肩上的蕨葉輕輕晃了一下。過了很久，你才發現那是牠在呼吸。）','……我不吃東西。根……會替我吃。土裡的養分、地脈的氣、雨水。','偶爾……舔一點石頭。這輛車的石頭……有一點星星的味道。','你剛才站在我旁邊，沒有發現我吧。……我不動的時候，就只是一座長苔蘚的小山。'],choices:[{t:'真的完全沒發現。',r:'……嗯。森林裡的鳥，常常在我的頭上築巢。牠們也沒發現。'},{t:'舔石頭？',r:'……很好吃。礦物……是森林裡，最慢的點心。'}]},
   {lines:['（牠慢慢抬起一隻巨大的手，又慢慢放下。地板輕輕震了一下——苔蘚棲台上，幾株小芽一起冒了出來。）','……我走過的地方，草會長，泉水會變清。','所以森林裡的精靈和走獸……都跟在我後面走。','牠們把我當成……一座會走路的庇護所。我很少說話。可是，我喜歡牠們跟著。'],choices:[{t:'這輛車也跟著你一起長出了新芽。',r:'（牠臉上的岩石紋路，好像鬆開了一點。那也許是一個笑。）……那這輛車，也是我的森林了。'}]}
  ],
  farewell:['……地脈在叫我。很慢，很遠。','我該回去，繼續睡了。下一次醒來……也許是一百年以後。','你那時候不在了也沒關係。我走過的地方，會長出新的森林。……那裡面，會有你的味道。']
 }"""
i=s.index('const UNKNOWN_LIFE'); j=s.rindex("\n};",0,i); s=s[:j]+ENTRY+s[j:]

ins_before(" board_sola:"," board_titan:{trigger:'arrive',loc:'dawnForest',auto:true,need:()=>state.journeyCount>=7&&!state.discoveredLifeforms.includes('titan'),run:n=>boarding('titan','列車停靠的時候，月台輕輕震了一下，又一下。森林邊緣，一座長滿苔蘚與蕨葉的小山緩緩站起，帶著一陣草木清香的晨霧，一步一步走上了車門。',n)},\n")
ins_before(" int_sirenora_levi:"," int_titan_lumi:{trigger:'carriage',car:'habitat',need:()=>aboard('titan')&&aboard('lumi'),title:'苔淵巨靈與露米',run:()=>interScene('lumi','titan',[\n"
 "   ['lumi','（露米繞著那座長苔蘚的小山轉了三圈。）……這座山，有呼吸！'],['titan','……嗯。'],['lumi','你也是森林來的嗎？你身上有古樹的味道，跟我家一樣！'],['titan','……很老的森林。比你的古樹……還老一點。'],\n"
 "   ['lumi','那我可以爬上去嗎？你肩膀上的蕨葉看起來好軟。'],['titan','（過了很久，巨大的手慢慢放到地上，掌心朝上。）……慢慢來。'],\n"
 "   ['self','露米踩著巨靈的手，爬上了長滿蕨葉的肩膀。牠角上的光點一個一個亮起來，照亮了巨靈像岩石一樣的臉。'],['titan','……森林裡的小東西，都喜歡待在這裡。'],['lumi','因為這裡是會走路的森林嘛。']\n"
 "  ],'露米爬上了苔淵巨靈長滿蕨葉的肩膀。','會走路的森林','露米踩著巨靈的手，爬上長滿蕨葉的肩膀。「因為這裡是會走路的森林嘛。」')},\n")
ins_before(" if(id==='sirenora') return"," if(id==='titan') return state.currentPhase==='voyage'?'……車在搖。像地脈……在翻身。':'……（牠一動也不動。肩上的蕨葉間，一隻小蟲正在散步。）';\n")
ins_before(" {id:'bye_sola',"," {id:'titan',title:'會走路的小山',who:'titan',have:()=>state.discoveredLifeforms.includes('titan'),text:PASSENGERS.titan.intro},\n")
ins_before(" {id:'int_sirenora_levi',"," {id:'int_titan_lumi',title:'會走路的森林',who:'lumi',who2:'titan',have:()=>done('int_titan_lumi'),text:'露米踩著巨靈的手，爬上長滿蕨葉的肩膀。「因為這裡是會走路的森林嘛。」'},\n")
ins_after("{id:'sirenora',passenger:'sirenora'},","\n {id:'titan',passenger:'titan'},")

# NOTES: after sirenora list
k=s.index(" sirenora:{secs:['habitat'"); e=s.index("]}\n",k)+2
s=s[:e]+""",
 titan:{secs:['habitat','habits','abilities','bio'],thanks:'……你寫得很慢。……很好。森林，也是這樣慢慢長出來的。',list:[
  {k:'habitat',p:'紅木森林的深處，霧不會散',n:'住在霧氣不散的古老紅木森林深處'},
  {k:'habits',p:'從你出生之前，到剛剛',n:'一睡就是數十年、甚至數百年'},
  {k:'habits',p:'土裡的養分、地脈的氣、雨水',n:'靠吸收土壤養分、地脈靈氣與雨水維生'},
  {k:'abilities',p:'我不動的時候，就只是一座長苔蘚的小山',n:'靜止時和周圍環境沒有兩樣（自然偽裝）'},
  {k:'abilities',p:'我走過的地方，草會長，泉水會變清',n:'行走時能讓植物生長、泉水變清（承載生態）'},
  {k:'bio',p:'一座會走路的庇護所',n:'森林的精靈與走獸把牠當成行走的庇護所'},
  {k:null,p:'這輛車的石頭……有一點星星的味道',n:'覺得車上的石頭有星星的味道'}]}"""+s[e:]

ins_after(" sirenora:{l:1,h:3,auto:true,ok:'霧……好濃，好安靜。柔柔的光從霧裡透過來。……我好像回到峽灣了。'}",
 ",\n titan:{t:1,h:2,ok:'（牠肩上的苔蘚吸飽了水氣，顏色深了一點。）……涼涼的，濕濕的。像紅木森林的霧。……我可以……再睡一下了。'}")
ins_after(" sirenora:['那些往後退的光……像夢一樣。抓不住，但會記得。','這裡的風很安靜。很適合做夢。']",
 ",\n titan:['……星星，走得好快。我一百年……才走一步。','……這裡的風，有森林的味道。我站一下就好。']")
ins_after(" sirenora:{dawnForest:'晨霧……雖然很淡，還是讓我想起峽灣。',starIslands:'這裡有很多被遺忘的夢，在星河裡漂。'}",
 ",\n titan:{dawnForest:'……這裡的樹，很年輕。（牠走過的地方，冒出了一小片新芽。）',starIslands:'……腳底下，沒有地脈。我……走慢一點。'}")
s=s.replace("id==='vandora'||id==='frost'?'idle-stand'","id==='vandora'||id==='frost'||id==='titan'?'idle-stand'",1)
open(P,'w',encoding='utf-8').write(s)
print('ok')
