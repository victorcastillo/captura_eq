function simulador(){
	$.ajax({
		url: '/registro/simulador/',
		datatype:'html',
		type: "POST",
		success: function(data) {
			$.fancybox(data);
		}
	});
}

/*
function proceso_inscripcion(){
	$.ajax({
		url: '/registro/proceso/inscripcion/',
		datatype:'html',
		type: "POST",
		success: function(data) {
			$.fancybox(data);
		}
	});
}
*/

function curp(){
	var iframe='<iframe src="http://consultas.curp.gob.mx/CurpSP/" width="500" height="400"></iframe>';
	$.fancybox(iframe);
}

/*
function recuperarPassword(){
	$.ajax({
		url: '/registro/password/reset/',
		data:({ 
			'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
		}),
		datatype:'html',
		type: "POST",
		success: function(data) {
			$.fancybox(data);
			$('#errores').hide();
		}
	});
}

function getInfoTipoIngreso(id) {
	$.ajax({
		url: '/registro/mostrar_tipo_ingreso/',
		datatype:'html',
		type: "POST",
		data:({ 
			csrfmiddlewaretoken : $("input[name=csrfmiddlewaretoken]").val(),
			'tipo_ingreso_id' : id
		}),
		beforeSend: function() {
			$.fancybox.showActivity();
		},
		success: function(data) {
			$.fancybox.hideActivity();
			$.fancybox(data);
		}
	});
}

function getReglamento(modalidad_id) {
	$.ajax({
		url: '/registro/mostrar_reglamento/',
		datatype:'html',
		type: "POST",
		data:({ 
			csrfmiddlewaretoken : $("input[name=csrfmiddlewaretoken]").val(),
			'modalidad_id' : modalidad_id
		}),
		beforeSend: function() {
			$.fancybox.showActivity();
		},
		success: function(data) {
			$.fancybox.hideActivity();
			$.fancybox(data);
		}
	});
}

function enviarPassword(){
	var email = $('form[name=formPassword] #id_email').val();
	$('#inputResetPassword').hide();
	$.ajax({
		url: '/registro/password/reset/',
		data:({ 
			csrfmiddlewaretoken : $("input[name=csrfmiddlewaretoken]").val(),
			email : email
		}),
		datatype:'html',
		type: "POST",
		success: function(data) {
			$.fancybox(data);
		}
	});
}
*/
