from flask import Flask, render_template, g, request, session, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

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
        return render_template("index.html", products=products_list, username=session.get("username", None))
    except mysql.connector.Error as err:
        print(err)
        return render_template("error.html", msg="Error querying data")
    finally:
        cur.close()

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