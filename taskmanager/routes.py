from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Category, Task

@app.route("/")
def home():
    tasks = list(Task.query.order_by(Task.id).all())
    return render_template("tasks.html", tasks=tasks)

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

#Delete Category
@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))

#add a new task
@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        task = Task(
            task_name=request.form.get("task_name"),
            task_description=request.form.get("task_description"),
            is_urgent=bool(True if request.form.get("is_urgent") else False),
            due_date=request.form.get("due_date"),
            category_id=request.form.get("category_id")
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_task.html", categories=categories)


#edit a new task
@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        task.task_name = request.form.get("task_name")
        task.task_description = request.form.get("task_description")
        task.is_urgent = bool(True if request.form.get("is_urgent") else False)
        task.due_date = request.form.get("due_date")
        task.category_id = request.form.get("category_id")
        db.session.commit()
    return render_template("edit_task.html", task=task, categories=categories)

#delete a task
@app.route("/delete_tasky/<int:task_id>") #when the function is called, it takes the task_id, 
def delete_task(task_id):
    task = Task.query.get_or_404(task_id) #then tries to query the database to find the task
    db.session.delete(task) #it then removes the task, using .delete method
    db.session.commit() # and commits the change to the database
    return redirect(url_for("home")) #before redirecting users back to the homepage