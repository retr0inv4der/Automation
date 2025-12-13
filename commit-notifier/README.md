# GitHub Commit Notifier

A small Linux utility that checks a GitHub repository for new commits and sends a desktop notification when one appears. It installs itself, compiles into a single binary, and runs quietly via cron like a well-behaved background process.

## What it does

- Polls the GitHub API for the latest commit of a repository
- Stores the last seen commit SHA locally
- Sends a desktop notification when a new commit is detected
- Runs automatically every 10 minutes using cron
- Installs as a single binary at `/usr/local/bin/notifier`

## Requirements

- Linux system with:
  - Python 3.8+
  - `cron` (cronie)
  - `systemd`
  - Desktop notification support (DBus)
- Internet access
- GitHub repository must be public (no auth/token support yet)

## Project Structure


- install.py # Installer, builder, cron setup
- notifier.py # Main notifier logic
- uninstall.py # Cleanup script
- requirements.txt # Python dependencies


## Dependencies

Managed automatically during installation:

- `requests`
- `notify2`
- `pyinstaller`

## Installation

Run the installer with your GitHub username and repository name:

```bash
python install.py <github-username> <repository-name>
```
Example:

```bash
python install.py retr0inv4der Automation
```
What this does:

Creates a virtual environment

Installs dependencies

Compiles notifier.py into a single binary using PyInstaller

Copies the binary to /usr/local/bin/notifier

Sets executable permissions

Creates a cron job that runs every 10 minutes

Cleans up build artifacts and the virtual environment

Cron Job Details
The installer adds a cron entry similar to:

```cron
*/10 * * * * DISPLAY=1 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus /usr/local/bin/notifier <user> <repo> >> /home/retr0/mew.txt
```
Notes:

DISPLAY and DBUS_SESSION_BUS_ADDRESS are required for desktop notifications


The DBus path assumes user ID 1000

If your user ID is different, adjust the path accordingly.

How it Works Internally
Fetches commits from:

```bash
https://api.github.com/repos/<user>/<repo>/commits
```
Extracts the latest commit SHA

Stores state in:

```bash
/tmp/commits.json
```
Compares current SHA with stored SHA

Sends a notification if they differ

Uninstallation
To completely remove the notifier:

```bash
python uninstall.py
```
This will:

Remove the cron job

Delete /usr/local/bin/notifier

## Known Limitations
No GitHub authentication (rate limits apply)

Assumes a graphical session is available

Hardcoded DBus path for user 1000

Only tracks the latest commit, not multiple commits

Possible Improvements
GitHub token support

Configurable polling interval

User-agnostic DBus detection

Support for multiple repositories

## Contributions

Contributions are welcome, but keep them sane.


Good contribution ideas:
- Fixing DBUS / DISPLAY auto-detection
- Supporting GitHub API tokens
- Making the cron setup user-agnostic
- Replacing cron with a systemd user timer
- Improving error handling and logging