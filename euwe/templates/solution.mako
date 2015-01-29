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
<div id='div_form_container' style='float:left;'>
  <form role="form" id='id_form_solution'>
    <div class='form-group'>
      <button class="btn btn-primary" id="id_btn_save_solution" name="form.saved" type="submit">Save</button>
    </div>
    <div style='clear:both;'></div>|
  </form>
</div>
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

  $('#id_btn_save_solution').click(function(){
    $.ajax({
      type: "POST",
      url: '/save',
      data: JSON.stringify({ 'id': "${id}", 'solution': board.fen() }),
      dataType: 'json',
      success: function(data) {
        console.log('save function')
        window.location.href = "/list";
      }
      });
    });

    $('#id_form_solution').submit(function(e){
      e.preventDefault();
    });

  //--- end example JS ---

  }; // end init()
  $(document).ready(init);
</%def>
