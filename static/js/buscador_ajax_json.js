function trim(cadena) {
	return cadena.replace(/^\s+|\s+$/g,"");
}
var timer_call = 100;
function resolverConflictos(key_down, selector, sufijo) {
   up_key = 38;
   down_key = 40;
   left_key = 37;
   right_key = 39;
   tab = 9;
   var prohibited_chars = [up_key,down_key, left_key, right_key, tab];
   for(i in prohibited_chars){                                
		   if(key_down.keyCode == prohibited_chars[i])
				   return false;
   }
  
   if(key_down.keyCode == 13) return false;
}
function funcionalidad(key_down, selector, sufijo){
	p_pais = 'input[name="pais'+sufijo+'"]';
	p_entidad = 'input[name="entidad'+sufijo+'"]';
	p_municipio = 'input[name="municipio'+sufijo+'"]';
	p_colonia = 'input[name="colonia'+sufijo+'"]';
	p_ciudad = 'input[name="ciudad'+sufijo+'"]';
	p_cp = 'input[name="cp'+sufijo+'"]';
	if(resolverConflictos(key_down, selector, sufijo) == false) return false;
	
	setTimeout(function(){ajax_codpos(selector,p_pais,p_entidad,p_municipio,p_cp,p_colonia,p_ciudad,key_down);}, timer = timer_call);
}
function getPais(abr) {
	for(i=0; i < resultado_ajax['paises'].length; i++) {
		if(resultado_ajax['paises'][i].abreviatura == abr) return resultado_ajax['paises'][i].nombre;
	}
	return '';
}
function getEntidad(abr, pais) {
	for(i=0; i < resultado_ajax['paises'].length; i++) {
		if(resultado_ajax['paises'][i].nombre == pais) {
			if(resultado_ajax['paises'][i].entidades) {
				for(var j=0; j < resultado_ajax['paises'][i].entidades.length; j++) {
					if(resultado_ajax['paises'][i].entidades[j].abreviatura == abr) return resultado_ajax['paises'][i].entidades[j].nombre;
				}
			}
		}
	}
	return '';
}

