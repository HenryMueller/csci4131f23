def htmlStrOut(strIn):  
    strOut = ""
    for i in range(len(strIn)):
        strIn[i] = strIn[i].replace("<", "&ltr;")  
        strOut += strIn[i]
    return strOut

def main():
    input = ["<p>", "This is a paragraph", "</p>"]  # "<" needs to be used as an html entity: "&lt;"
    output = htmlStrOut(input)
    print(input)
    print(output)

if __name__ == "__main__":
    main()
