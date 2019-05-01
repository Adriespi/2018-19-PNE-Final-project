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
        print(meth_list)
        meth = meth_list[0]
        print(meth)
        if meth == '/':
            j = open('indexfinalpractice.html','r')#open the html file to use it
            info = j.read()
            selectinfo = 'text/html'
            code = 200 #http status code for 'ok'
        elif meth == 'listSpecies':
            server = 'http://rest.ensembl.org'
            dir = '/info/species?'
            try:
                print(meth_list)
                top = meth_list[0][6:]
            except IndexError:
                top = 'none'
            j = requests.get(server + dir, headers={'Content-Type': 'application/json'})
            readjson = j.json()
            species = '<ul>'#creating a string for the list of species
            k = 0 #setting up a counter and initializing it in 0
            for i in readjson['species']:
                species = species + '<li>' + i['display_name']#adding item to the list (</li>)
                species = species + '</li>'
                k += 1
                #stablish the condition for the for loop to stop
                if str(k) == top:
                    break
            l = open('top.html','w')
            l.write('''<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>FULL LIST OF AVAILABLE SPECIES</title>
            </head>
            <body>
                Total number of the species : {} <br>
                Names of the species selected : {} <br>
                Limit chosen : {}
            </body>
            </html>'''.format(len(readjson["species"]), species, top))
            f = open('top.html','r')
            code = 200
            info = f.read()
            selectinfo = 'text/html'

        elif meth == '/karyotype':#the use selects the karyotype endpoint
            server = 'http://rest.ensembl.org'#api rest
            dir = '/info/assembly/'#endpoint
            #we put the whole karyotype extraction info in a try just in case the user does not enter one of the index options
            try:
                userschoice = meth_list[1][7:]
                userschoice = userschoice.replace('+','_').lower()
                f = requests.get(server + dir + userschoice + '?',headers={'Content-Type": "application/json'})#data that must be extracted
                karyotype = ''#creating empty variable to store data
                readjson = f.json()

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
                j = open('data_error.html','r')
                code = 200
                info = j.read()
                selectinfo = 'text/html'

            except IndexError:
                j = open('parameter_error.html','r')
                code = 200
                info = j.read()
                selectinfo = 'text/html'

        elif meth == "/chromosomeLength":
            try:
                options = meth_list[1].split("&")
                chromosome = options[1][7:].upper()
                userschoice = options[0][7:]
                userschoice = userschoice.replace("+", "_")
                server = "http://rest.ensembl.org"
                dir = "/info/assembly/"
                f = requests.get(server + dir + userschoice + "?", headers={"Content-Type": "application/json"})


                decoded = f.json()
                chromosomelength = "none"
                for i in decoded["top_level_region"]:
                    if i["name"] == chromosome:
                        chromosomelength = i["length"]
                if chromosomelength == "none":
                     j = open("data_error.html", "r")
                     selectinfo = 'text/html'
                else:
                    j = open("length.html", "w")
                    j.write('''<!DOCTYPE html>
                                <html lang="en">
                                    <head>
                                         <meta charset="UTF-8">
                                        <title>SELECTED CHROMOSOME'S LENGTH</title>
                                    </head>
                                    <body>
                                        Chromosome length:   {}
                                    </body>
                                </html>'''.format(chromosomelength))


                    # Read the file
                    j = open("length.html", 'r')
            except IndexError:
                j = open("parameter_error.html", "r")
                code = 200
            # Read the file
            info = j.read()
            selectinfo= 'text/html'



        else:
            j = open("url_error.html", "r")
            code = 200
            info = j.read()
            selectinfo = 'text/html'
        # Generating the response message
        self.send_response(code)
        # Define the content-type header:
        self.send_header('Content-Type', selectinfo)
        self.send_header('Content-Length', len(str.encode(info)))
        self.end_headers()
        # response message
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









