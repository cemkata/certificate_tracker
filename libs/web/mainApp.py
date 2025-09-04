from bottle import Bottle, route, template, request, redirect
from libs.database.DB_controler import execute_sql_statment

import uuid
import re
import datetime

app = Bottle()

WARNING = 30
ERROR = 15


@app.route('/')
def index():
   #certificates = [{'service':'WebSite wiki', 'ip':'10.22.1.2', 'name': 'wiki.home.lab', 'certauth':'Self-signed', 'from':'03.10.2023', 'to':'03.10.2025', 'certId':'1'}, {'service':'WebSite elog', 'ip':'10.22.1.3', 'name': 'elog.home.lab', 'certauth':'Self-signed', 'from':'02.10.2023', 'to':'02.10.2025', 'certId':'2'}] ##DEMO data
   sql_str = f'''SELECT `server_service`, `server_ip`, `server_name`,
`certificates_authority`, `generated_on_day`, `generated_on_month`, `generated_on_year`, `valid_to_year`,
`valid_to_month`, `valid_to_day`, `id` FROM `certificates_info_tbl`;'''
   rows = execute_sql_statment(sql_str)
   certificates = []
   today = datetime.datetime.today()
   tittle = f'''Certificates information table (generated on {today.strftime('%Y-%m-%d')})'''
   for r in rows:
        tmp = {'service':r[0], 'ip':r[1], 'name': r[2], 'certauth':r[3], 'from':str(r[4])+"-"+str(r[5])+"-"+str(r[6]), 'to':str(r[7])+"-"+str(r[8])+"-"+str(r[9]), 'certId':r[10]}
        print(tmp)
        validto = datetime.datetime(r[7], r[8], r[9])
        delta = validto - today
        if delta.days <= ERROR:
            tmp['color'] = "red"
            tmp ['service'] = '/!\\ '+ tmp ['service']
        elif delta.days <= WARNING:
            tmp['color'] = "yellow"
            tmp ['service'] = '\\!/ '+ tmp ['service']
        else:
            tmp['color'] = "limeGreen"
        certificates.append(tmp)
   return template('index', certificates = certificates, tittle = tittle)

@app.route('/editserver')
def edit():
    serverID = request.query.id or -1
    if serverID == -1:
        redirect("/")
    try:
        int(serverID)
    except ValueError:
        redirect("/")
    sql_str = f'''SELECT `server_service`, `server_ip`, `server_name`,
`certificates_authority`, `generated_on_day`, `generated_on_month`, `generated_on_year`, `valid_to_day`,
`valid_to_month`, `valid_to_year`, `id` FROM `certificates_info_tbl` where `id` = {serverID};'''
    r = execute_sql_statment(sql_str, SINGLE_ROW = True)
    from_date = ""
    to_date = ""
    for i in [4,5,6]:
        if r[i] < 10:
            from_date += "0"+str(r[i])
        else:
            from_date += str(r[i])
        if i == 6:
            break
        from_date +="-"
    for i in [7,8,9]:
        if r[i] < 10:
            to_date += "0"+str(r[i])
        else:
            to_date += str(r[i])
        if i == 9:
            break
        to_date +="-"

    return template('add_edit', server_service=r[0], server_ip=r[1], server_name = r[2],\
        certificate_by = r[3], cert_from = from_date, cert_valid_to = to_date, cid = serverID)

@app.route('/deeteserver')
def delete():
    serverID = request.query.id or -1
    if serverID == -1:
        redirect("/")
    try:
        int(serverID)
    except ValueError:
        redirect("/")
    sql_str = f'''DELETE FROM "certificates_info_tbl" WHERE "id" = {serverID};'''
    _ = execute_sql_statment(sql_str, SINGLE_ROW = True)
    redirect("/")

@app.route('/addnewserver')
def add():
    return template('add_edit')

@app.post('/add') # or @app.route('/add', method='POST')
def add_certificate():
    server_service = request.forms.server_service
    server_ip = request.forms.server_ip
    server_name = request.forms.server_name
    certificate_by = request.forms.certificate_by
    cert_from = request.forms.cert_from.split("-")
    cert_valid_to = request.forms.cert_valid_to.split("-")
    if checkValues(server_ip, cert_from, cert_valid_to, certificate_by):
        errStr = "There is wrong server IP or genrated date ot Valid to field."
        return template('add_edit', error_str = errStr, server_service=server_service, server_ip=server_ip, server_name = server_name,\
        certificate_by = certificate_by, cert_from = request.forms.cert_from, cert_valid_to = request.forms.cert_valid_to)
    else:
        cid = genUniqueID()
        sql_str = f'''INSERT INTO "certificates_info_tbl"("id","server_ip","server_service","server_name","certificates_authority",
        "generated_on_year","generated_on_month","generated_on_day","valid_to_year","valid_to_month","valid_to_day")
        VALUES ({cid},"{server_ip}","{server_service}","{server_name}","{certificate_by}",{int(cert_from[0])},{int(cert_from[1])},{int(cert_from[2])},{int(cert_valid_to[0])},{int(cert_valid_to[1])},{int(cert_valid_to[2])});'''
        _ = execute_sql_statment(sql_str, SINGLE_ROW = True)
    redirect("/")

@app.post('/update') # or @app.route('/update', method='POST')
def update_certificate():
    server_service = request.forms.server_service
    server_ip = request.forms.server_ip
    server_name = request.forms.server_name
    certificate_by = request.forms.certificate_by
    cert_from = request.forms.cert_from.split("-")
    cert_valid_to = request.forms.cert_valid_to.split("-")
    serverID = request.forms.cid
    if checkValues(server_ip, cert_from, cert_valid_to, certificate_by):
        errStr = "There is wrong server IP or genrated date ot Valid to field."
        return template('add_edit', error_str = errStr, server_service=server_service, server_ip=server_ip, server_name = server_name,\
        certificate_by = certificate_by, cert_from = request.forms.cert_from, cert_valid_to = request.forms.cert_valid_to, cid = serverID)
    else:
        sql_str = f'''UPDATE "certificates_info_tbl" set "server_ip" = "{server_ip}","server_service" = "{server_service}","server_name" = "{server_name}","certificates_authority" = "{certificate_by}",
        "generated_on_year" = {int(cert_from[0])},"generated_on_month" = {int(cert_from[1])},"generated_on_day" = {int(cert_from[2])},"valid_to_year" = {int(cert_valid_to[0])},"valid_to_month" = {int(cert_valid_to[1])},"valid_to_day" = {int(cert_valid_to[2])} where `id` = {serverID};'''
        _ = execute_sql_statment(sql_str, SINGLE_ROW = True)
    redirect("/")

def genUniqueID():
    u = int(str(uuid.uuid4())[:8], 16)
    sql_str = f'''SELECT count(*) FROM `certificates_info_tbl` WHERE `id` = {u};'''
    checkSelectOrUpdate = int(execute_sql_statment(sql_str, SINGLE_ROW = True)[0])
    if checkSelectOrUpdate == 0:
        return u
    else:
         return genUniqueID()

def checkValues(server_ip, cert_from, cert_valid_to, certificate_by):
    ip_pattern = re.compile(r'(?:^|\b(?<!\.))(?:1?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:1?\d\d?|2[0-4]\d|25[0-5])){3}(?=$|[^\w.])')
    if not ip_pattern.match(server_ip):
        return True
    elif server_ip.lower() == "localhost":
        server_ip == server_ip.lower()
        return True
    if len(cert_from) !=3:
        return True
    if len(cert_valid_to) !=3:
        return True
    if len(certificate_by) == 0:
        return True
    return False