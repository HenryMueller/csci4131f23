from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib #Only for parse.unquote and parse.unquote_plus.
import json
import base64
from typing import Union, Optional
import re
# If you need to add anything above here you should check with course staff first.

# PUT YOUR GLOBAL VARIABLES AND HELPER FUNCTIONS HERE.
# It is not required, but is is strongly recommended that you write a function to parse form data 
# out of the URL, and a second function for generating the contact log page html.

sale = { "active": False }
# sale = { "active": True, "message": "50% off, get it quick!"}

next_id = 28        # the next id to give to a contact starting with
                    # 28 because there are (currently) 27 tester contacts

contacts = {        # nested dictionary of all contacts that have submitted forms. 
                                            # Contains:
    "test"  : {                             # name,
        "id" : 1,                           # id,
        "email" : "testemail@example.com",  # email, 
        "date"  : "2012-5-26",              # email sent day, 
        "type"  : "Question",               # service, 
        "ssn"   : "Yes"                     # and SSN included
    },
    "Joe Schmo" : {
        "id" : 2,
        "email" : "JoSchmoo@google.com",
        "date"  : "2077-4-1",
        "type"  : "Comment",
        "ssn"   : "No"
    },
    "Alice Johnson": {
        "id" : 3,
        "email": "alice.j@example.com",
        "date": "2021-8-15",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Bob Smith": {
        "id" : 4,
        "email": "bob.smith@example.com",
        "date": "2019-3-10",
        "type": "Question",
        "ssn": "No"
    },
    "Eva Brown": {
        "id" : 5,
        "email": "eva.brown@example.com",
        "date": "2020-12-5",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Michael Davis": {
        "id" : 6,
        "email": "michael.d@example.com",
        "date": "2018-6-20",
        "type": "Question",
        "ssn": "No"
    },
    "John Doe": {
        "id" : 7,
        "email": "john.doe@example.com",
        "date": "2015-11-20",
        "type": "Question",
        "ssn": "Yes"
    },
    "Jane Smith": {
        "id" : 8,
        "email": "jane.smith@example.com",
        "date": "2019-02-14",
        "type": "Comment",
        "ssn": "No"
    },
    "Chris Johnson": {
        "id" : 9,
        "email": "chris.j@example.com",
        "date": "2020-07-30",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Emily White": {
        "id" : 10,
        "email": "emily.w@example.com",
        "date": "2017-05-12",
        "type": "Question",
        "ssn": "No"
    },
    "Daniel Brown": {
        "id" : 11,
        "email": "daniel.b@example.com",
        "date": "2018-09-08",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Sophia Clark": {
        "id" : 12,
        "email": "sophia.c@example.com",
        "date": "2016-03-25",
        "type": "Comment",
        "ssn": "No"
    },
    "Liam Johnson": {
        "id" : 13,
        "email": "liam.j@example.com",
        "date": "2023-11-08",
        "type": "Question",
        "ssn": "Yes"
    },
    "Olivia Wilson": {
        "id" : 14,
        "email": "olivia.w@example.com",
        "date": "2023-11-12",
        "type": "Comment",
        "ssn": "No"
    },
    "Noah Anderson": {
        "id" : 15,
        "email": "noah.a@example.com",
        "date": "2023-11-18",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Emma Davis": {
        "id" : 16,
        "email": "emma.d@example.com",
        "date": "2023-11-23",
        "type": "Question",
        "ssn": "No"
    },
    "Liam Smith": {
        "id" : 17,
        "email": "liam.s@example.com",
        "date": "2023-11-29",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Ava Johnson": {
        "id" : 18,
        "email": "ava.j@example.com",
        "date": "2023-12-02",
        "type": "Question",
        "ssn": "Yes"
    },
    "Ethan White": {
        "id" : 19,
        "email": "ethan.w@example.com",
        "date": "2023-12-07",
        "type": "Comment",
        "ssn": "No"
    },
    "Sophia Martin": {
        "id" : 20,
        "email": "sophia.m@example.com",
        "date": "2023-12-12",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Mia Brown": {
        "id" : 21,
        "email": "mia.b@example.com",
        "date": "2023-12-17",
        "type": "Question",
        "ssn": "No"
    },
    "James Davis": {
        "id" : 22,
        "email": "james.d@example.com",
        "date": "2023-12-22",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Isabella Martinez": {
        "id" : 23,
        "email": "isabella.m@example.com",
        "date": "2023-12-28",
        "type": "Comment",
        "ssn": "No"
    },
    "Liam Harris": {
        "id" : 24,
        "email": "liam.h@example.com",
        "date": "2023-12-03",
        "type": "Question",
        "ssn": "Yes"
    },
    "Olivia Robinson": {
        "id" : 25,
        "email": "olivia.r@example.com",
        "date": "2023-12-08",
        "type": "Comment",
        "ssn": "No"
    },
    "Noah Johnson": {
        "id" : 26,
        "email": "noah.j@example.com",
        "date": "2023-12-13",
        "type": "Comment",
        "ssn": "Yes"
    },
    "Emma Wilson": {
        "id" : 27,
        "email": "emma.w@example.com",
        "date": "2023-12-18",
        "type": "Question",
        "ssn": "No"
    }
}

