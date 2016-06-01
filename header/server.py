import http.cookies

def application(environ, start_response):
    status = '200 OK'
    
    content = "<meta charset='utf-8' /><h1>Дизайн-студия Times New Roman</h1>"
    
    if environ["PATH_INFO"] == "/":
      content += '<form method="get" action="/admin"><p>Password: <input type="text" name="password" value="" /></p><button type="submit">Submit</button></form>'
    elif environ["PATH_INFO"] == "/admin":
      if environ["QUERY_STRING"] == "password=upml_a6342":
        content += "<p>Это успех! Флаг: <b>UPMLCUPA902525366</b></p>"
      else:
        content += "<p>Не судьба :( Ключ к успеху находится выше того, что вы видите.</p>"
    else:
      content += "<b>404 NOT FOUND</b>"

    content = content.encode("utf-8")
    
    response_headers = [('Content-type', 'text/html; charset=utf-8'),
                        ('Content-Length', str(len(content))),
                        ('X-TODO-DELETE-Key', 'upml_a6342')
                       ]
    
    start_response(status, response_headers)

    return [content]