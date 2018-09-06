
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
  console.log("coucou");
  form = $("#newind")
  nom = form.find("input[name = 'nom']").val()
  comm = form.find("[name = 'commentaire']").val()
  animaux = new Array()
  $("#newinddrop .animdiv").each(function(i){animaux.push($(this).data("id"))})

  result = {
    "nom": nom,
    "commentaire": comm,
    "animaux": animaux
  }
  console.log(result);

  donnees = JSON.stringify(result)
  path = '/creer_ind'

  $.ajax({
    url: path,
    type: "POST",
    success: function(rep){console.log(rep)},
    error: function(err){console.log(err)},
    data: donnees,
    dataType: "text"
  })


}

drop2 = function(event, ui){
  ui.draggable.detach().appendTo(this)
}

count_anim_cam = function(){
  $(this).parent("nav").each(function(index, nav) {
    $(nav).find("select.cameras option").each(function(index, opt) {
      cam = $(opt).attr("class")
      nb = $(nav).find(".camdiv." + cam + ">.animdiv").filter(function(i){
        return($(this).css("display") != "none")
      }).length
      $(opt).text(cam + "(" +nb+ ")")
    });
  });
}

$(function(){
  $('img').on('dragstart', function(event) { event.preventDefault(); })
  $(".camdiv").hide()
  $(".animdiv").draggable({"helper": 'clone'})
  $(".droppable").droppable({"drop":drop2})

  $(".cameras option").click(function(){click_camera($(this).attr("class"))})


  $(document).keypress(zomm_press)
  $("select.cameras").click(count_anim_cam)


})
