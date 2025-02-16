var $ = jQuery.noConflict();

function registrar() {
    activarBotonCreacion();
    $.ajax({
        data: $('#form_creacion').serialize(),
        url: $('#form_creacion').attr('action'),
        type: $('#form_creacion').attr('method'),
        success: function (response) {
            notificacionSuccess(response.mensaje);
            cerrar_modal_creacion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresCreacion(error);
            activarBotonCreacion();
        }
    });
}

function editar() {
    activarBotonEdicion();
    $.ajax({
        data: $('#form_edicion').serialize(),
        url: $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'),
        success: function (response) {
            notificacionSuccess(response.mensaje);
            cerrar_modal_edicion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresEdicion(error);
            activarBotonEdicion();
        }
    });
}

function eliminar(pk) {
    $.ajax({
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
        },
        url: '/usuario/eliminar_usuario/' + pk + '/',
        type: 'post',
        success: function (response) {
            notificacionSuccess(response.mensaje);
            cerrar_modal_eliminacion();
            console.log("menjsae del servidor", response);
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            console.log(error);

        }
    });

}

