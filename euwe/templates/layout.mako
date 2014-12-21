<!DOCTYPE html>
<html lang="${request.locale_name}">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Euwe Chess Tactics Engine">
    <meta name="author" content="Dinesh Weerapurage">
    <link rel="shortcut icon" href="${request.static_url('euwe:static/img/pyramid-16x16.png')}">

    <title>Euwe Chess Tactics Engine for Absolute Begineers.</title>

    <!-- Bootstrap core CSS -->
    <link href="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this scaffold -->
    <link href="${request.static_url('euwe:static/css/theme.css')}" rel="stylesheet">
    <link rel="stylesheet" href="${request.static_url('euwe:static/css/chessboard-0.3.0.css')}" />

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="//oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="//oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>
    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="//oss.maxcdn.com/libs/jquery/1.10.2/jquery.min.js"></script>
    <script src="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/js/bootstrap.min.js"></script>
    <script src="${request.static_url('euwe:static/js/chessboard-0.3.0.js')}"></script>

    <script type="text/javascript">
    ${next.javascript()}
    </script>

    <div id="board" style="width: 400px"></div>
  </body>
</html>
