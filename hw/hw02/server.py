from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib

# PUT YOUR GLOBAL VARIABLES AND HELPER FUNCTIONS HERE.
# It is not required, but is is strongly recommended that you write a function to parse form data out of the URL, 
# and a second function for generating the contact log page html.
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
    
    contacts[newName] = {                                           # this way, the data is formatted in order
        "email" : email,                                            # for when we need to get it in the other function
        "date"  : date,
        "type"  : typep,
        "ssn"   : ssn
    }
    return

def adminContactLog():
    open('admin/contactlog/contactlog.html', "w").close()
    dynamFile = open('admin/contactlog/contactlog.html', "w")       # open the file

    inTable = """"""                                                # table creation
    for thisName in contacts:
        thisEmail = contacts[thisName]["email"]
        thisDate = contacts[thisName]["date"]
        thisType = contacts[thisName]["type"]
        thisSsn = contacts[thisName]["ssn"]
        inTable += """                  <tr>\n"""                                           # new table row
        inTable += """                        <td>""" + thisName + """</td>\n"""            # start with name data
        inTable += """                        <td><a href="mailto:""" + thisEmail + """">""" + thisEmail + """</a></td>\n""" # email data
        inTable += """                        <td>""" + thisDate + """</td>\n"""  # date data
        inTable += """                        <td>""" + thisType + """</td>\n"""  # message type data
        inTable += """                        <td>""" + thisSsn + """</td>\n"""   # y/n ssn data
        inTable += """                  </tr>\n"""                                          # end current contact's row

    htmlTemp = """
<!DOCTYPE html>
<html lang=en>
    <head>
        <meta charset="UTF-8">
        <title>Admin: My Contacts</title>
        <link href="/main.css" rel="stylesheet">
    </head>
    <body>
        <nav>
            <ul>
                <li><a href="/">Main Page</a></li>
                <li><a href="/contact">Contact</a></li>
                <li><a href="/testimonies">Testimonies</a></li>
                <li><a href="/admin/contactlog">Contact List</a></li>
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

def server(url):
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe#test`
    then the `url` parameter will have the value "/contact?name=joe". So you can expect the PATH
    and any PARAMETERS from the url, but nothing else.

    This function is called each time another program/computer makes a request to this website.
    The URL represents the requested file.

    This function should return two strings in a list or tuple. The first is the content to return
    The second is the content-type.
    """
    #YOUR CODE GOES HERE!
    path = url
    queryString = ""
    
    if '?' in url:                                  # separate *partial* URL and data
        path = url[:url.index("?")]                 # everything in url before '?' (and data)
        queryString = url[url.index("?") + 1:]          # all the data neatly in one string
    
    if (path == "/" or path == "/main"):            # opens the main page
        return open("static/html/mainpage.html").read(), "text/html"
    
    elif (path == "/contact"):                      # opens the contacts page
        if (queryString != ""):                     # contact has data
            extractQueries(queryString)             # function call to make new dict input
        
        return open("static/html/contactform.html").read(), "text/html"
    
    elif (path == "/testimonies"):                  # opens the testimonies page
        return open("static/html/testimonies.html").read(), "text/html"
    
    elif (path == "/admin/contactlog"):             # opens the admin contacts log page
        adminContactLog()
        return open("admin/contactlog/contactlog.html").read(), "text/html"
    
    elif (path == "/images/main"):
        return open("static/images/main/mainpage.jpg", "rb").read(), "image/jpeg"
    
    elif (path == "/main.css"):
        return open("static/css/main.css").read(), "text/css"
    
    else:                                           # undefined path, 404 error page
        return open("static/html/404.html").read(), "text/html"


# You shouldn't need to change content below this. It would be best if you just left it alone.

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Call the student-edited server code.
        message, content_type = server(self.path)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(200)
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
    server = ('', PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()
run()
