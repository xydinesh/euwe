<%inherit file="layout.mako" />

<%def name="header_title()">
Euwe, Chess tactics engine for absolute beginners
</%def>

<%def name="body_content_before_board()">
<h1>Welcome to ${project}, ${userid}</h1>
</%def>

<%def name="body_content_after_board()">
<div id='div_form_container'>
  <form role="form" id='id_form_play'>
    <div class='form-group'>
      <button class="btn btn-primary" id="id_btn_play" name="form.played" type="submit">Check Solution</button>
    </div>
  </form>
</div>
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

$('#id_btn_play').click(function(){
  $.ajax({
    type: "GET",
    url: '/answer',
    data: 'id=${id}&solution='+board.fen(),
    dataType: 'json',
    success: function(data) {
      if (data['result'] == 'success') {
        alert('Success');
      }
    }
    });
  });

  $('#id_form_play').submit(function(e){
    e.preventDefault();
  });
}; // end init()
$(document).ready(init);
 </%def>
