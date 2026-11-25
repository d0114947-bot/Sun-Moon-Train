p='/home/claude/game/src.html'; s=open(p).read()
def R(a,b,n=1):
    global s; assert s.count(a)==n,(s.count(a),a[:90]); s=s.replace(a,b)
# 沉睡之地：拿掉秘器劇情（使用者 2026-11-25：秘器劇情有點多餘）。程式都留著，NO_ARTIFACT 改成 false 就恢復
R("const NO_CURTAIN=true;","""const NO_CURTAIN=true;
/* 秘器劇情：暫時拿掉（使用者 2026-11-25：玩起來覺得多餘）。教學一完成就接「這裡究竟是什麼地方？」→ 第一次異常。改成 false 就恢復 */
const NO_ARTIFACT=!window.ARTIFACT_TEST;
if(NO_ARTIFACT) document.head.insertAdjacentHTML('beforeend','<style>#act1 .a1-icon,#act1 .a1-big,#act1 .a1-still{display:none!important}</style>');""")
R(" function noticeScene(){ setStage('notice');"," function noticeScene(){ if(NO_ARTIFACT) return endingScene(); setStage('notice');")
R("  if(a.stage==='first') a.stage='held';\n","  if(a.stage==='first') a.stage='held';\n  if(NO_ARTIFACT&&['notice','held','again'].includes(a.stage)&&!a.ended) a.stage='ending';   /* 舊存檔停在秘器劇情裡：直接接結尾 */\n")
R("  if(['held','again','free','ending'].includes(a.stage)){ icon().classList.add('show');","  if(!NO_ARTIFACT&&['held','again','free','ending'].includes(a.stage)){ icon().classList.add('show');")
R("  if(['again','free'].includes(stg)){\n   a.sinceFirst=","  if(!NO_ARTIFACT&&['again','free'].includes(stg)){\n   a.sinceFirst=")
R(" function tapArtifact(){ if(!el||busy||lock) return;"," function tapArtifact(){ if(NO_ARTIFACT||!el||busy||lock) return;")
open(p,'w').write(s); print('ok')
