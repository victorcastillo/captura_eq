/*
function subirDocumento(id_documento, usuario_id, licenciatura_id) {
  $.post("/registro/subir_documento/", {
    id_documento: id_documento,
    usuario_id: usuario_id,
    licenciatura_id: licenciatura_id
  }, function(html) {
    $.fancybox(html,{
      onClosed:function() {
        window.location = '/documentos/';
      }
    });
  });
}

function listadoArchivosDocumento( nombreContenedor ){
	$("#listadoArchivos").html('Recuperando listado de archivos.');
	$.post("/registro/htmlListadoArchivosDocumento/", { nombreContenedor : nombreContenedor },
	function(html) {
		$("#listadoArchivos").html(html);
	});
}

function descargar( posicion ){
	var nombreContenedor  = $("#nombreContenedor").val();
	$.post("/registro/descargar/", { nombreContenedor : nombreContenedor , posicion : posicion },
	function( url ) {
		window.location = url ;
	});
}

function listadoArchivosDocumentoDescarga(){
	var nombreContenedor  = $("#nombreContenedor").val();
	$("#listadoArchivos").html('Recuperando listado de archivos.');
	$.post("/registro/htmlListadoArchivosDescarga/", { nombreContenedor : nombreContenedor },
	function(html) {
		$("#listadoArchivos").html(html);
	});
}

function eliminar( posicionObjeto ){
	var nombreContenedor  = $("#nombreContenedor").val();
	$("#listadoArchivos").html('Eliminando archivo.');
	$.post("/registro/eliminarArchivoNube/", { nombreContenedor : nombreContenedor , posicionObjeto : posicionObjeto },
	function(html) {
		listadoArchivosDocumento( nombreContenedor );
	});
}

function descargarDocumento(usuario_id,id_documento){
	$.ajax({
		url: '/registro/url_archivo_nube/',
		data:({ 
				id_documento : id_documento,
				usuario_id   : usuario_id,
				csrfmiddlewaretoken : $("input[name=csrfmiddlewaretoken]").val()
			}),
		datatype:'html',
		type: "POST",
		success: function(data) {
			$("#descargarDocumento").html(data);
		}
	});
}
*/

function retroalimentacionDocumento( id_documento ){
	if( id_documento != undefined ){
		$.ajax({
			url: '/registro/ajax_retroalimentacion_documento/',
			data:({ 
					id_documento : id_documento 
				}),
			datatype:'html',
			type: "POST",
			success: function(data) {
				if( data != ' ' || data != null ){
					$.fancybox(data);
				}
			}
		});
	}
}

/*
function historialDocumento(id_documento,documentacion_usuario){
	$.ajax({
		url: '/registro/historial_documento/',
		data:({ 
				id_documento : id_documento ,
				documentacion_usuario : documentacion_usuario
			}),
		datatype:'html',
		type: "POST",
		success: function(data) {
			$.fancybox(data);
		}
	});
}

function subir(){
	var archivo_documento = $("#archivo_documento").val();
	var id_documento 	  = $("#id_documento").val();
	var licenciatura_id 	  = $("#licenciatura_id").val();
	var observaciones     = $("#observaciones").val();
	var nombreContenedor  = $("#nombreContenedor").val();
	if(archivo_documento!=""){
		$("#listadoArchivos").html('Subiendo archivo.');
		$("#archivo_documento").hide();
		$.ajaxFileUpload
		(
			{
				url:'/registro/archivo_nube/',
				secureuri:false,
				fileElementId:'archivo_documento',
				dataType: 'json',
				data:{
						id_documento:id_documento,
						observaciones:observaciones,
                                                licenciatura_id:licenciatura_id
					},
				success: function (data, status)
				{
					if(data.exito == 1){
						listadoArchivosDocumento( nombreContenedor );
						$("#archivo_documento").attr('value','');
						$("#archivo_documento").show();
					}else{
						//alert(data.error);
						window.location = '/documentos/';
					}
				},
				error: function (data, status, e)
				{
					$.fancybox.close();
				}
			}
		);
	}else{
		alert('Seleccione un archivo.');
	}
}
*/

function terminar(){
	var id_documento = $("#id_documento").val();
	window.location = "/documentos/?documento="+id_documento.toString();
}
