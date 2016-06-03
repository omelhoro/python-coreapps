$= jQuery
$ ->
	$("button").click (e) ->
		switch $(e.target).prop("id")
			when "update" then ex9.update()
			when "show" then ex9.show "foo", (res) -> 
				$("#tab").children().remove()
				$("#tab").append($(res))
			when "delete" then ex9.delete()
			when "insertn" then ex9.insert_new()