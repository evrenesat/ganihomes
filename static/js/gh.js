gh = {
    index_init:function () {
        var self = this;
        self.akGorunur = 0
        self.akCont = $('#arabg_cont')
        self.ak = $('#arabg')
        self.ak.fadeTo('fast',.5)
        self.doRePlacements();
        $(window).resize(function () { self.doRePlacements() });
        $('#araf input').focus(function () { self.akToggle(0) });
        $('html').click(function () { self.akToggle(1) });
        $('#araf, #arabg_cont').click(function(){event.stopPropagation();})
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
        var self = this
        if (typeof(gorunurluk) != 'undefined') self.akGorunur = gorunurluk;
        if (self.akGorunur == 0) {
            self.akCont.show('fast', function () {
                self.ak.animate({top:'0'}, { "duration":"fast" }).fadeTo('fast',1)
            });
            self.akGorunur = 1;
        } else {
            self.ak.fadeTo('fast',.5,function () {
                self.akCont.hide();
                self.ak.css({top:'-477px'});
            })
            self.akGorunur = 0;
        }
    },
    doRePlacements:function () {
        var self = this
        self.rePlacer('#araf', '#mhtabela', 740, -70, 1);
        self.rePlacer('#araf', '#arabg_cont', -7, 20);
    },
    rePlacer:function (src_id, trg_id, off_left, off_top, show) {
        // re-place the target object relatively to src object.
        //optionaly show it after placement.
        var trg = $(trg_id), sof = $(src_id).offset();
        if (typeof(show) != 'undefined') trg.fadeIn('fast');
        trg.offset({top:sof.top + off_top, left:sof.left + off_left});
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
