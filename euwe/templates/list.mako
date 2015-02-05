<%inherit file="layout.mako" />

<%def name="header_title()">
${title}
</%def>

<%def name="body_content_before_board()">
<h1>Welcome to ${project}, ${userid}</h1>
<div id="message">
${message}
</div>
<div id='flash-msg'>
  % for fmsg in request.session.pop_flash():
  <p>${fmsg}</p>
  % endfor
</div>
</%def>

<%def name="body_content_after_board()">
<form id='id_form_list' name='id_form_list' role='form'>
<div class="row" id="id_cb_div">
<div class='form-group'>
  <button class="btn btn-primary" id="id_btn_delete" type="submit" name='position.delete'>Delete</button><br/>
</div>
  %for position in positions:
    <div class="col-sm-2">
      <div class="thumbnail">
        <div class = "form-group">
          <input type="checkbox" name="${position.id}" value="${position.id}">${position.id}<br>
        </div>
        <div class="chess-board" id="${position.id}"></div>
      </div>
    </div>
  %endfor
  <div style="clear:both"></div>
</div>
</form>
</%def>

<%def name="javascript()">
%for position in positions:
var board${position.id} = new ChessBoard("${position.id}", {
  position: "${position.fen}",
  showNotation: false
  })
%endfor

var init = function() {

$('#id_form_list').submit(function(e){
  e.preventDefault();
  });

$('.chess-board').dblclick(function() {
    var status = $(this).attr('id');
    console.log(status);
    window.location.href = "/play?id=" + status;
  });

$('#id_btn_delete').click(function(){
    var deferreds = [];
    $('#id_cb_div :checked').each(function() {
      var v = $(this).val();
      deferreds.push($.ajax({
          async: true,
          url: '/list?position.delete&id=' + v,
          type: 'delete',
        }));

      });

      $.when.apply($, deferreds).done(function() {
        window.location.href = "/";
      });
    });

  } // end of init
$(document).ready(init);
</%def>
