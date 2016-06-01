import http.cookies

def application(environ, start_response):
    status = '200 OK'

    response_headers = [('Content-type', 'text/html; charset=utf-8')]
    
    cookie = http.cookies.SimpleCookie(environ.get("HTTP_COOKIE"))
    content = "<meta charset='utf-8' /><h1>Панель управления заводом по производству печенья</h1><p>Вы не можете просматривать данную страницу.</p>"
    
    if cookie.get("admin") is None:
      response_headers.append(('Set-Cookie', 'admin=0'))
    elif cookie.get("admin").value == "1":
      content = "<meta name='charset' content='utf-8' /><h1>Панель управления заводом по производству печенья</h1><p>Пароль: <b>Qwerty123</b></p>"
    
    content = content.encode('utf-8')
    clh = ('Content-Length', str(len(content)))
    response_headers.append(clh)

    start_response(status, response_headers)

    return [content]