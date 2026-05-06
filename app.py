from flask import Flask, render_template, g, request, session, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import requests

app = Flask(__name__)

# Application config
app.config["DATABASE_USER"] = "root"
app.config["DATABASE_PASSWORD"] = "candyestefoartecute"
app.config["DATABASE_DB"] = "handlevaktenDB"
app.config["DATABASE_HOST"] = "localhost"
app.secret_key = 'something_secret'
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

@app.cli.command("sync-products")
def cli_sync():
    """Flask CLI command for starting the products synchronization from the terminal."""
    sync_products_from_api()

def sync_products_from_api():
    """Fetches paginated product data from the Kassal API and stores it in the local database,
    updating existing rows when the same product already exists."""
    db = get_db()
    cur = db.cursor(buffered=True)

    api_url = f"https://kassal.app/api/v1/products?size=100"
    params = {"size": 100, "page": 1}
    # Bearer token authentication
    token = "bM1N0OzcN6s6ffUxw7L057n8ZmmnXCTpX5xd6CP3"
    headers = { # optional parameter to request.get()
        "Authorization": f"Bearer {token}",
    }
    while api_url:
        # API call
        response = requests.get(api_url, headers=headers, params=params, timeout=5)
        if response.status_code in (500, 502, 503, 504):
            print(f"Skipping page {params['page']} due to server error {response.status_code}")
            params["page"] += 1
            continue
        response.raise_for_status() # raise error is status code != 200

        payload = response.json()
        products = payload["data"]

        if not products:
            break

        for product in products:
            # sync products table
            cur.execute(
            """
            INSERT INTO products (product_id, product_name, image_url, description, updated_at)
            VALUES (%s, %s, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE
                product_name = VALUES(product_name),
                image_url = VALUES(image_url), 
                description = VALUES(description), 
                updated_at = NOW()
            """,  (
                product['id'],
                product['name'],
                product['image'],
                product['description']
            ))

            # sync stores table
            cur.execute(
            """
            INSERT INTO stores (store_name, store_code, store_logo)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                store_name = VALUES(store_name),
                store_code = VALUES(store_code),
                store_logo = VALUES(store_logo)
            """, (
                product['store']['name'],
                product['store']['code'],
                product['store']['logo']
            ))

            # sync prices table
            cur.execute( "SELECT store_id FROM stores WHERE store_code = %s",
                (product['store']['code'],)
            )
            store_id = cur.fetchone()[0]
            cur.execute("""
            INSERT INTO prices (product_id, store_id, price)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                product_id = VALUES(product_id),
                store_id = VALUES(store_id),
                price = VALUES(price)
            """, (
                product['id'],
                store_id,
                product['current_price']
            ))

        db.commit()
        params["page"] += 1

    cur.close()


