from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/news')
def new():
    return render_template("news.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        f = request.form
        print(f)
        return render_template("confirmation.html", form_data=f)
    elif request.method == "GET"
        temp_form_data={
            "firstname" : "James",
            "surname" : "Lovelock",
            "email" : "jlovelock@gmail.com",
            "aboutme" : "I love playing badminton with friends <3"
        }
        return render_template("signup.html", **temp_form_data)

if __name__ == "__main__":
    app.run(debug=True)