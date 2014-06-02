$(document).ready(function () {

 
  $('#id_modalidad').change(function () {
    obtener_contenido(this, 'id_modalidad');

    return false;
  });
  
  
  $('#id_ciclo').change(function () {
	  var id_sel= $(this).attr('value');
	  $('#boton_siguiente').attr('class','input_disable_continuar');
	  $('#boton_siguiente').attr('onClick','');
	  obtener_materia(id_sel);
	 

    return false;
  });
  
  
    

   
  
  function obtener_contenido(thisSelect,id_Modalidad) {
    $thisSelect = $(thisSelect);
    var id = $thisSelect.attr('value');
    if (id == '1') {
      $.get('/registro/obtener_carreras/', function (data, textStatus, jqXHR) {
        if (textStatus == 'success') {
			$('#id_carrera').html('')
			$('#id_carrera').append('<option  value="0">Seleccione una opción...</option>');
			
			  for (var dato in data) {
				$('#id_carrera').append('<option value="' + data[dato]["id"]+ '">' + data[dato]["licenciatura"]  +'</option>');
			  }
         }      
        
      }); // $.get(..
    } // if(id != ...
    if (id==2)
    {
		
      $.get('/registro/obtener_educacion_continua/', function (data, textStatus, jqXHR) {
        if (textStatus == 'success') {
			$('#id_carrera').html('')
			$('#id_carrera').append('<option  value="0">Seleccione una opción...</option>');
			
			  for (var dato in data) {
				$('#id_carrera').append('<option value="' + data[dato]["id"]+ '">' + data[dato]["licenciatura"] + '</option>');
			  }//for
		  }//if (textStatus
         });//get
	 
		
	}// fin  id==2

  } // function obtener_(...
  
	 
  function cambio_checkbox(id_materia){
	  alert ("cambio"+id_materia);
  }
  

    return false;
  });

function valida_acceso(){
	$.get('/registro/valida_acceso_materias/', function (data, textStatus, jqXHR) {
		if (textStatus == 'success') {
			
			if(data["acceso"] == 'permitido'){
				$.get('/registro/valida_numero_ordenes/', function (datax, textStatus, jqXHR) {
				if (textStatus == 'success') {
					if(data["acceso"] == 'permitido'){
						valida_inicio();
					}else{
						$('#wrapper_contenido').html('');
						$('#wrapper_contenido').append('<ul>');
						$('#wrapper_contenido').append('<li type="circle">NO PAGAS.</li>');

						$('#wrapper_contenido').append('</ul>');
						$('#wrapper_contenido').append('</ul>');
						
					}		
				}
				});
			}else{
				$('#wrapper_contenido').html('');
				$('#wrapper_contenido').append('<ul>');
				$('#wrapper_contenido').append('<li type="circle">CAS0 1.</li>');
				$('#wrapper_contenido').append('<li type="circle">CAS0 2.</li>');
				$('#wrapper_contenido').append('</ul>');
				
			}
				
		}
	}); // $.get(..
 
}



  
function valida_inicio(){
  
  $.get('/registro/valida_preorden/', function (data, textStatus, jqXHR) {
		if (textStatus == 'success') {
			T=data["valida"];
			if(T>0){
				 vistaModalidad();	
			}
	}
}); // $.get(..
 
}
  


function cambio_checkbox(){
	var seleccionados = $('input:checkbox:checked').length;

	if(seleccionados > 0){
		$('#boton_siguiente').attr('class','input_submit_continuar');
		$('#boton_siguiente').attr('onClick','javascript:validaSiguiente()');
	}else{
		$('#boton_siguiente').attr('class','input_disable_continuar');
		$('#boton_siguiente').attr('onClick','');
		
	}
}

function validaSiguiente(){ 

	var ids="";
	var ciclo_id = $("#id_ciclo").val();
	$('input:checkbox:checked').each(function() {
			a="SEL_"+($(this).val());
			b=$('#'+a).val();
			x=b.split('|');
			ids=ids.concat('|'+x[0]);
	});
	
	$.post('/registro/guardar_materias_ciclo/',{'ciclo_id':ciclo_id,'ids': ids, 'csrfmiddlewaretoken':csrf}, function (data, textStatus, jqXHR) {
        if (textStatus == 'success') {
			location.href="/registro/colegiaturas";
			
		}
	});
	

}


