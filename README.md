# certificate_tracker
Small tool to log and monitor the ssl certificates status
it needs bootle execpt [bottle framework](https://github.com/bottlepy/bottle) and python sqlite3 libs (if they are not installed by default).
You do not need to install the framework, only download the bottle.py file and put it in the same folder.

***mainScript.py***
This is the main file 
  
Edit the config.ini 
<pre>
  port = 8888   ;port of the server
  ip = 127.0.0.1   ;where the server will listen
  dbpath = ./db_file.db    ;path to the database 
</pre>

By default this tool will mark the expiring rows in yellow 30 days, before final date and in red 15 days, before final date.

If you want to change this edit the libs/web/mainApp.py, you can change the following values:
WARNING = 30
ERROR = 15

