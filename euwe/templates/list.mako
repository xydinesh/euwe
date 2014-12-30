<%inherit file="layout.mako" />

<%def name="header_title()">
${title}
</%def>

<%def name="body_content_before_board()">
<h1>Welcome to ${project}, ${userid}</h1>
<div id="message">
${message}
</div>
</%def>

<%def name="body_content_after_board()">
<div class="row" id="id_cb_div">
<button class="btn btn-primary" id="id_btn_delete">Delete</button><br/>
  %for position in positions:
    <div class="col-sm-2">
      <input type="checkbox" name="${position.id}" value="${position.id}">${position.id}<br>
      <div id="board${position.id}" style="width: 200px; float: left; margin-right: 10"></div>
    </div>
  %endfor
  <div style="clear:both"></div>
</div>
</%def>

<%def name="javascript()">
%for position in positions:
var board${position.id} = new ChessBoard("board${position.id}", {
  position: "${position.fen}",
  showNotation: false
  })
%endfor

$('#id_btn_delete').click(function(){
    $('#id_cb_div :checked').each(function() {
      var v = $(this).val();
      $.ajax({
          url: '/delete/' + v,
          type: 'DELETE',
          success: function(result) {
            // console.log(result);
          }
        });

      });
    });

</%def>
