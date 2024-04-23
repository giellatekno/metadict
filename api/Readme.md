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
