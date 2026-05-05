Generate and submit fake test accounts to the password storage webapp at http://127.0.0.1:5000/.

The user has requested: $ARGUMENTS

Parse the number of accounts to generate from the user's request. If no number is specified, default to 5.

For each account, generate realistic but fake data:
- **website**: a short lowercase name (e.g. "github", "netflix", "spotify", "amazon", "twitter", "reddit", "linkedin", "dropbox", "notion", "slack")
- **username**: a realistic lowercase username (e.g. "john_doe", "alex.smith", "coolguy42")
- **password**: a strong-looking password mixing letters, numbers, and symbols (e.g. "Tr0ub4dor&3", "correct-horse-battery")
- **url**: a realistic full URL for that website (e.g. "https://github.com")

Make sure all (website, username) pairs are unique across the batch to avoid duplicates.

Submit each account using the Bash tool with curl to POST to http://127.0.0.1:5000/add with the form fields. URL-encode any special characters in the password.

Use this curl pattern for each account:
```
curl -s -X POST http://127.0.0.1:5000/add -d "website=WEBSITE&username=USERNAME&password=PASSWORD_URLENCODED&url=URL"
```

After submitting all accounts, print a summary table showing:
- How many succeeded
- How many failed (with the error reason if available)
- A list of all accounts that were successfully added
