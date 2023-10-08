from flask import Flask
from routes.user import user_blueprint
from routes.category import category_blueprint
from routes.asset import asset_blueprint
from routes.recipe import recipe_blueprint
from routes.ingredient import ingredient_blueprint

app = Flask(__name__)
app.register_blueprint(user_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(asset_blueprint)
app.register_blueprint(recipe_blueprint)
app.register_blueprint(ingredient_blueprint)


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
  return response

@app.route("/")
def index():
    return "<h1>Hello!</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)