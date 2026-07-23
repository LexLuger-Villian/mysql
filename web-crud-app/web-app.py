from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = "secure_random_secret_key"

# Database Configuration Details
DB_CONFIG = {
    "host": "localhost",
    "user": "root",        # Replace with your MySQL username
    "password": "my-secure-password",        # Replace with your MySQL password
    "database": "my_app_db",
    "cursorclass": pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

# READ: View all records & CREATE: Handle user addition
@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        try:
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()
            flash("User Added Successfully!", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("index"))
        
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", users=users)

# UPDATE: Handle individual row alterations
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        try:
            cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, id))
            conn.commit()
            flash("User Updated Successfully!", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("index"))
        
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("update.html", user=user)

# DELETE: Wipe records instantly via ID parameters
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        conn.commit()
        flash("User Deleted Successfully!", "warning")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {str(e)}", "danger")
    cursor.close()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