def extractQueries(newQuery):
    try:
        print(newQuery)
        # newQuery = urllib.parse.unquote(newQuery)

        splitNewQuery = newQuery.split("&")                             # returns a list of the data from the query string

        index = 0
        for nameData in splitNewQuery:
            if "name" in nameData:                                      # get index of name 
                index = splitNewQuery.index(nameData)

        
        nameData = splitNewQuery[index]                                 # get the string containing the name
        newName = nameData[nameData.index("=") + 1:]                    # get the name for the new dict element
        newName = newName.replace("+", " ")                             # replace the "+" space char with an actual space
        newName = urllib.parse.unquote(newName)                     # changes html special chars into readable ones
        
        
        if (newName == ""):
            return 400

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
            "id"    : next_id,                                           # for when we need to get it in the other function
            "email" : email,
            "date"  : date,
            "type"  : typep,
            "ssn"   : ssn
        }

        print("contacts[newName]: ")
        print(contacts[newName])

        next_id = next_id + 1
        print("next_id = " + next_id)
        
        return 201
    
    except:
        return 400

def adminContactLog():
    open('admin/contactlog/contactlog.html', "w").close()
    dynamFile = open('admin/contactlog/contactlog.html', "w")       # open the file

    inTable = """"""                                                # table creation
    for thisName in contacts:
        thisRow   = contacts[thisName]["id"]
        thisEmail = contacts[thisName]["email"]
        thisDate  = contacts[thisName]["date"]
        thisType  = contacts[thisName]["type"]
        thisSsn   = contacts[thisName]["ssn"]
        inTable += """                <tr id="tRow""" + str(thisRow) + """">\n"""               # new table row
        inTable += """                    <td class="name">""" + thisName + """</td>\n"""            # start with name data
        inTable += """                    <td class="email"><a href="mailto:""" + thisEmail + """">""" + thisEmail + """</a></td>\n""" # email data
        inTable += """                    <td class="countDown">""" + thisDate + """</td>\n"""  # date data
        inTable += """                    <td class="type">""" + thisType + """</td>\n"""  # message type data
        inTable += """                    <td class="ssn">""" + thisSsn + """</td>\n"""   # y/n ssn data
        inTable += """                    <td class="delButton"><button class="delete R""" + str(thisRow) + """">Delete</button></td>\n""" # Delete button
        inTable += """                </tr>\n"""                                          # end current contact's row

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

        <div class="sale">
            <div>
                <label for="sale-input">Set Sale:</label>
                <input type="text" id="sale-input" name="sale-input" required>
            </div>

            <div>
                <button id="set-sale">Set</button>
            </div>

            <div>
                <button id="del-sale">Delete</button>
            </div>
        </div>

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

def authLogic(valid: dict[str, str], headers: dict[str, str]):
    auth = headers.get("Authorization")

    if auth and auth.startswith("Basic "):
        encCredentials = auth.split(" ")[1]
        decCredentials = base64.b64decode(encCredentials).decode("utf-8")
        username, password = decCredentials.split(":")

        if username in valid and password == valid[username]:
            resBody = "Auth Successful"
            resCode = 200
            resHeaders = {"Content-Type": "text/plain"}
        
        else:
            resBody = "Auth Failure - credentials invalid"
            resCode = 403
            resHeaders = {"Content-Type": "text/plain",
                          "WWW-Authenticate": "Basic realm='User Visible Realm'"}
    else:
        resBody = "Auth header required"
        resCode = 401
        resHeaders = {"Content-Type": "text/plain",
                      "WWW-Authenticate": "Basic realm='User Visible Realm'"}
    
    return resBody, resCode, resHeaders

