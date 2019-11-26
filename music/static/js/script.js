var currentsound;
var currentimg;

 function play_pause(songid,img) {

 if ( currentimg ){
     currentimg.src = "/static/images/play.png";
 }
 var myAudio = document.getElementById(songid);
     if(myAudio.paused) {
     myAudio.play();
     img.src = "/static/images/pause.png";
     } else{
     myAudio.pause();
     img.src = "/static/images/play.png";
     }
     $("audio").on("play", function(){
 var _this = $(this);
 $("audio").each(function(i,el){
     if(!$(el).is(_this))
         $(el).get(0).pause();
 });
 currentimg = img;
});
}
