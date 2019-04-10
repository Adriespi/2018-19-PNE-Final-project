#SERVER CODE: FINAL PRACTICE#
#First things first; we import the libraries needed#

import http.server
import termcolor
import socketserver


#Next step is defining the port we're going to use#
PORT = 8000
socketserver.TCPServer.allow_reuse_adress = True #this code line allow us to reuse the same port over and over again#

#IN order to continue, we must create a class for our server related to the http protocol#
class TestHandler(http.server.BaseHTTPRequestHandler):
    #get function: access to the get method in the http protocol request
    def get_method(self):
        termcolor.cprint(self.requestline,'blue')#first line
        #stablish the path to follow(.path)
        meth_list = self.path.split('?')
        meth = meth_list[0]
        if meth == '/':
            j = open('indexfinalpractice.html','r')#open the html file to use it
            info = j.read()
            selectinfo = 'text/html'
            code = 200
        elif meth == '/karyotype':#the use selects the karyotype endpoint
            server = 'http://rest.ensembl.org'#api rest endpoint
            dir = '/info/assembly/'
            #we put the hole karyotype extraction info in a try just in case the user does not enter one of the index options
            try:





