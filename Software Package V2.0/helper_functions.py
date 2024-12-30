def getParameter(data, key):
    if key in data:
        return data[key]
    else:
        return 'NA'

def parseGet( input ):
    #print(input)
    outputData = {}
    data = input.split('?')
    outputData['URL'] = data[0]
    if len(data) > 1:
        urlData = data[1].split('&')
        for i in range(len(urlData)):
            param = urlData[i].split('=')
            outputData[param[0]] = param[1]
    return outputData