# The method signature is a bit "hairy", but don't stress it -- just check the documentation below.
def server(method: str, url: str, body: Optional[str], headers: dict[str, str]) -> tuple[Union[str, bytes], int, dict[str, str]]:    
    print("\nSERVER FUNC\n")
    """
    method will be the HTTP method used, for our server that's GET, POST, DELETE
    url is the partial url, just like seen in previous assignments
    body will either be the python special None (if the body wouldn't be sent)
         or the body will be a string-parsed version of what data was sent.
    headers will be a python dictionary containing all sent headers.

    This function returns 3 things:
    The response body (a string containing text, or binary data)
    The response code (200 = ok, 404=not found, etc.)
    A _dictionary_ of headers. This should always contain Content-Type as seen in the example below.
    """
    # Parse URL -- this is probably the best way to do it. Delete if you want.
    if "?" in url:
        url, *parameters = url.split("?", 1)
        print("Parameters:")
        print(parameters)
        print("END PARAMETERS")
    print("URL")
    print(url)
    print("END URL")
    print("Headers:")
    print(headers)
    print("END HEADERS")
    print("Body:")
    print(body)
    print("END BODY")

    credentials = {'admin':'password'}
    
    # opens the main page
    if (method == "GET" and (url ==  "/" or url == "/main")):
        return open("static/html/mainpage.html").read(), 200, {"Content-Type": "text/html; charset=utf-8"}
    
    # opens the contacts page
    elif (url == "/contact"):
        if (method == "GET"):                                               # GET method
            return open("static/html/contactform.html").read(), 200, {"Content-Type": "text/html; charset=utf-8"}
        elif (method == "POST"):                                            # POST method
            statusCode : int = extractQueries(body)
            if (statusCode == 201):                                         # if the data was correct
                return open("static/html/contactform.html").read(), statusCode, {"Content-Type": "text/html; charset=utf-8"}
            else:                                                           # input data was incorrect, status = 401
                return open("static/html/400.html").read(), statusCode, {"Content-Type": "text/html; charset=utf-8"}
    
    # opens the testimonies page
    elif (method == "GET" and url ==  "/testimonies"):
        return open("static/html/testimonies.html").read(), 200, {"Content-Type": "text/html; charset=utf-8"} 
    
    # opens the admin contacts log page
    elif (method == "GET" and url ==  "/admin/contactlog"):
        authResponse = authLogic(credentials, headers)
        if authResponse[1] != 200:
            return authResponse
        
        adminContactLog()
        return open("admin/contactlog/contactlog.html").read(), 200, {"Content-Type": "text/html; charset=utf-8"}
    
    # opens the mainpage image
    elif (method == "GET" and url ==  "/images/main"):
        return open("static/images/main/mainpage.jpg", "rb").read(), 200, {"Content-Type": "image/jpeg"}
    
    # opens main css theme
    elif (method == "GET" and url ==  "/main.css"):
        return open("static/css/main.css").read(), 200, {"Content-Type": "text/css"}
    
    # opens alternate css theme
    elif (method == "GET" and url ==  "/main.dark.css"):
        return open("static/css/main.dark.css").read(), 200, {"Content-Type": "text/css"}
    
    # opens the js for the contact log
    elif (method == "GET" and url ==  "/js/table.js"):
        return open("static/js/table.js").read(), 200, {"Content-Type": "text/javascript"}
    
    # opens the js for the contact page
    elif (method == "GET" and url ==  "/js/contact.js"):                    
        return open("static/js/contact.js").read(), 200, {"Content-Type": "text/javascript"}
    
    # opens the js for the workings of every page
    elif (method == "GET" and url ==  "/js/main.js"):                       
        return open("static/js/main.js").read(), 200, {"Content-Type": "text/javascript"}
    
    # deletes the clicked on contact from the contact dictionary
    elif (method == "DELETE" and url ==  "/api/contact"):
        authResponse = authLogic(credentials, headers)
        if authResponse[1] != 200:
            return authResponse
        
        if not headers.get("Content-Type") == "application/json":           # content-type != json
            return "body not json", 400, {"Content-Type": "text/plain"}
        else:                                                               # content-type == json
            try:
                body = json.loads(body)                                     # parse body into python dictionary
                if "id" not in body:                                        # id parameter is not found
                    return "id property is required", 400, {"Content-Type": "text/plain"}
                
                else:                                                       # id parameter is found
                    for contact in contacts:                                # loop through all contacts
                        if (contacts[contact]["id"] == int(body["id"])):    # if current contact's id matches the desired body's id,
                            contacts.pop(contact)                           # delete the contact
                            return "contact deleted", 200, {"Content-Type": "text/plain"}    # return, contact found and deleted
                    # loop has finished but no contact was found means the contact must have been deleted previously
                    return "already deleted", 404, {"Content-Type": "text/plain"}
            except:
                return "body not json", 400, {"Content-Type": "text/plain"}
    
    # GET request to GET the current sale and message (if any)
    elif (method == "GET" and url ==  "/api/sale"):
        global sale
        print(sale)
        return json.dumps(sale), 200, {"Content-Type": "application/json"}
    
    # POST request to SET the current sale
    elif (method == "POST" and url ==  "/api/sale"):
        authResponse = authLogic(credentials, headers)
        if authResponse[1] != 200:
            return authResponse
        
        if not headers.get("Content-Type") == "application/json":
            return "(POST-not headers) body not json", 400, {"Content-Type": "text/plain"}
        else:
            try:
                body = json.loads(body)
                if "message" not in body:
                    return "message and sale properties are required", 400, {"Content-Type": "text/plain"}
                else:
                    sale = {"active": True, "message": body["message"] }
                    return "sale", 200, {"Content-Type": "text/html; charset=utf-8"}
            except:
                return "(POST-except) body not json", 400, {"Content-Type": "text/plain"}
    
    # DELETE request to remove the current sale
    elif (method == "DELETE" and url ==  "/api/sale"):
        authResponse = authLogic(credentials, headers)
        if authResponse[1] != 200:
            return authResponse

        sale = {"active": False}
        return "deleted sale", 200, {"Content-Type": "text/plain"}

    # And another freebie -- the 404 page will probably look like this.
    # Notice how we have to be explicit that "text/html" should be the value for
    # header: "Content-Type" now?]
    # I am sorry that you're going to have to do a bunch of boring refactoring.
    else:
        return open("static/html/404.html").read(), 404, {"Content-Type": "text/html; charset=utf-8"}


