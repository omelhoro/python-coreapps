$= jQuery
ex11= ex14
$ ->

	class User
		constructor: (@name) ->
			@TAB= $("#tab")
			@_present_table()
			@_menu_handlers()
			@st_selected=[]


		_present_table: ->
			ex11.get_tab_for_user @name, (res) =>
				@TAB.children().remove()
				@TAB.append($(res))
				$("tr").click (e) =>
					cur_row= $(e.currentTarget)
					cur_row.toggleClass("selected")

		_select: ->
			$("tr.selected").each (i,e) =>
				$childs= $(e).children()
				nm= $($childs[2]).text()
				qua= $($childs[3]).text()
				@st_selected.push([nm,qua])
			@st_selected

		_menu_handlers: ->
			$("#menu > button").unbind()
			$("#menu > button").click (e) =>
				switch $(e.target).prop("id")
					when "update"
						ex11.update_price "foo"
						@_present_table()
					when "buyone"
						for sym in @_select()
							ex11.modify {user:@name,stsym:sym[0],plus:true,curqua:sym[1]}
						@_present_table()
					when "sellone"
						for sym in @_select()
							if parseInt(sym[1])>0
								ex11.modify {user:@name,stsym:sym[0],plus:false,curqua:sym[1]} 
						@_present_table()
					when "logout"
						$("#user").children().remove()
						$("div#login").show()
						new Login()
				@st_selected=[]
	class Login
		constructor: ->
			@usern=@passw=@submit=null
			@_present_login()
			@_check_login()
			@submit.click()

		_add_menu: ->
			div= $("<div id='menu'></div>")
			tab= $("<div id='tab'></div>")
			$("#user").append(tab).append(div)
			menu= {
				"update":"Price update"
				"buyone":"Buy one"
				"sellone": "Sell one"
				"logout": "Log out"
			}
			format_menu = (k,v) -> "<button id=#{k}>#{v}</button>"
			($("#menu").append(format_menu(k,v)) for k,v of menu)

		_check_login: ->
			$("#submit").click =>
				usern= @usern.val()
				passw= @passw.val()
				ex11.login {"usern":usern, "passw":passw}, (res) =>
					console.log res,usern
					if res
						$("div#login").hide()
						@usern.remove()
						@passw.remove()
						@submit.remove()
						@_add_menu()
						new User(usern)
					else
						@usern.css("backgroundColor","red")
						@passw.css("backgroundColor","red")

		_present_login: ->
			@usern= $("<input value='Igor' id='usern'/>")
			@passw= $("<input value='Igor' type='password' id='passw'/>")
			@submit= $("<button id='submit'>Submit</button>")
			$("#login").append(@usern).append(@passw).append(@submit)

	new Login()



