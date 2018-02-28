
remplir_creation = function(){
  $("header").append($("<select id='creation'></select>"))
  $("#definition fieldset").each(function(){
    var esp = $(this).attr("class")
    var opt = $("<option></option>")
    opt.text(esp)
    opt.addClass(esp)
    $("#creation").append(opt)
  })
}

clic_sur_creation = function(){
  var esp = $(this).attr("class")
  var nouveau = $("#definition fieldset."+esp).clone().prependTo("#animaux")
  select_radiobutton(nouveau.find("input:radio").prop("checked", true))
}

select_radiobutton = function(obj){
  $("#animaux .contain_caract").addClass("cache")
  $(obj).parent().siblings(".contain_caract").removeClass("cache")
}

$(function(){
  remplir_creation()
  $("#creation option").on("click", clic_sur_creation)
  wheelzoom(document.querySelectorAll("#principale"))
  $(".photo").click(function(){$("#principale").attr("src",$(this).data("url"))})

})
