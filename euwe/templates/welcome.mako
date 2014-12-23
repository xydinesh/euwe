<%inherit file="layout.mako" />

<%def name="title()">
Euwe, Chess tactics engine for absolute beginners
</%def>
<%def name="body_content()">
<h1>Welcome to ${project}</h1>
</%def>

<%def name="javascript()">
var init = function() {

//--- start example JS ---
var board = new ChessBoard('board', 'start');
//--- end example JS ---

}; // end init()
$(document).ready(init);
 </%def>
