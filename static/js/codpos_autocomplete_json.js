function codpos_autocomplete_json(){
	$('input[name="pais"]').keydown(function(e){
		funcionalidad(e, 'input[name="pais"]', '');
	});
	
	$( 'input[name="pais"]' ).autocomplete({
		source: [],
		messages: {
			noResults: '', 
			results: function(){},
		}, // elimina mensaje de ayuda "results" 		
		close: function( event, ui ) {
			$('input[name="pais"]').val($('input[name="pais"]').val().trim()); 
		}
	});
		
	// name = 'entidad'
	$('input[name="entidad"]').keydown(function(e){
		funcionalidad(e, 'input[name="entidad"]', '');
	});
	
	$( 'input[name="entidad"]').autocomplete({
		source: [],
		messages: {
			noResults: '', 
			results: function(){},
		}, // elimina mensaje de ayuda "results" 
		close: function( event, ui ) {
			colocarValores('entidad', '_datos_personales', event);
			/*
			if(event.keyCode ==13 || event){
				var tmp_ent=$('input[name="entidad"]').val().split(' | ');
				if(tmp_ent.length > 1){
					for(var index in ent_results) {
						if(tmp_ent[0] == index)
							tmp_ent[0] = ent_results[index];
					}
					for(var index in pais_results) {
						if(tmp_ent[1] == index)
							tmp_ent[1] = pais_results[index];
					}
					if(tmp_ent[0]) {
						$('input[name="entidad"]').val(tmp_ent[0].trim());
						$('input[name="pais"]').val(tmp_ent[1].trim());
					}
				}
			}		*/
		}
	});
		
	// name = 'municipio'
	$('input[name="municipio"]').keydown(function(e){
		funcionalidad(e, 'input[name="municipio"]', '');
	});
	
	$( 'input[name="municipio"]' ).autocomplete({
		source: [],
		messages: {
			noResults: '', 
			results: function(){},
		}, // elimina mensaje de ayuda "results" 
		close: function( event, ui ) {
			colocarValores('municipio', '', event);
			/*
			if(event.keyCode ==13 || event){
				var tmp_mpio = $('input[name="municipio"]').val().split(' | ');
				if(tmp_mpio.length > 1) {
					for(var index in ent_results) {
						if(tmp_mpio[1] == index)
							tmp_mpio[1] = ent_results[index];
					}
					for(var index in pais_results) {
						if(tmp_mpio[2] == index)
							tmp_mpio[2] = pais_results[index];
					}
					if(tmp_mpio[0]) {
						$('input[name="municipio"]').val(tmp_mpio[0].trim());
						$('input[name="entidad"]').val(tmp_mpio[1].trim());
						$('input[name="pais"]').val(tmp_mpio[2].trim());
					}
				}
			}	*/
		}
	});
		
	// name = 'cp'
	$('input[name="cp"]').keydown(function(e){
		funcionalidad(e, 'input[name="cp"]', '');
	});

	$( 'input[name="cp"]' ).autocomplete({
		source: [],
		messages: {
			noResults: '', 
			results: function(){},
		}, // elimina mensaje de ayuda "results" 
		close: function( event, ui ) {
			colocarValores('cp', '', event);
			/*
			if(event.keyCode ==13 || event){	
				var tmp_cp=$('input[name="cp"]').val().split(' | ');				
				if(tmp_cp.length > 1) {
					$('input[name="cp"]').val(tmp_cp[0].trim());
					$('input[name="colonia"]').val(tmp_cp[1].trim());
					if(tmp_cp[2] && tmp_cp[2].substr(0,3) == 'Cd.') {
						for(var index in ent_results) {
							if(tmp_cp[4] == index)
								tmp_cp[4] = ent_results[index];
						}
						for(var index in pais_results) {
							if(tmp_cp[5] == index)
								tmp_cp[5] = pais_results[index];
						}
						
						$('input[name="ciudad"]').val(tmp_cp[2].substr(4).trim());
						$('input[name="municipio"]').val(tmp_cp[3].trim());
						$('input[name="entidad"]').val(tmp_cp[4].trim());
						$('input[name="pais"]').val(tmp_cp[5].trim());
						
					}
					else{
						for(var index in ent_results) {
							if(tmp_cp[3] == index)
								tmp_cp[3] = ent_results[index];
						}
						for(var index in pais_results) {
							if(tmp_cp[4] == index)
								tmp_cp[4] = pais_results[index];
						}
						$('input[name="ciudad"]').val('');
						$('input[name="municipio"]').val(tmp_cp[2].trim());
						$('input[name="entidad"]').val(tmp_cp[3].trim());
						$('input[name="pais"]').val(tmp_cp[4].trim());
					}
				}
			}*/		
		}
	});
		
	// name = 'colonia'
	$('input[name="colonia"]').keydown(function(e){
		funcionalidad(e, 'input[name="colonia"]', '');
	});
	
	$( 'input[name="colonia"]' ).autocomplete({
		messages: {
			noResults: '', 
			results: function(){},
		}, // elimina mensaje de ayuda "results" 
		close: function( event, ui ) {
			if(event.keyCode ==13 || event){
				colocarValores('colonia', '', event);
				/*
				var tmp_colonia=$('input[name="colonia"]').val().split(' | ');
				if(tmp_colonia.length > 1) {
					if(tmp_colonia[0]) {
						$('input[name="colonia"]').val(tmp_colonia[0].trim());					
					}
					if(tmp_colonia[1] && tmp_colonia[1].substr(0,3) == 'Cd.') {
						for(var index in ent_results) {
							if(tmp_colonia[3] == index)
								tmp_colonia[3] = ent_results[index];
						}
						for(var index in pais_results) {
							if(tmp_colonia[4] == index)
								tmp_colonia[4] = pais_results[index];
						}
						
						$('input[name="ciudad"]').val(tmp_colonia[1].substr(4).trim());
						$('input[name="municipio"]').val(tmp_colonia[2].trim());
						$('input[name="entidad"]').val(tmp_colonia[3].trim());
						$('input[name="pais"]').val(tmp_colonia[4].trim());				
						$('input[name="cp"]').val(tmp_colonia[5].substr(5).trim());
					}
					else{
						for(var index in ent_results) {
							if(tmp_colonia[2] == index)
								tmp_colonia[2] = ent_results[index];
						}
						for(var index in pais_results) {
							if(tmp_colonia[3] == index)
								tmp_colonia[3] = pais_results[index];
						}
						
						$('input[name="municipio"]').val(tmp_colonia[1].trim());
						$('input[name="entidad"]').val(tmp_colonia[2].trim());
						$('input[name="pais"]').val(tmp_colonia[3].trim());				
						$('input[name="cp"]').val(tmp_colonia[4].substr(5).trim());
					}
				}*/
			}				
		}
	});
		
	// name = 'ciudad'
	$('input[name="ciudad"]').keydown(function(e){
		funcionalidad(e, 'input[name="ciudad"]', '');
	});

	$( 'input[name="ciudad"]' ).autocomplete({
		source: [],
		messages: {
			noResults: '', 
			results: function(){},
		}, // elimina mensaje de ayuda "results" 
		close: function( event, ui ) {
			colocarValores('ciudad', '', event);
			/*
			if(event.keyCode ==13 || event){
				var tmp_ciudad=$('input[name="ciudad"]').val().split(' | ');
				if(tmp_ciudad.length > 1) {
					for(var index in ent_results) {
						if(tmp_ciudad[3] == index)
							tmp_ciudad[3] = ent_results[index];
					}
					for(var index in pais_results) {
						if(tmp_ciudad[4] == index)
							tmp_ciudad[4] = pais_results[index];
					}
					if(tmp_ciudad[0]) { 
						$('input[name="ciudad"]').val(tmp_ciudad[0].substr(4).trim());
						$('input[name="colonia"]').val(tmp_ciudad[1].trim());
						$('input[name="municipio"]').val(tmp_ciudad[2].trim());
						$('input[name="entidad"]').val(tmp_ciudad[3].trim());
						$('input[name="pais"]').val(tmp_ciudad[4].trim());
						$('input[name="cp"]').val(tmp_ciudad[5].substr(5).trim());
					}
				}
			}*/
		}
	});	
} // fin codpos_autocomplete_json()
