<!DOCTYPE html>
<html>
<head>
		<title>Server/Certificate</title>
		<link rel="icon" href="/favicon.ico"/>		
		<link rel='stylesheet' href='/static/css/style.css'>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		% if defined('error_str'):
		<link rel='stylesheet' href='/static/css/1b-icon.css'>
		% end
</head>
<body>
<h3>Server/Certificate</h3>
<div>

% if defined('error_str'):
    <div class="bar error">
      <i class="ico">&#9747;</i> {{error_str}}
    </div>
	<br>	
% end

% if defined('cid'):
<form action="./update" method="post">
% else:
<form action="./add" method="post">
% end

<%
import json
columm_names = []
try:
  file = open('names.json', 'r')
  data = json.load(file)
  columm_names = data['names']
except:
  pass
end

if len(columm_names) != 6:
  columm_names = ['Server service', 'Server IP', 'Server name', 'Cerificate by', 'Generated on', 'Valid to']
end
%>

<table>
  <tr>
    <td><label for="server_service">{{columm_names[0]}}:</label><label style="color:red">*</label></td>
    <td>
% if defined('server_service'):
	<input id="server_service" name="server_service" value="{{server_service}}" required>
% else:
	<input type="text" id="server_service" name="server_service" required>
% end
	</td>
  </tr>
  <tr>
	<td><label for="server_ip">{{columm_names[1]}} (format x.x.x.x):</label><label style="color:red">*</label></td>
	<td>
% if defined('server_ip'):
	<input type="text" id="server_ip" name="server_ip" value="{{server_ip}}" required>
% else:
	<input type="text" id="server_ip" name="server_ip" required>
% end
	</td>
  </tr>
  
  <tr>
	<td><label for="server_name">{{columm_names[2]}}:</label><label style="color:red">*</label></td>
	<td>
% if defined('server_name'):
	<input type="text" id="server_name" name="server_name" value="{{server_name}}" required>
% else:
	<input type="text" id="server_name" name="server_name" required>
% end
	</td>
  </tr>
  
  <tr>
	<td><label for="certificate_by">{{columm_names[3]}}:</label><label style="color:red">*</label></td>
	<td>
% if defined('certificate_by'):
	<input type="text" id="certificate_by" name="certificate_by" value="{{certificate_by}}" required>
% else:
	<input type="text" id="certificate_by" name="certificate_by" required>
% end
	</td>
  </tr>
  
  <tr>
	<td><label for="cert_from">{{columm_names[4]}}:</label><label style="color:red">*</label></td>
	<td>
% if defined('cert_from'):
	<input type="date" id="cert_from" name="cert_from" value="{{cert_from}}" required>
% else:
	<input type="date" id="cert_from" name="cert_from" required>
% end
	</td>
  </tr>
  
  <tr>
	<td><label for="cert_valid_to">{{columm_names[5]}}:</label><label style="color:red">*</label></td>
	<td>
% if defined('cert_valid_to'):
	<input type="date" id="cert_valid_to" name="cert_valid_to" value="{{cert_valid_to}}" required>
% else:
	<input type="date" id="cert_valid_to" name="cert_valid_to" required>
% end
	</td>
  </tr>
</table>

% if defined('cid'):
	<input type="hidden" id="cid" name="cid" value="{{cid}}">
% end
	<input type="submit" value="Submit">
</form>
</div>
<input type="button" id = "backButton" onclick="self.location = '/';" value="Cancel" />
</body>
</html>
<%
import datetime
today = datetime.date.today()
%>
<!-- Copyright {{today.year}} CEMKATA -->