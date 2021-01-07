from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_restful import Api, Resource, reqparse
import json
import goat_scraper


# Create the application instance   
app = Flask(__name__)
api = Api(app)

class popularSneakers(Resource): #gets top 100 sneakers from site
    def get(self, query_id=""):
        sneakers = goat_scraper.getAllSneakers()
        return jsonify(sneakers)

class sneakerById(Resource):
    def get(self, query_id):
        sneaker = goat_scraper.getSneaker(query_id) #dictionary of sizes and each price
        return jsonify(sneaker)

class sneakerPrice(Resource):
    def get(self, query_id):
        priceMap = goat_scraper.getSneakerSizesAndPrices(query_id)
        return jsonify(priceMap)

class sneakerBySearch(Resource):
    def get(self, keyword):
        results = goat_scraper.getAllSneakers(keyword)
        return jsonify(results)

#endpoints
api.add_resource(popularSneakers, '/', '/sneakers/'  )
api.add_resource(sneakerById, '/sneakers/<string:query_id>')
api.add_resource(sneakerPrice, '/sneakers/<string:query_id>/sizes')
api.add_resource(sneakerBySearch, '/sneakers/search/<string:keyword>')

# Home page
# @app.route('/')
# def home():
#      return redirect(url_for('get_all_shoes'))

# @app.route('/shoes/')
# def get_all_shoes():
#      return jsonify(goat_scraperV3.getAllSneakers())
#     # return render_template('home.html')


# @app.route('/shoes/<query_id>')
# def get_shoe(query_id):
#     body = jsonify(goat_scraperV3.setSneakerSizesAndPrices(query_id))
#     return render_template("home.html")

# def api_all():
#     return jsonify(goat_scraperV3.getAllSneakers())
#     # return jsonify(books)


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run()