import BaseHTTPServer, os, time

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			f = self.context.files[self.path[1:]]
		except KeyError:
			try:
				f = self.context.files[os.path.join(self.path[1:], 'index')]
			except KeyError:
				self.send_error(404, "Not found")
				return
		
		self.send_response(200)
		self.send_header('Content-type', f.content_type)
		self.end_headers()
		self.wfile.write(f.data())
				

def serve(context, port):
	Handler.context = context
	s = BaseHTTPServer.HTTPServer(('', port), Handler)
	s.serve_forever()
	
if __name__ == '__main__':
	import sys
	import core
	
	c = core.Context(sys.argv[1])
	c.run()
	serve(c, 8080)

