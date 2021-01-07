# 👟SNKR FINDR🔎
A REST API created for sneakerheads.
The ***SNKR FINDR*** API allows the user to obtain essential information on sneakers including:

- Sneaker Name
- Colorway
- Product ID
- Retail Price
- Image URL
- Release Date
- Price map of each corresponding size

## Getting Started
In order to make requests to the API, we will be using the [Requests](https://requests.readthedocs.io/en/master/) library.

1. Begin by installing the library. Navigate to your project directory in terminal and type: 
```
pip install requests
```

2. Once the Requests library has been installed, make sure to import it in your project:
```Python 
import requests
```

3. You're all set to start using the SNKR FINDR API 👍

## HTTP Requests
Now that you have the requests library installed, it's time to make some API requests.

**Example:**
```Python
import requests

#get the trending sneakers
popularSneakers = requests.get(https://snkr-findr.herokuapp.com/sneakers)

#get sneaker using product id (sneaker_id)
sneaker = requests.get(https://snkr-findr.herokuapp.com/sneakers/<sneaker_id>

#get sneaker(s) using search
searchSneaker = requests.get(https://snkr findr.herokuapp.com/sneakers/search/<keyword>
```

**Sample JSON Response**:
```
[
  {
    "displayed_size": 16,
    "image_url": "https://image.goat.com/attachments/product_template_pictures/images/043/946/217/original/567948_00.png.png",
    "lowest_price": 325,
    "name": "Air Jordan 1 Retro High OG 'Dark Mocha'",
    "query_id": "air-jordan-1-retro-high-og-555088-105",
    "retail_price": 170
  },
  {
    "displayed_size": 18,
    "image_url": "https://image.goat.com/attachments/product_template_pictures/images/023/941/742/original/482560_00.png.png",
    "lowest_price": 200,
    "name": "Air Jordan 1 Retro High OG 'Obsidian'",
    "query_id": "air-jordan-1-retro-high-og-obsidian-555088-140",
    "retail_price": 160
  },
  ....
  {
    "displayed_size": 18,
    "image_url": "https://image.goat.com/attachments/product_template_pictures/images/035/766/930/original/519961_00.png.png",
    "lowest_price": 199,
    "name": "Air Jordan 1 Retro High OG 'Royal Toe'",
    "query_id": "air-jordan-1-retro-high-og-royal-toe-555088-041",
    "retail_price": 170
  }
]
```

## Technologies
This project was made with:
- Python
- Flask + Flask_Restful
- Requests Library
- Heroku
  
## Data Source

Currently the API is only able to collect information from [GOAT](goat.com) but the end goal is to obtain sneaker data from [StockX](https://stockx.com/), [Stadium Goods](https://www.stadiumgoods.com/), [Flight Club](https://www.flightclub.com/) and other Foot sites.