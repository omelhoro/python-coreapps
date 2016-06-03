dgi=  (t)-> document.getElementById(t)
dgi1= (t) -> document.getElementById(t)
dgt=  (t) -> document.getElementsByTagName(t)
dgn= (t) -> document.getElementsByName(t)
ctn= (t)-> document.createTextNode(t)

check = -> 
	e= dgi('name')
	errp= dgi('inputErrors')
	howmanys= dgn("howmany")
	res= (el for el in howmanys when el.checked==true)
	namelen= e.value.trim().length
	form = dgt("form")[0]
	errp.textContent= ""
	switch [res.length == 0,namelen==0].join()
		when "true,true"
			txt = ctn(" No name given and no friends selected!"); 
			errp.appendChild(txt)
		when "true,false"
			txt = ctn(" No friends selected!"); 
			errp.appendChild(txt)
		when "false,true"
			txt = ctn(" No name given!"); 
			errp.appendChild(txt)
		when "false,false" then form.submit()

