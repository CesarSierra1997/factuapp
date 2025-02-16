var $ = jQuery.noConflict();

function abrir_modal_creacion(url) {
    jQuery('#creacion').load(url, function () {
        jQuery(this).modal('show');
    });
}

function abrir_modal_edicion(url) {
    jQuery('#edicion').load(url, function () {
        jQuery(this).modal('show');
    });
}

function abrir_modal_eliminacion(url) {
    jQuery('#eliminacion').load(url, function () {
        jQuery(this).modal('show');
    });
}

function cerrar_modal_creacion(){ 
    $('#creacion').modal('hide');
}

function cerrar_modal_edicion(){ 
    $('#edicion').modal('hide');
}

function cerrar_modal_eliminacion(){ 
    $('#eliminacion').modal('hide');
}


function activarBotonCreacion(){
    if($('#boton_creacion').prop('disabled')){
        $('#boton_creacion').prop('disabled',false);
    }else{
        $('#boton_creacion').prop('disabled',true);
    }
}

function activarBotonEdicion(){
    if($('#boton_edicion').prop('disabled')){
        $('#boton_edicion').prop('disabled',false);
    }else{
        $('#boton_edicion').prop('disabled',true);
    }
}

function mostrarErroresCreacion(errores){
    $('#errores').html("");
    let error = "";
    for (let item in errores.responseJSON.error){
        error += '<div class="alert alert-danger">' + errores.responseJSON.error[item] + '</div>';
    }
    $('#errores').append(error);
}

function mostrarErroresEdicion(errores){
    $('#erroresEdicion').html("");
    let error = "";
    for (let item in errores.responseJSON.error){
        error += '<div class="alert alert-danger">' + errores.responseJSON.error[item] + '</div>';
    }
    $('#erroresEdicion').append(error);
}

function notificacionError(mensaje){
    Swal.fire({
        title:'¡Error!',
        text: mensaje,
        icon: 'error'
    })
}

function notificacionSuccess(mensaje){
    Swal.fire({
        title:'Buen trabajo',
        text: mensaje,
        icon: 'success'
    })
}

function notificacionWarning(mensaje){
    Swal.fire({
        title:'Algo no salio bien',
        text: mensaje,
        icon: 'warning'
    })
}

