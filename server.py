#SERVER CODE: FINAL PRACTICE#
#First things first; we import the libraries needed#

import http.server, http.client
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
        elif self.path.startswith("/listSpecies"):  # listSpecies is select and you send the info

            info = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>LISTSPECIES</title>
        </head>
        <body style="background-color: lightgreen;">
        <p>list of species available:<br> </p>
        <ul>
        {}
        </ul>
        <a href="/"> Main page </a>
        </body>
        </html>"""
            if path == "/listSpecies":
                server = "http://rest.ensembl.org"
                dir = "/info/species?"
                r = requests.get(server + dir, headers={"Content-Type": "application/json"})
                if not r.ok:
                    f = open('error.html', 'r')
                    info = f.read()
                infojson = r.json()
                list_species = """"""
                for k, i in enumerate(infojson['species'][:int(len(infojson['species']))], start=1):
                    names = i['name']
                    list_species += "<li>{}) Common name  : {}</li>".format(k, names)
                info = info.format(list_species)
                #extracting information and storing it in the list
            else:
                server = "http://rest.ensembl.org"
                dir = "/info/species?"
                r = requests.get(server + dir, headers={"Content-Type": "application/json"})
                if not r.ok:
                    f = open('error.html', 'r')
                    info = f.read()
                infojson = r.json()
                list_species = """"""
                limit = path.split('=')[1]
                if limit == '':
                    rank = int(len(infojson['species']))
                else:
                    rank = int(limit)

                for k, i in enumerate(infojson['species'][:rank], start=1):
                    names = i['name']

                    list_species += "<li>{}) Common name  : {}</li>".format(k, names)

                info = info.format(list_species)

        #2ºkaryotype option
        elif self.path.startswith('/karyotype'):
            info = """<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>KARYOTYPE </title>
                </head>
                <body style="background-color: lightgreen;">
                    <p>Karyotype selected:</p>
                    {}<br>
                    <a href="/"> back to the main page </a>
                </body>
                </html>
                """
            #prove that the specie sis in the list
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



        elif self.path.startswith('/chromosomeLength'):
            try:
                c = str(path.split('=')[2])
                s = str(path.split('=')[1].split('&')[0])

                if s == '' or c == '':
                    f = open('data_error.html','r')
                    info = f.read()
                #the user must enter a couple non-empty values
                else:
                    server = "http://rest.ensembl.org"
                    dir = "/info/assembly/" + s + "/" + c + "?"
                    r = requests.get(server + dir, headers={"Content-Type": "application/json"})
                    #.ok is the code 200, which means there's no errors
                    if r.ok:
                        infojson = r.json()
                        length = infojson['length']
                        info = """<!DOCTYPE html>
                                    <html lang="en">
                                    <head>
                                        <meta charset="UTF-8">
                                        <title>CHROMOSOME LENGTH</title>
                                    </head>
                                    <body style="background-color: lightgreen;">
                                        <p>Species: {} / Chromosome:{} / Length : {}</p>
                                        <br>
                                        <a href="/"> Main page </a>
                                    </body>
                                    </html>
                                   """


                        info = info.format(s,c, length)
                    else:
                        f = open('data_error.html', 'r')
                        info = f.read()
            except KeyError:
                f = open('data_error.html', 'r')
                info = f.read()
            except IndexError:
                f = open('data_error.html', 'r')
                info = f.read()

        else:
            f = open('data_error.html', 'r')
            info = f.read()


        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(info)))
        self.end_headers()
        self.wfile.write(str.encode(info))#response message



###MAIN PROGRAMME
with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print("serving at port {}".format(PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()