# You shouldn't need to change content below this. It would be best if you just left it alone.


class RequestHandler(BaseHTTPRequestHandler):
    def c_read_body(self):
        # Read the content-length header sent by the BROWSER
        content_length = int(self.headers.get("Content-Length", 0))
        # read the data being uploaded by the BROWSER
        body = self.rfile.read(content_length)
        # we're making some assumptions here -- but decode to a string.
        body = str(body, encoding="utf-8")
        return body

    def c_send_response(self, message, response_code, headers):
        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")
        
        # Send the first line of response.
        self.protocol_version = "HTTP/1.1"
        self.send_response(response_code)
        
        # Send headers (plus a few we'll handle for you)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", len(message))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        

    def do_POST(self):
        # Step 1: read the last bit of the request
        try:
            body = self.c_read_body()
        except Exception as error:
            # Can't read it -- that's the client's fault 400
            self.c_send_response("Couldn't read body as text", 400, {'Content-Type':"text/plain"})
            raise
                
        try:
            # Step 2: handle it.
            message, response_code, headers = server("POST", self.path, body, self.headers)
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response("The server function crashed.", 500, {'Content-Type':"text/plain"})
            raise
        

    def do_GET(self):
        try:
            # Step 1: handle it.
            message, response_code, headers = server("GET", self.path, None, self.headers)
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response("The server function crashed.", 500, {'Content-Type':"text/plain"})
            raise


    def do_DELETE(self):
        # Step 1: read the last bit of the request
        try:
            body = self.c_read_body()
        except Exception as error:
            # Can't read it -- that's the client's fault 400
            self.c_send_response("Couldn't read body as text", 400, {'Content-Type':"text/plain"})
            raise
        
        try:
            # Step 2: handle it.
            message, response_code, headers = server("DELETE", self.path, body, self.headers)
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response("The server function crashed.", 500, {'Content-Type':"text/plain"})
            raise



def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
