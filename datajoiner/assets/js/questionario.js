
"use strict";

$(function(){
    //http://stackoverflow.com/questions/7862233/twitter-bootstrap-tabs-go-to-specific-tab-on-page-reload
    // Javascript to enable link to tab

    var hasErrors = false;
    for(var key in formErrors){
        if(fieldsToTabs[key]){
            console.log("rrr", key, fieldsToTabs[key]);
            $('.nav-tabs a[href='+fieldsToTabs[key]+']').tab('show');
            hasErrors = true;
            break;    
        }
    }

    if(!hasErrors){
        for(var key in inlineErrors){
            $('.nav-tabs a[href=#spostamenti-evitati]').tab('show');
            hasErrors = true;
            break;    
        }
    }
    

    if(!hasErrors){
        var url = document.location.toString();
        if (url.match('#')) {
            $('.nav-tabs a[href=#'+url.split('#')[1]+']').tab('show');
        } else{
            $('.nav-tabs a:first').tab('show') ;
        }
        $('html, body').scrollTop(0);
    }
    $(".tab-content").removeClass("hide");



    // Change hash for page-reload
    $('.nav-tabs a').on('shown.bs.tab', function (e) {
      window.location.hash = e.target.hash;
      $('html, body').scrollTop(0)
    });

    //var loadedMovements = {{ form.instance.spostamento_set|length }};
    //console.log("xx", loadedMovements);
    window.showAnother = function(){
        var sel = $(".hide");
        if(sel.length){
            $(sel[0]).removeClass('hide');
        }
    }


    var bindChoicesAltro = function(driverSelector, drivenSelector, drivenContainer, options){
        var options = options || {};
        //qualifica altro
        $(driverSelector).on('change', function(evt){
            var value = $(this).val();
            value = value || '';
            if(value.toLowerCase() == 'altro'){
                $(drivenContainer).removeClass('hide');
            } else {
                $(drivenContainer).addClass('hide');
                if(options.reset){
                    $(drivenSelector).val('');    
                }
            }
        });

        if(options.initialCheck){
            $(driverSelector).trigger('change');
        }
    };


    //bindings
    bindChoicesAltro(
        '#id_qualifica',
        '#id_qualifica_altro',
        '#id_qualifica_altro_container',
        { 
            reset : false,
            initialCheck : true
        }
    );

    //bindings
    bindChoicesAltro(
        '#id_luogo_lavoro',
        '#id_luogo_lavoro_altro',
        '#id_luogo_lavoro_altro_container',
        { 
            reset : false,
            initialCheck : true
        }
    );

    //bindings
    bindChoicesAltro(
        '#id_attivita_alternativa',
        '#id_attivita_alternativa_altro',
        '#id_attivita_alternativa_altro_container',
        { 
            reset : false,
            initialCheck : true
        }
    );



    
    
    


});