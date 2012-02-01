Number.prototype.formatMoney = function(c, d, t){
var n = this, c = isNaN(c = Math.abs(c)) ? 2 : c, d = d == undefined ? "," : d, t = t == undefined ? "." : t, s = n < 0 ? "-" : "", i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", j = (j = i.length) > 3 ? j % 3 : 0;
   return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
 };
$.getScript = function(url, callback, cache){
	$.ajax({
			type: "GET",
			url: url,
			success: callback,
			dataType: "script",
			cache: cache || true
	});
};

(function($) {

	$.fn.easyTooltip = function(options){

		// default configuration properties
		var defaults = {
			xOffset: 10,
			yOffset: 25,
			tooltipId: "easyTooltip",
			clickRemove: false,
			content: "",
			useElement: ""
		};

		var options = $.extend(defaults, options);
		var content;

		this.each(function() {
			var title = $(this).attr("title");
			$(this).hover(function(e){
				content = (options.content != "") ? options.content : title;
				content = (options.useElement != "") ? $("#" + options.useElement).html() : content;
				$(this).attr("title","");
				if (content != "" && content != undefined){
					$("body").append("<div id='"+ options.tooltipId +"'>"+ content +"</div>");
					$("#" + options.tooltipId)
						.css("position","absolute")
						.css("top",(e.pageY - options.yOffset) + "px")
						.css("left",(e.pageX + options.xOffset) + "px")
						.css("display","none")
						.fadeIn("fast")
				}
			},
			function(){
				$("#" + options.tooltipId).remove();
				$(this).attr("title",title);
			});
			$(this).mousemove(function(e){
				$("#" + options.tooltipId)
					.css("top",(e.pageY - options.yOffset) + "px")
					.css("left",(e.pageX + options.xOffset) + "px")
			});
			if(options.clickRemove){
				$(this).mousedown(function(e){
					$("#" + options.tooltipId).remove();
					$(this).attr("title",title);
				});
			}
		});

	};

})(jQuery);

