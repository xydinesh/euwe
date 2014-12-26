<%inherit file="layout.mako" />

<%def name="header_title()">
Euwe, Chess tactics engine for absolute beginners
</%def>

<%def name="body_content()">
<h1>Welcome to ${project}</h1>
</%def>

<%def name="javascript()">
var init = function() {

//--- start example JS ---
var cfg = {
  draggable: true,
  dropOffBoard: 'snapback', // this is the default
  position: 'start'
};

%if position is not UNDEFINED:
%if position:
cfg["position"] = "${position.fen}"
%endif
%endif
var board = new ChessBoard('board', cfg);
//--- end example JS ---

}; // end init()
$(document).ready(init);
 </%def>
