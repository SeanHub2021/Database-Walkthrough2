from taskmanager import db 


class Category(db.Model):
    #schema for the Category model
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(25), unique=True, nullable=False) 
    #nullable=False means, it cannot be blank!
    #string can only be 25 characters, and has to be unique - no duplicates!
    tasks = db.relationship("Task", backref="category", cascade="all, delete", lazy=True)
    # not visible in the table, references the one-to-many relationship established in the Task class.
    # lazy = true, finds in the db any tasks linked to the categories

    def __repr__(self):
        #repr to represent itself in the form of a string
        return self.category_name

class Task(db.Model):
    #schema for the Category model
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50), unique=True, nullable=False)
    task_description = db.Column(db.Text, nullable=False) #db.Text allows for alot more text, like a paragraph instead of a column title
    is_urgent = db.Column(db.Boolean, default=False, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id", ondelete="CASCADE"), nullable=False)
    #The category id = an integer, get the foreign key from the category ID created in the Category class
    #Each task must have a category selected. A category can have many tasks, but a task can only have one category. 
    #This is a "One-to-many" style relationship between the data, you could have many-to-many, but not here!
    #And so, if the category is deleted, it will delete any tasks associated with it (with the same category id), so as not to throw up id errors. 
    #This is paired with the 'tasks' variable in the Category class.

    def __repr__(self):
        #repr to represent itself in the form of a string
        return "#{0} - Task: {1} | Urgent: {2}".format(
            self.id, self.task_name, self.is_urgent #these items format the text, as numbers in the array, in the line above
        )

