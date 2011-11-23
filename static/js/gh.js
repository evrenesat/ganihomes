gh = {
    bas:function (m) {
        $('#arabg').prepend(m + '<br>')
    },
    init:function () {
        var usableHeight = $(window).height(), hdr_h = 0, logo_pad = 0, sc_pad = 0;

        if (usableHeight > 800)hdr_h = 110, logo_pad = -6, sc_pad = 20;
        else if (usableHeight > 610)  hdr_h = 90, logo_pad = -6;

        if (hdr_h)$('#hdr').css({height:hdr_h + 'px'})
        if (logo_pad)$('.logo div').css({marginTop:logo_pad + 'px'})
        if (sc_pad)$('.showcase').css({paddingTop:sc_pad + 'px'})
    },
    index_init:function () {
        var self = this;
        self.akGorunur = 0
        self.sks = {}
        $('#arabg').fadeTo('fast', .5)
        self.doRePlacements();
        self.otoTamamla('arainput')
        $(window).resize(function () {
            self.doRePlacements()
        });
        $('#araf input').focus(function () {
            self.akToggle(0)
        });
        $('html').click(function () {
            self.akToggle(1)
        });
        $('#araf, #arabg_cont').click(function (event) {
            event.stopPropagation();
        })
        $('#howitworks a').click(function () {
            $('#howitworks').removeClass('ui-state-active');
        })
        $('.slidiv').mouseenter(
            function () {
                sld = $(this)
//            console.log(sld.index()+1)
//            sld.parents('.tabborder').smoothDivScroll("moveToElement", "number", sld.index()+1);
                sld.find('.sbaner').animate({height:'110px'});
            }).mouseleave(function () {
                $(this).find('.sbaner').animate({height:'40px'})
            });
        self.makeScroller('GVS1')
        self.makeScroller('GVS2')
        self.makeScroller('GVS3')
    },
    makeScroller:function (container_id, hidden) {
        if (typeof(hidden) == 'undefined') hidden = false;
        var sk = $('#' + container_id);
        this.sks[container_id] = sk
        sk.smoothDivScroll({
            hiddenOnStart:hidden,
            autoScroll:"", //"onstart" ,
            autoScrollDirection:'endlessloopright',
            autoScrollStep:2,
            autoScrollInterval:50,
            visibleHotSpots:"onstart"
        });
        sk.find('div.scrollingHotSpotRight').bind('mouseleave', function () {
            sk.smoothDivScroll("startAutoScroll").smoothDivScroll("option", "autoScrollDirection", 'endlessloopright')
        })

        sk.find('div.scrollingHotSpotLeft').bind('mouseleave', function () {
            sk.smoothDivScroll("startAutoScroll").smoothDivScroll("option", "autoScrollDirection", 'endlessloopleft')
        });
        sk.find('.scrollableArea .slidiv').mouseenter(function () {
            sk.smoothDivScroll('stopAutoScroll')
        })
        sk.find('.scrollableArea .slidiv').mouseleave(function () {
            sk.smoothDivScroll('startAutoScroll')
        })
    },
    akToggle:function (gorunurluk) {
        //toggles find menu
        var self = this, ak = $('#arabg'), akCont = $('#arabg_cont')
        if (typeof(gorunurluk) != 'undefined') self.akGorunur = gorunurluk;
        if (self.akGorunur == 0) {
            akCont.show('fast', function () {
                ak.animate({top:'0'}, { "duration":"fast" }).fadeTo('fast', 1)
            });
            self.akGorunur = 1;
        } else {
            ak.fadeTo('fast', .5, function () {
                akCont.hide();
                ak.css({top:'-477px'});
            })
            self.akGorunur = 0;
        }
    },
    doRePlacements:function () {
        var self = this
        self.rePlace('#araf', '#mhtabela', 720, -65, 1);
        self.rePlace('#araf', '#arabg_cont', -7, 20);
    },
    rePlace:function (src_id, trg_id, off_left, off_top, show) {
        // re-place the target object relatively to src object.
        var trg = $(trg_id), sof = $(src_id).offset();
        if (typeof(show) != 'undefined' && show == 1) trg.fadeIn('fast');
        var ntop = sof.top + off_top, nleft = sof.left + off_left;
        trg.css({top:ntop, left:nleft});
//        if (typeof(debug) != 'undefined') this.bas(['sof.left ', sof.left, ' sof.top ', sof.top, ' off_left ', off_left, ' off_top ', off_top, ' trg.left ', trg.css('left'), ' trg.top ',trg.css('top'), 'ntop',ntop, 'nleft',nleft])
    },
    otoTamamla:function (id) {
        self = this
        var availableTags = [
            "İzmir",
            "İstanbul",
            "Ankara",
            "Antalya",
            "New York",
            "Madrid",
            "Londra",
            "Kıbrıs",
            "Aydın",
            "Manisa",
            "Karşıyaka, İzmir, Türkiye",
            "Bornova, İzmir, Türkiye",
            "Alsancak, İzmir, Türkiye",
            "Taksim, İstanbul, Türkiye",
            "Bursa",
            "Denizli",
            "Konya",
            "Avusturalya",
            "Amerika Birleşik Devletleri",
            "Hollanda",
            "İspanya",
            "Rusya"
        ];
        it='';
        $("#" + id).autocomplete({minLength: 3, source:availableTags, appendTo:'#araoneri'});

    }
};

$(window).ready(function () {
    gh.init()
    $('#tabs').tabs();
    if (window.PIE) {
        $('.piee').each(function () {
            PIE.attach(this);
        });
    }
})

//
//,focus: function(event, ui) {
//                   console.log($("#araoneri li").length)
//                   focitem=$("#araoneri li:contains("+ui.item.value+")'").index();
//                   console.log(focitem)
//                   if(focitem < 1)focitem = 1;
//   //                console.log(focitem)
//                   $('#araoneri').scrollTo('ul li:eq('+ focitem +')');
//               }
