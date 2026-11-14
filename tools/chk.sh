cd /tmp/claude-0/-home-claude/abce22cd-6235-5141-b5ff-f91aa22653ed/scratchpad
python3 - <<'P'
import re
s=open('/home/claude/game/src.html').read()
js='\n;\n'.join(re.findall(r'<script>(.*?)</script>',s,re.S))
open('chk.js','w').write(js)
P
node --check chk.js && python3 build.py >/dev/null && python3 build.py pages >/dev/null && echo BUILD_OK
