import http.server,functools,threading
class H(http.server.SimpleHTTPRequestHandler):
    extensions_map={**http.server.SimpleHTTPRequestHandler.extensions_map,'.html':'text/html; charset=utf-8'}
    def log_message(self,*a): pass
def run(port,d): http.server.ThreadingHTTPServer(('127.0.0.1',port),functools.partial(H,directory=d)).serve_forever()
threading.Thread(target=run,args=(8765,'/home/claude/game'),daemon=True).start()
run(8766,'/home/claude/site')
