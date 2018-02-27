$(function(){
  $.getJSON($SCRIPT_ROOT + "/especes", {}, function(data){
    console.log(data.especes);
  })


})
