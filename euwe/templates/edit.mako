<%inherit file="layout.mako" />

<%def name="header_title()">
${title}
</%def>

<%def name="body_content()">
<h1>Welcome to ${project}</h1>
<div id="message">
${message}
</div>

<form method='POST' action='/positons/edit'>
  <button class='btn btn-primary' id='id_btn_start'>Start</button>
  <button class="btn btn-primary" id="id_btn_clean">Clean</button>
  <button class="btn btn-primary" id="id_btn_save">Save</button>
  <div id="id_text_area"></div>
</form>
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