function colocarValores(selector, sufijo, event) {
	if(event.keyCode ==13 || event) {
		var tmp=$('input[name="'+selector+sufijo+'"]').val().split('|');
		if(tmp.length > 1) {
			if(selector == 'entidad') {
				$('input[name="pais'+sufijo+'"]').val(getPais(trim(tmp[1])));
				$('input[name="entidad'+sufijo+'"]').val(trim(tmp[0]));
			}
			if(selector == 'municipio') {
				$('input[name="pais'+sufijo+'"]').val(getPais(trim(tmp[2])));
				$('input[name="entidad'+sufijo+'"]').val(getEntidad(trim(tmp[1]), $('input[name="pais'+sufijo+'"]').val()));
				$('input[name="municipio'+sufijo+'"]').val(trim(tmp[0]));
				
			}
			if(selector == 'cp') {
				$('input[name="cp'+sufijo+'"]').val(trim(tmp[0]));
				$('input[name="colonia'+sufijo+'"]').val(trim(tmp[1]));
				if(trim(tmp[2]).substr(0,3) == 'Cd.') {
					$('input[name="ciudad'+sufijo+'"]').val(trim(tmp[2]).substr(4));
					$('input[name="pais'+sufijo+'"]').val(getPais(trim(tmp[5])));
					$('input[name="entidad'+sufijo+'"]').val(getEntidad(trim(tmp[4]), $('input[name="pais'+sufijo+'"]').val()));
					$('input[name="municipio'+sufijo+'"]').val(trim(tmp[3]));
				} else {
					$('input[name="pais'+sufijo+'"]').val(getPais(trim(tmp[4])));
					$('input[name="entidad'+sufijo+'"]').val(getEntidad(trim(tmp[3]), $('input[name="pais'+sufijo+'"]').val()));
					$('input[name="municipio'+sufijo+'"]').val(trim(tmp[2]));
				}
			}
			if(selector == 'colonia') {
				$('input[name="colonia'+sufijo+'"]').val(trim(tmp[0]));
				if(trim(tmp[1]).substr(0,3) == 'Cd.') {
					$('input[name="cp'+sufijo+'"]').val(trim(tmp[5]).substr(5));
					$('input[name="ciudad'+sufijo+'"]').val(trim(tmp[1]).substr(4));
					$('input[name="pais'+sufijo+'"]').val(getPais(trim(tmp[4])));
					$('input[name="entidad'+sufijo+'"]').val(getEntidad(trim(tmp[3]), $('input[name="pais'+sufijo+'"]').val()));
					$('input[name="municipio'+sufijo+'"]').val(trim(tmp[2]));
				} else {
					$('input[name="cp'+sufijo+'"]').val(trim(tmp[4]).substr(5));
					$('input[name="pais'+sufijo+'"]').val(getPais(trim(tmp[3])));
					$('input[name="entidad'+sufijo+'"]').val(getEntidad(trim(tmp[2]), $('input[name="pais'+sufijo+'"]').val()));
					$('input[name="municipio'+sufijo+'"]').val(trim(tmp[1]));
				}
			}
			if(selector == 'ciudad') {
				if(trim(tmp[0]).substr(0,3) == 'Cd.') {
					$('input[name="colonia'+sufijo+'"]').val(trim(tmp[1]));
					$('input[name="cp'+sufijo+'"]').val(trim(tmp[5]).substr(5));
					$('input[name="ciudad'+sufijo+'"]').val(trim(tmp[0]).substr(4));
					$('input[name="pais'+sufijo+'"]').val(getPais(trim(tmp[4])));
					$('input[name="entidad'+sufijo+'"]').val(getEntidad(trim(tmp[3]), $('input[name="pais'+sufijo+'"]').val()));
					$('input[name="municipio'+sufijo+'"]').val(trim(tmp[2]));
				} else {
					/* Nunca debe entrar aqui */
					alert('No ma error');
				}
			}
		}
	}
}
/*
var search_on_cp = 0; // detecta si la busqueda se hizo sobre el input cp
var abr_codigos = new Array();
var abr_colonias = new Array();
var abr_ciudades = new Array();
var abr_municipios = new Array();
var abr_entidades = new Array();
var abr_paises = new Array();
*/

