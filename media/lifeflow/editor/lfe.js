var display_error = function(txt, elem) {
  if (elem == undefined) { elem = "#errors"; };
  var msg = $('<div class="error-msg"><p>'+txt+'</p></div>');
  msg.insertAfter($(elem)).fadeIn('slow').animate({opacity: 1.0}, 5000).fadeOut('slow', function() { msg.remove(); });
};

var display_message = function(txt, elem) {
  if (elem == undefined) { elem = "#messages" };
  var msg = $('<div class="normal-msg"><span>'+txt+'</span></div>');
  msg.insertAfter($(elem)).fadeIn('slow').animate({opacity: 1.0}, 1000).fadeOut('slow', function() { msg.remove(); });
};


/* Talking with the LifeFlow API */

var delete_model = function(model, pk, onCompleteFunc) {
  if ( ! onCompleteFunc) onCompleteFunc = function() {};
  $.ajax({url:"/editor/delete_model/", type:"POST", data:{model:model, pk:pk},
	complete:onCompleteFunc});
};

var create_model = function(model, args, onCompleteFunc) {
  if (! onCompleteFunc) onCompleteFunc = function() {};
  if (! args) args = {};
  args["model"] = model;
  $.ajax({type:"POST", url:'/editor/create_model/', data:args,
	complete:onCompleteFunc});
}

var update_model = function(model, pk, args) {
  var onComplete = function(res,status) {
    if (status == "success") {
      display_message("Saved.");
    }
    else {
      display_error(res.responseText);
    }
  }
  if (!args) args = {};
  args["model"] = model;
  args["pk"] = pk;
  $.ajax({type:"POST", url:'/editor/update/', data:args, complete:onComplete});
};

/* Used by projects.html */

var edit_project = function(pk) {
  if (pk)
    window.location =  pk + "/details/";
  else
    display_error("Please select a project to edit!");
}

/* Used by overview.html */

var edit = function(lst, type) {
  var index = lst[0].selectedIndex
  if (index != -1) {
    var chosen = lst.children()[index]
    window.location = "edit/" + type + "/" + chosen.value + "/title/";
  }
  else {
    display_error("You haven't selected anything to edit!");
  }
};

var move = function (lst, dest, urlBase) {
  var index = lst[0].selectedIndex
  if (index == -1) { display_error("Nothing selected to move."); }
  else {
    var chosen = lst.children()[index];
    var pk = chosen.value;
    var url = urlBase +"/" + pk + "/";
    $.ajax({url:url, complete:function(res,status) {
      if (status == "success") {
        chosen.value = res.responseText;
        chosen.parentNode.removeChild(chosen);
        dest.prepend(chosen);
      }
      else { display_error(res.responseText); }
}})}};
