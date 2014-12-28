<%inherit file="layout.mako" />

<%def name="header_title()">
${title}
</%def>

<%def name="body_content_before_board()">
<h1>Welcome to ${project}</h1>
</%def>

<%def name="body_content_after_board()">
<div id="message">
${message}
</div>
<div id="login_form">
<form method='POST' action='/login'>
  <input type="text" name='username' id='id_username' placeholder='username'/>
  <input type="password" name="password" id="id_password" placeholder='password'/>
  <input type="submit" value="Log In" name="form.submitted"/>
</form>
</div>
</%def>

<%def name="javascript()">
</%def>
