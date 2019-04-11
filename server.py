#SERVER CODE: FINAL PRACTICE#
#First things first; we import the libraries needed#

import http.server
import termcolor
import socketserver
import requests

#Next step is defining the port we're going to use#
PORT = 8000
socketserver.TCPServer.allow_reuse_adress = True #this code line allow us to reuse the same port over and over again#

#IN order to continue, we must create a class for our server related to the http protocol#
class TestHandler(http.server.BaseHTTPRequestHandler):
    #get function: access to the get method in the http protocol request
    def do_GET(self):
        termcolor.cprint(self.requestline,'blue')#first line
        #stablish the path to follow(.path)
        meth_list = self.path.split('?')
        meth = meth_list[0]
        if meth == '/':
            j = open('indexfinalpractice.html','r')#open the html file to use it
            info = j.read()
            selectinfo = 'text/html'
            code = 200 #http status code for 'ok'
        elif meth == '/karyotype':#the use selects the karyotype endpoint
            server = 'http://rest.ensembl.org'#api rest endpoint
            dir = '/info/assembly/'
            #we put the hole karyotype extraction info in a try just in case the user does not enter one of the index options
            try:
                userschoice = meth_list[1][7:]
                userschoice = userschoice.replace('+','_').lower()
                f = request.get(server + dir + userschoice + '?',headers={'Content-Type": "application/json'})#data that must be extracted
                karyotype = ''#creating empty variable to store data
                readjson = r.json()

                for i in readjson['karyotype']:
                    karyotype = karyotype + '<br>' + i
                j = open('karyotype.html','w')#next step is opening, writing and reading the html
                j.write('''<!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <title>SPECIES' KARYOTYPE</title>
                            </head>
                            <body>
                               Chromosome names : {}
                            </body>
                            </html>'''.format(karyotype))
                j = open('karyotype.html','r')
                code = 200 #ok
                #the following code in meant to work in case the user enters non-existing options
                #or incorrect parameters
            except KeyError:
                j = open('aqui van los nombres del archivo html de los errores','r')
                code = 200
            except IndexError:
                j = open('aqui van los nombres del archivo html de los errores','r')
                code = 200
            info = j.read()
            selectinfo = 'text/html'

        else:
            j = open("error.html", "r")
            code = 200
            info = j.read()
            selectinfo = 'text/html'
        # Generating the response message
        self.send_response(code)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', selectinfo)
        self.send_header('Content-Length', len(str.encode(info)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(info))

        return


Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()


print("")
print("Server Stopped")









