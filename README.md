# Overdueist
Overdueist is a small Python application for recurring notifications of overdue [Todoist](https://todoist.com) tasks.
It runs as a lightweight cronjob script that checks for incomplete Todoist tasks in your account and sends you a notification via any service [Apprise](https://github.com/caronc/apprise) supports.

# Description/Motivation
Todoist is an awesome service, and one I've used for years. However one thing it does not natively support is nagging-style notifications of tasks after their due date has passed.
Reading through community discussions, the consensus seems to be that this would be a non-feature and it instead is indicative of you not checking the app frequently enough.
However, for someone as scatter-brained as me, this is easier said than done! Luckily, Todoist's powerful API makes implementing this a cinch.

# Features
- Requires just your personal Todoist API key
- Supports notifications via any of the [155+ services](https://appriseit.com/services/) that Apprise does
- Runs via cron (or similar) for flexible scheduling
- Optionally integrates with [Healthchecks](https://healthchecks.io) to monitor that it is running

# Roadmap (Time Permitting)
- Native Todoist integration
- Run as an optional daemon instead of via cron
- Custom task filters
- Custom Apprise routing

# Setup
1. Install Overdueist via `pipx install apprise`
2. Optain your Todoist API key at https://app.todoist.com/app/settings/integrations/developer
  - As Todoist mentions, keep this token safe!
  - See below for how to set this token in your cron file
3. If you do not already have one, setup an Apprise config file.
  - See the [Apprise documentation](https://appriseit.com/getting-started/configuration/) on Configuration
  - Overdueist by default looks in the [same locations](https://appriseit.com/getting-started/configuration/#default-configuration-locations) Apprise does for config file(s).
    This can also be overridden via the `--apprise-config` flag or `APPRISE_CONFIG_PATH` environment variable.
4. Set up your preferred cronjob to run `overdueist` at each time you want it to check for tasks. See below for an example.

## Example Crontab
Below is my personal crontab for Overdueist. It notifies of overdue tasks 5 minutes after every hour, between the hours of 8am to 8pm.

To keep your Todoist token secure, it's recommended that you set this in your user-specific crontab via `crontab -e`

Tip: Use [crontab guru](https://crontab.guru) to help with cron syntax

```
OVERDUEIST_API_TOKEN=your-token
5 8-20 * * * overdueist > /dev/null
```

## Example SystemD Time
TODO
