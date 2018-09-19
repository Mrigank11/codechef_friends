# CC Friends API
Because, it's always better with friends :)

## OAuth2
- `/oauth/redirect` : redirect to codechef
- `/oauth/callback` : handle response

## API 
Root endpoint: `/api/`

- [x] `GET /users/?q=<query>` : Search/List users registered on "Codechef_friends"
- [ ] `GET /users/<username>` : returns `User` object, containing basic user info
- [x] `GET /friends`* : returns user's list of friends
- [x] `PUT /friends`* : add friend, requires:
	- Friends' codechef id
- [x] `DELETE /friends`* : remove friend, requires:
	- Friends' codechef id

`*` needs authentication header

## TODO
- [ ] Remove request_oauthlib (?). Because codechef is not following the RFC

## Demo
- `pipenv install` 
- `./manage.py runserver <port>` to start server
- Open `/oauth/redirect` to start flow, and recieve tokens
