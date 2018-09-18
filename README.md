# CC Friends API
Because, it's always better with friends :)

## OAuth2
- `/oauth/redirect` : redirect to codechef
- `/oauth/callback` : handle response

## API 
All API endpoints return JSON in the following format:
```json
{
	"success": Bool
	"result": < The Result>
}
```
Root endpoint: `/api/`

- `GET /users` : Search/List users registered on "Codechef_friends"
- `GET /users/<username>` : returns `User` object, containing basic user info
- `GET /friends`* : returns user's list of friends
- `POST /friends/add`* : add friend, requires:
	- Friends' codechef id
- `POST /friends/remove`* : remove friend, requires:
	- Friends' codechef id

`*` needs authentication header
