(function(){


showAddDocument = function(url){
    $(".modal-dialog").remove();
    console.log("ss", url)
    $.get(url).success(function(data){
        $("#myModal").append(data);
        $("#myModal").modal();
        $("#form-submit").on('click', function(){
            
        var form = $("form", $("#myModal"));
        form.attr("action", url);

            // prepare Options Object 
        var options = { 
            //target:     '#divToUpdate', 
            url:        url,
            success:    function() { 
                alert('Thanks for your comment!'); 
            } 
        }; 
         
        // pass options to ajaxForm 
        form.ajaxForm(options).ajaxSubmit(
            {
                success : function(){
                    $("#myModal").modal('hide').html("");
                    location.reload();
                }
            }
        );

        });
        


        });



}


$(function(){




    $("#add-document").on('click', function(){
        var url = $(this).attr("data-href");
        console.log("xxx", url);
        showAddDocument(url);
    })

});




})();