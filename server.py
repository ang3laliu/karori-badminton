from flask import Flask, render_template, request, redirect, url_for, session
from db_functions import run_search_query_tuples, run_commit_query
from datetime import datetime

app = Flask(__name__)
app.secret_key = "abcdefghijklmnop"
db_path = 'data/badminton.sqlite'


@app.template_filter()
def news_date(sqlite_dt):
    # create a date object
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %Y %H:%M %p")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/play')
def play():
    return render_template("play.html")


@app.route('/learn')
def learn():
    return render_template("learn.html")


@app.route('/news')
def news():
    # query for the page
    sql = """select news.news_id, news.title, news.subtitle, news.content, news.newsdate, member.name
       from news
       join member on news.member_id= member.member_id
       order by news.newsdate desc;
       """
    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)
    return render_template("news.html", news=result)


@app.route('/news_cud', methods=['GET', 'POST'])
def news_cud():
    # colllect data from the web address
    # this happens regardless of GET or POST
    data = request.args
    required_keys = ['id', 'task']
    # check that we have the required keys
    # run error page if a problem
    for k in required_keys:
        if k not in data.keys():
            message = "Do not know what to do with create read update on news (key not present)"
            return render_template('error.html', message=message)
    # yes, we have an id and a task key
    # if I have arrived directly from the page
    if request.method == "GET":
        # is the task to delete ?
        if data['task'] == 'delete':
            sql = "delete from news where news_id = ?"
            values_tuple = (data['id'],)
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news'))
        # is the task to update ?
        elif data['task'] == 'update':
            sql = """ select title, subtitle, content from news where news_id=?"""
            values_tuple = (data['id'],)
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("news_cud.html",
                                   **result,
                                   id=data['id'],
                                   task=data['task'])
        # is the task to add ?
        elif data['task'] == 'add':
            # dummy data for testing
            temp = {'title': 'Test Title', 'subtitle': 'Test subtitle', 'content': 'Test Content'}
            temp = {}  # switches off temp
            return render_template("news_cud.html",
                                   id=0,
                                   task=data['task'],
                                   **temp)
        # run error if not one of these
        else:
            message = "Unrecognised task coming from news page"
            return render_template('error.html', message=message)
    # if it is a POST, we are coming from a form submission
    elif request.method == "POST":
        # collected form information
        f = request.form
        # print(f)
        if data['task'] == 'add':
            # add the new news entry to the database
            # member is fixed for now
            sql = """insert into news(title,subtitle,content, newsdate, member_id) 
                        values(?,?,?, datetime('now', 'localtime'),?)"""
            #
            values_tuple = (f['title'], f['subtitle'], f['content'], session['member_id'])
            result = run_commit_query(sql, values_tuple, db_path)
            # once added redirect to news page to see the newly added news item
            return redirect(url_for('news'))
        elif data['task'] == 'update':
            # we are updating so 'rewrite' all the data even if
            sql = """update news set title=?, subtitle=?, content=?, 
            newsdate=datetime('now', 'localtime') where news_id=?"""
            values_tuple = (f['title'], f['subtitle'], f['content'], data['id'])
            result = run_commit_query(sql, values_tuple, db_path)
            # collect the data from the form and update the database at the sent id
            return redirect(url_for('news'))
        else:
            # let's put in an error catch
            message = "Unrecognised task coming from news form submission"
            return render_template('error.html', message=message)


@app.route('/login', methods=["GET", "POST"])
def login():
    error = "Your credentials are unrecognised"
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        f = request.form
        sql = """ select member_id, name, password, authorisation from member where email = ? """
        values_tuple = (f['email'],)
        result = run_search_query_tuples(sql, values_tuple, db_path, True)
        if result:
            result = result[0]
            if result['password'] == f['password']:
                # start a session
                session['name'] = result['name']
                session['authorisation'] = result['authorisation']
                session['member_id'] = result['member_id']
                print(session)
                return redirect(url_for('index'))
            else:
                return render_template("login.html", error=error)
        else:
            return render_template("login.html",  error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        f = request.form
        print(f)
        sql = """insert into member (name, email, password, authorisation)
        values(?,?,?, 1)"""
        name = f['firstname'] + " " + f['surname']
        values_tuple=(name, f['email'], f['password'])
        result = run_commit_query(sql, values_tuple, db_path)
        return redirect(url_for('index'))
    elif request.method == "GET":
        carried_data = request.args
        #print(carried_data)
        if len(carried_data) == 0:
            temp_form_data = {
                "firstname": "James",
                "surname": "Lovelock",
                "email": "jlovelock@gmail.com",
                "password": "jameslovelock"
            }
            temp_form_data = {}
        else:
            temp_form_data = carried_data
        return render_template("signup.html", **temp_form_data)


if __name__ == "__main__":
    app.run(debug=True, port=8000)