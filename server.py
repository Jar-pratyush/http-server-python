'''
The basic idea behind creating this web server's first version is pretty simple:
1. We will use our laptop as both the server and the client that will connect to the server and verify the functionality.
2. We wait for our connection to the server and then send an HTTP request (since we are starting with HTTP of course)
3. We parse that request and figure out what it wants.
4. Either fetch the data or generate it dynamically.
5. Format as HTML and 
6. Send it back as the response. We will verify our shell and the browser Response.
'''

import http.server
import os
import sys

class ServerException(Exception):
    pass


class RequestHandler(http.server.BaseHTTPRequestHandler):
    '''
    The HTTP requests will be handled by returning a fixed page.
    '''
    Page = '''\
<html>
<body>
<p>Hello, Web</p>
</body>
</html>
            '''

    'Handling a get Request'
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type","text/html")
        #Calcute the length of the header information dynamically as it is a better practice than hardcoding it.
        content = self.Page.encode('utf-8')
        self.send_header("Content-Length",str(len(self.Page)))
        self.end_headers()
        # The stream has been update to io.BufferedBaseStream. The reason why we need to send the Page as encoded is because self.wfile.write needs a buffer to be passed and right now Page is a string so we need to transform it to a buffer first. And encoded strings are also kind of buffers hence this would work. But not directly accessing Page and passing it.
        # self.wfile.write(self.Page)
        #Use dynamically calculated length instead of hardcoding it.
        # self.wfile.write(self.Page.encode())
        self.wfile.write(content)
        # wfile - Output stream for writing a response back to the client.

class RequestHandler2(http.server.BaseHTTPRequestHandler):
    Page = '''\
<html>
<head>
<title>Server Test Page</title>
</head>
<body>
<p><H1>TEST REPONSE ON CALLING GET METHOD</H1></p>
<br>
<table>
<tr> <td>Header</td> <td>Value</td> </tr>
<tr> <td>Date and Time</td> <td>{date_time}</td> </tr>
<tr> <td>Client Host</td> <td>{client_host}</td> </tr>
<tr> <td>Cliend Port</td> <td>{client_port}</td> </tr>
<tr> <td>Command</td>     <td>{command}</td> </tr>
<tr> <td>Path</td>        <td>{path}</td> </tr>
</table>
</body>
</html>
    '''
    def do_GET(self):
        page = self.create_page()
        self.send_page(page)

    def create_page(self):
        values = {
            'date_time' : self.date_time_string(),
            'client_host' : self.client_address[0],
            'client_port' : self.client_address[1],
            'command'     : self.command,
            'path'        : self.path
        }
        page = self.Page.format(**values)
        return page
    def send_page(self,page):
        self.send_response(200)
        self.send_header("Content-Type","text/html")
        # content = self.Page.encode('utf-8')
        content = page.encode('utf-8')
        self.send_header("Content-Length",str(len(page)))
        self.end_headers()
        self.wfile.write(content)

class RequestHandler3(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            #Extract the full path of the requested file.
            full_path = os.getcwd() + self.path

            # Throw an execption on the server if the path does not exist
            if not os.path.exists(full_path):
                #The {0} in the message of exception is just to show that we are going to take the first item of the list from format(self.path) which means that format returns a list
                raise ServerException("'{0}' not found".format(self.path))
            #If we find that the full path that has been requested for from our desktop is a file we are going to process it
            elif os.path.isFile(full_path):
                self.handle_file(full_path)
            #If the path is not a file but is any other thing we are going to not handle it
            else:
                raise ServerException("Found an Unknown object '{0}".format(self.path))
        except Exception as msg:
                self.handle_error(msg)

            


if __name__ == '__main__':
    serverAddress = ('',8080)
    # server = http.server.HTTPServer(serverAddress,RequestHandler)
    server = http.server.HTTPServer(serverAddress,RequestHandler2)
    try:
        print("Script running on a Infinite Wait Time. Ctrl+C to terminate.")
        server.serve_forever()
    except KeyboardInterrupt:
        #The Idea is that the server will listen for infinite time on port 8080 and once we call Ctrl+C to termiate the program we would have made the port enter a Zombie State for 1 to 2 minutes making it unresponsive to immediate termination requests. So we intoduce a simple idea that is to free the port immediately.
        print("\nStopping Server due to keyboard interrupt.")
        server.server_close() #Immediately free the port 8080
        print("Program terminated manually!")
        sys.exit(0)
