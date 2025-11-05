# Oxylabs Residential Proxy - Public API

**Version:** 1.0.1  
**Base path:** /v1  
**Authentication:** Bearer token obtained from POST /login

Summary:

- Manage sub-users for a given user (identified by userId UUID).
- Endpoints cover creation, listing, retrieval of stats, update, deletion, and target stats.
- Responses use standard HTTP status codes and JSON error objects: { "error": "message" }.

Endpoints:

1) POST /login
    - Purpose: Obtain access token.
    - Responses: 200 (token), 401 (Unauthorized).

2) GET /users/{userId}/sub-users
    - Path params:
      - userId (UUID) — required
    - Success response (200): JSON array of SubUser objects:
      - id (integer)
      - username (string)
      - status ("active" | "disabled")
      - created_at (string, timestamp)
      - traffic (double, GB)
      - traffic_limit (double | null)
      - auto_disable (boolean)
      - lifetime (boolean)
    - Errors: 401, 404

3) POST /users/{userId}/sub-users
    - Path params:
      - userId (UUID) — required
    - Body (application/json):
      - username (string, required) — letters, digits, underscores only
      - password (string, required) — 12–64 chars; must include lowercase, uppercase, digit, and one of: # _ ~ + =
      - traffic_limit (double | null, optional) — null => unlimited; number => GB limit; 0 => no more traffic
      - lifetime (boolean, optional) — true = unlimited subscription
      - auto_disable (boolean, optional)
    - Success response (201): { "id": integer }
    - Errors: 400 (invalid params or max sub-users reached), 401, 404

4) GET /users/{userId}/sub-users/{subUserId}
    - Path params:
      - userId (UUID) — required
      - subUserId (int) — required
    - Query params:
      - type (string, required) — one of: 24h, week, month, current_month, lifetime, custom
         - custom requires date_from and date_to
      - date_from / date_to (string, required for custom) — 'YYYY-MM-DD' or 'YYYY-MM-DD HH' (hours optional)
         - If HH provided, the range is limited to 7 days.
      - time_zone (string, optional) — TZ identifier for date_from/date_to (e.g., "Europe/Berlin")
    - Success response (200):
      {
         "traffic": (double),
         "traffic_by_period": { "date": (double), ... }
      }
    - Errors: 400 (invalid params), 401, 404

5) PATCH /users/{userId}/sub-users/{subUserId}
    - Path params:
      - userId (UUID) — required
      - subUserId (int) — required
    - Body (application/json) — all fields optional:
      - password (string) — same rules as create
      - traffic_limit (double | null)
      - lifetime (boolean)
      - status (string) — "active" | "disabled"
      - auto_disable (boolean)
    - Success response: 200 OK
    - Errors: 400 (invalid params), 401, 404

6) DELETE /users/{userId}/sub-users/{subUserId}
    - Path params:
      - userId (UUID) — required
      - subUserId (int) — required
    - Success response: 204 No Content
    - Errors: 401, 404

7) GET /users/{userId}/sub-users/{subUserId}/target-stats
    - Purpose: Retrieve sub-user's target statistics for a specified date (last 30 days only).
    - Path params:
      - userId (UUID) — required
      - subUserId (int) — required
    - Query params:
      - date (date string, required) — e.g., '2023-01-23'
    - Success response (200):
      { "results": [ { "date": "YYYY-MM-DD", "target": "string", "traffic": double, "requests": int }, ... ] }
    - Errors: 400, 401, 404

Common Error Codes:

- 400: Missing or invalid parameters (including validation rules)
- 401: Missing or invalid Authorization header
- 404: Resource not found

Validation & Notes:

- Username: letters, digits, underscores only.
- Password: 12–64 characters; must include lowercase, uppercase, digit, and one of: # _ ~ + =.
- traffic_limit semantics:
  - null => unlimited traffic
  - numeric (double) => GB limit
  - 0 => no more traffic allowed
