function showChilds(parent) {
    $.getJSON("/getposts?parent="+parent, function(result){
        $.each(result, function(i, post) {
            posthtml = "<div class='post' id='post-"+post['id']+"'><p class='post-user'>"+post['username']+"</p><p class='post-message'>"+post['message']+"</p><div id='post-"+post['id']+"-children'></div></div>";
            $("#post-"+parent+"-children").append(posthtml);
        });
    });
}
