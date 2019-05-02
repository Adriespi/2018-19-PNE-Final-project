#SERVER CODE: FINAL PRACTICE#
#First things first; we import the libraries needed#

import http.server, http.client
import termcolor
import socketserver
import requests, json

#Next step is defining the port we're going to use#
PORT = 8000
socketserver.TCPServer.allow_reuse_adress = True #this code line allow us to reuse the same port over and over again#

#IN order to continue, we must create a class for our server related to the http protocol#
class TestHandler(http.server.BaseHTTPRequestHandler):
    #get function: access to the get method in the http protocol request
    def do_GET(self):
        path = self.path
        #1ºmain page
        if path == '/':
            j = open('indexfinalpractice.html','r')#open the html file to use it
            info = j.read()
        #2ºlist species option
        elif self.path.startswith('/listSpecies'):
            info = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>SPECIES' LIST</title>
        </head>
        <body style="background-color: blue;">
        <p>Full list of available species:<br> </p>
        <ul>
        {}
        </ul>
        <a href="/"> Back to the main page </a> 
        </body>
        </html>"""
            #href used in order for the user to be able to go back to th main page
            if path == '/listSpecies':
                server = 'http://rest.ensembl.org'
                dir = '/info/species?'
                l = requests.get(server + dir, headers={'Content-Type: ''application/json'})
                if not l.ok: #in case request fails, which means there's an error
                    f = open('data_error.html','r')
                    info = f.read()#read error html file
                listspecies= ''''''
                infojson = l.json()
                for k, i in enumerate(infojson['species'][:int(len(general['species']))], start=1):
                    index = i['name']
                    listspecies += "<li>{}) Name  : {}</li>".format(k, index)

                info = info.format(listspecies)
            else:
                server = 'http://rest.ensembl.org'
                dir = '/info/species?'
                l = requests.get(server + dir, headers={'Content-Type: ''application/json'})
                if not l.ok:
                    f = open('data_error.html','r')
                    info = f.read()
                infojson = l.json()
                listspecies= ''''''
                num = path.split('=')[1] #defining the maximum number of elements in the species list
                if  num == '':
                    num2 = int(len(infojson['species']))
                else:
                    num2 = int(num)
                for k, i in enumerate(infojson['species'][:num2],start=1):
                    index = i['name']
                    listspecies += "<li>{}) Name  : {}</li>".format(k, index)

        #2ºkaryotype option
        elif self.path.startswith('/karyotype'):
            info = """<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>KARYOTYPE INFO</title>
                </head>
                <body style="background-color: green;">
                    <p>Here is show the karyotype of the specie you have selected</p>
                    {}<br>
                    <a href="/"> back to the main page </a>
                </body>
                </html>
                """
            #first show that the species is in the list
            species = (path.split('=')[1]).lower()
            t = 'info/assembly/' + species + '?content-type=application/json'
            PORT = 80
            SERVER = 'rest.ensembl.org'
            connection = http.client.HTTPConnection(SERVER, PORT)
            connection.request("GET", t)
            c = connection.getresponse()
            data = c.read().decode('utf-8')
            infojson = json.loads(data)

            #now we proceed to provide the inf to the user

            try:
                karyo = infojson['karyotype']
                if karyo == list():
                    info = info.format("Oops, no karyotype for this species \n Try again! ")
                #just in case there's no karyotype for the species selected
                else:
                    karyo2 = list()
                    for i in karyo:
                        if i == 'MT':
                            #get rid of the mt chromosome
                            continue
                        else:
                            karyo2.append(i)
                    info = info.format(karyo2)
            except KeyError:
                f = open('data_error.html', 'r')
                info = f.read()
            except IndexError:
                f = open('data_error.html', 'r')
                info = f.read()



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









