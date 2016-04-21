"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, request, session
import jinja2

import melons


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<int:melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """


    melon = melons.get_by_id(melon_id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    #TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    
    # - get the list-of-ids-of-melons from the session cart
    # - loop over this list:
    #   - keep track of information about melon types in the cart
    #   - keep track of the total amt ordered for a melon-type
    #   - keep track of the total amt of the entire order
    # - hand to the template the total order cost and the list of melon types

    # ex. session is {"shopping cart": [44, 31, 18]}
    list_of_ids = session["shopping_cart"]
    session.setdefault("cart", {})
    
    # while list_of_ids != []:
    for melon_id in list_of_ids:
        #if melon_id in list_of_ids:
        # we have the id, now we need to get its price and name
        melon = melons.get_by_id(melon_id)
        
        if melon_id in session["cart"]:
            session["cart"][melon_id]["qty"] += 1
            session["cart"][melon_id]["subtotal"] = session["cart"][melon_id]["price"] * session["cart"][melon_id]["qty"]
        else:
            session["cart"][melon_id] = {"price": melon.price, "name": melon.common_name, 
                                        "qty": 1, "subtotal": session["cart"][melon_id]["price"] *  
                                        session["cart"][melon_id]["qty"] }
    cart = session["cart"]
                                        
    return render_template("cart.html", cart=cart)


@app.route("/add_to_cart/<int:melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    # melon is an object of the class Melon
    # melon = melons.get_by_id(melon_id)

    # if the cart is not in the session, we add our shopping cart to the session
    if shopping_cart not in session:
        session["shopping_cart"] = [melon_id]
    else:
        session["shopping_cart"].append(melon_id) 

    flash("Melon successfully added to shopping cart!")
    return redirect("/cart")

    # ex. session is {"shopping cart": [44, 31, 18]}
    #render_template("melon_details.html", melon=melon_added)


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
