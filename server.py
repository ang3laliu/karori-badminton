from flask import Flask

app = Flask(__name__)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    temp_form_data={
        "firstname" : "James",
        "surname" : "Lovelock",
        "email" : "jlovelock@gmail.com",
        "aboutme" : "I love playing badminton with friends <3"
    }
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)