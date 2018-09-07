
z_press = false

click_camera = function(){
  cam = $(this).attr("class")
  $(this).parents("nav").find(".camdiv").hide()
  camdiv = $(this).parents("nav").find(".camdiv." + cam)
  camdiv.find("img").each(function(index, img) {
    $(img).attr('src', $(img).data('src'))
  })
  camdiv.show()
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

open_serie = function(){
  series = $(this).data("series")
  for (ser in series){
    chemin = "/serie/" + series[ser]
    win = window.open(chemin, '_blank');
    if (win) {
      //Browser has allowed it to be opened
      win.focus();
    } else {
      //Browser has blocked it
      alert('Veiller autoriser l ouverture d un nouvel onglet.');
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
  $(".animdiv").draggable({"helper": 'clone'}).dblclick(open_serie)
  $(".droppable").droppable({"drop":drop2})

  $(".cameras option").click(click_camera)


  $(document).keypress(zomm_press)
  $("select.cameras").click(count_anim_cam)


})
