var fix = $(".navbar-inner"), pos = fix.offset();
$(window).scroll(function() {
    if ($(window).scrollTop()) {
        $(".navbar-inner").css({

           "box-shadow":  "1px 1px 12px #b5bbbf"
        });
    } else {
       
       $(".navbar-inner").css({
            "box-shadow":  ""
        }); 
    }
});







$(function() {
        var fdu = $('#form_doc_upload');

        $("#id_doc_file_name").change(function(){
            var fileName = $(this).val();
            $.ajax({
                type: fdu.attr('method'),
                url: fdu.attr('action'),
                data: fdu.serialize(),
                context: this,
                cache: false,
                success: function(data){
                    $(".preview").html(data);
                },
                error: function(data) {
                    var ermsg = "Can't upload the file: "+ fileName+"<br/>Something went wrong!"
                    $(".preview").html(ermsg);
                }
            });


            /*if(fileName) {
                alert(fileName + " was selected");
            } else {
                alert("no files selected");
            }*/

            return false;

         });



        
        $('#loadingIndicator').hide();

        $('#loadingIndicator').bind('ajaxStart', function() {
            $(this).show();
          }).bind('ajaxComplete', function() {
            $(this).hide();
          });

        $(".comments-list").click(function() {
            
            var ID = $(this).attr("id");

            $.ajax({
        
                type: "POST",
                url: "viewajax.php",
                data: "fid="+ID,
                cache: false,
                success: function(html){
                    $(".comment-list"+ID).prepend(html);
                    $("#tc"+ID).remove();
                    $("#tc").remove();
                    $(".comments-list").remove();
                }

            });

            return false;

       });

});











$(document).ready(function(){
       
          $("#button-fr").attr("disabled", "disabled");
          //$("#button-shr").attr("disabled", "disabled");
           
          $("#content-fr").keyup(function(){
              if ($(this).val().trim().length > 0) {
                  $("#button-fr").removeAttr("disabled");
              } else {
                  $("#button-fr").attr("disabled", "disabled");
              }

          });



          $("#content-shr").keyup(function(){
              if ($(this).val().trim().length > 0) {
                  $("#button-shr").removeAttr("disabled");
              } else {
                  $("#button-shr").attr("disabled", "disabled");
              }

          });


        

	// This hides the menu when the page is clicked anywhere other than the menu.
		$(document).bind('click', function(e) {
			var $clicked = $(e.target);
		    if (! $clicked.parents().hasClass("menu")){
		        $(".menu dd ul").hide();
				$(".menu dt a").removeClass("selected");
			}

		});
		
		$(".menu dt a").click(function() {

			var clickedId = "#" + this.id.replace(/^link/,"ul");

		        // Hides everything else that the current menu 
			$(".menu dd ul").not(clickedId).hide();

		        //Toggles the menu.
			$(clickedId).toggle();

		        //Add the selected class.
			if($(clickedId).css("display") == "none"){
				$(this).removeClass("selected");
			}else{
				$(this).addClass("selected");
			}

		});
		
// This function shows which menu item was selected in corresponding result place
		$(".menu dd ul li a").click(function() {
			var text = $(this).html();
			$(this).closest('dl').find('.result').html(text);
		    $(".menu dd ul").hide();
		});

		
	});




$(document).ready(function()
{


$(".account").click(function()
{
var X=$(this).attr('id');
if(X==1)
{
$(".submenu").hide();
$(this).attr('id', '0'); 
}
else
{
$(".submenu").show();
$(this).attr('id', '1');
}

});

//Mouse click on sub menu
$(".submenu").mouseup(function()
{
return false
});

//Mouse click on my account link
$(".account").mouseup(function()
{
return false
});


//Document Click
$(document).mouseup(function()
{
$(".submenu").hide();
$(".account").attr('id', '');
});
});


