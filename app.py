from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_apispec import MethodResource, FlaskApiSpec, marshal_with, doc
from marshmallow import Schema, fields
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
import goat_scraper


# Create the application instance
app = Flask(__name__)
api = Api(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='SNKR FINDR',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

# class sneakerSummarySchema(Schema):
#     sneakers = fields.List()
#     sneaker = fields.Dict()
#     name = fields.Str()
#     query_id = fields.Int()
#     retail_price = fields.Int()
#     lowest_price = fields.Int()
#     displayed_size = fields.Int()
#     image_url = fields.Str()
    
@doc(description='Returns a list of the top 100 sneakers from GOAT.com.', tags=['Sneakers'])
class popularSneakers(MethodResource): #gets top 100 sneakers from site
    # @marshal_with(sneakerSummarySchema)
    def get(self):
        sneakers = goat_scraper.getAllSneakers()
        return jsonify(sneakers)

@doc(description='Returns the sneaker with matching ID.', tags=['Sneakers'])
class sneakerById(MethodResource):
    def get(self, query_id):
        sneaker = goat_scraper.getSneaker(query_id) #dictionary of sizes and each price
        return jsonify(sneaker)

@doc(description='Returns a price map for each corresponding size of a given sneaker.', tags=['Sneakers'])
class sneakerPrice(MethodResource):
    def get(self, query_id):
        priceMap = goat_scraper.getSneakerSizesAndPrices(query_id)
        return jsonify(priceMap)

@doc(description='Returns a list of sneakers that match the provided keyword.', tags=['Sneakers'])
class sneakerBySearch(MethodResource):
    def get(self, keyword):
        results = goat_scraper.getAllSneakers(keyword)
        return jsonify(results)

#endpoints
api.add_resource(popularSneakers, '/sneakers/')
api.add_resource(sneakerById, '/sneakers/<string:query_id>')
api.add_resource(sneakerPrice, '/sneakers/<string:query_id>/sizes')
api.add_resource(sneakerBySearch, '/sneakers/search/<string:keyword>')

docs.register(popularSneakers)
docs.register(sneakerById)
docs.register(sneakerBySearch)
docs.register(sneakerPrice)

if __name__ == '__main__':
    app.run(debug=True)