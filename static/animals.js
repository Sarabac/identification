
z_press = false

click_camera = function(cam){
  $(".camdiv").hide()
  $(".camdiv." + cam).show()
}

zomm_press = function(e){
  var t = String.fromCharCode(e.which)
  console.log(t)
  if (t == "z"){
    z_press = !z_press
    if(z_press){
      $(".photo").elevateZoom({scrollZoom : true})
    }else{
      img = $(".photo")
      $('.zoomContainer').remove();
      img.removeData('elevateZoom');
      img.removeData('zoomImage');
    }

  }
}


$(function(){
  $(".camdiv").hide()
  $(".cameras option").click(function(){click_camera($(this).attr("class"))})


  $(document).keypress(zomm_press)


})