function vistaModalidad(){
	$.get('/registro/obtener_vista_especialidad/', function (data, textStatus, jqXHR) {
			if (textStatus == 'success') {
			//Obteniendo campos ya editados
					$('#centro_contenedor_gde').html('');
					$('#centro_contenedor_gde').append('<div id="select_modalidad"><p class="p_label_datos">Modalidad:</p></div>');
					$('#centro_contenedor_gde').append('<div id="select_licenciatura"><p class="p_label_datos">Nombre del programa:</p></div>');
					
					//$('#select_modalidad').html('');
					$('#select_modalidad').append('<p>'+data["modalidad"]+'</p>');
					$('#select_modalidad').append('<input type="hidden" name="id_modalidad" id="id_modalidad"  value="'+data["id_modalidad"]+'" />');
					//$('#select_licenciatura').html('')
					$('#select_licenciatura').append('<p>'+data["licenciatura"]+'</p>');
					$('#select_licenciatura').append('<input type="hidden" name="id_licenciatura" id="id_licenciatura"  value="'+data["id_licenciatura"]+'" />');
					
			
			//$('#boton_input').html('');
			
			div = document.getElementById('contenedor_flotante');
				div.style.display ='';
				
			obtenerCiclo();
					 
			
		}
	}); // $.get(..
}

function obtenerCiclo(){
	id_default=document.getElementById("id_ciclo").value;
	obtener_materia(id_default);
		/*opc1=document.getElementById("id_modalidad").value;
		csrf=$("input[name=csrfmiddlewaretoken]").val();
		var id_default=0;
		$.get('/registro/obtener_ciclo_especialidad/', function (data, textStatus, jqXHR) {
			if (textStatus == 'success') {
			//Obteniendo cciclos disponibles
			
			
					$.get('/registro/obtener_ciclo_default/', function (data1, textStatus2, jqXHR) {
							var temp=0;
							if (textStatus2 == 'success') {
								id_default=data1["id"];
								//alert(id_default)
							$('#id_ciclo').html('');
							$('#id_ciclo').append('<option  value="0">Seleccione un ciclo...</option>');
							  for (var dato in data) {
								  tem=data[dato]["id"];
								 
								  if(id_default==tem){
									  $('#id_ciclo').append('<option  selected value="' + data[dato]["id"]+ '">' + data[dato]["ciclo"] + ' ('+data[dato]["inicio"]+' - '+data[dato]["fin"]+')</option>');
								  }else{
									  $('#id_ciclo').append('<option value="' + data[dato]["id"]+ '">' + data[dato]["ciclo"] + ' ('+data[dato]["inicio"]+' - '+data[dato]["fin"]+') </option>');
								  }
								
								//8989
							  }//for
							obtener_materia(id_default);
						}
							
					}); // $.get(..
							
			
			div = document.getElementById('contenedor_flotante');
			div.style.display ='';
			
			}
			}); // $.get(..
			*/
}


function validaSeleccion(){
	opc1=document.getElementById("id_modalidad").value;
	
	opc2=document.getElementById("id_carrera").value;
	X=document.getElementById("id_carrera").value;
	X=$("#id_carrera option[value='"+opc2.toString()+"']").text();
	csrf=$("input[name=csrfmiddlewaretoken]").val();
	
	if(opc1< 1)
	{
		alert("Por favor seleccione una modalidad");
	}
	else
	if(opc2< 1){
		alert("Por favor seleccione una especialidad");
	}
	else{
		
		if(opc1 == 1){
			a=confirm("Te estás inscribiendo a la licenciatura "+X+" ¿Estás seguro de continuar?");
		}else{
			a=confirm("Te estás inscribiendo a "+X+" ¿Estás seguro de continuar?");
		}
	
		if(a){
			$.post('/registro/guardar_seleccion_especialidad/', {'A': opc1, 'B':opc2, 'csrfmiddlewaretoken':csrf}, function (data, textStatus, jqXHR) {
			if (textStatus == 'success') {
				
				vistaModalidad();
				obtenerCiclo();

				
			 }
			 else if(textStatus == 'failed'){
				 alert("Error a guardar la licenciatura")
			 }
		
              
        
			}); // $.get(..
		}
		
	}
	
}


function sortNumber(a, b)
{
return a - b;
}


function agregarSeleccionAsignatura(){
	var campo=document.getElementById("asiganturasDisponibles");
	var opciones = campo.length; 
	var x = 0; 
	var n = 0; 
	arr = new Array();
		while(x<opciones){
			if(campo.options[x].selected){ 
				
				arr[n] = campo.options[x].value; 
				alert(campo.options[x].value);
				n++;
			}
			x++;
		}
		
	var sel=document.getElementById("seleccionados").value;
	AS=sel.split(",");
	arr2=AS.concat(arr);
	document.getElementById("seleccionados").value=arr2.sort(sortNumber);
	
	

	$.ajax({
  		type: "POST",
  		url		: "/registro/carga_lista/",
  		data 	: ({
				ids : document.getElementById("seleccionados").value
			}),	
  		dataType: "html",
   		success: function(dataHtml){
			$("#selectMultiple").html(dataHtml);
		}
 	});
	
	
 
} 

