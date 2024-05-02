# Config files required

`gh_app.toml` which should contain:

```text
client_id = "Iv1.f208b6793cca35ec"
client_secret = "GH APP CLIENT SECRET HERE"
```

`jwt_secret.txt` contains the local jwt key. It can be generated with the
following command:

```bash
openssl rand --hex 32 > jwt_secret.txt
```


# Authentication and authorization

## Terminology

- *Authenticating* is the process of verifying that users are who they say they
are. In our case we know that a github user is a specific person.
- *Authorization* is the process of setting permissions for an authenticated
user (i.e. letting a known github user access our closed dictionaries).
- *Github App* is a registered app on github.
  Our Github App is at https://github.com/organizations/giellatekno/settings/apps/giellatekno-metadictionary
- *JWT* is *Json Web Token*. It is a json object that for example can say
  "user x logged in at some datetime". It is signed by a private key.
  We use two different JWTs: One to authorize our app to github, and one to
  keep track of our own logged in users.


## Overview

Users log in by clicking a link that takes them to github. They log in,
authenticate our app, and gets redirected back to our app. Our app can then
check if that github user is a member of the giellatekno/metadictionary-access
team. If they are, they can see restricted dictionaries.


## Authenticating

To authenticate users through github, we must have a "Github App". On the
settings page on the giellatekno organization, all the way to the bottom of
the left side, we have "developer settings -> github apps". Under there, we have
the app "giellatekno-metadictionary":
https://github.com/organizations/giellatekno/settings/apps/giellatekno-metadictionary
It has an associated client id and client secret.

The login link on the frontend links to github login, and contains the client id.
The user authorizes the app (first time only), and logs in. This redirects
the user to our *api* (_not_ the frontend), and contains what in oauth-terminology
is called a "code". The API exchanges this code (together with the github
app client secret) for a "user access token" from github, then finally redirects
back to the frontend, setting a cookie on the browser to save the token.

(Note: The code exchange process has to happen on the API, because we need to
keep the client secret...secret. The secret cannot in any way be embedded on
the frontend, because if it were, then another site could pretend that they
are us.)


## Authorization

Checking if a github username is a member of our team is done by calling
this endpoint on github: 
`https://api.github.com/orgs/{org_name}/teams/{team_name}/memberships/{login_name}`
We know the organization name, and the team name. The login name of the logged
in user, we get from github. We send a basic user info query, and give the
user access token.

The Github API call requires that the caller has the permissions to see members 
of that team. This is where the second authentication comes in.

Although we could use the user access token to ask github if that user is a
member of our team, we instead ask on behalf of the app. It is a bit more
involved.


### Authenticating our github app as itself

First, our app must "authenticate as itself". This is done through a different
access token, one that authenticates the app, and not the user. Github apps
can be public, and when others use it, they *install* it on their organization.
Our github app is private, and can only be installed by us (and it is) - but we
still have to go through the same authentication process.

So, this is a 2-step process. First, we authenticate as the app, *then* we
authenticate as our particular *installation* - hence why the token we get back
is called an *installation access token* (or *IAT*).

We authenticate as *the github app* simply by generating a JWT, which we sign
our private key, that only the app knows. This key can be found towards the
bottom of the app page:

https://github.com/organizations/giellatekno/settings/apps/giellatekno-metadictionary

We send this JWT to github, which can verify that the JWT came from our app.
It can then give us an IAT for a given installation. In our case, we only have
one known installation (we know the ID, and the ID doesn't change), so we don't
need the endpoints for determining the installation ID.

Finally, we can call
`https://api.github.com/orgs/{org_name}/teams/{team_name}/memberships/{login_name}`
with the IAT as authentication. The permissions for what the installation can
can access are given by the app, and accepted when the app is installed. In our
case, we specifically need read "members" permission, and we have set that.


## Authenticating and authorizing flow

Below is an example flow of the full login flow. As a final note, note that
the flow gets a lot more complicated whenever we use the tokens to do queries
later, because every single token we use can fail, in multiple ways. The tokens
may simply have expired, but the remotes (both GH API and Our API) may also be
down, and our code should handle all such cases as gracefully as possible.

```
|-(Browser)-----------|
| user clicks login   |
|---------------------|-----[client id]---------------------------------------------------------------------->|--(Github)-------------------|
                                                                                                              |  User logs in to Github     |
                                                                                                              |  User accepts our app       |
                                                       |--(Our API)---------------|<----------[code]----------|-----------------------------|
                                                       |  Exchange code for UAT   |
                                                       |                          |
                                                       |--------------------------|---[code, client secret]-->|--(Github)-------------------|
                                                                                                              |  Accept code, generate UAT  |
                                                                                                              |                             |
                                                       |--(Our API)---------------|<-----------[UAT]----------|-----------------------------|
                                                       |  Get user login          |
                                                       |                          |
                                                       |--------------------------|------------[UAT]--------->|--(Github)-------------------|
                                                                                                              |   Find user info            |
                                                                                                              |                             |
                                                       |--(Our API)---------------|<-------[user info]--------|-----------------------------|
                                                       |  Is user in our team?    |
                                                       |  But: Do we need an IAT  |
                                                       |--------------------------|--[Need IAT, send JWT]---->|--(Github)-------------------|
                                                                     |                                        |  Generate IAT               |
                                                                     |                                        |                             |
                                                                [We have IAT]                    |------------|-----------------------------|
                                                                     |                           |
                                                                     v                           |
                                                        |-------------------------|<----[IAT]----|
                                                        | Now check user in team  |
                                                        |                         |
                                                        |-------------------------|-----[IAT]---------------->|--(Github)-------------------|
                                                                                                              |  Check user in team         |
                                                                                                              |                             |
                                                       |--(Our API)---------------|<---[user in our team]-----|-----------------------------|
                                                       |  Generate Our JWT        |
                                                       |  (UAT + our permissions  |
|--(Browser)----------|<-----[Our jwt, as cookie]------|--------------------------|
|  Now authenticated  |
|  With our JWT       |
|---------------------|
```
