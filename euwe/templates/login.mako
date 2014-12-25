<%inherit file="layout.mako" />

<%def name="header_title()">
${title}
</%def>

<%def name="body_content()">
<h1>Welcome to ${project}</h1>
<div id="message">
${message}
</div>

<form method='POST' action='/login'>
  <input type="text" name='username' id='id_username' placeholder='username'/>
  <input type="password" name="password" id="id_password" placeholder='password'/>
  <input type="submit" value="Log In" name="form.submitted"/>
</form>
</%def>

<%def name="javascript()">
</%def>