gh = {
    bas:function (m) {
        $('#arabg').prepend(m + '<br>')
    },
    initPagesAndSetLang:function(){
        parts = document.location.pathname.split('/')
        for (p in parts){
            p = parts[p]
            var fname = 'init_' + p
            if(p.length==2)this.LANGUAGE_CODE = p
            else if(fname in this){
                this[fname]()
                return
            }

        }
    },
    STATIC_URL : '',
    LANGUAGE_CODE : 'en',
    popap:function(trigger, popap_id, offset_x, offset_y){
        var self = this, ptimer = 0, popap = $(popap_id);
        this.rePlace(trigger, popap_id, offset_x, offset_y);
        setTimer= function(){if(!ptimer)ptimer = setTimeout(function(){popap.fadeOut();ptimer=0;},1500);}
        clearTimer= function(){clearTimeout(ptimer);ptimer=0;}
        popap.mouseleave(setTimer).mouseenter(clearTimer)
        $(trigger).mouseover(function(){ setTimer(); popap.slideDown() })
    },
    popmodal:function(trigger, popap_id, offset_x, offset_y){
        var self = this, popap = $(popap_id);
        this.rePlace(trigger, popap_id, offset_x, offset_y);
        popap.prepend("<div class='closex'>x</div>").find('.closex').click(function(){popap.fadeOut();})
        $(trigger).click(function(){  popap.slideDown() })
    },
    init:function () {
        var self = this;
        this.popap('.smdil', '#langcurr', -40, 20)
        this.STATIC_URL = $('#script0').attr('src').split('js/')[0]
        var usableHeight = $(window).height(), hdr_h = 0, logo_pad = 0, sc_pad = 0;
        if (usableHeight > 800)hdr_h = 110, logo_pad = -6, sc_pad = 20;
        else if (usableHeight > 610)  hdr_h = 90, logo_pad = -6;
//        if (hdr_h)$('#hdr').css({height:hdr_h + 'px'})
//        if (logo_pad)$('.logo div').css({marginTop:logo_pad + 'px'})
//        if (sc_pad)$('.showcase').css({paddingTop:sc_pad + 'px'})
//        $('#smekle').click(function(){document.location='/add_place/'})
//        $('#smkayit').click(function(){document.location='/register/'})
//        $('#smgir').click(function(){document.location='/login/'})


        if(!this.selected_currency){
            this.selected_currency = $.cookie('gh_curr') || 0}
        this.fillCurrencies()
        this.initPagesAndSetLang()

        $("#sosicon li").hover(function() {
        var e = this;
        $(e).find("a").stop().animate({ top: "-10px" }, 200, function(){
        $(e).find("a").animate({ top: "5px" }, 500, function(){
        $(e).find("a").animate({ top: "0px" }, 300);
        });
        });
        });


    },
    fillCurrencies:function(){
        var self = this
        dv = $('#currs')
        for (c in gh_crc){
            var cc = gh_crc[c]
            if(!this.selected_currency && cc[0]=='1.0')this.selected_currency = c
            $('<span />').attr('data-crr',c).click(function(e){self.setCurrency(e.target)}).html('<sub>'+cc[2]+'</sub> '+cc[1]).appendTo(dv);
                }
        this.setCurrRates()
        this.priceScanConvert()
    },
    currency_change_trigger_onkeyup:'#id_price, #id_weekend_price, #id_extra_price, #id_cleaning_fee',
    setCurrency:function(ob){

        var cid = (typeof(ob)!='number') ? $(ob).data('crr') : ob
        $.cookie('gh_curr', cid, { expires: 365, path: '/' });
        this.selected_currency = cid
        this.setCurrRates()
        this.priceScanConvert()
        if($("#pcalendar").length)this.makeAvailabilityTab(1)
        this.calculateTotalPrice()
        $('#id_currency').val(cid)
        $('.current_curr').html(gh_crc[cid][1])
        $(this.currency_change_trigger_onkeyup).trigger('keyup')

    },
    setCurrRates:function(){
        var selCrr = parseFloat(gh_crc[this.selected_currency][0])
        for (c in gh_crc){
            var cc = gh_crc[c]
            this.currRates[c] = selCrr / parseFloat(cc[0])
        }
    },
    getCurrPrice:function(p){
        //cc[3] 1 ise para birimi once(usd 1) degilse (1 usd)
      var cc = gh_crc[this.selected_currency]
//      if (typeof(p)=='undefined')return cc[1]
      p = "<span class='gprc'>"+p+"</span>"
      c = "<span class='gcrc'> "+cc[2]+" </span>"
      return cc[3]==1 ? c + p : p + c
    },
    priceScanConvert:function(){
      var self = this
      var cc = gh_crc[this.selected_currency]
      $('a.smdil').html('<sub>'+cc[2]+'</sub> '+cc[1])
      $('.gh-prc').each(function(){
          var ob = $(this)
          var cid = ob.data('crc')
          var setCrcName = this.className.indexOf("crc") > -1
          prc = self.convertPrice(parseFloat(ob.data('prc')),cid)
          if(setCrcName) ob.html(self.getCurrPrice(prc))  //parabirimi yanina ilistirilecekse
          else {// bol sifirli bir para birimiyse kurus kismini atiyoruz
              cprc = prc.split(',')
              var sub = cprc[0].length<6 ? "<sub>,"+cprc[1]+"</sub>" : ''
              ob.html(cprc[0]+sub)
          }
      })
     $('.only-crc').html(cc[1])
    },
    currRates:{},
    selected_currency:0,
    otokompliti:function(req,res){
        $.getJSON('/' + this.LANGUAGE_CODE + '/sac/?q=' +req.term, function(data) {
          var items = [];
          $.each(data, function(i) {
              var line = []
              var place = data[i]
             for(var p in place){
                 if(place[p] && line.indexOf(place[p])<0){line.push(place[p])}
             }
              items.push(line.join(', '))
          });
            res(items)
        });

    },
    init_search:function () {
        var self = this
        var sbar = $('#sidesearch')
        var sbardis = $('#searchbar')
        var sbox = $('#searchbox')

        $(window).scroll(function(){
//            console.log($(document).scrollTop(), sbar.hasClass('fixmenu'))
            if($(document).scrollTop()>170 && !sbar.hasClass('fixmenu')){sbar.addClass('fixmenu');sbardis.height(sbox.height())}
            else if($(document).scrollTop()<170 && sbar.hasClass('fixmenu')){sbar.removeClass('fixmenu')}
        })
        $( "#pricediv" ).slider({ range: true,  max: 500, min:20, animate: true,step: 10, values: [1,500],
            change: function(event, ui) {
                var values = $( this ).slider( "option", "values" );
                $('#pmin').val(values[0]);
                $('#pmax').val(values[1]);
                self.jsearch()
            }
        });
        if(window.PIE){
            $('#searchbar .ackapa').mouseenter(function(){PIE.attach(this);})//$(this).css('padding-bottom','50px')}).mouseleave(function(){$(this).removeClass('acik')})
        }
//        $('#searchbar').mouseleave(function(){$('#searchbar .acik').removeClass('acik')})
        $('.vDateField').datepicker({dateFormat: 'yy-mm-dd', minDate: '0', changeMonth: true  });
        $("#id_query").autocomplete({minLength: 1,
            source:function(request, response){
                self.otokompliti(request, response)
            }
        })
        $('#id_query').keydown(function(event){if(event.keyCode == '13')self.jsearch()})
        $('#submit').click(function(){self.jsearch()})
        this.jsearch()
        $('#searchbar li').click(function(){$(this).toggleClass('hit');self.jsearch()}).disableSelection()
    },
    stimers : [],
    playTimedSlides:true,
    setTimedSlides:function(){
        if(!this.playTimedSlides)return
        var self = this;
        if(this.stimers){$.each(this.stimers, function(i,val){clearTimeout(val)});this.stimers=[]}
        var slideset = $('#nasilsunum')
        var son_slide=false
        $.each(slide_timings, function(i,val){
                if(son_slide){
                    return
                }
                if(val<0){son_slide = true; }
                timer= function (sonmu){
                    return setTimeout(function(son_slide){
                        slideset.find('.sunumslide:eq('+i+')').fadeIn(1000).siblings().fadeOut(500)
                        if(sonmu && slide_timings[i+1])setTimeout(function(){self.setTimedSlides()},slide_timings[i+1]*1000)
                        },  Math.abs(val)  * 1000)
                }(son_slide)
                self.stimers.push(timer)
        })
    },
    init_index:function () {
        var self = this;
        this.akGorunur = 0
//        this.sks = {}
        $('#arabg').fadeTo('fast', .5)
        this.doRePlacements();
        this.popmodal('#askquestion', '#questbox', -45, 30)
        $('#questbox .innput').focus(function(){
            var t=$(this);
            if(!t.data('default'))t.data('default',t.val())
            if(t.data('default')==t.val())t.val('')
        }).blur(function(){
                var t=$(this);
                if(!t.val())t.val(t.data('default'))
            })
        this.form_submit_handler($('#questboxdiv'))
        $('#arainput').autocomplete({minLength: 1,appendTo:'#araoneri', source:function(request, response){
                        self.otokompliti(request, response)
                    }
                }).keydown(function(event){if(event.keyCode == '13'){
                $('#id_query').val($('#arainput').val());
                $('#arabg form').submit()
            }})

        $(window).resize(function () {
            self.doRePlacements()
        });
        $('#araf input').focus(function () {
            self.akToggle(0)
        });
        $('#aradugme').click(function () {$('#id_query').val($('#arainput').val());$('#arabg form').submit()});
    //        $('.logo').mouseover(function () {$('.krm').removeClass('krm').addClass('dekrm')}).mouseleave(function () {$('.dekrm').removeClass('dekrm').addClass('krm')});

        $('html').click(function (data) {
//            console.log(data.srcElement, data.target)
            if(data.target.className.indexOf("ui-")>-1)return;
            self.akToggle(1)
        });
        $('#araf, #arabg_cont').click(function (event) {
            event.stopPropagation();
        })

        $('#howitworks a').click(function () {
            $('#howitworks').removeClass('ui-state-active');


        })

        $( "#pricediv" ).slider({ range: true,  max: 500, min:20, animate: true,step: 10, values: [1,500],
            change: function(event, ui) {
                var values = $( this ).slider( "option", "values" );
                $('#pmin').val(values[0]);
                $('#pmax').val(values[1]);
            }
        });
        $('.vDateField').datepicker({dateFormat: 'yy-mm-dd', minDate: '0', changeMonth: true  });

        this.makeScroller(0);
//        this.makeScroller('GVS2', 0);
//        this.makeScroller('GVS3',0);
    },
    playvideo:function(){
        var self = this;
        $.get('/static/howembed.txt', function(data){
            $('#nasilvideo').html(data)
            self.playTimedSlides = true
            self.setTimedSlides()
        })

    },
    sk:null,
    makeScroller:function (id) {
        this.playTimedSlides = false
        var self =this;
        $('#GVS').empty().remove()
        $.get(this.url('slides/'+id), function(data){
            $('div.grit').html('')
            $('#nasilvideo').html('')
            $('#tabs-'+id).html(data)
            if(self.sk)self.sk.smoothDivScroll('destroy')
            self.priceScanConvert()
            var sk = $('#GVS');


            sk.find('.slidiv').mouseenter(
                function () {sld = $(this); sld.find('.sbaner').animate({height:'46px'});}).mouseleave(function(){
                    $(this).find('.sbaner').animate({height:'28px'})
                });


            sk.smoothDivScroll({
    //            hiddenOnStart:hidden,
//                autoScroll:"onstart",
//                autoScrollDirection: "endlessloopleft",
                autoScrollStep:3,
                autoScrollInterval:50,
                visibleHotSpots:"always"
            });
            sk.smoothDivScroll("startAutoScroll").smoothDivScroll("option", "autoScrollDirection", 'endlessloopleft')
            sk.find('div.scrollingHotSpotRight').mouseleave( function () {
                sk.smoothDivScroll("option", "autoScrollDirection", 'endlessloopright').smoothDivScroll("startAutoScroll")
            })

            sk.find('div.scrollingHotSpotLeft').mouseleave(function () {
                sk.smoothDivScroll("option", "autoScrollDirection", 'endlessloopleft').smoothDivScroll("startAutoScroll")
            });
            sk.find('.scrollableArea .slidiv').mouseenter(function () {
                sk.smoothDivScroll('stopAutoScroll')}).mouseleave(function () {
                    sk.smoothDivScroll('startAutoScroll')
            })
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
//        this.rePlace('#araf', '#mhtabela', 720, -65, 1);
        this.rePlace('#araf', '#arabg_cont', -27, 20);
    },
    rePlace:function (src_id, trg_id, off_left, off_top, show) {
        // re-place the target object relatively to src object.
        var trg = $(trg_id), sof = $(src_id).offset();
        if (typeof(show) != 'undefined' && show == 1) trg.fadeIn('fast');
        var ntop = sof.top + off_top, nleft = sof.left + off_left;
        trg.css({top:ntop, left:nleft});
    },
    changeForm:function(id,static_header){
        var self = this;
        $('#wfContainer').scrollTo('#form'+id,800);
        if(typeof(static_header)=='undefined'){
            $('.wfhdr').fadeTo(400, 0)
            $('#wfhdr'+id).fadeTo(800, 1)
        }
    },
    gcGosterGizle:function(){
        $('#adres_form').toggleClass('to_neverland');
        $('#adres_harita').toggleClass('to_neverland');
        return false
    },
    //////////////////////////////////////////////////////
    ////////////////////MAPPPS - GEOCODING////////////////
    //////////////////////////////////////////////////////
    gmapsLoad:function(initFunc){
        var self = this
            this.setLatLon()
        if(typeof(initFunc)=='undefined')initFunc='gh.gcinit';
            $.getScript('http://maps.googleapis.com/maps/api/js?sensor=false&callback='+initFunc)

    },
    //FIXME: lat lon should be came from geoip!!!
    lat:38.434,
    lon:27.125,
    glatlng:'',
    gZoom:8,
    setLatLon:function(){
        if($('#id_lat').val()!='0.0')this.lat = $('#id_lat').val().replace(',','.')
        if($('#id_lon').val()!='0.0')this.lon = $('#id_lon').val().replace(',','.')
    },
    getLatLon:function(l){
            $('#id_lat').val(l.lat())
            $('#id_lon').val(l.lng())
    },
    markerMaps:function(){
        var self = this;
//        console.log(self)
        this.gmapsLoad('gh.gcinit')
    },
    placeMarkerGoto:function (marker,id){
        var self=this;
        google.maps.event.addListener(marker, 'click', function() {self.gotoplace(id) });
    },
    searchMap:function(){
        var self=this;
        this.gZoom = 11;
        this.gcinit(true)
        for(i=0 ;i<this.search_results.length;i++){
            var d = this.search_results[i]
            if(d.index){
                var image = new google.maps.MarkerImage('/static/images/markers/marker' + (d.index) + '.png',
                                      new google.maps.Size(20, 34),
                                      new google.maps.Point(0, 0),
                                      new google.maps.Point(10, 34));
                var myLatLng = new google.maps.LatLng(d.lt, d.ln);
                var marker = new google.maps.Marker({
                  position: myLatLng,
                  map: this.map,
                  icon: image,
                  title: d.tt,
                  zIndex: i+1
                });
                this.placeMarkerGoto(marker, d.id)

            }
        }
    },
    _circleMaps:function(){
        this.gmapsLoad('gh.drawCircle')
    },
    gotoplace:function(id){
        document.location=this.url('places/'+id)
    },
    drawCircle:function(){
        this.gZoom = 14;
        this.gcinit(true);

        var mapOptions = {
          strokeColor: "#FF0000",
          strokeOpacity: 0.8,
          strokeWeight: 2,
          fillColor: "#FF0000",
          fillOpacity: 0.35,
          map: this.map,
          center: this.glatlng,
          radius: 500
        };
        cityCircle = new google.maps.Circle(mapOptions);
    },
    gcinit:function(nomarker){
        this.geocoder = new google.maps.Geocoder();
        this.glatlng = new google.maps.LatLng(this.lat,this.lon);
//        console.log(this.glatlng,this.lat,this.lon)
        var myOptions = { zoom: this.gZoom, center: this.glatlng, mapTypeId: google.maps.MapTypeId.ROADMAP, mapTypeControl:false, streetViewControl:false }
        this.map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
        if(typeof(nomarker)=='undefined')this.marker = new google.maps.Marker({ map: this.map, position: this.glatlng, draggable: true });
        this.infoWindow = new google.maps.InfoWindow()
    },
    popup_html:'<a id="adresikullan" href="javascript:void(0)" onclick="gh.gcAdresTamam()">Bu adresi kullan</a>',
    geocodeAddress: function () {
        var self = this;
        this.geocoder.geocode( { 'address': $('#id_address').val()}, function(results, status) {
          if (status == google.maps.GeocoderStatus.OK) {
//              a=results[0].geometry.location
            self.map.setCenter(results[0].geometry.location);
            self.gcResult = results[0];
            self.infoWindow.setContent(results[0].formatted_address+self.popup_html)
            self.marker.setPosition(results[0].geometry.location)
            self.infoWindow.open(self.map, self.marker);

          } else {
            alert("Adres bulunamadı, lütfen girdiğiniz bilgileri gözden geçirip tekrar deneyiniz.\n\nHata Kodu: " + status);
          }
        });
      },
    getGCResult:function(){return this.gcResult;},
    gcAdresTamam:function(){
        acs = this.gcResult.address_components
        this.getLatLon(this.gcResult.geometry.location)
        for (i in acs){
            var ac = acs[i]
            var typ = ac.types[0]
//            console.log(ac.long_name, typ)
            if(typ=='country')$('#id_country').val(ac.short_name)
            if(typ=='route')$('#id_street').val(ac.long_name)
            if(typ=='neighborhood')$('#id_neighborhood').val(ac.long_name)
            if(typ=='postal_code')$('#id_postcode').val(ac.long_name)
            if(typ=='administrative_area_level_2')$('#id_district').val(ac.long_name)
            if(typ=='administrative_area_level_1')$('#id_state').val(ac.long_name)
            if(typ=='locality')$('#id_city').val(ac.long_name)
        }
        this.gcGosterGizle()
    },
    //////////////////////////////////////////////////////
    ////////////////////ENDO OF MAPPPS - GEOCODING////////
    //////////////////////////////////////////////////////
    isUnAvailable:function(d){
        var d = parseInt($.datepick.formatDate('yymmdd', d));
        return $.inArray(d,gh_rdts) >-1
    },
    sessional_prices:{},
    convertPrice:function(prc,cid){
        if(typeof(cid)=='undefined')cid = gh_prcs[3]
        return (this.currRates[cid] * prc).formatMoney(2, ',', '.')
    },
    prepareSessionalPrices:function(){
        if(gh_prcs[0].length>0){
            for (p in gh_prcs[0]){
                p = gh_prcs[0][p]
                //p = [start_date_array(yyyy,mm,dd), end_date_array, price, weekend_price]
                var loopDate = new Date(p[0][0],p[0][1]-1,p[0][2]);
//                console.log(p)
                var endDate = new Date(p[1][0],p[1][1]-1,p[1][2]);
                while (loopDate.valueOf() < endDate.valueOf() + 86400000) {
//                    sessional_prices[p[0].toString().substring(2) + p[1].toString() + p[2].toString()] = ''
                    this.sessional_prices[$.datepick.formatDate('yymmdd', loopDate)] =
                        (loopDate.getDay() in [0,6] && p[3]) ? p[3] : p[2]
                    loopDate.setTime(loopDate.valueOf() + 86400000);
                }
            }
        }
    },
    total:{ndays:0, price:0.0},
    calculateTotalPrice:function(){
//        console.log(this.total.price)
        if(this.total.price){

            var tprice = this.total.price
            if(mdiscount && this.total.ndays >=30) {
                var mdisc = tprice * mdiscount / 100
                tprice =tprice -  mdisc
                $('#mdiscount').show('normal').find('span').html('-'+this.getCurrPrice(this.convertPrice(mdisc)))
                $('#wdiscount').hide('normal')
            }
            else if(wdiscount && this.total.ndays >=7) {
                var wdisc = tprice * wdiscount / 100
                tprice =tprice -  wdisc
                $('#wdiscount').show('normal').find('span').html('-'+this.getCurrPrice(this.convertPrice(wdisc)))
                $('#mdiscount').hide('normal')
            }
            var tprice = tprice + cleaning_fee + (tprice*service_fee/100)
            var nog = parseInt($('#id_no_of_guests').val())
            if(exlimit < nog) tprice = tprice + (exprice * (nog-exlimit))
            if (cleaning_fee){
                $('#cleaningfee').show('normal').find('span').html(this.getCurrPrice(this.convertPrice(cleaning_fee)))
            }
            if (service_fee){
                $('#servicefee').show('normal').find('span').html(this.getCurrPrice(this.convertPrice(tprice*service_fee/100)))
            }
            $('#totalPriceValue').html(this.getCurrPrice(this.convertPrice(tprice)))
            $('#displayed_price').val(tprice)
            $('#ndays').val(this.total.ndays)
            $('#currencyid').val(this.selected_currency)
        }
    },
    checkReservationDates:function(dates){
        var loopDate = new Date();
        loopDate.setTime(dates[0]);
        if(dates[0])$.cookie('selected_dates', $.toJSON(dates))
        $('#id_checkin').val($.datepick.formatDate('yyyy-mm-dd', dates[0]))
        $('#id_checkout').val($.datepick.formatDate('yyyy-mm-dd', dates[1]))
        this.total = {ndays:0, price:0.0}
        try{
            var days=1 ,price=0.0;
            while (loopDate.valueOf() < dates[1].valueOf() + 86400000) {
//                console.log(loopDate.getDay())
    //            sdate = $.datepick.formatDate('yymmdd', loopDate)
                if (this.isUnAvailable(loopDate)){
                    $('#pcalendar').datepick('setDate',-1);
                    $('.vDateField').val('')
                    this.selected_dates = {}
                    throw 'unv_dates';
                }
                else{
                    days ++;
                    price += this.dPrice(loopDate)
                }
                loopDate.setTime(loopDate.valueOf() + 86400000);
            }
        }catch(er){
            if(er=='unv_dates'){
                alert(trns('dates_not_available') );
                $.cookie('selected_dates','')
            }
        }
        this.total.ndays = days-1
        this.total.price = price
        this.calculateTotalPrice()
    },
    dPrice:function(d){
        return this.sessional_prices[$.datepick.formatDate('yymmdd', d)] ||
            ((d.getDay() in [0,6] && gh_prcs[2]) ? gh_prcs[2] : gh_prcs[1])
    },
    dayPrice:function(d){
        return this.convertPrice(this.dPrice(d))
    },
    makeAvailabilityTab:function(destroy){
        var self = this
        if(typeof(destroy)!='undefined')$('#pcalendar').datepick('destroy')
        $('#pcalendar').datepick({monthsToShow:2, minDate:0,  rangeSelect: true,
            onSelect: function(dates) { self.checkReservationDates(dates)},
            onDate: function(date, current){
                return self.isUnAvailable(date) ?
                    {selectable:false, dateClass:'datepick-reserved'} : { content:
                date.getDate() + '<br><sub>' + self.dayPrice(date) + '</sub>'}
            }

        });

    },
    bookPlace: function(e){
        cin = $('#id_checkin').val()
        cout = $('#id_checkout').val()
        if(!cin || !cout){
            $('#info-select-dates').removeClass('gizli').fadeTo(300,0.3).fadeTo(800,1)
            return false
        }
        if(this.total['ndays']<min_stay){
            $('#info-stay-more').removeClass('gizli').fadeTo(300,0.3).fadeTo(800,1)
            return false
        }
        if(max_stay>0 && this.total['ndays']>max_stay){
            $('#info-stay-less').removeClass('gizli').fadeTo(300,0.3).fadeTo(800,1)
            return false
        }
        $(e.target).parents('form').submit()
    },
    get_bookmarks:function(){
        return ($.cookie('ganibookmarks') || '').split(',')
    },
    is_bookmarked:function(id){
      return this.get_bookmarks().indexOf(id)>-1
    },
    bookmark:function(caller){
        var self = this
        if(!AUTH){
            this.setMessage('login_for_bookmark',function(){self.gotoLogin()})
            return
        }

        var pid = $('#placeid').val()
        var data ={'pid':pid}
        var caller = $(caller)
        var bookmark_array = this.get_bookmarks()
        if (bookmark_array.indexOf(pid)>-1 ){
            data['remove']=1
            caller.removeClass('bookmarked')
            bookmark_array.splice(bookmark_array.indexOf(pid),1)
        }else {
            caller.addClass('bookmarked')
            bookmark_array.push(pid)
        }
        $.cookie('ganibookmarks', bookmark_array.join(','), {expires:1234});
        $.post('/bookmark/',data)
    },
    sendMessageToHost:function(){
        var self = this
        var pid = $('#placeid').val()
        var msgbox = $('#hostmsg')
        if (!msgbox.val())return
        var sendbutton = $('#sendhostmessage')
        var data ={'pid':pid, 'message': msgbox.val()}
        sendbutton.prop('disabled', true)
        $.post('/'+this.LANGUAGE_CODE+'/send_message_to_host/',data,function(result){
            if(result.message){
                msgbox.addClass('sent','slow').val(result.message).prop('disabled', true)
                sendbutton.fadeOut(500)

            }
        })
        if(!AUTH){
            this.setMessage('login_for_sendmessage',function(){self.gotoLogin()})
            return
        }

    },
    setMessage:function(msg,fn){
        $.post('/'+this.LANGUAGE_CODE+'/set_message/'+msg,function(data){
            if(fn)fn(data)
        })
    },
    gotoLogin:function(next){
        if(typeof(next)=='undefined')next = document.location.pathname
        document.location = '/'+this.LANGUAGE_CODE+'/login/?next='+next
    },
    init_places:function(){
        var self = this;
        x={}
        var s=0;
        $('#amenul .mhelp').easyTooltip()


        $('#toptabs').tabs();

        $('#availtrans img').click(function(){
            var pid = $('#placeid').val()
            $.get('/place_translation/'+pid + '/' + $(this).data('lang') + '/', function(data){
                $('#descdiv').html(data[0])
                $('#titlediv').html(data[1])
            }  )
        })


//        $('#uygtab').click(function(){})

        $('#addbookmark').click(function(){self.bookmark(this)}).addClass(
        this.is_bookmarked($('#placeid').val()) ? 'bookmarked' : ''
        )
        $('#contacthost').click(function(){
            $('#hostbox').addClass('write')
        })
        $('#sendhostmessage').click(function(){self.sendMessageToHost()})
        $('#id_no_of_guests').change(function(){self.calculateTotalPrice()})


        this.setLatLon()
        this.currentImg = $('.pthumb').first()
        $('#bookitbutton').click(function(e){return self.bookPlace(e)})
        $('.pthumb').click(function(){return self._gotoNextPhoto(this)})
        $('#phimg').click(function(){self._changePlacePhoto(ez)})
        $('#openmap').click(function(){self._circleMaps()})
        $('#photoslider-right').click(function(){self._changePlacePhoto()})
        $('#photoslider-left').click(function(){self._changePlacePhoto('prev')})
        $(window).resize(function(){self.replace_pricetag()}).trigger('resize')
        $.getScript(this.STATIC_URL + 'datepick/jquery.datepick.js',function(){
            $.getScript(self.STATIC_URL + 'datepick/jquery.datepick-'+self.LANGUAGE_CODE+'.js',function(){
                self.makeAvailabilityTab()
                self.prepareSessionalPrices()
                var dates = $.cookie('selected_dates')
                if(dates){
                    dates=$.evalJSON(dates)
                    $('#pcalendar').datepick('setDate',new Date(dates[0]),new Date(dates[1]))

                }
            })



            $('.vDateField').datepicker({dateFormat: 'yy-mm-dd', minDate: '0', changeMonth: true ,
                beforeShowDay: function(date) { return self.isUnAvailable(date) ? [false,'datepick-reserved','']:[true,'',''] },
                onSelect: function(dateText, inst) {
                    self.selected_dates[$(this).attr('id')] = $(this).datepicker("getDate")
                    if(self.selected_dates.id_checkin || self.selected_dates.id_checkout){
                        if(self.selected_dates.id_checkin && !self.selected_dates.id_checkout)self.selected_dates.id_checkout=self.selected_dates.id_checkin
                        else if(self.selected_dates.id_checkout && !self.selected_dates.id_checkin)self.selected_dates.id_checkin=self.selected_dates.id_checkout
                        $('#pcalendar').datepick('setDate',self.selected_dates.id_checkin,self.selected_dates.id_checkout)
                    }
                }

            });

        })
    this.init_social_plugins()
    },
    init_social_plugins:function(){
        (function(d, s, id) {
          var js, fjs = d.getElementsByTagName(s)[0];
          if (d.getElementById(id)) {return;}
          js = d.createElement(s); js.id = id;
          js.src = "//connect.facebook.net/en_US/all.js#xfbml=1";
          fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
        $.getScript("https://apis.google.com/js/plusone.js")

    },
    selected_dates:{},
    replace_pricetag : function(){this.rePlace('#titlediv', '.fetiket', 615, -3);},

    _gotoNextPhoto:function(current_photo){
        var next
//        xx=this
//        return false;
        current_photo = $(current_photo)
        this._changePlacePhoto(current_photo)
        if($("#photoslider_container li").length > current_photo.index() + 1){
            next = '+='+ current_photo.find('img').width() +'px';
        }else next = $('#photoslider_container li').first()

        $('#photoslider_container').scrollTo(next, 800);
        return false
    },
    _changePlacePhoto:function(ob){
        if(typeof(ob)=='undefined')ob = this.currentImg.next()
        else if(ob=='prev')ob = this.currentImg.prev()
        if(ob.html()){
            this.currentImg = ob
            var url = "url("+ob.find('a').attr('href')+") no-repeat center center"
            $('#phimg').fadeTo(100,0,function(){
                $('#phimg').css('background', url).fadeTo(100,1)
            })
        }
    },
    upload_init:function(place_id){
        var self = this;
        self.uploadeds = place_photos
        if(typeof(place_id)=='undefined')place_id=''
        $('#uploaded').sortable({update: function(event, ui) {
            var iids = []
            $('#uploaded div').each(function(index) {iids[index] = this.id.replace('img_','');});
            self.uploadeds = iids
            $.post('/'+self.LANGUAGE_CODE+'/dashboard/save_photo_order/'+place_id, {iids:JSON.stringify(iids)})
        }})
        self.renderUpPlacePhotos()
        $.getScript(this.STATIC_URL+'js/jquery.fileupload.js', function(){

        $('#fileupload').fileupload({
               dataType: 'json',
               url: '/upload_photo/'+place_id,
               done: function (e, data) {
//                   console.log(data)
                   self.uploadeds.push(data.result[0].id)
                   self.renderUpPlacePhotos()
//                   $.each(data.result, function (index, file) {
//                       $('<img />').attr('src',(file.turl)).attr('id','img_'+file.id).dblclick(function(){
//                           $.post('/delete_photo/'+file.id,function(data){$('#img_'+file.id).hide('slow')})
//                       }).appendTo('#uploaded');
//                   });

               }
           });
        })
    },
    profile_upload_init:function(){
        var self = this;

        $.getScript(this.STATIC_URL+'js/jquery.fileupload.js', function(){

        $('#pfoto').fileupload({
               dataType: 'json',
               url: '/dashboard/pfoto/',
               done: function (e, data) {
                   src = $('#pfotoimg').attr('src').split('?')[0]
                   $('#pfotoimg').attr('src',src + '?rnd='+Math.random())


               }
           });
        })
    },
    renderUpPlacePhotos:function(){
        var self = this
        $("#uploaded").html($("#upPlacePhotosTpl").jqote(this.uploadeds))
        $('#uploaded .delete').click(function(){
            imgid = $(this).data('imgid')
           $.post('/delete_photo/'+imgid,function(data){
               $('#img_'+imgid).hide('slow')
               self.uploadeds.splice(self.uploadeds.indexOf(imgid),1)
           })
        })
    },
    init_login: function(){this.tosUrl()},
    init_register: function(){this.tosUrl()},
    tosUrl:function(){
        $('#regtoslabel  a').attr('href', this.url('13/tos')).attr('target','_blank')
        $('.registerform').submit(function(){
            if(!$('#regtoscheck').prop('checked')){
                alert(JSTRANS.accept_terms_of_service)
                return false;
            }
        })
    },
//        $('html').click(function (data) {
//            $('#uyekapsar').addClass('silik');
//        });
//        $('#uyekapsar').click(function (event) {
//            event.stopPropagation();
//        })
//        $('#uyeol input').focus(function(){
//            $('#uyekapsar').removeClass('silik');
//        })
//        $('#uyeol').mouseenter(function(){
//            $('#uyekapsar').removeClass('silik');
//        })
//    },
    ecordion_state:{},
    ecordion:function(cont){
        var self = this
        $(cont+" > li > div").click(function(){
            $(this).addClass('focused').parent().siblings().find('div').removeClass('focused')
            if(false == $(this).next().is(':visible')) {
                $(cont+" ul").slideUp(300);
            }
            $(this).next().slideToggle(300);

            return false;
        });
        var cnt = cont.replace('#','')

        //expand/collapse all
        this.ecordion_state[cnt]=0
        return function(state){
//            console.log(self.ecordion_state)
            var sel = $(cnt+' li > ul')
            if (typeof(state)!='undefined')self.ecordion_state[cnt] = state
            if (!self.ecordion_state[cnt]){
                sel.slideDown(300);
                self.ecordion_state[cnt]=1
            }else{
                sel.slideUp(300);
                self.ecordion_state[cnt]=0
            }
            return self.ecordion_state[cnt]
        }


    },
    init_faq:function(){
        $('#litetabs').tabs()
        var fn2 = this.ecordion('.faqcats')
        var fn1 = this.ecordion('.faqcat')
            $('#litetabs .expclp').click(function(){
                $('#litetabs .expclp').toggleClass('expanded')
              if(fn1()==1)fn2(0)
            })
        this.form_submit_handler($('#questboxdiv'))

    },
    dialog:function(id){
        return $(id).dialog({ position: 'center', modal: true  })
    },
    init_dashboard: function(){
        var self = this;

        this.ecordion('#menuccordion')
        var meco =$('#menuccordion')
        $(window).scroll(function(){
//            console.log($(document).scrollTop(), meco.hasClass('fixmenu'))
            if($(document).scrollTop()>170 && !meco.hasClass('fixmenu')){meco.addClass('fixmenu')}
            else if($(document).scrollTop()<170 && meco.hasClass('fixmenu')){meco.removeClass('fixmenu')}
        })
//        this.box = $('#dlg').dialog({ position: 'center', autoOpen:false, modal: true  })
        $('.btn').click(function(data){
            var target_div=''
            $(data.target).parents('.btn').andSelf().each(function(){
                if(typeof($(this).attr('class'))=='string' &&
                    $(this).attr('class').indexOf('btn')>=0){
                    target_div=$(this);
                }
            })
            if (target_div){
                var param = target_div.data('param')
                $(target_div.attr('class').split(' ')).each(function(){
                    if(this.indexOf('show_')==0){

                        self.showFrame(this.split('show_')[1])
                    }
                    if(this.indexOf('do_')==0){
                        if (param)self[this](self,param)
                        else self[this](self)
                    }
                })
                }
            });
        self.hashCall()
//        self.loadTemplate('dashboard_place_listing.tpl',function(){})
//        this.editPrices(2)
//        this.editAvailability(2)
    },
    hashCall:function(){
        var hs = []
        if(document.location.hash){
            var hs = document.location.hash.replace('#','').split(',')
        }
        else if(document.location.search){
//            console.log(document.location.search)
            var hs = document.location.search.replace('?','').split('=')
        }
        if(typeof(hs[0])!='undefined'){
            if (typeof(hs[1])!='undefined'){
                if(hs[1]=='this')hs[1] = this
                this[hs[0]](hs[1])
            }
            else this[hs[0]]()
        }
    },
    TEMPLATES:{},
    loadTemplate:function(tpl_file,fn){
        var self = this
        if(!this.TEMPLATES[tpl_file]){
            $.get('/templates/'+tpl_file, function(doc) {
                    self.TEMPLATES[tpl_file] = $.jqotec(doc);
                    if(fn)fn()
            });
        }
        return this.TEMPLATES[tpl_file]
    },
    showFrame:function(target,data){

        $('div.dbcontent').hide()
        if(typeof(target)=='string') target = $('#'+target)
        if(typeof(data)!='undefined' && data!='')target.html(data)
        target.show('normal')

        if (window.PIE) {
            $('.piee').each(function () {
                PIE.attach(this);
            });
        }
        return target
    },
    new_place_wizard_html:'',
    add_place_url:function(id){
        return '/' + this.LANGUAGE_CODE + '/add_place_ajax/' +
            (typeof(id)=='undefined' ? '' : id)
    },
    search_url:function(){ return '/' + this.LANGUAGE_CODE + '/jsearch/'},
    do_dbAddPlaceWizzard:function(self){
        var frm=$('#addplace_wizard')
//        console.log('wwwwjmm')
        var icerik = frm.html()
        if (!icerik||icerik.indexOf('npw-flag')==-1){
//            console.log('aajmm')
            if(!self.new_place_wizard_html){
                self.showFrame('loading')
                $.get(self.add_place_url(),function(data){
                    self.new_place_wizard_html = '<!--npw-flag-->'+data
                    self.showFrame(frm,self.new_place_wizard_html)
                    self.init_placeWizzard()
                })
            }else {
//                console.log('jmm')
                self.showFrame(frm,self.new_place_wizard_html)
                self.init_placeWizzard()
            }

        }else self.showFrame(frm)
    },
    getCurrentCurrency:function(){
        return gh_crc[this.selected_currency]
    },
    setSearchPrices:function(data){
        var lats=0.0, lons=0.0, say=0
        for(i in data){
            if(data[i].lt){
                lats=lats + parseFloat(data[i].lt)
                lons=lons + parseFloat(data[i].ln)
                say = say+1
                data[i].index = say;
            }
            var prc = this.convertPrice(parseFloat(data[i].prc),data[i].cid)
            cc = this.getCurrentCurrency()
            currency = "<span class='gcrc'> "+cc[2]+" </span>"
            cprc = prc.split(',')
            prc = cprc[0].length<6 ? cprc[0] + " <span class='decimal'>,"+cprc[1]+"</span>" : cprc[0]
            prc = "<span class='gprc'>"+prc+"</span>"
            data[i].price = cc[3]==1 ? currency + prc : prc + currency
        }
        if(!isNaN(lats))$('#id_lat').val(   lats/say)
        if(!isNaN(lons))$('#id_lon').val(lons/say)
        this.search_results = data
        return data
    },
    jsearch:function(){
        var self=this
        $('#searchbar .kapsar').each(function(){
                var keys = []
                $(this).find('li.hit').each(function(){keys.push($(this).data('ids'))})
                $('#ids_'+$(this).data('key')).val('['+keys.join(',')+']')
        })
        $('#scurrency').val(this.selected_currency)
        $.post('/jsearch/', $("#search_form").serialize(),function(data){
        data =self.setSearchPrices(data)
//        console.log(data)
        $("#resul").html($("#wideResultsTpl").jqote(data));
            self.gmapsLoad('gh.searchMap')
            //FIXME: haritayi tekrar tekrar yukluyor
        });

    },
    markReqFields:function(container_id, label_fors){
        if(typeof(label_fors)=='undefined'){
            $("#"+container_id+" label").append('<span class="redstar">*</span>')
            $("#"+container_id).find('input, select').data('required','1')
        }
        else{
            for(l in label_fors){
                $("#"+container_id+" label[for=id_"+label_fors[l]+"]").each(function(){
                    $(this).append('<span class="redstar">*</span>')
                })
            $("#"+container_id+" #id_"+label_fors[l]).data('required','1')
            }
        }

    },
    checkReqFields:function(selector){
        var req_missing = false
        $(selector).find('input, select').each(function(){
            var ob = $(this)
            if(ob.data('required') && !ob.val()){
                ob.addClass('reqmissing')
                req_missing = true
                ob.blur(function(){
                    if($(this).val())$(this).removeClass('reqmissing')
                })
            }
        })
        if(req_missing){
            alert(trns('place_fill_all_req_fields'))
            $('#form1 .reqmissing').first().focus()
            return false
        }
        return true
    },
    init_add_place:function(place_id){
        var self = this;
        $( "#paccordion").accordion({ autoHeight: false, collapsible: true });
        $('#id_address').keydown(function(event){if(event.keyCode == '13')self.geocodeAddress()});
        $('#addrFindBut').click(function(){self.geocodeAddress()});
        $('#gotodetails').click(function(){
            if(self.checkReqFields('#form2')){
                self.changeForm(3);
            }
        });
        $('#gotomap').click(function(){
            if(self.checkReqFields('#form1')){
                self.changeForm(2);
                self.markerMaps();
            }
            return false
        });
        $('#id_currency').val(this.selected_currency).change(function(){
            self.setCurrency(parseInt($(this).val()))
        })
        $('#id_price').keyup(function(){
            var pr = $(this).val()
            try{
                pr =  pr * ((100-host_fee)/100)
                if (isNaN(pr))throw 'NaN'
            }
            catch(er){
                pr = ''
            }

            $('#yprice').html(self.getCurrPrice(pr.formatMoney(2, ',', '.')))
        })
        $('#id_price').trigger('keyup')
        $('#apbutton3').click(function(){$('#addplaceform').submit()});
        this.markReqFields('form1')
        this.markReqFields('form2',['country','city','street'])
        this.upload_init(place_id)
        self.changeForm(1)
//        $('#uploaded img').dblclick(function(){
//            $.post('/delete_photo/'+$(this).attr('id').replace('img_',''),function(data){$('#img_'+data).hide('slow')})
//        })
    },
    init_placeWizzard:function(place_id){
        if(typeof(place_id)=='undefined')place_id=''
        var self=this
        $('#addplaceform').submit(function(){
            $.post(self.add_place_url(place_id), $("#addplaceform").serialize(),function(data){
                if(data.new_place_id>0)self.do_listPlaces(self)
                else self.showFrame('results','<div class="error">Error occured. Code : '+data.errors+'</div>')
                $("#addplaceform").html()
            });
            return false;
        })
        $('#id_currency').change(function(){
            self.setCurrency(parseInt($(this).val()))
        })
        this.init_add_place(place_id)
    },
    editPlaceWizzard:function(id){
        var self = this
        this.showFrame('loading')
        $.get(this.add_place_url(id)    ,function(data){
            self.showFrame('addplace_wizard',data)
            self.gcGosterGizle()
            self.init_placeWizzard(id)


            self.setLatLon()
        })
    },
    translateStrings:function(container){
        if(typeof(container)=='undefined')container=''
        $(conatiner + ' .trans').each(function(){
            t = $(this)
            t.html(JSTRANS[t.data('trans')])
        })
    },
    do_listPlaces:function(self){
        this.genericEdit('/dashboard/list_places/')


    },
    durl:function(cmd){
        return ('/'+this.LANGUAGE_CODE + '/dashboard/' + cmd + '/').replace('//','/')
    },
    url:function(cmd){
        return ('/'+this.LANGUAGE_CODE +'/'+ cmd + '/').replace('//','/')
    },
    publishPlace:function(id){
        var self = this;
        $.post(this.durl('publish_place'),{'id':id},function(data){
            if(data.url)document.location = data.url
            else if(data.message){
                self.do_listPlaces()
                alert(data.message)
            }
        })
    },
    deletePlace:function(id){
        var self = this;
        $.post(this.durl('delete_place'),{'id':id},function(data){
            self.do_listPlaces()
            if(data.message)alert(data.message)
        })
    },
    showBookingRequest:function(id){
        this.genericEdit('/dashboard/show_booking/'+id)
    },
//    confirmBooking:function(id){
//        $.post(this.durl('confirm_booking'),{'id':id},function(data){
//            self.do_listPlaces()
//            if(data.message)alert(data.message)
//        })
//    },
//    show_message:function(m){
//        md = $('#message')
//        md.find('span').html(m)
//        md.fadeTo(300,0.0).fadeTo(800,1).fadeTo(300,0.3).fadeTo(300,1)
//    },
    do_editProfile:function(self){
        this.genericEdit('/dashboard/edit_profile/',function(){
            $('#id_brithdate').datepicker({dateFormat: 'yy-mm-dd', maxDate: '0',
                            changeMonth: true  ,changeYear: true , yearRange: '1910:2012' });
        })
    },
    do_trips:function(self, tab_id){
        this.genericEdit('/dashboard/trips/',function(){
            $('#litetabs').tabs({ selected: tab_id })
        })
    },
    do_showRequests:function(self, tab_id){
        this.genericEdit('/dashboard/show_requests/',function(){
            $('#litetabs').tabs({ selected: tab_id })
        })
    },
    do_showReviews:function(self, tab_id){
        this.genericEdit('/dashboard/show_reviews/')
    },
    showMessage:function(id){
        this.genericEdit('/dashboard/show_message/'+id)
    },
    addFriend:function(id){
        $.post('/'+this.LANGUAGE_CODE+'/dashboard/add_friend/'+id,function(data){
            $('#friendshipbox').html(data.message)
        })
    },
    confirmFriendship:function(id){
        message_id = $('#mid').val()
        $.post('/'+this.LANGUAGE_CODE+'/dashboard/confirm_friendship/',{'id':id, 'mid':message_id},function(data){
            $('#accdecfriend').html(data.message)
        })
    },
    sendMessage:function(id){
        this.genericEdit('/dashboard/new_message/'+id)
    },
    do_editPayment:function(self){
        this.genericEdit('/dashboard/edit_payment/',function(){
            $('#generic input:radio').click(function(){
                $('.ptforms').hide()
                $('#form_'+this.id).show()
            })
//            optionElements= $('#id_country')
//            var options = jQuery.makeArray(optionElements).
//                                   sort(function(a,b) {
//                                     return (a.innerHTML > b.innerHTML) ? 1 : -1;
//                                   });
//              selectElement.html(options);
              $('#id_country').change(function(){
                  var ob=$(this)
                  if (iban_countries.indexOf(ob.val())>-1)$('#detailed').hide()
                  else $('#detailed').show()
              }).trigger('change')
//            $('#pt'+current_payment_selection).trigger('click')


        })
    },
    do_showMessages:function(self){
        this.genericEdit('/dashboard/show_messages/')
    },
    do_showFriends:function(self){
        this.genericEdit('/dashboard/friends/')
    },
    do_supportCreate:function(self){
        this.genericEdit('/dashboard/support_create/')
    },
    do_changePassword:function(self){
        this.genericEdit('/dashboard/change_password/')
    },
    do_inviteFriend:function(self){
        this.genericEdit('/dashboard/invite_friend/')
    },
    do_showFaq:function(self){
        var self = this
        this.genericEdit('/dashboard/show_faq/',function(){
            self.init_faq()
        })
    },
    editAvailability:function(place_id){
        var self = this
        $('#un-avail').remove() //FIXME: bu gecicicozum
        $.datepick = {regional:{},setDefaults:function(lang){self.cal.lang = lang}}
        this.genericEdit('/dashboard/calendar/'+place_id,function(){
            $.getScript(self.STATIC_URL + 'js/jquery.calendar-widget.js',function(){
          $.getScript(self.STATIC_URL + 'datepick/jquery.datepick-'+self.LANGUAGE_CODE+'.js',function(){
              self.initCal()
          })
//            $.each($.datepick.regional,function(e,v){self.cal.lang=v})

        })
        })
    },
    editDescription:function(id){
        var self = this
        this.genericEdit('/dashboard/edit_description/'+id,function(){
            self.ecordion('#desccordion')

        })
    },
    cal : {
        start : '', end : '',
        obj:'#takvim',
        requested_dates : [],
        booked_dates : [],
        reserved_dates : [],
        selected_dates : []
    },
    initCal:function(){
        var self = this
        for(i=0;i<12;i++)$("#takvim").calendarWidget({ month: i, year: 2012 ,
            monthNames: this.cal.lang.monthNames,
            dayNames: this.cal.lang.dayNamesShort,
            firstWeekDay: this.cal.lang.firstDay
        }).disableSelection();
        $(this.cal.obj).find('td.current-month').click(function(){
        if(!self.cal.start) self.cal.start = this.id
        else{
            if(!self.cal.end) self.cal.end = this.id
            else {
                self.cal.start = this.id
                self.cal.end = ''
            }
        }
        if (self.cal.start && self.cal.end){
            self.askWhatToDo()
        }
    }).hover(function(){
                if (self.cal.start && !self.cal.end){
                    self.tempSelect(this.id)
                }
            })

      for (i in this.cal.reserved_dates){
          d = this.cal.reserved_dates[i]
          this.cal.start = '20' + d[0]
          this.cal.end = '20' + d[1]
          if(d[2]==1)typ = 'unavail'
          else if(d[2]==2)typ = 'requested'
          else if(d[2]==3)typ = 'booked'
          this.selectAvailDates(typ)
      }
    },
    tempSelect:function(end){
        end = parseInt(end.replace('i',''));
        var start = parseInt(this.cal.start.replace('i',''))
        if (start>end) {var e = end; end = start; start = e }
        $(this.cal.obj).find('td.calhvr').removeClass('calhvr')
        for(i=start;i<=end;i++)$(this.cal.obj).find('#i'+i).addClass('calhvr')
    },
    askWhatToDo:function(){
        $('#un-avail').dialog({modal:true, minWidth: 400, minHeight: 150})
    },
    selectAvailDates:function(availability, save){
        $('#un-avail').dialog('close')
        $(this.cal.obj).find('td.calhvr').removeClass('calhvr')
        var end = this.cal.end, start = this.cal.start
        end = parseInt(end.replace('i',''));
        start = parseInt(start.replace('i',''))
//        console.log(start,end)
        if (start>end) {var e = end; end = start; start = e }
        for(i=start;i<=end;i++)$(this.cal.obj).find('#i'+i+':not(.booked)').addClass(availability).removeClass(availability=='avail' ? 'unavail' : 'avail')
        if(save)this.saveUnavailableDates()
    },
    saveUnavailableDates:function(){
        var start =0, end=0, self=this, seldates = []
        $('#takvim td.current-month').each(function(){
            if($(this).hasClass('unavail')){
                if(!start)start = this.id
                end= this.id
            }
            else if(end){
                seldates.push([parseInt(start.replace('i','')),parseInt(end.replace('i','')) ])
                start=0, end=0
            }

        })
        var url = '/'+self.LANGUAGE_CODE+url

        $.post('/'+self.LANGUAGE_CODE+'/dashboard/save_calendar/'+this.cal.place_id, {unavails:JSON.stringify(seldates)})
    },

    editPrices:function(id){
        var self = this
        this.genericEdit('/dashboard/edit_prices/'+id,function(){
            $('.datef input').datepicker({dateFormat: 'yy-mm-dd', minDate: '0',
                            changeMonth: true  ,changeYear: true  });
            $('#litetabs').tabs()
            $('.helptext:empty').remove()
            $('#id_currency').change(function(){
                cr = gh_crc[$(this).val()]
//                    console.log(cr)
                $('.current_curr').html(cr[1])
                self.setCurrency(parseInt($(this).val()))
            }).trigger('change')

            $('.yourpayout').each(function(){
                var sp = $(this)

                $('#'+sp.attr('id').replace('_payout','')).keyup(function(){
                                var pr = $(this).val()
                                try{ pr =  pr * ((100-host_fee)/100); if (isNaN(pr))throw 'NaN'}
                                catch(er){ pr = '' }
                                if(pr)sp.fadeIn('slow').html(self.getCurrPrice(pr.formatMoney(2, ',', '.')))
                                else sp.hide()
                            }).trigger('keyup')
            })




        })
    },
    genericEdit:function(url,fn){
        var self = this
        var url = '/'+self.LANGUAGE_CODE+url
        $.get(url, function(data){
            frame = self.showFrame('generic',data)
            self.form_submit_handler(frame,url,function(){
                self.profile_upload_init()
                if(typeof(fn)!='undefined')fn()
                $('#litetabs').tabs()

            })

        });

    },

    form_submit_handler:function(frame,url,fn){
        var self = this
        var form = frame.find('form')
//        console.log(form)
        if(typeof(fn)!='undefined')fn()
        if(typeof(url)=='undefined')url = form.attr('action')
        form.submit(function(){
            $.post(url, form.serialize(),function(data){
                frame.html(data)
                self.form_submit_handler(frame, url, fn)
            });
            return false;
        });

    }



};

//MSGS={
//    'Those dates are not available':'Seçtiğiniz tarihler uygun değil.'
//}

function trns (msg){
     return  JSTRANS[msg] || msg;
 }



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

//console.log($("#araoneri li").length)
//focitem=$("#araoneri li:contains("+ui.item.value+")'").index();
//console.log(focitem)
//if(focitem < 1)focitem = 1;
////                console.log(focitem)


