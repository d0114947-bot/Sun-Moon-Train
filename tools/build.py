# 建置：src.html（相對檔名）
#   python3 build.py          → game/index.html（圖片以 data URI 內嵌，供 claude.ai 發佈）
#   python3 build.py pages    → site/index.html + site/assets/（GitHub Pages 用）
import base64,os,re,shutil,sys
d='/home/claude/game'; s=open(d+'/src.html').read()
MIME={'jpg':'image/jpeg','webp':'image/webp','png':'image/png','mp4':'video/mp4','mp3':'audio/mpeg'}
files=sorted(set(re.findall(r"'([\w-]+\.(?:jpg|webp|png|mp4|mp3))'",s)))
for f in files: assert os.path.exists(f'{d}/{f}'),f
pages=len(sys.argv)>1 and sys.argv[1]=='pages'
if pages:
    out='/home/claude/site'; os.makedirs(out+'/assets',exist_ok=True)
    for f in files:
        shutil.copy2(f'{d}/{f}',f'{out}/assets/{f}'); s=s.replace(f"'{f}'",f"'assets/{f}'")
    head='<!doctype html>\n<html lang="zh-Hant">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E%3Ccircle cx=%2232%22 cy=%2232%22 r=%2226%22 fill=%22%23f3d9a0%22/%3E%3Ccircle cx=%2242%22 cy=%2226%22 r=%2222%22 fill=%22%231d1a33%22/%3E%3C/svg%3E">\n'
    if not s.lstrip().lower().startswith('<!doctype'):
        s=head+s
    open(out+'/index.html','w').write(s)
    open(out+'/.nojekyll','w').write('')
    print('site/index.html',round(os.path.getsize(out+'/index.html')/1e6,2),'MB;',len(files),'assets')
else:
    for f in files:
        if f.endswith('.mp3'): s=s.replace(f"'{f}'","''"); continue   # 內嵌版不放音樂（太大）；遊戲會自動略過
        uri='data:'+MIME[f.rsplit('.',1)[1]]+';base64,'+base64.b64encode(open(f'{d}/{f}','rb').read()).decode()
        s=s.replace(f"'{f}'","'"+uri+"'")
    assert ".jpg'" not in s and ".webp'" not in s and ".mp4'" not in s and ".mp3'" not in s
    open(d+'/index.html','w').write(s)
    print('index.html',round(os.path.getsize(d+'/index.html')/1e6,2),'MB;',len(files),'assets')
