# WriteBunny Developer Notes

## Push to GitHub
git push -u origin master

## OAuth2 - Local development
* Add the following line to /etc/hosts
    `127.0.0.1       dev.writebunny.com`

## Google API references
* https://developers.google.com/drive/web/
* https://developers.google.com/google-apps/calendar/

## Deploy
appcfg.py update ./

## inotify_file_watcher.py
Allow inotify to watch more files at once:
echo fs.inotify.max_user_watches=100000 | sudo tee -a /etc/sysctl.conf; sudo sysctl -p
