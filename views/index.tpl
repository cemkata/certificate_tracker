<html>
<head>
		<title>{{tittle}}</title>
		<link rel='stylesheet' href='/static/css/newStyle.css'>
		<link rel="shortcut icon" href="/favicon.ico">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0;">
		<script src="/static/js/scripts.js" type="text/javascript"></script>
		<script>
			function confirmEdit(qid) {
				window.location.href = './editserver?id=' + qid;
			}
			function confirmDelete(qid) {
				if (confirm('Are you sure you want to delete this server/certificate?')) {
				  window.location.href = './deeteserver?id=' + qid;
				} 
			}
		</script>
</head>

<body>
<h2>{{tittle}}</h2>
<input type="button" class="btnGreen" onclick="self.location = '/addnewserver';" value="Add new server/certificate">
<h2> </h2>
<table class="table responsive" id="myTable">
  <thead>
    <tr class = "boldText">
      <td onclick="sortTable(0)" class="sortable">Server service</td>
      <td onclick="sortTable(1)" class="sortable">Server IP</td>
      <td onclick="sortTable(2)" class="sortable">Server name</td>
      <td onclick="sortTable(3)" class="sortable">Cerificate by</td>
      <td onclick="sortTable(4)" class="sortable">Generated on</td>
      <td onclick="sortTable(5)" class="sortable">Valid to</td>
      <td>Edit</td>
      <td>Delete</td>
    </tr>
  </thead>
  <tbody>
  %for c in certificates:
    <tr class = "{{c['color']}}">
      <td data-label="Service">{{c['service']}}</td>
      <td data-label="Ip">{{c['ip']}}</td>
      <td data-label="Server name">{{c['name']}}</td>
      <td data-label="Cerificate by">{{c['certauth']}}</td>
      <td data-label="Generated on">{{c['from']}}</td>
      <td data-label="Valid to">{{c['to']}}</td>
      <td data-label="Edit"><input type="button" class="btnBlue" onclick="confirmEdit({{c['certId']}})" value="Edit" /></td>
      <td data-label="Delete"><input type="button" class="btnRed" onclick="confirmDelete({{c['certId']}})" value="Delete" /></td>
    </tr>
  %end
  </tbody>
</table>
</table>
</body>
</html>

<%
import datetime
today = datetime.date.today()
%>
<!-- Copyright {{today.year}} CEMKATA -->