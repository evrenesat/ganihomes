
function rePlacer(src_id,trg_id,off_left, off_top, show){
    // re-place the target object relatively to src object.
    //optionaly show it after placement.
    var trg=$(trg_id)
    var sof=$(src_id).offset();
//    console.log(sof.left, sof.top)
//    console.log(off_top, off_left)
    if(typeof(show)!='undefined') trg.show('slow')
    trg.offset({top: sof.top + off_top, left: sof.left + off_left});



}
function doRePlacements(){
        rePlacer('#araf','#mhtabela', 740, -70, 1);
//        rePlacer('#vitrin','#arabg', 15, -5, 1);
        rePlacer('#vitrin','#arabg_cont', 15, -5);
}
$(window).ready(function(){
gh = {
    araKutuGorunur : 0,
    araKutuCont: $('#arabg_cont'),
    araKutu : $('#arabg'),
    araKutuGosterGizle : function(){
        var self = this
        console.log(this.araKutuGorunur)
        console.log(this.araKutuCont)
        if (this.araKutuGorunur==0){
            this.araKutuCont.show('fast',function(){self.araKutu.animate({top:'0'}, { "duration": "slow" })});
            this.araKutuGorunur=1;

        }
        else{
            this.araKutu.animate({top:'477px'},'fast',function(){self.araKutuCont.hide()})
            this.araKutuGorunur=0;
        }
    }


}
//gh.araKutuGosterGizle();
});
