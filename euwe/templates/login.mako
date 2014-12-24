<%inherit file="layout.mako" />

<%def name="header_title()">
${title}
</%def>

<%def name="body_content()">
<h1>Welcome to ${project}</h1>
<form method='POST' action='/login'>
  <input type="text" name='username' id='id_username' placeholder='username'/>
  <input type="password" name="password" id="id_password" placeholder='password'/>
  <input type="submit" value="submit" name="submit"/>
</form>
</%def>

<%def name="javascript()">
</%def>
