from flask import Flask, request
import MySQLdb

app = Flask(__name__)

#  MySQL Database connection (edit password as needed)
db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="1234",   # ← replace with your MySQL password
    db="users"
)
cursor = db.cursor()

#  HOME route (fixes your “URL not found” issue)
@app.route("/")
def home():
    return '''
        <h1>Welcome to Flask Assignment App </h1>
        <p>Available Routes:</p>
        <ul>
            <li><a href="/hello">/hello</a> - Test route</li>
            <li><a href="/users">/users</a> - List of all users</li>
            <li><a href="/new_user">/new_user</a> - Add new user</li>
            <li><a href="/users/1">/users/&lt;id&gt;</a> - View single user</li>
        </ul>
    '''

# Route 1: /hello
@app.route("/hello")
def hello():
    return "Hello World!"

#  Route 2: /users
@app.route("/users")
def users():
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()

    html = "<h1>All Users</h1><table border='1'>"
    html += "<tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th></tr>"
    for u in data:
        html += f"<tr><td>{u[0]}</td><td><a href='/users/{u[0]}'>{u[1]}</a></td><td>{u[2]}</td><td>{u[3]}</td></tr>"
    html += "</table><br><a href='/new_user'>Add New User</a>"
    return html

#  Route 3: /new_user
@app.route("/new_user", methods=["GET", "POST"])
def new_user():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        role = request.form["role"]

        cursor.execute(
            "INSERT INTO users (name, email, role) VALUES (%s, %s, %s)",
            (name, email, role)
        )
        db.commit()

        return "<h3>User added successfully!</h3><a href='/users'>Go back</a>"

    return '''
        <h1>Add New User</h1>
        <form method="POST">
            Name: <input type="text" name="name"><br><br>
            Email: <input type="email" name="email"><br><br>
            Role: <input type="text" name="role"><br><br>
            <input type="submit" value="Add User">
        </form>
        <br><a href="/users">Back to Users</a>
    '''

#  Route 4: /users/<id>
@app.route("/users/<int:id>")
def user_detail(id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()

    if user:
        return f'''
            <h1>User Details</h1>
            <p><b>ID:</b> {user[0]}</p>
            <p><b>Name:</b> {user[1]}</p>
            <p><b>Email:</b> {user[2]}</p>
            <p><b>Role:</b> {user[3]}</p>
            <a href="/users">Back to All Users</a>
        '''
    else:
        return "<h3>User not found!</h3><a href='/users'>Back</a>", 404

@app.errorhandler(404)
def not_found(e):
    return "<h2 style='color:red;'> Page Not Found (404)</h2><a href='/'>Go Home</a>", 404

if __name__ == "__main__":
    app.run(debug=True)
