from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Category, Task

@app.route("/")
def home():
    return render_template("tasks.html")

@app.route("/categories")
def categories():
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories) #cat=cat: first categories is the name in the html, the second is now the list defined above.

@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST": 
        category = Category(category_name=request.form.get("category_name"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html") # by default the normal method is GET, so this behaves an ELSE condition since its not part of the POST block, so if not POST then = GET
# when a user clicks the  add_category button, this will use the "GET" method and render the add_category template.
# once they submit the form, this will call the SAME function, but will check if the request being made is a POST method.

@app.route("/add_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit() #after that, we should commit the change from the session to the database
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)