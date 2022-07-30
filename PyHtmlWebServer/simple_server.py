import http.server 

class CGIRequestHandler(http.server.CGIHTTPRequestHandler): # create a subclass of CGIHTTPRequestHandler for dealing with CGI requests 
    def do_GET(self): # do_GET method is used to handle GET requests
        if self.path == '/': # if the path is '/'
            self.path = 'index.html' # set the path to index.html
        elif self.path == '/page': # if the path is '/page'
            self.path = 'cgi-bin/page.py' # set the path to cgi-bin/page.py
        return http.server.CGIHTTPRequestHandler.do_GET(self) # call the original do_GET method
 
handler = CGIRequestHandler # set the handler to CGIRequestHandler, the handler is used to handle the request

PORT = 8000 # set the port to 8000 for the server

server = http.server.HTTPServer(("",PORT), handler) # create a server with the port and handler specified above
server.serve_forever() # start the server and wait for requests
#create folder cgi-bin in directory.