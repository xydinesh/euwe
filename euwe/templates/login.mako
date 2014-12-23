<%inherit file="layout.mako" />

<%def name="title()">
${title}
</%def>

<%def name="body_content()">
<h1>Welcome to ${project}</h1>
<form method='POST'>
  <input type="text" name='username' id='id_username' placeholder='username'/>
  <input type="password" name="password" id="id_password" placeholder=''/>
  <input type="submit" value="submit"/>
</form>
</%def>

<%def name="javascript()">
</%def>
