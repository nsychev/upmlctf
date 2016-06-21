import psycopg2
from urllib.parse import unquote

MAIN_PAGE = '''<meta charset="utf-8" />
<h1>Почта России: клиенты</h1>
<form method="get" action="/users">
<p>Введите ID клиента, чтобы получить информацию о нём</p>
<p><input type="text" name="id" value="1" /></p>
<p><button type="submit">Получить</button></p>
</form>
<hr/>
<p>Copyright &copy; russianpost.ru, 2010</p>
<!-- TODO: improve input escaping -->'''

CLIENTS_PAGE = '''<meta charset="utf-8" />
<h1>Почта России: информация о клиенте {0}</h1>
<p>{1}</p>
<hr/>
<p><a href="/">Пробить ещё одного клиента</a></p>
<p>Copyright &copy; russianpost.ru, 2010</p>
'''
LABEL_ERROR = '''Извините, но таких клиентов у нас нет.'''
LABEL_FOUND = '''Фамилия, имя:<b>{0}</b></p><p>Возраст (полных лет): {1}</p><p><font color="gray">Не любит Почту России</font>'''

def application(environ, start_response):
    status = '200 OK'
    
    if environ["PATH_INFO"] == "/":
      content = MAIN_PAGE
    elif environ["PATH_INFO"] == "/users":
      if environ["QUERY_STRING"] == "":
        content = CLIENTS_PAGE.format(0, LABEL_ERROR)
      elif not("=" in environ["QUERY_STRING"]):
        content = CLIENTS_PAGE.format(0, LABEL_ERROR)
      else:
        id = unquote(environ["QUERY_STRING"].split("=")[1]).replace("+", " ")
        query = "SELECT * FROM users WHERE id={0}".format(id)
        conn = psycopg2.connect("dbname=hackme user=hacker password=thisismajic host=127.0.0.1 port=5432")
        cur = conn.cursor()
        try:
          cur.execute(query)
        except:
          cur = None
          line = None
        if cur is not None:
          try:
            line = cur.fetchone()
          except Exception as e:
            line = None
        if line is None:
          content = CLIENTS_PAGE.format(id, LABEL_ERROR)
        else:
          content = CLIENTS_PAGE.format(id, LABEL_FOUND.format(line[1], line[2]))
        if cur is not None: cur.close()
        conn.close()
    else:
      content = "404 Not Found"
      
        
        

    content = content.encode("utf-8")
    
    response_headers = [('Content-type', 'text/html; charset=utf-8'),
                        ('Content-Length', str(len(content)))
                       ]
    
    start_response(status, response_headers)

    return [content]