- lifetime: when true, subscription is unlimited (no recurring traffic resets).
- auto_disable: when true, sub-user is disabled when traffic_limit is reached.
- For custom time ranges: if hours are provided, queries are limited to a 7-day range.
- Example error payload: { "error": "example error message" }

Schema Summaries:

- NewSubUser: { username*, password*, traffic_limit?, lifetime?, auto_disable? }
- SubUser: { id, username, status, created_at, traffic, traffic_limit, auto_disable, lifetime }
- SubUserStats: { traffic, traffic_by_period }
- SubUserTargetStats: { results: [...] }
- UpdatableSubUserFields: { password?, traffic_limit?, lifetime?, status?, auto_disable? }
- UserToken: { user_id, token }
- Error: { error }
*/
 1.0.1
OAS 3.0
/swagger-ui/v1/spec.yaml
Public API for management of Oxylabs Residential Proxy service

Servers

/v1

Authorize
Login

POST
/login
Get access token

Sub Users

GET
/users/{userId}/sub-users
Get sub users for a user

Parameters
Try it out
Name Description
userId *
string($uuid)
(path)
00000000-0000-0000-0000-000000000000
Responses
Code Description Links
200
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "id": 12345,
    "username": "test_username_123",
    "status": "active",
    "created_at": "2022-01-24 13:54",
    "traffic": 92.45,
    "traffic_limit": 1000,
    "auto_disable": true,
    "lifetime": true
  }
]
No links
401
Missing or invalid Authorization header

Media type

application/json
Example Value
Schema
{
  "error": "example error message"
}
No links
404
Resource not found

Media type

application/json
Example Value
Schema
{
  "error": "example error message"
}
No links

POST
/users/{userId}/sub-users
Create a new sub user

username (required) must consist of letters, digits, and underscores

password (required) must be between 12 and 64 characters long, must contain a lowercase, uppercase letter, a digit, and one of the following special characters: #_~+=

traffic_limit (optional) available values: null - unlimited traffic; {double} (e.g. 20) - 20 GB limit; 0 - no more traffic allowed

lifetime (optional) makes subscription period unlimited (no recurring traffic resets).

auto_disable (optional) available values: true - disable when traffic limit is reached. false - do not disable when traffic limit is reached.

Parameters
Try it out
Name Description
userId *
string($uuid)
(path)
00000000-0000-0000-0000-000000000000
Request body

application/json
Example Value
Schema
{
  "username": "test_username_1",
  "password": "Strong_Password#209",
  "traffic_limit": 2000.68,
  "lifetime": true,
  "auto_disable": true
}
Responses
Code Description Links
201
Created

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "id": 12345
}
No links
400
Invalid parameters, or user has reached the maximum number of sub users

Media type

application/json
Example Value
Schema
{
  "error": "example error message"
}
No links
401
Missing or invalid Authorization header

Media type

application/json
Example Value
Schema
{
  "error": "example error message"
}
No links
404
Resource not found

Media type

application/json
Example Value
Schema
{
  "error": "example error message"
}
No links

GET
/users/{userId}/sub-users/{subUserId}
Get traffic stats for a sub user

Parameters
Try it out
Name Description
userId *
string($uuid)
(path)
00000000-0000-0000-0000-000000000000
subUserId *
integer($int64)
(path)
12345
type*
string
(query)
24h - since 1 day ago.

week - since 7 days ago.

month - since one full month ago (~ 30 days).

current_month - from the first day of this month to today.

lifetime - since subscription started. (only for sub-users with lifetime subscription).

custom type needs date_from and date_to query parameters (e.g. 2019-06-15 17). hh (hours) are optional. Queries with hh (hours) parameters are limited to 7 days range.

Available values : 24h, week, month, current_month, lifetime, custom

24h
date_from
string
(query)
Required for custom type

'2023-01-23' or '2023-01-23 15'
date_to
string
(query)
Required for custom type

'2023-01-23' or '2023-01-23 15'
time_zone
string($time-zone)
(query)
Optional TZ identifier for date_from and date_to fields

