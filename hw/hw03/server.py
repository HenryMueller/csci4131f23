from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib

# PUT YOUR GLOBAL VARIABLES AND HELPER FUNCTIONS HERE.
# It is not required, but is is strongly recommended that you write a function to parse form data 
# out of the URL, and a second function for generating the contact log page html.

contacts = {        # nested dictionary of all contacts that have submitted forms. 
                                            # Contains:
    "test"  : {                             # name,
        "email" : "testemail@example.com",  # email, 
        "date"  : "2012-5-26",              # email sent day, 
        "type"  : "Question",               # service, 
        "ssn"   : "Yes"                     # and SSN included
    },
    "Joe Schmo" : {
        "email" : "JoSchmoo@google.com",
        "date"  : "2077-4-1",
        "type"  : "Comment",
        "ssn"   : "No"
    },
    "Alice Johnson": {
        "email": "alice.j@example.com",
        "date": "2021-8-15",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Bob Smith": {
        "email": "bob.smith@example.com",
        "date": "2019-3-10",
        "type": "Question",
        "ssn": "No"
    },
    "Eva Brown": {
        "email": "eva.brown@example.com",
        "date": "2020-12-5",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Michael Davis": {
        "email": "michael.d@example.com",
        "date": "2018-6-20",
        "type": "Question",
        "ssn": "No"
    },
    "John Doe": {
        "email": "john.doe@example.com",
        "date": "2015-11-20",
        "type": "Question",
        "ssn": "Yes"
    },
    "Jane Smith": {
        "email": "jane.smith@example.com",
        "date": "2019-02-14",
        "type": "Comment",
        "ssn": "No"
    },
    "Chris Johnson": {
        "email": "chris.j@example.com",
        "date": "2020-07-30",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Emily White": {
        "email": "emily.w@example.com",
        "date": "2017-05-12",
        "type": "Question",
        "ssn": "No"
    },
    "Daniel Brown": {
        "email": "daniel.b@example.com",
        "date": "2018-09-08",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Sophia Clark": {
        "email": "sophia.c@example.com",
        "date": "2016-03-25",
        "type": "Comment",
        "ssn": "No"
    },
    "Liam Johnson": {
        "email": "liam.j@example.com",
        "date": "2023-11-08",
        "type": "Question",
        "ssn": "Yes"
    },
    "Olivia Wilson": {
        "email": "olivia.w@example.com",
        "date": "2023-11-12",
        "type": "Comment",
        "ssn": "No"
    },
    "Noah Anderson": {
        "email": "noah.a@example.com",
        "date": "2023-11-18",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Emma Davis": {
        "email": "emma.d@example.com",
        "date": "2023-11-23",
        "type": "Question",
        "ssn": "No"
    },
    "Liam Smith": {
        "email": "liam.s@example.com",
        "date": "2023-11-29",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Ava Johnson": {
        "email": "ava.j@example.com",
        "date": "2023-12-02",
        "type": "Question",
        "ssn": "Yes"
    },
    "Ethan White": {
        "email": "ethan.w@example.com",
        "date": "2023-12-07",
        "type": "Comment",
        "ssn": "No"
    },
    "Sophia Martin": {
        "email": "sophia.m@example.com",
        "date": "2023-12-12",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Mia Brown": {
        "email": "mia.b@example.com",
        "date": "2023-12-17",
        "type": "Question",
        "ssn": "No"
    },
    "James Davis": {
        "email": "james.d@example.com",
        "date": "2023-12-22",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Isabella Martinez": {
        "email": "isabella.m@example.com",
        "date": "2023-12-28",
        "type": "Comment",
        "ssn": "No"
    },
    "Liam Harris": {
        "email": "liam.h@example.com",
        "date": "2023-12-03",
        "type": "Question",
        "ssn": "Yes"
    },
    "Olivia Robinson": {
        "email": "olivia.r@example.com",
        "date": "2023-12-08",
        "type": "Comment",
        "ssn": "No"
    },
    "Noah Johnson": {
        "email": "noah.j@example.com",
        "date": "2023-12-13",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Emma Wilson": {
        "email": "emma.w@example.com",
        "date": "2023-12-18",
        "type": "Question",
        "ssn": "No"
    }
}

