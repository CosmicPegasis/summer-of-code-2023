# Requests

![](./Pasted%20image%2020230623233329.png)


Most of the requests are simple fetch requests for various libraries such as JQuery and stylesheets. These requests are made by index.php because it is a dynamic webpage. There's also a JQuery ajax request to fetch notifications(guessing from the name).

## index.php
![](./Pasted%20image%2020230623233506.png)
For index.php:
- Cache-control: Specifies caching policies. max-age=0 means no cache.
- Connection: A now prohibited header field, used to specify whether the connection should be kept open or closed after the current request is done.
- Content-encoding: Compression format
- Content-Language: self explanatory
- Content-Length: self explanatory
- Content-Script-Type: servers as the file extension type
- Content-(Style)-Type: self explanatory
- Date: self explanatory
- Keep-Alive: Again a now prohibited response header used to signify the time duration for the server to keep the socket open for additional requests.
- Pragma: Used for backwards compatibility with HTTP/1.0
- Server: self explananatory
- Vary: Used to signify what other parts of the request other than the method called and url used influenced the making of this response.
- X-Frame-Options: Allow or disallow embedding frames, iframes etc. For example moodle only allows embedding only to other webpages from the same server.
- X-Ua-Compatible: Everyone hates Internet Explorer lol.

## What happens when I log in?
My username and password is matched to a database and if both match to a single database entry then the server responds with an OK, the front end then requests for various resources, which the server provides. If my credentials do not completely match an entry, the server responds with 401 (unauthorized) and the front end shows invalid login.

## What cookies are used?
![](./Pasted%20image%2020230624001005.png)
Moodle uses to cookies once logged in, one is a clear session cookie that is sent with requests for authentication purposes. The other is for the remember username button that you can optionally check at the login.