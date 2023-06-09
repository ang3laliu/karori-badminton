from flask import Flask, render_template, request, redirect, url_for
from db_functions import run_search_query_tuples
from datetime import datetime

app = Flask(__name__)
db_path = 'badminton.sqlite'

@app.template_filter()
def news_date(sqlite_dt):
    # create a date object
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %Y %I:%M %p")

@app.route('/')
def index():
    return render_template("layout.html")

@app.route('/play')
def play():
    return render_template("play.html")

@app.route('/news')
def news():
    # query for the page
    sql = """select news.title, news.subtitle, news.content, member.name
        from news
        join member on news.member_id = member.member_id
        order by news.newsdate desc;
        """
    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)
    return render_template("news.html")

@app.route('/news_cud', methods=['GET', 'POST'])
def new_cud():
    # collect data from the web address
    data = request.args
    required_keys = ['id', 'task']
    for k in required_keys:
        if k not in data.keys():
            message = "Do not know what to do with create read update on news (key not present)"
            return render_template('error.html', message=message)
    # have an id and a task key
    if request.method == "GET":
        if data['task'] == 'delete':
            return "<h1> I want to delete <\h1>"
        elif data['task'] == 'update':
            return "<h1> I want to update <\h1>"
        elif data['task'] == 'add':
            return "<h1> I want to add <\h1>"
        else:
            message = "Unrecognised task coming from the news page"
            return render_template('error.html', message=message)
    return render_template("news_cud.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        f = request.form
        print(f)
        return render_template("confirmation.html", form_data=f)
    elif request.method == "GET":
        temp_form_data={
            "firstname" : "James",
            "surname" : "Lovelock",
            "email" : "jlovelock@gmail.com",
            "aboutme" : "I love playing badminton with friends <3"
        }
        return render_template("signup.html", **temp_form_data)


if __name__ == "__main__":
    app.run(debug=True)