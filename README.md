# Slack-last-login

A really simple script to obtain all available access logs from your Slack workspace and to find the last login time for each user.

[API documentation](https://api.slack.com/methods/team.accessLogs)

## Warnings

* This script uses legacy tokens - [more info here](https://api.slack.com/custom-integrations/legacy-tokens)
* Do **not** share your token!
* API limitations ([more info](https://api.slack.com/methods/team.accessLogs)):
  * 1000 logs per page
  * 100 pages
  * 20 requests per minute

## Requirements

* Python >= 3.6
* requests (`pip install requests`)
* Slack API token
  * [Token generator page](https://api.slack.com/custom-integrations/legacy-tokens)
  * Place your token to `api_token.py.tpl` and rename the file `api_token.py.tpl` → `api_token.py`

## Usage

Just run `python3 team_access_log.py`. It will show you a progress and produce two files:

* `raw_data.csv` which contains all downloaded access logs converted from JSON to CSV for further processing
* `last_logins.csv` which contains an information about last login and a count of inactive days for each user

## License

MIT
