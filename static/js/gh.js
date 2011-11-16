
function rePlacer(src_id,trg_id,off_left, off_top, show){
    // re-place the target object relatively to src object.
    //optionaly show it after placement.
    trg=$(trg_id)
    sof=$(src_id).offset();
    trg.offset({top: sof.top + off_top, left: sof.left + off_left});
    if(typeof(show)!='undefined') trg.show('slow')


}