function quitarSeleccionAsignatura(){
	var campo=document.getElementById("asignaturasSeleccionadas");
	var opciones = campo.length; 
	var x = 0; 
	var n = 0; 
	arr = new Array();
		while(x<opciones){
			if(campo.options[x].selected){ 
				
				arr[n] = campo.options[x].value; 
				alert(campo.options[x].value);
				n++;
			}
			x++;
		}
	var sel=document.getElementById("seleccionados").value;
	AS=sel.split(",");
	 for(i=0;i<arr.length;i++){
	 }
	document.getElementById("seleccionados").value=AS;
	$.ajax({
  		type: "POST",
  		url		: "/registro/carga_lista/",
  		data 	: ({
				ids : document.getElementById("seleccionados").value
			}),	
  		dataType: "html",
   		success: function(dataHtml){
			$("#selectMultiple").html(dataHtml);
		}
 	});
 
} 


function cambioBimestre(idSelect){
	var sel=document.getElementById("SEL_"+idSelect).value;
	d=sel.split("|");
	id="#precio_"+d[2];
	//$(id).append('');
	$(id).html(d[1]);
	
	
}



  
  function obtener_materia(id_sel) {
	var id=id_sel
	if (id != '0') {
			csrf=$("input[name=csrfmiddlewaretoken]").val();
        $.fancybox.showActivity();
      $.post('/registro/obtener_materias_especialidad/',{'ciclo': id, 'csrfmiddlewaretoken':csrf}, function (data, textStatus, jqXHR) {
        $.fancybox.hideActivity();
        if (textStatus == 'success') {
			
			$.get('/registro/obtener_materias_default/', function (datax, textStatus2, jqXHRx) {
			if (textStatus2 == 'success') { 
			 var index_datax=0;
			 var lt=datax.length;
			 var l=datax[0]["id_materia"];
			 var ix=0;
			 $('#dtable_seleccion_cursos').html('');
      	  	 $('#dtable_seleccion_cursos').append('<table id="table_seleccion_cursos">');
      	  	 $('#table_seleccion_cursos').append('<tr> <th id="th_clave">Clave</th><th id="th_nombre">Nombre</th><th id="th_checkbox">Cursar</th><th id="th_bimestre">Inicio</th><th id="th_costo">Costo</th></tr>');
			 for (var dx in datax) {
				 ix++;
			 }
			
			 for (var dato in data) {
				 var bimestre=data[dato]["bimestre"];
				 var precio='';
				 var chekeado='';
				 var seleccionado='';
				 var i=0;
				 var duracionDefault=false;
				 var precioDefault='';
				 var seleccion='<select class="input_select_datos_ch" id="SEL_'+data[dato]["id"]+'" onChange="javascript:cambioBimestre('+data[dato]["id"]+');" >';
				 
				 cont=0;
				 
				 for (var seccion in bimestre) {
					 seleccionado='';
					 if(cont==0){
						 precio=bimestre[i]["costo"];
						 cont++;
					 }
					 if(l > -1){
						 if(index_datax < ix){
							 if(datax[index_datax]["id_ciclo"]==bimestre[i]["id"]){
								 seleccionado='selected';
								 precio=bimestre[i]["costo"];
							 }
						}
					}
					 
					 seleccion=seleccion.concat('<option '+seleccionado+' value="'+bimestre[i]["id"]+'|'+bimestre[i]["costo"]+'|'+data[dato]["id"]+'"> '+bimestre[i]["inicio"]+'</option>');
					 if(bimestre[i]["duracion"]>3){
						 duracionDefault=true;
						 precioDefault=precio;
					 }
					 i=i+1;
				 }
				 if(duracionDefault)
				 {
					 seleccion='<select class="input_select_datos_ch" disabled=true>';
					 seleccion='<option>1 Bimestre</option>';
					 precio=precioDefault;
				 }
				 seleccion=seleccion.concat("</select>");
				 
				 chekeado='';
				 if(l> -1){
					 if(index_datax < ix){
						 if(datax[index_datax]["id_materia"]==data[dato]["id"] ){
							 chekeado='checked';
							 $('#boton_siguiente').attr('class','input_submit_continuar');
							 $('#boton_siguiente').attr('onClick','javascript:validaSiguiente()');
							 index_datax++;
						 }
					}
					 
				 }
				 //$('#table_seleccion_cursos').append('<tr id="'+data[dato]["id"]+'">');
				 $('#table_seleccion_cursos').append('<tr> <td>'+data[dato]["clave"]+'</td>  <td class="left">'+data[dato]["materia"]+'</td> <td><input type="checkbox" '+chekeado+' value="'+data[dato]["id"]+'" onClick="javascript:cambio_checkbox();" /></td><td>'+seleccion+'</td><td id="precio_'+data[dato]["id"]+'">'+precio+'</td></tr>');

			  }//for
			  $('#dtable_seleccion_cursos').append('</table>');
			  }
			});//get
         }
         
        
      }); // $.post(..
    } // if(id != ...
  }

  

