<%inherit file="layout.mako" />

<%def name="header_title()">
${title}
</%def>

<%def name="body_content_before_board()">
<h1>Welcome to ${project}</h1>
<div id="message">
${message}
</div>
</%def>

<%def name="body_content_after_board()">
<form method='POST'>
  <button class="btn btn-primary" id="id_btn_save" name="form.saved">Save</button>
</form>
<button class='btn btn-primary' id='id_btn_start'>Start Position</button>
<button class="btn btn-primary" id="id_btn_clear">Clear</button>
<button class="btn btn-primary" id='id_btn_flip'>Flip Board</button>
<textarea id="id_text_area" value=""></textarea>
</%def>

<%def name="javascript()">
var init = function() {

  //--- start example JS ---
  var cfg = {
    draggable: true,
    dropOffBoard: 'snapback', // this is the default
    position: 'start',
    sparePieces: true
  };

  %if position is not UNDEFINED:
  %if position:
  cfg["position"] = "${position.fen}"
  %endif
  %endif
  var board = new ChessBoard('board', cfg);

  $('#id_btn_start').on('click', board.start);
  $('#id_btn_clear').on('click', board.clear);
  $('#id_btn_flip').on('click', board.flip);

  $('#id_btn_save').click(function(){
    $.ajax({
      type: "POST",
      url: '/save',
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify({ 'fen': board.fen() }),
      dataType: 'json',
      success: function(data) {alert(data);}
      });
    });

  //--- end example JS ---

  }; // end init()
  $(document).ready(init);
</%def>
