gh = {
    bas : function(m){
        $('#arabg').prepend(m + '<br>')
    },
    index_init:function () {
        var self = this;
        self.akGorunur = 0
        $('#arabg').fadeTo('fast',.5)
        self.doRePlacements();
        $(window).resize(function () { self.doRePlacements() });
        $('#araf input').focus(function () { self.akToggle(0) });
        $('html').click(function () { self.akToggle(1) });
        $('#araf, #arabg_cont').click(function(event){event.stopPropagation();})
        $('.slidiv').mouseenter(function(){$(this).find('.sbaner').animate({height:'110px'})}).
            mouseleave(function(){$(this).find('.sbaner').animate({height:'40px'})})
        self.makeScroller('#GVS1')
    },
    makeScroller:function (container_id, hidden) {
        if (typeof(hidden) == 'undefined') hidden = false;
        $sk = $(container_id);
        $sk.smoothDivScroll({
            hiddenOnStart:hidden,
            autoScroll:"", //"onstart" ,
            autoScrollDirection:'endlessloopright',
            autoScrollStep:1,
            autoScrollInterval:20,
            visibleHotSpots:"onstart"
        });
        $sk.find('div.scrollingHotSpotRight').bind('mouseleave', function () {
            $sk.smoothDivScroll("startAutoScroll").smoothDivScroll("option", "autoScrollDirection", 'endlessloopright')
        })

        $sk.find('div.scrollingHotSpotLeft').bind('mouseleave', function () {
            $sk.smoothDivScroll("startAutoScroll").smoothDivScroll("option", "autoScrollDirection", 'endlessloopleft')
        });
        $sk.find('.scrollableArea .slidiv').bind('mouseenter', function () {
            $sk.smoothDivScroll('stopAutoScroll')
        })
        $sk.find('.scrollableArea .slidiv').bind('mouseleave', function () {
            $sk.smoothDivScroll('startAutoScroll')
        })
    },
    akToggle:function (gorunurluk) {
        //toggles find menu
        var self = this, ak = $('#arabg'), akCont = $('#arabg_cont')
        if (typeof(gorunurluk) != 'undefined') self.akGorunur = gorunurluk;
        if (self.akGorunur == 0) {
            akCont.show('fast', function () {
                ak.animate({top:'0'}, { "duration":"fast" }).fadeTo('fast',1)
            });
            self.akGorunur = 1;
        } else {
            ak.fadeTo('fast',.5,function () {
                akCont.hide();
                ak.css({top:'-477px'});
            })
            self.akGorunur = 0;
        }
    },
    doRePlacements:function () {
        var self = this
        self.rePlace('#araf', '#mhtabela', 740, -80, 1);
        self.rePlace('#araf', '#arabg_cont', -7, 20);
    },
    rePlace:function (src_id, trg_id, off_left, off_top, show) {
        // re-place the target object relatively to src object.
        var trg = $(trg_id), sof = $(src_id).offset();
        if (typeof(show) != 'undefined' && show==1) trg.fadeIn('fast');
        var ntop= sof.top + off_top, nleft = sof.left + off_left;
        trg.css({top:ntop, left: nleft});
//        if (typeof(debug) != 'undefined') this.bas(['sof.left ', sof.left, ' sof.top ', sof.top, ' off_left ', off_left, ' off_top ', off_top, ' trg.left ', trg.css('left'), ' trg.top ',trg.css('top'), 'ntop',ntop, 'nleft',nleft])
    }
};

$(window).ready(function () {
    $('#tabs').tabs();
    if (window.PIE) {
        $('.piee').each(function () {
            PIE.attach(this);
        });
    }
})
