from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io
import json
import re
import sys
sys.path.insert(0, './bot')
import natasha_chat
from geotext import GeoText

####################################################################
def getWords(data):
    return re.compile(r"[\w']+").findall(data)

def oldner(event, userid):
    with open('data.json', 'r') as f:
         data = json.load(f)
    flag = False
    for i in data["people"]:
        if i["userid"] == userid:
            i["count"] = i["count"] + 1
            flag = True
            with open('data.json', 'w') as f:
                 json.dump(data, f)
            return i
    if flag == False:
        killbill = {
              "userid": userid,
              "location":"",
              "food":"",
              "generated":"False",
              "flag":"",
              "count":0
              }
        data["people"].append(killbill)
        with open('data.json', 'w') as f:
             json.dump(data, f)
        return killbill

    #print len(data['people'])
    # Writing JSON data
def updatejson(person):
    with open('data.json', 'r') as f:
         data = json.load(f)
    for i in data['people']:
        if i['userid'] == person['userid']:
            i['location'] = person['location']
            i['count'] = i['count'] + 1
            break
    with open('data.json', 'w') as f:
         json.dump(data, f)

def lambda_handler(event, userid, context):
    # Reading data back
    person = oldner(event, userid)
    c = getWords(event)
    d1 = ['i', 'live', 'in', 'please', 'hi', 'give', 'find', 'who', 'what', 'my', 'hungry', 'near', 'me', 'thank', 'you', \
            'want', 'to', 'eat', 'like','liked', 'I', 'can', 'you', 'suggest', 'of', 'is', 'are', 'near', 'there', 'some', \
            'little', 'now', 'wanna', 'want', 'at', 'on', 'in', 'near', 'area', 'next', 'and', 'how', 'about', 'or', \
            'the', 'a', 'an', 'about', 'for', 'with', 'should', 'could', 'would', 'out','time','person','year','way','day',\
            'thing','man','world','life','hand','part','child','eye','woman','place','work','week', 'doing',\
            'case','point','government','company','number','group','problem','fact','be','have','do','say',\
            'get','make','go','know','take','see','come','think','look','want','give','use','find','tell', 'telling',\
            'ask','work','seem','feel','try','leave','call','good','new','first','last','long','great','little','own','other',\
            'old','right','big','high','different','small','large','next','early','young','important','few',\
            'public','bad','same','able','to','of','in','for','on','with','at','by','from','up','about','into',\
            'over','after','beneath','under','above','the','and','a','that','I','it','not','he','as','you', \
            'this','but','his','they','her','she','or','an','will','my','one','all','would','there','their', 'talk', \
            'talking', 'love', 'loved', 'hello', 'help', 'helping', 'helped', 'pleasure', 'bye', 'goodbye', 'care', 'later', \
            'no','nothing', 'thanks', 'welcome', 'something', 'hey']
    a = ''
    for c_cmall in c:
        if c_cmall not in d1:
            a = a + c_cmall.title() + ' '
        else:
            a = a + c_cmall + ' '
    #print a
    potentiav = GeoText(a)
    b = potentiav.cities
    #print 'b',b
    if b == [] and person["location"] == "":
        g = 'jankiap50@' + natasha_chat.eliza_chat(event) + ' @ I cant find the city from your text, @ please specify both food and city/town/neighbourhood'
        print g
        return
    else:
        flag = False
        if b == []:
            flag = True
            b.append('')
            b[0] = person["location"]
        else:
            person["location"] = b[0]
            updatejson(person)
        d2 = getWords(b[0])
        #print d2
        a = ''
        for c_cmall in c:
            if c_cmall not in d1 and c_cmall not in d2:
                a = a + c_cmall + ' '
        a = api_callee({ 'item': a, 'location': b[0]}, 0)
        if flag == True:
            a = a + "The last location you gave was " + b[0] + " @ @ @ @ @"
        else:
            a = a + " @ @ @ @ @"
        print a
        return

def api_callee(event, context):
    # read API keys
    with io.open('config_secret.json') as cred:
        creds = json.load(cred)
        auth = Oauth1Authenticator(**creds)
        client = Client(auth)

    params = {
        'term': event['item'],
        'lang': 'en',
        'limit': 5
    }

    response = client.search(event['location'], **params)
    placesYelp = ""

    placesYelp = str(response.businesses[0].name) +'@'+ \
                str(response.businesses[0].mobile_url.partition("?")[0]) +'@' + \
                str(response.businesses[0].image_url) +'@' + \
                str(response.businesses[0].rating) +'@' + \
                str(response.businesses[0].display_phone)+'@' + \
                str(response.businesses[1].name)+'@' + \
                str(response.businesses[1].mobile_url.partition("?")[0])+'@' + \
                str(response.businesses[1].image_url) +'@' + \
                str(response.businesses[1].rating)+'@' + \
                str(response.businesses[1].display_phone)+'@' + \
                str(response.businesses[2].name)+'@' + \
                str(response.businesses[2].mobile_url.partition("?")[0])+'@'+ \
                str(response.businesses[2].image_url) +'@' + \
                str(response.businesses[2].rating)+'@' + \
                str(response.businesses[2].display_phone)+'@' + \
                str(response.businesses[3].name)+'@' + \
                str(response.businesses[3].mobile_url.partition("?")[0])+'@' + \
                str(response.businesses[3].image_url) +'@' + \
                str(response.businesses[3].rating)+'@' + \
                str(response.businesses[3].display_phone)+'@' + \
                str(response.businesses[4].name)+'@' + \
                str(response.businesses[4].mobile_url.partition("?")[0])+'@'+ \
                str(response.businesses[4].image_url) +'@' + \
                str(response.businesses[4].rating)+'@' + \
                str(response.businesses[4].display_phone)+'@'

    #return response.businesses[0].name, response.businesses[0].url.partition("?")[0], response.businesses[0].rating, response.businesses[0].display_phone
    #print str(placesYelp)
    return placesYelp
    #return placesYelp
    #print str(response.businesses[0].name)
    #return str(response.businesses[0].name)

#file = open("data.txt", "w")
#file.write(sys.argv[2])
#file.close()
# Writing JSON data
#with open('data.json', 'w') as f:
#     json.dump(sys.argv[2], f)

#print type(lambda_handler({ 'item': 'blueberry cheesecake', 'location': 'san francisco'}, 0))
#print lambda_handler({ 'item': 'blueberry cheesecake', 'location': 'san francisco'}, 0)
#print lambda_handler("I would like to live in new york city, or in lake forest area.", 0)
lambda_handler(str(sys.argv[1]), sys.argv[2], 0)