var accentMap = {
"á": "a",
'é': 'e',
"í": "i",
"ó": "o",
"ú": "u",
"ä": "a",
"ë": "e",
"ï": "i",
"ö": "o",
"ü": "u"
};
var normaliza = function( term ) {
	var ret = "";
	for ( var i = 0; i < term.length; i++ ) {
		ret += accentMap[ term.charAt(i) ] || term.charAt(i);
	}
	//alert(ret);
	return ret;
};
/*
function get_cp( cac, municipio, entidad, pais){
	for(var i = 0; i < cac.length; i++){
			var cp = cac[i].codigo;
			var colonia = cac[i].asentamiento;
			var ciudad = cac[i].ciudad;		
			
			ent_name = entidad.nombre;
			ent_abr = entidad.abreviatura;
			ent_results[ent_abr] = ent_name;
			pais_name = pais.nombre;
			pais_abr = pais.abreviatura;
			pais_results[pais_abr] = pais_name;
			
			if(ciudad != null){
				if(search_on_cp == 1){ // si la busqueda fue sobre input cp
					abr_codigos.push(cp+' | '+colonia+' | '+'Cd. '+ciudad+' | '+municipio.nombre+' | '+entidad.abreviatura+' | '+pais.abreviatura);
				}
				else{ // si la busqueda fue sobre input asentamiento
					abr_colonias.push(colonia+' | '+'Cd. '+ciudad+' | '+municipio.nombre+' | '+entidad.abreviatura+' | '+pais.abreviatura+' | '+'C.P. '+cac[i].codigo);
				}
			}
			else{
				if(search_on_cp == 1){ // si la busqueda fue sobre input cp
					abr_codigos.push(cp+' | '+colonia+' | '+municipio.nombre+' | '+entidad.abreviatura+' | '+pais.abreviatura);
				}
				else{ // si la busqueda fue sobre input asentamiento
					abr_colonias.push(colonia+' | '+municipio.nombre+' | '+entidad.abreviatura+' | '+pais.abreviatura+' | '+'C.P. '+cac[i].codigo);
				}
			}
		}
}

function get_ciudad(ciudad, municipio, entidad, pais){
	for(i = 0; i < ciudad.length; i++){
		var cac = ciudad[i].elementosCAC;
		var ciudad_nombre = ciudad[i].nombre;
		for(j = 0; j < cac.length; j++){
			var colonia = cac[j].asentamiento;
			var cp = cac[j].codigo;
			
			ent_name = entidad.nombre;
			ent_abr = entidad.abreviatura;
			ent_results[ent_abr] = ent_name;
			pais_name = pais.nombre;
			pais_abr = pais.abreviatura;
			pais_results[pais_abr] = pais_name;
			abr_ciudades.push('Cd. '+ciudad_nombre+' | '+colonia+' | '+municipio.nombre+' | '+entidad.abreviatura+' | '+pais.abreviatura+' | '+'C.P. '+cp);
		} 
	}
}

function get_municipio(municipios, entidad, pais){
	for(var i = 0; i < municipios.length; i++){
		var cac = municipios[i].elementosCAC;
		var ciudad = municipios[i].elementosCiudad;	
		
		if(cac != null){
			get_cp(cac, municipios[i], entidad, pais);
		}
		
		if(ciudad != null){
			// results de ciudad
			get_ciudad(ciudad, municipios[i], entidad, pais);
		}
		ent_name = entidad.nombre;
		ent_abr = entidad.abreviatura;
		ent_results[ent_abr] = ent_name;
		pais_name = pais.nombre;
		pais_abr = pais.abreviatura;
		pais_results[pais_abr] = pais_name;
		abr_municipios.push(municipios[i].nombre+' | '+entidad.abreviatura+' | '+pais.abreviatura);
	}
}

function get_entidad( entidades, pais ){
	for(var i = 0; i < entidades.length; i++){
		var municipio = entidades[i].municipios;
		if(municipio != null){	
			get_municipio(municipio, entidades[i], pais);
		}
		ent_name = entidades[i].nombre;
		ent_abr = entidades[i].abreviatura;
		ent_results[ent_abr] = ent_name;
		pais_name = pais.nombre;
		pais_abr = pais.abreviatura;
		pais_results[pais_abr] = pais_name;		
		abr_entidades.push(entidades[i].nombre+' | '+pais.abreviatura); 
	}	
}

function json_codpos_results_anterior( json ){
	ent_results = [];
	pais_results = [];
	var pais = json.paises;
	// si existe pais
	if(pais != null){
		for(var i = 0; i<pais.length; i++){
			var entidad = pais[i].entidades			
			// si existe entidad
			if(entidad != null){
				//obtiene entidad y pais
				get_entidad(entidad, pais[i]);
			}
			abr_paises.push(pais[i].nombre);		
		}
		if(abr_colonias != '')
			return abr_colonias;
		if(abr_codigos != '')
			return abr_codigos;
		if(abr_ciudades != '')
			return abr_ciudades;			
		if(abr_municipios != '')
			return abr_municipios;
		if(abr_entidades != '')
			return abr_entidades;
		if(abr_paises != '')
			return abr_paises;
	}
}
* */
var resultado_ajax=[];
function json_codpos_results( json, selector ){
	sugerencias=[];
	resultado_ajax=json;
	if(selector.search('pais') >= 0) {
		if(json['paises']) {
			for(var i=0; i < json['paises'].length; i++){
				sugerencias.push(json['paises'][i].nombre);
			}
		}
	}
	if(selector.search('entidad') >= 0) {
		if(json['paises']) {
			for(var i=0; i < json['paises'].length; i++) {
				if(json['paises'][i].entidades){
					for(var j=0; j < json['paises'][i].entidades.length; j++) {
						sugerencias.push(json['paises'][i].entidades[j].nombre + ' | ' + json['paises'][i].abreviatura);
					}
				}	
			}
		}
	}
	if(selector.search('municipio') >= 0) {
		if(json['paises']) {
			for(var i=0; i < json['paises'].length; i++) {
				if(json['paises'][i].entidades){
					for(var j=0; j < json['paises'][i].entidades.length; j++) {
						if(json['paises'][i].entidades[j].municipios){
							for(var k=0; k < json['paises'][i].entidades[j].municipios.length; k++) {
								sugerencias.push(json['paises'][i].entidades[j].municipios[k].nombre 
									+ ' | ' + json['paises'][i].entidades[j].abreviatura
									+ ' | ' + json['paises'][i].abreviatura
								);
							}
						}
					}
				}
			}
		}
	}
	if(selector.search('cp') >= 0) {
		if(json['paises']) {
			for(var i=0; i < json['paises'].length; i++) {
				if(json['paises'][i].entidades){
					for(var j=0; j < json['paises'][i].entidades.length; j++) {
						if(json['paises'][i].entidades[j].municipios){
							for(var k=0; k < json['paises'][i].entidades[j].municipios.length; k++) {
								if(json['paises'][i].entidades[j].municipios[k].elementosCAC){
									for(var l=0; l < json['paises'][i].entidades[j].municipios[k].elementosCAC.length; l++) {
										if(json['paises'][i].entidades[j].municipios[k].elementosCAC[l].ciudad) {
											sugerencias.push(json['paises'][i].entidades[j].municipios[k].elementosCAC[l].codigo
												+ ' | ' + json['paises'][i].entidades[j].municipios[k].elementosCAC[l].asentamiento
												+ ' | Cd. ' + json['paises'][i].entidades[j].municipios[k].elementosCAC[l].ciudad
												+ ' | ' + json['paises'][i].entidades[j].municipios[k].nombre 
												+ ' | ' + json['paises'][i].entidades[j].abreviatura
												+ ' | ' + json['paises'][i].abreviatura
											);
										} else {
											sugerencias.push(json['paises'][i].entidades[j].municipios[k].elementosCAC[l].codigo
												+ ' | ' + json['paises'][i].entidades[j].municipios[k].elementosCAC[l].asentamiento
												+ ' | ' + json['paises'][i].entidades[j].municipios[k].nombre 
												+ ' | ' + json['paises'][i].entidades[j].abreviatura
												+ ' | ' + json['paises'][i].abreviatura
											);
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
	if(selector.search('colonia') >= 0) {
		if(json['paises']) {
			for(var i=0; i < json['paises'].length; i++) {
				if(json['paises'][i].entidades){
					for(var j=0; j < json['paises'][i].entidades.length; j++) {
						if(json['paises'][i].entidades[j].municipios){
							for(var k=0; k < json['paises'][i].entidades[j].municipios.length; k++) {
								if(json['paises'][i].entidades[j].municipios[k].elementosCAC){
									for(var l=0; l < json['paises'][i].entidades[j].municipios[k].elementosCAC.length; l++) {
										if(json['paises'][i].entidades[j].municipios[k].elementosCAC[l].ciudad) {
											sugerencias.push(json['paises'][i].entidades[j].municipios[k].elementosCAC[l].asentamiento
												+ ' | Cd. ' + json['paises'][i].entidades[j].municipios[k].elementosCAC[l].ciudad
												+ ' | ' + json['paises'][i].entidades[j].municipios[k].nombre 
												+ ' | ' + json['paises'][i].entidades[j].abreviatura
												+ ' | ' + json['paises'][i].abreviatura
												+ ' | C.P. ' + json['paises'][i].entidades[j].municipios[k].elementosCAC[l].codigo
											);
										} else {
											sugerencias.push(json['paises'][i].entidades[j].municipios[k].elementosCAC[l].asentamiento
												+ ' | ' + json['paises'][i].entidades[j].municipios[k].nombre 
												+ ' | ' + json['paises'][i].entidades[j].abreviatura
												+ ' | ' + json['paises'][i].abreviatura
												+ ' | C.P. ' + json['paises'][i].entidades[j].municipios[k].elementosCAC[l].codigo
											);
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
	if(selector.search('ciudad') >= 0) {
		if(json['paises']) {
			for(var i=0; i < json['paises'].length; i++) {
				if(json['paises'][i].entidades){
					for(var j=0; j < json['paises'][i].entidades.length; j++) {
						if(json['paises'][i].entidades[j].municipios){
							for(var k=0; k < json['paises'][i].entidades[j].municipios.length; k++) {
								if(json['paises'][i].entidades[j].municipios[k].elementosCiudad){
									for(var l=0; l < json['paises'][i].entidades[j].municipios[k].elementosCiudad.length; l++) {
										if(json['paises'][i].entidades[j].municipios[k].elementosCiudad[l].elementosCAC) {
											for(var m=0; m < json['paises'][i].entidades[j].municipios[k].elementosCiudad[l].elementosCAC.length; m++) {
												if(json['paises'][i].entidades[j].municipios[k].elementosCiudad[l].elementosCAC[m].ciudad) {
													sugerencias.push('Cd. ' + json['paises'][i].entidades[j].municipios[k].elementosCiudad[l].elementosCAC[m].ciudad
														+ ' | ' + json['paises'][i].entidades[j].municipios[k].elementosCiudad[l].elementosCAC[m].asentamiento
														+ ' | ' + json['paises'][i].entidades[j].municipios[k].nombre 
														+ ' | ' + json['paises'][i].entidades[j].abreviatura
														+ ' | ' + json['paises'][i].abreviatura
														+ ' | C.P. ' + json['paises'][i].entidades[j].municipios[k].elementosCiudad[l].elementosCAC[m].codigo
													);
												} else {
													/* Nunca debe entrar aqui */
													alert('No ma error');
												}
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
	return sugerencias;
}

function ajax_codpos(selector, p_pais, p_entidad,p_municipio,p_cp,p_colonia,p_ciudad){
	var get_pais = $(p_pais).val();		
	var get_entidad = $(p_entidad).val();
	var get_municipio = $(p_municipio).val();
	var get_cp = $(p_cp).val();
	var get_colonia = $(p_colonia).val();
	var get_ciudad = $(p_ciudad).val();

	if(!get_entidad){
		get_entidad = "";
	}	
	if(!get_municipio){
		get_municipio = "";
	}	
	if(!get_cp){
		get_cp = "";
	}	
	if(!get_colonia){
		get_colonia = "";
	}	
	if(!get_ciudad){
		get_ciudad = "";
	}	


	var long_cadena = 0;

	//var long = 0;

	search_on_cp = 0;
	abr_paises = [];
	abr_entidades = [];
	abr_municipios = [];
	abr_ciudades = [];
	abr_codigos = [];
	abr_colonias = [];

	if(selector == p_cp)
		search_on_cp = 1;	
	if(selector.search(p_pais))
		long_cadena = 2;
	if(selector.search(p_entidad))
		long_cadena = 2;
	if(selector.search(p_municipio))
		long_cadena = 3;
	if(selector.search(p_cp))
		long_cadena = 3;
	if(selector.search(p_colonia))
		long_cadena = 3;
	if(selector.search(p_ciudad))
		long_cadena = 3;
	
	// proceso ajax
	var url = "http://services.scalaproject.com:8080/sugerencia/autocompleta/jsonp/get/?pais="+get_pais+"&entidad="+get_entidad+"&municipio="+get_municipio+"&codigopostal="+get_cp+"&asentamiento="+get_colonia+"&ciudad="+get_ciudad+"&callback=?";
	if($(selector).val().length >= long_cadena){ 
		$.ajax({			
			type: "GET",
			url: url,	
			//async: false,
			jsonpCallback: 'jsonCallback',
			contentType: "application/x-javascript",
			dataType: 'jsonp',
			success: function(json){					
				available_tags = json_codpos_results( json, selector );	
				$(selector).autocomplete({
					source: function( request, response ) {
						var matcher = new RegExp( $.ui.autocomplete.escapeRegex( request.term ), 'i' );
						response( $.grep( available_tags, function( value ) {
									return matcher.test(  value  ) || matcher.test( normaliza( value ) );
						}) );
	    			},
					max : 10,
				});							
			}
		});
	} // fin proceso ajax
}

function jsonCallback() {
	nada=0;
}
