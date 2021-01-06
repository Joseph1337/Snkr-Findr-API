import json
import requests
import pprint
from time import sleep
import random


#extracts all user-agents from the provided 'ua_file.txt' into a list then randomly selects a user-agent
def getUserAgent():
    randomUserAgent = ""
    listOfUserAgents = []
    userAgentFile = 'ua_file.txt'
    with open('ua_file.txt') as file:
        listOfUserAgents = [line.rstrip("\n") for line in file]
    return random.choice(listOfUserAgents)


class Sneaker:
    def __init__(self, name, query_id, retail_price, displayed_size, price, image_url):
        self.name = name
        self.query_id = query_id

        if(retail_price == None):
            self.retail_price = "N/A"
        else:
            self.retail_price = retail_price/100

        if(displayed_size == None):
            self.displayed_size = "N/A"
        else:
            self.displayed_size = displayed_size
        if(price==None):
            self.lowest_price = "N/A"
        else:
            self.lowest_price = price/100
        self.image_url = image_url
        # self.sizeAndPrice = sizeAndPrice


#function to get all sneakers from 'Shop All' page
def getAllSneakers(keyword=''):
    sneakersList = []
    #api call to retrieve sneaker details
    url = 'https://2fwotdvm2o-3.algolianet.com/1/indexes/*/queries'
    #size you want to look for:
    shoe_size = ""
    search_field = keyword
    #data sent with POST request
    for page in range(0,5):
        form_data = {
            "requests": [{
            "indexName":"product_variants_v2",
            "params":"",
            "highlightPreTag" : "<ais-highlight-0000000000>",
            "highlightPostTag": "</ais-highlight-0000000000>",
            "distinct": "true",
            "query": keyword,
            "facetFilters": [["presentation_size:" + str(shoe_size)],["product_category:shoes"]],
            "maxValuesPerFacet": 30,
            "page": page,
            "facets": ["instant_ship_lowest_price_cents","single_gender","presentation_size","shoe_condition","product_category","brand_name","color","silhouette","designer","upper_material","midsole","category","release_date_name"],
            "tagFilters":""
            }]
        }
        query_params = {
            'x-algolia-agent': 'Algolia for JavaScript (3.35.1); Browser (lite); JS Helper (3.2.2); react (16.13.1); react-instantsearch (6.8.2)',
            'x-algolia-application-id': '2FWOTDVM2O',
            'x-algolia-api-key': 'ac96de6fef0e02bb95d433d8d5c7038a'
        }
        response = requests.post(url, data=json.dumps(form_data), params=query_params).json()['results'][0]['hits']

        for sneaker in response:
            sneakersList.append((Sneaker(sneaker['name'], sneaker['slug'], sneaker['retail_price_cents'], sneaker['size'], sneaker['lowest_price_cents'], sneaker['original_picture_url']).__dict__))  # getSneakerSizesAndPrices(sneaker['slug'])))
            # sleep(random.randrange(1,3))

    return sneakersList


def getSneaker(query_id):
    sneakerInfo = {}
    url = "https://www.goat.com/web-api/v1/product_templates/" + query_id
    user_agent = getUserAgent()
    headers = {
        "User-Agent": user_agent,
        "Accept": "application/json",
        "Referer": "https://www.goat.com/sneakers/" + query_id
        }
    for i in range(0, 10):
        try:
            headers.update({"user-agent": getUserAgent()})
            response = requests.get(url, headers=headers).json()
            print(response)
            sneakerInfo['Name'] = response['name']
            sneakerInfo['Colorway'] = response['details']
            sneakerInfo['Style ID'] = response['sku']
            sneakerInfo['Release Date'] = response['releaseDate'].split('T')[0]
            sneakerInfo['Price Map'] = getSneakerSizesAndPrices(query_id)
            sneakerInfo['Image'] = response['mainPictureUrl']
            break
        except: #runs into captcha, so retry
            sleep(random.randrange(1,3))
            continue

    else:
        return {"message": "Could not connect to GOAT.com while searching for " + query_id}
    return sneakerInfo


def getSneakerSizesAndPrices(query_id): #helper method for getSneakr to get prices via separate api call
        sizeAndPrice = {}
        url = 'https://www.goat.com/web-api/v1/product_variants'
        user_agent = getUserAgent()
        headers = {
            "user-agent": user_agent,
            "accept" : "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language" : "en-US,en;q=0.9",
            "referer": 'https://www.google.com/'
        }

        query_params = {
            "productTemplateId": query_id
        }
        for i in range(0, 10):
            try:
                headers.update({"user-agent": getUserAgent()})
                response = requests.get(url, headers=headers, params=query_params, timeout=10)
                # print(response.text)
                if(response.status_code >= 200 and response.status_code < 400):
                    page = response.json()
                    for i in range(0, len(page)):
                        #check ONLY for new shoes with boxes in good condition
                        if(page[i]['boxCondition'] == "good_condition" and page[i]['shoeCondition'] == "new_no_defects"):
                            sizeAndPrice.update({page[i]['size']: page[i]['lowestPriceCents']['amount']/100})
                # elif (response.json()['success'] == False): #catches if query_id invalid
                elif("success" in response.json()):
                    if(response.json()['success'] == False):
                        sizeAndPrice.update({"message": "Invalid product id."})
                        break
                else:
                    raise PermissionError

            except (PermissionError):#request got blocked by captcha
                continue

            except requests.exceptions.Timeout as err:
                continue
            else:
                break

        else: # if not sizeAndPrice:
            sizeAndPrice.update({"Size_Timeout": "Price_Timeout"})

        return sizeAndPrice