'Europe/Berlin'
Responses
Code Description Links
200
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "traffic": 142.68,
  "traffic_by_period": {
    "2023-01-25": 120.73,
    "2023-01-26": 21.95
  }
}
No links
400
Missing or invalid parameters

Media type

application/json
Example Value
Schema
{
  "error": "example error message"
}
No links
401
Missing or invalid Authorization header

Media type

application/json
Example Value
Schema
{
  "error": "example error message"
}
No links
404
Resource not found

Media type

application/json
Example Value
Schema
{
  "error": "example error message"
}
No links

PATCH
/users/{userId}/sub-users/{subUserId}
Update a sub user

password (optional) must be between 12 and 64 characters long, must contain a lowercase, uppercase letter, a digit, and one of the following special characters: #_~+=

traffic_limit (optional) available values: null - unlimited traffic; {double} (e.g. 20) - 20 GB limit; 0 - no more traffic allowed

lifetime (optional) makes subscription period unlimited (no recurring traffic resets).

status (optional) available values: "active", "disabled"

auto_disable (optional) available values: true - disable when traffic limit is reached; false - do not disable when traffic limit is reached.

Parameters
Try it out
Name Description
userId *
string($uuid)
(path)
00000000-0000-0000-0000-000000000000
subUserId *
integer($int64)
(path)
12345
Request body

application/json
Example Value
Schema
{
  "password": "New_Password#561",
  "traffic_limit": 43.87,
  "lifetime": true,
  "status": "active",
  "auto_disable": true
}
Responses
Code Description Links
200
Ok

No links
400
Missing or invalid parameters

Media type

application/json
Example Value
Schema
{
  "error": "example error message"
}
No links
401
Missing or invalid Authorization header

Media type

application/json
Example Value
Schema
{
  "error": "example error message"
}
No links
404
Resource not found

Media type

application/json
Example Value
Schema
{
  "error": "example error message"
}
No links

DELETE
/users/{userId}/sub-users/{subUserId}
Delete a sub user

Parameters
Try it out
Name Description
userId *
string($uuid)
(path)
00000000-0000-0000-0000-000000000000
subUserId *
integer($int64)
(path)
12345
Responses
Code Description Links
204
Ok

No links
401
Missing or invalid Authorization header

Media type

application/json
Example Value
Schema
{
  "error": "example error message"
}
No links
404
Resource not found

Media type

application/json
Example Value
Schema
{
  "error": "example error message"
}
No links

GET
/users/{userId}/sub-users/{subUserId}/target-stats
Get target stats for a sub user

Retrieves sub user's target statistics for specified date (only the last 30 days are available).

Parameters
Try it out
Name Description
userId *
string($uuid)
(path)
00000000-0000-0000-0000-000000000000
subUserId *
integer($int64)
(path)
12345
date*
string($date-time)
(query)
2023-01-23
Responses
Code Description Links
200
Ok

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "results": [
    {
      "date": "2023-01-24",
      "target": "string",
      "traffic": 0,
      "requests": 0
    }
  ]
}
No links
400
Missing or invalid parameters

Media type

application/json
Example Value
Schema
{
  "error": "example error message"
}
No links
401
Missing or invalid Authorization header

Media type

application/json
Example Value
Schema
{
  "error": "example error message"
}
No links
404
Resource not found

Media type

application/json
Example Value
Schema
{
  "error": "example error message"
}
No links
Users

GET
/users/{userId}/client-stats
Get client stats for a user

Schemas
ClientStats{
traffic [...]
date_from [...]
date_to [...]
}
ID
NewSubUser{
username*[...]
password* [...]
traffic_limit [...]
lifetime [...]
auto_disable [...]
}
SubUserStats{
traffic [...]
traffic_by_period {...}
example: { "2023-01-25": 120.73, "2023-01-26": 21.95 }
}
SubUserTargetStats{
results [...]
}
SubUser
UpdatableSubUserFields{
password [...]
traffic_limit [...]
lifetime [...]
status [...]
auto_disable [...]
}
UserToken{
user_id [...]
token [...]
}
Error{
error [...]
}
