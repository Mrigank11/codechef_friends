# CC Friends API
Because, it's always better with friends :)

**NOTE**: All endpoints can be tested using the nice interface provided by DRF. Just open endpoints in browser.

## OAuth2
Root endpoint: `/oauth`
- `GET /redirect` : redirect to codechef
- `GET /callback` : handle response
- `POST /cli_auth` : handles new user on cf-friends given tokens
	- requires tokens as JSON

## API 
Root endpoint: `/api`

- [x] `GET /users/?q=<query>` : Search/List users registered on "Codechef_friends"
- [x] `GET /users/<username>` : fetch user info from codechef
- [x] `GET /friends`* : returns user's list of friends
- [x] `PUT /friends`* : add friend, requires:
	- Friends' codechef id
- [x] `DELETE /friends/<username>`* : remove friend, requires:
	- Friends' codechef id

`*` needs authentication header

## TODO
- [ ] Remove request_oauthlib (?). Because codechef is not following the RFC

## Demo
- `pipenv install` 
- `./manage.py runserver <port>` to start server
- Open `/oauth/redirect` to start flow, and recieve tokens
