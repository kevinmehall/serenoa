import BaseHTTPServer, os, time

refresh_timeout = 10

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		context = self.server.context

		# refresh the tree if the timeout has passed
		if self.server.refresh_time < time.time() - refresh_timeout:
			print "Refreshing...", self.server.refresh_time, time.time()
			context.run()
			self.server.refresh_time = time.time()

		try:
			f = context.files[self.path[1:]]
		except KeyError:
			try:
				f = context.files[os.path.join(self.path[1:], 'index')]
			except KeyError:
				self.send_error(404, "Not found")
				return
		
		self.send_response(200)
		self.send_header('Content-type', f.content_type)
		self.end_headers()
		self.wfile.write(f.data())
				

def serve(context, port):
	s = BaseHTTPServer.HTTPServer(('', port), Handler)
	s.context = context
	s.refresh_time = 0
	s.serve_forever()
	
if __name__ == '__main__':
	import sys
	import core
	
	c = core.Context(sys.argv[1])
	serve(c, 8080)

