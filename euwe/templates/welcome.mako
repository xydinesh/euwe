 <%inherit file="layout.mako" />

<%def name="javascript()">
var init = function() {

//--- start example JS ---
var board = new ChessBoard('board', 'start');
//--- end example JS ---

}; // end init()
$(document).ready(init);
 </%def>