@app.route('/')
def products():
    db = get_db()
    cur = db.cursor()
    try: 
        # Query the first 20 unique product ids from the database
        offset = 0
        limit = 20
        cur.execute(
        """ SELECT product_id
            FROM products
            ORDER BY product_id ASC
            LIMIT %s OFFSET %s """, (limit, offset))
        rows = cur.fetchall()
        product_ids = [row[0] for row in rows]

        # retrieve product info based on product id
        products = {}
        placeholders = ", ".join(["%s"] * len(product_ids))
        cur.execute(
        f""" SELECT p.product_id, p.product_name, p.image_url, pr.price, s.store_name 
            FROM products p 
            JOIN prices pr ON p.product_id = pr.product_id 
            JOIN stores s ON pr.store_id = s.store_id
            WHERE p.product_id IN ({placeholders})""", (product_ids)
        )

        for (product_id, product_name, image_url, price, store_name) in cur:
            if product_id not in products:
                products[product_id] = {
                    "product_id": product_id,
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

        products_list = list(products.values())
        return render_template("products.html", products=products_list, username=session.get("username", None))
    except mysql.connector.Error as err:
        print(err)
        return render_template("error.html", msg="Error querying data")
    finally:
        cur.close()

@app.route('/api/products')
def api_products():
    """
    Return a paginated batch of products as JSON.

    Query parameters:
        offset(int):
            Number of products to skip before returning results.
    
    Response: 
        A JSON array of product objects.
    """
    offset = request.args.get("offset", type=int)
    limit = 20

    cur = get_db().cursor()

    cur.execute(
    """ SELECT product_id
        FROM products
        ORDER BY product_id ASC
        LIMIT %s OFFSET %s """, (limit, offset))
    rows = cur.fetchall()
    product_ids = [row[0] for row in rows]

    # retrieve product info based on product id
    products = {}
    placeholders = ", ".join(["%s"] * len(product_ids))
    cur.execute(
    f""" SELECT p.product_id, p.product_name, p.image_url, pr.price, s.store_name 
        FROM products p 
        JOIN prices pr ON p.product_id = pr.product_id 
        JOIN stores s ON pr.store_id = s.store_id
        WHERE p.product_id IN ({placeholders})""", (product_ids)
    )

    for (product_id, product_name, image_url, price, store_name) in cur:
        if product_id not in products:
            products[product_id] = {
                "product_id": product_id,
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

    products_list = list(products.values())

    return products_list


@app.route('/product_page')
def product_page():
    product_id = request.args.get("id", type=int)
    if not product_id:
        return render_template("error.html", msg="No product id provided")
    
    db = get_db()
    cur = db.cursor()
    
    try:
        cur.execute("SELECT product_name, image_url, description FROM products WHERE product_id = %s", (product_id,))
        product = cur.fetchone()
        if not product:
            return render_template("error.html", msg="Error 404: Product not found")
        
        product = {
            "product_name": product[0],
            "image_url": product[1],
            "description": product[2],
            "prices_at_store": [],
            "allergens": [],
            "price_history": []
        }
        
        cur.execute("""
                    SELECT s.store_name, pr.price 
                    FROM prices pr 
                    JOIN stores s 
                    ON pr.store_id = s.store_id 
                    WHERE pr.product_id = %s
                    ORDER BY pr.price ASC
                    """, (product_id,))
        prices = cur.fetchall()
        for (store_name, price) in prices:
            product["prices_at_store"].append({
                "store_name": store_name,
                "price": price
            })
            
        cur.execute("""
                    SELECT p.product_name, a.allergen_name
                    FROM products p
                    JOIN product_allergens pa ON p.product_id = pa.product_id
                    JOIN allergens a ON pa.allergen_id = a.allergen_id
                    WHERE pa.product_id = %s
                    ORDER BY a.allergen_name
                    """, (product_id,))
        allergens = cur.fetchall()
        product["allergens"] = [allergen_name for (_, allergen_name) in allergens]
        
        cur.execute("""
                    SELECT s.store_name, ph.price, ph.date
                    FROM price_history ph
                    JOIN stores s ON ph.store_id = s.store_id
                    WHERE ph.product_id = %s
                    ORDER BY ph.date DESC
                    """, (product_id,))
        for store_name, price_history, date in cur.fetchall():
            product["price_history"].append({
                "store_name": store_name,
                "price_history": price_history,
                "date": date
            })
            
        return render_template("product_page.html", product=product)
    
    except mysql.connector.Error as err:
        print(err)
        return render_template("error.html", msg="Error querying data")
    finally:
        cur.close()

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not all([email, password]):
            flash("Alle felt må fylles ut!")
            return render_template("login.html")
        
        try:
            conn = get_db()
            cur = conn.cursor()
            sql = ("SELECT password_hash, user_id, first_name FROM users WHERE email=%s")
            cur.execute(sql, (email,))
            user = cur.fetchone()

            if user:
                password_hash = user[0]
                if check_password_hash(password_hash, password):
                    session["user_id"] = user[1]
                    session["username"] = user[2]
                    return redirect(url_for("index"))
                else:
                    flash("Wrong password!")
            else:
                flash("User not found! Please register.")
        except mysql.connector.Error as err:
            print(err)
            return render_template("error.html", msg="Error querying data")
        finally:
                cur.close()
    
    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email, password, first_name, last_name = (
            request.form.get("email", "").strip(),
            request.form.get("password", "").strip(),
            request.form.get("first_name"),
            request.form.get("last_name")
        ) 
        hash = generate_password_hash(password)

        # validerer alle felt
        if not all([email, password, first_name, last_name]):
            flash("Alle felt må fylles ut!")
            return render_template("register.html")
        elif "@" not in email:
            flash("Ugyldig epostadresse!")
            return render_template("register.html")
        elif len(password) < 8:
            flash("Passordet må være minst 8 tegn!")
            return render_template("register.html")

        try:
            db = get_db()
            cur = db.cursor()

            # sjekker om eposten allerede finnes i databasen
            cur.execute(("SELECT * FROM users WHERE email=%s"), (email,))
            if cur.fetchone():
                flash("Denne eposten er allerede registrert!")
                return render_template("register.html")
            else:
                sql = ("INSERT INTO users(email, password_hash, first_name, last_name, account_type) VALUE (%s, %s, %s, %s, %s)")
                cur.execute(sql, (email, hash, first_name, last_name, "user"))
                db.commit()
                flash("Registrering vellykket!")
        except mysql.connector.Error as err:
            print(err)
            return render_template("error.html", msg="Error querying data")
        finally:
                cur.close()
    
    return render_template("register.html")

@app.route("/profile", methods=["GET"])
def view_profile():
    if "user_id" not in session:
        return redirect("/login")

    try:
        db = get_db()
        cur = db.cursor()
        user_id = session["user_id"]
        sql = ("SELECT first_name, last_name, email, created_at FROM users WHERE user_id=%s")
        cur.execute(sql, (user_id,))
        user = cur.fetchone()
        return render_template("profile_page.html", first_name=user[0], last_name=user[1], email=user[2], created_at=user[3])
    except mysql.connector.Error as err:
        print(err)
        return render_template("error.html", msg="Error querying data")
    finally:
        cur.close()

@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    if "user_id" in session:
        session.pop("user_id")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()


if __name__ == "__main__":
    app.run()