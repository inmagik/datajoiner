if (!Array.prototype.indexOf) {
    Array.prototype.indexOf = function (elt /*, from*/) {
        var len = this.length >>> 0;
        var from = Number(arguments[1]) || 0;
        from = (from < 0) ? Math.ceil(from) : Math.floor(from);
        if (from < 0) from += len;

        for (; from < len; from++) {
            if (from in this && this[from] === elt) return from;
        }
        return -1;
    };
}

 

var questionario = {};
window.questionario = questionario;


questionario.showAnother = function(){
        var sel = $(".spostamento.hide:first");
        if(sel.length){
            sel.removeClass('hide');
        }
    };

questionario.bindVisibleField = function(driverSelector, drivenSelector, drivenContainer, options){
        
        var options = options || {};
        var showValue = options.showValue || 'altro';
        $(driverSelector).on('change', function(evt){
            
            var value = $(this).val();
            value = value || '';
            if(value.toLowerCase() == showValue){
                $(drivenContainer).removeClass('hide');
            } else {
                $(drivenContainer).addClass('hide');
                if(options.reset && drivenSelector){
                    if(drivenSelector.length){
                        for(var i=0,n=drivenSelector.length;i<n;i++){
                            $(drivenSelector[i]).val('');            
                        }
                    } else {
                        $(drivenSelector).val('');        
                    }
                }
            }
        });

        if(options.initialCheck){
            $(driverSelector).trigger('change');
        }
    };


questionario.bindDisabledField = function(driverSelector, drivenSelector, options){
        var options = options || {};
        var showValue = options.showValue || 'altro';
        $(driverSelector).on('change', function(evt){
            var value = $(this).val();
            value = value || '';

            var condition = (value.toLowerCase() == showValue);
            if(options.exclude){
                condition = !condition;
            }

            if(condition){
                if(drivenSelector.length){
                    for(var i=0,n=drivenSelector.length;i<n;i++){
                        $(drivenSelector[i]).prop('disabled', false);            
                    }
                } else {
                    $(drivenSelector).prop('disabled', false);            
                }
                
            } else {
                if(drivenSelector.length){
                    for(var i=0,n=drivenSelector.length;i<n;i++){
                        $(drivenSelector[i]).prop('disabled', true);            
                    }
                } else {
                    $(drivenSelector).prop('disabled', true);            
                }
            }
            
        });

        if(options.initialCheck){
            $(driverSelector).trigger('change');
        }
    };


questionario.chainSelects = function(driverSelect, drivenSelect, lookupDictionary, options){

    var originalOptions =  $(drivenSelect + " option").clone();
    var options = options || {};

    $(driverSelect).on('change', function(){
        var val = $(this).val();
        var allowedValues = lookupDictionary[val] || [];
        $(drivenSelect).empty();

        originalOptions.each(function(idx){
            var t = $(this);
            var value = parseInt(t.val());
            var condition = (allowedValues.indexOf(value) != -1);
            if(options.keepEmpty){
                condition = condition || !value;
            }
            if(condition){
                $(drivenSelect).append(t)
            } else {
                
            }
            
        });

        $(drivenSelect).change();

    });

    if(options.initialCheck){
        $(driverSelect).trigger('change');
    }


};


questionario.ajaxSelect = function(driverSelect, drivenSelect, optionsUrl, options){

    var options = options || {};

    $(driverSelect).on('change', function(){
        var val = $(this).val();
        var currentValue = $(drivenSelect).val();
        //$(drivenSelect).val('');
        
        var url = optionsUrl + val;
        if(val){
            $.ajax({
                url : url,
                success : function(data){

                    var d = $(drivenSelect);
                    d.prop('disabled', false);
                    d.html(data);
                    var option = $("option[value="+currentValue+"]",d);
                    if(option.length){
                        d.val(currentValue);  
                    } else {
                        d.val('');
                    }
                    d.trigger('change');  
                }
            });
        } else {
            var d = $(drivenSelect);
            d.prop("disabled", true);
            d.val('');
            d.trigger('change');  
        }

        

        

    });

    if(options.initialCheck){
        $(driverSelect).trigger('change');
    }

};



questionario.formDirty = [];
questionario.valuesMap = {};






//doc ready stuff.
//listening dor changes and adding placeholders

$(function(){
        
        var confirmChanges = function(evt, href){
            
            var currentLocation = window.location;
            if(href && currentLocation.pathname ==  href){
                return false;    
            }
            
            
            if(questionario.formDirty.length){
                evt.preventDefault();    
                
            
                BootstrapDialog.show({
                    title  : 'Dati modificati',
                    message: 'I dati sono stati modificati. Salvare le modifiche prima di lasciare la scheda?',
                    buttons: [
                    {
                        label: 'Salva',
                        cssClass: 'btn-success',
                        icon: 'glyphicon glyphicon-ok',
                        action: function(dialogItself){
                            $("form").attr('action', '?next='+href);
                            dialogItself.close();
                            $('button[type=submit]').click();
                            
                        }
                    }, 
                    {
                        label : 'Annulla modifiche',
                        icon: 'glyphicon glyphicon-ban-circle',
                        cssClass: 'btn-warning',
                        action: function(dialogItself){
                            dialogItself.close();
                            window.location = href;
                        }

                    }, 
                    {
                        label : 'Rimani sulla pagina',
                        icon: 'glyphicon glyphicon-ban-circle',
                        cssClass: 'btn-default',
                        action: function(dialogItself){
                            dialogItself.close();
                        }

                    }, 
                    ]
                });
                return false;


            }
        };
        


        var changeHandler =  function(){
            var $item = $(this);
            var val;
            var name = $item.attr('name');
            if($item.attr('type') == 'checkbox'){
                val = $item.prop('checked');
            } else{
                val = $item.val();    
            }
            var idx = questionario.formDirty.indexOf(name);
            var isDirty = idx != -1;
            if(questionario.valuesMap[name] != val){
                if(!isDirty){
                    questionario.formDirty.push(name);
                }
                
            } else {
                if(isDirty){
                    questionario.formDirty.splice(idx,1);
                }
            }
            
        };

        $("input[type=text],.panel:not('.hide') input[type=checkbox],select,textarea").on('change', changeHandler);

        $("input[type=text],.panel:not('.hide') input[type=checkbox],select,textarea").each(function(idx, item){
            var $item = $(item);
            var val;
            if($item.attr('type') == 'checkbox'){
                val = $item.prop('checked');
            } else{
                val = $item.val();    
            }
            
            var name = $item.attr('name');
            questionario.valuesMap[name] = val;

        });

        
        $("a").on('click', function(evt){

            var href = $(this).attr('href');
            return confirmChanges(evt, href);
        });


        $('input, textarea').placeholder();
         

    });
    
          