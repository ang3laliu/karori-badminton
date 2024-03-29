from db_functions import run_search_query_tuples

def get_news(p):
    sql = """select news.title, news.subtitle, news.content, news.newsdate, member.name
    from news
    join member on news.member_id = member.member_id
    """
    result = run_search_query_tuples(sql, (), db_path, True)

    for row in result:
        for k in row.keys():
            print(k)
            print(row[k])

def get_all():
    sql="select * from news"


if __name__ == "__main__":
    db_path = 'data/badminton.sqlite'
    get_news(db_path)