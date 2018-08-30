

click_camera = function(cam){
  $(".camdiv").hide()
  $(".camdiv." + cam).show()
}

$(function(){
  $(".camdiv").hide()
  $(".cameras option").click(function(){click_camera($(this).attr("class"))})
  $(".photo").elevateZoom({scrollZoom : true})


})
