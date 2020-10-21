
    $(document).ready(function() {

      var isLoggedIn = 0
      console.log(isLoggedIn)
  
        if(isLoggedIn == 1) {
            $('#login').show();
            $('#logoutform').show();
        } else {
            $('#login').show();
            $('#logooutform').show();
        }
  
      $('#submit').on('click', function(e) {
          e.preventDefault();
      
          var username = $('#username').val();
          var pwd = $('#password').val();
      
      
          if(username != "" && pwd != "" ) {
                $.ajax({
                    method: "POST",
                    url: '/login',
                    contentType: 'application/json;charset=UTF-8',
                    data: JSON.stringify({'username': username, 'password': pwd}),
                    dataType: "json",
                    success: function(data) {
                        localStorage.setItem('loggedin', 1);
                      
                        $('#login').show();
                        $('#logoutform').show();
                    },
                  error: function(err) {
                      console.log(err);
                  }
              });
          }
      }
  );
  
  $('#logout').on('click', function(e) {
      e.preventDefault();
      
      $.ajax({
          url: '/logout',
          dataType: "json",
          success: function(data) {
              localStorage.setItem('loggedin', 0);
              $('#login').show();
              $('#logoff').show();
          },
      });
  });
});
