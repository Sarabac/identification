
remplir_creation = function(){
  $("header").append($("<div id='creation'></div>"))
  $("#definition fieldset").each(function(){
    var esp = $(this).attr("class")
    var opt = $("<button></button>")
    opt.text(esp)
    opt.addClass(esp)
    $("#creation").append(opt)
  })
}

enregistrer = function(){

  individus = new Array()
  $("#animaux fieldset").each(function(i){
    modalites = new Array()
    $(this).find("option:selected").each(function(i){
      num = $(this).data("num")
      if(num!=0){//different de "aucun"
        modalites.push(num)
      }
    })
    individus.push({
      id_e: $(this).data("num"),
      photos: $(this).data("photos"),
      modalites: modalites
    })
  })
  id_serie = $("#principale").data("serie")
  donnees = JSON.stringify( {"individus": individus, "serie": id_serie} )
  path = '/enregistrer' + "/" + id_serie
  retour = '/series#' + id_serie

  $.ajax({
    url: path,
    type: "POST",
    success: function(rep){$(location).attr("href", retour)},
    error: function(err){console.log(err)},
    data: donnees,
    dataType: "text"
  })


}

clic_sur_creation = function(){
  var esp = $(this).attr("class")
  var nouveau = $("#definition fieldset."+esp).clone().prependTo("#animaux")
  console.log(nouveau);
  nouveau.find("input:checkbox").prop('checked', true).trigger("click").prop('checked', true)
}

chargement = function(){
  for(i in Acharger){
    animal = Acharger[i]
    field = $("#definition fieldset[data-num="+animal["id"]+"]").clone().prependTo("#animaux")
    for (j in animal["modalites"]){
      modalite = animal["modalites"][j]
      field.find("option[data-num="+modalite+"]").prop("selected", true)
    }
    field.data("photos", animal["photos"])
    if (animal["photos"].indexOf($("nav .select").data("num"))>=0){
      field.find(":checkbox").prop("checked", true)
    }
  }

}

clic_sur_miniature = function(){
  $("#principale").attr("src",$(this).data("url"))
  $(".photo").removeClass("select")
  $(this).addClass("select")

  //on change les cases checkees qui indiquent qu'un animal s'y trouve
  num = $(this).data("num")
  $("#animaux fieldset").each(function(i){
    check = $(this).find(".check_animal")
    if ($(this).data("photos").includes(num)){
      check.prop("checked", true)
    }else{
      check.prop("checked", false)

    }
  })
}

click_check = function(self){
  field = $(self).parent().parent()
  photos = field.data("photos")
  id_photo = $("nav .select").data("num")
  if ($(self).is(":checked")){
    if (!(photos.includes(id_photo))){
      photos.push(id_photo)
    }
  }else{
    if (photos.includes(id_photo)){
      index = photos.indexOf(id_photo)
      photos.splice(index, 1)
    }
  }
  field.data("photos", photos)
}

shortcut = function(){
  $(document).keydown(function(e) {
    var t = String.fromCharCode(e.which)
    console.log(t)
    if (t == "W"){enregistrer()}
    if (t == "D"){$(".check_animal").prop('checked', true).trigger("click").prop('checked', true)}
    if (t == "A"){$(".check_animal").prop('checked', false).trigger("click").prop('checked', false)}
  })
}

$(function(){
  remplir_creation()
  $("#creation button").on("click", clic_sur_creation)
  wheelzoom(document.querySelectorAll("#principale"))
  $(".photo").on("click", clic_sur_miniature)
  $($(".photo")[0]).trigger("click")

  chargement()

  shortcut()
})