def extractQueries(newQuery):
    print(newQuery)
    # newQuery = urllib.parse.unquote(newQuery)

    splitNewQuery = newQuery.split("&")                             # returns a list of the data from the query string
    # for item in splitNewQuery:                                      # have to wait until after the incoming query is split
    #     print(item)
    #     unquotedItem = urllib.parse.unquote(item)                           #   in order to make sure its split properly
    #     print(unquotedItem)
    #     splitNewQuery.index[item] = unquotedItem                            # (it will handle user inputting wierd stuff: '&', '=')

    index = 0
    for nameData in splitNewQuery:
        if "name" in nameData:                                      # get index of name 
            index = splitNewQuery.index(nameData)

    
    nameData = splitNewQuery[index]                                 # get the string containing the name
    newName = nameData[nameData.index("=") + 1:]                    # get the name for the new dict element
    newName = newName.replace("+", " ")                             # replace the "+" space char with an actual space
    newName = urllib.parse.unquote(newName)                         # changes html special chars into readable ones

    email = ""
    date  = ""
    typep = ""
    ssn   = "No"

    for currData in splitNewQuery:                                  # getting variables for rest of dictionary input
        dataName = currData[:currData.index("=")]                   # current data's name (id)
        dataVal  = currData[currData.index("=") + 1:]               # current data's value
        if (dataName == "email"):
            email = dataVal
            email = urllib.parse.unquote(email)                     # changes special characters to readable ones
        elif (dataName == "date"):
            date = dataVal
        elif (dataName == "drop"):
            typep = dataVal
            typep = typep.capitalize()
        elif (dataName == "option1"):
            ssn = "Yes"
    
    if (email == "" or date == "" or typep == "" or (ssn != "No" and ssn != "Yes")):
        return 400
    
    contacts[newName] = {                                           # this way, the data is formatted in order
        "email" : email,                                            # for when we need to get it in the other function
        "date"  : date,
        "type"  : typep,
        "ssn"   : ssn
    }
    return 201

def adminContactLog():
    open('admin/contactlog/contactlog.html', "w").close()
    dynamFile = open('admin/contactlog/contactlog.html', "w")       # open the file

    rowNum = 0
    inTable = """"""                                                # table creation
    for thisName in contacts:
        thisEmail = contacts[thisName]["email"]
        thisDate  = contacts[thisName]["date"]
        thisType  = contacts[thisName]["type"]
        thisSsn   = contacts[thisName]["ssn"]
        inTable += """                <tr id="tRow""" + str(rowNum) + """">\n"""               # new table row
        inTable += """                    <td class="name">""" + thisName + """</td>\n"""            # start with name data
        inTable += """                    <td class="email"><a href="mailto:""" + thisEmail + """">""" + thisEmail + """</a></td>\n""" # email data
        inTable += """                    <td class="countDown">""" + thisDate + """</td>\n"""  # date data
        inTable += """                    <td class="type">""" + thisType + """</td>\n"""  # message type data
        inTable += """                    <td class="ssn">""" + thisSsn + """</td>\n"""   # y/n ssn data
        inTable += """                    <td class="delButton"><button class="delete R""" + str(rowNum) + """">Delete</button></td>\n""" # Delete button
        inTable += """                </tr>\n"""                                          # end current contact's row
        rowNum += 1

    htmlTemp = """
<!DOCTYPE html>
<html lang=en>
    <head>
        <meta charset="UTF-8">
        <title>Admin: My Contacts</title>
        <link href="/main.css" rel="stylesheet" id="css">
        <script src="/js/main.js" async></script>
        <script src="/js/table.js" async></script>
    </head>

    <body>
        <nav>
            <ul>
                <li><a href="/">Main Page</a></li>
                <li><a href="/contact">Contact</a></li>
                <li><a href="/testimonies">Testimonies</a></li>
                <li><a href="/admin/contactlog">Contact Log</a></li>
                <li><button class="dark-mode">Dark Mode</button></li>
            </ul>
        </nav>

        <h2>My Contacts and Appointments</h2>

        <div class="div-table">
            <table class="dynam-table">
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Send Email By</th>
                    <th>Message Type</th>
                    <th>SSN Included</th>
                    <th>Delete Row</th>
                </tr>
""" + inTable + """
            </table>
        </div>

    </body>
</html>
"""

    dynamFile.write(htmlTemp)
    dynamFile.close()
    return

