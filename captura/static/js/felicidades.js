function obtener_mis_materias() {
	$.ajax({
		url: '/registro/getMisMaterias/',
		datatype:'html',
		type: "GET",
		success: function(data) {
			$('#tabla_materias').html(data);
		}
	});
}
