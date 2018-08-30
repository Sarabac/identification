
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
      $(".photo:visible").elevateZoom({scrollZoom : true})
    }else{
      img = $(".photo")
      $('.zoomContainer').remove();
      img.removeData('elevateZoom');
      img.removeData('zoomImage');
    }
  }
}

creer_individu = function(){
  form = $("#newind")
  nom = form.find("input[name = 'nom']").val()
  comm = form.find("[name = 'commentaire']").val()

  result = {
    "nom": nom,
    "commentaire": comm
  }

}

drop2 = function(event, ui){

  ui.draggable.detach().appendTo(this)
}

$(function(){
  $('img').on('dragstart', function(event) { event.preventDefault(); })
  $(".camdiv").hide()
  $(".animdiv").draggable({"helper": 'clone'})
  $(".droppable").droppable({"drop":drop2})

  $(".cameras option").click(function(){click_camera($(this).attr("class"))})


  $(document).keypress(zomm_press)


})