def server_GET(url: str) -> tuple[str | bytes, str, int]:
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe`
    then the `url` parameter will have the value "/contact?name=joe". (so the schema and
    authority will not be included, but the full path, any query, and any anchor will be included)

    This function is called each time another program/computer makes a request to this website.
    The URL represents the requested file.

    This function should return three values (string or bytes, string, int) in a list or tuple. The first is the content to return
    The second is the content-type. The third is the HTTP Status Code for the response
    """
    #YOUR CODE GOES HERE!

    path = url
    queryString = ""
    
    if '?' in url:                                  # separate *partial* URL and data
        path = url[:url.index("?")]                 # everything in url before '?' (and data)
        queryString = url[url.index("?") + 1:]          # all the data neatly in one string
    
    if (path == "/" or path == "/main"):            # opens the main page
        return open("static/html/mainpage.html").read(), "text/html", 200
    
    elif (path == "/contact"):                      # opens the contacts page
        # if (queryString != ""):                     # contact has data
        #     extractQueries(queryString)             # function call to make new dict input
        # don't need the two lines above anymore, parameters are ignored in GET request
        return open("static/html/contactform.html").read(), "text/html", 200
    
    elif (path == "/testimonies"):                  # opens the testimonies page
        return open("static/html/testimonies.html").read(), "text/html", 200
    
    elif (path == "/admin/contactlog"):             # opens the admin contacts log page
        adminContactLog()
        return open("admin/contactlog/contactlog.html").read(), "text/html", 200
    
    elif (path == "/images/main"):
        return open("static/images/main/mainpage.jpg", "rb").read(), "image/jpeg", 200
    
    elif (path == "/main.css"):
        return open("static/css/main.css").read(), "text/css", 200
    
    elif (path == "/main.dark.css"):
        return open("static/css/main.dark.css").read(), "text/css", 200
    
    elif (path == "/js/table.js"):
        return open("static/js/table.js").read(), "text/javascript", 200
    
    elif (path == "/js/contact.js"):
        return open("static/js/contact.js").read(), "text/javascript", 200
    
    elif (path == "/js/main.js"):
        return open("static/js/main.js").read(), "text/javascript", 200
    
    else:                                           # undefined path, 404 error page
        return open("static/html/404.html").read(), "text/html", 404
    
    pass 

def server_POST(url: str, body: str) -> tuple[str | bytes, str, int]:
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe`
    then the `url` parameter will have the value "/contact?name=joe". (so the schema and
    authority will not be included, but the full path, any query, and any anchor will be included)

    This function is called each time another program/computer makes a POST request to this website.

    This function should return three values (string or bytes, string, int) in a list or tuple. The first is the content to return
    The second is the content-type. The third is the HTTP Status Code for the response
    """
    
    if (url == "/contact"):
        print("URL:  " + url)
        print("Body: " + body)
        statusCode : int = extractQueries(body)
        if (statusCode == 201):
            return open("static/html/contactform.html").read(), "text/html", statusCode
        else:
            return open("static/html/400.html").read(), "text/html", statusCode
    
    else:
        return open("static/html/404.html").read(), "text/html", 404

    pass

# You shouldn't need to change content below this. It would be best if you just left it alone.

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the content-length header sent by the BROWSER
        content_length = int(self.headers.get('Content-Length',0))
        # read the data being uploaded by the BROWSER
        body = self.rfile.read(content_length)
        # we're making some assumptions here -- but decode to a string.
        body = str(body, encoding="utf-8")

        message, content_type, response_code = server_POST(self.path, body)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(response_code)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return

    def do_GET(self):
        # Call the student-edited server code.
        message, content_type, response_code = server_GET(self.path)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(response_code)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return


def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
