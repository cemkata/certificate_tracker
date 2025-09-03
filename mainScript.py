###!/usr/bin/env python3
# -*- coding: utf-8 -*-

web_Start = True

ver = 1.2
projectName = "Certificates monitor"

if web_Start:
 import configer
 import libs.web.staticFiles as staticFiles
 import libs.web.mainApp as mainApp
 from bottle import Bottle, run

 #https://stackoverflow.com/questions/26923101/does-bottle-handle-requests-with-no-concurrency
 app = Bottle()
 rootApp = application = app
 config = configer.init()
 
 mainApp.WARNING = config.WARNING
 mainApp.ERROR = config.CRITICAL
 
 app.mount('/', staticFiles.app)
 app.mount('/', mainApp.app)


 print(f"Starting {projectName} - version {ver}")
 run(app, host = config.host, port = config.port, debug=True)

