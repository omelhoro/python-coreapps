// Generated by CoffeeScript 1.7.1
(function() {
  var $;

  $ = jQuery;

  $(function() {
    return $("button").click(function(e) {
      switch ($(e.target).prop("id")) {
        case "update":
          return ex9.update();
        case "show":
          return ex9.show("foo", function(res) {
            $("#tab").children().remove();
            return $("#tab").append($(res));
          });
        case "delete":
          return ex9["delete"]();
        case "insertn":
          return ex9.insert_new();
      }
    });
  });

}).call(this);
