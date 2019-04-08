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
    #get function


