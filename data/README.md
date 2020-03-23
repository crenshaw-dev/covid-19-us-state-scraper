# data

Each file is named for the number of seconds since the epoch at the time the stats were collected.

At first I had these updating on a one-hour loop. Now checks are performed every 60sec and files created only if there
are changes.