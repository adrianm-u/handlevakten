from flask import Flask, render_template, g
import mysql.connector

app = Flask(__name__)

# Application config
app.config["DATABASE_USER"] = "root"
app.config["DATABASE_PASSWORD"] = "password"
app.config["DATABASE_DB"] = "handlevaktenDB"
app.config["DATABASE_HOST"] = "localhost"
app.debug = True  # only for development

def get_db():
    if not hasattr(g, "_database"):
        print("create connection")
        g._database = mysql.connector.connect(host=app.config["DATABASE_HOST"], user=app.config["DATABASE_USER"],
                                       password=app.config["DATABASE_PASSWORD"], database=app.config["DATABASE_DB"])
    return g._database


@app.teardown_appcontext
def teardown_db(error):
    """Closes the database at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        print("close connection")
        db.close()


@app.route('/')
def index():
    db = get_db()
    cur = db.cursor()
    try: 
        # henter produktene fra databasen
        products = {}
        sql = "SELECT p.product_id, p.product_name, p.image_url, pr.price, s.store_name " \
        " FROM products p " \
        " JOIN prices pr ON p.product_id = pr.product_id " \
        " JOIN stores s ON pr.store_id = s.store_id"

        cur.execute(sql)

        for (product_id, product_name, image_url, price, store_name) in cur:
            if product_id not in products:
                products[product_id] = {
                    "product_name": product_name,
                    "image_url": image_url,
                    "prices_at_store": [{
                        "store_name":  store_name,
                        "price": price}],
                }
            else:
                products[product_id]["prices_at_store"].append({
                    "store_name": store_name,
                    "price": price
                })

        print(products)
        products_list = list(products.values())
        return render_template("index.html", products=products_list)
    except mysql.connector.Error as err:
        print(err)
        return render_template("error.html", msg="Error querying data")
    finally:
        cur.close()

# @app.route('/product_page')


if __name__ == "__main__":
    app.run()