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
    init:function () {
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
        $('.smdil').mouseover(function(){$('#langcurr').show('normal').mouseleave(function(){$(this).hide()})})
        this.rePlace('.smdil', '#langcurr', -10, 25);
        if(!this.selected_currency){
            this.selected_currency = $.cookie('gh_curr') || 0}
        this.fillCurrencies()
        this.initPagesAndSetLang()

    },
    fillCurrencies:function(){
        var self = this
        dv = $('.currs')
        for (c in gh_crc){
            var cc = gh_crc[c]
            if(!this.selected_currency && cc[0]=='1.0')this.selected_currency = c
            $('<span />').attr('data-crr',c).click(function(e){self.setCurrency(e.target)}).html('<sub>'+cc[2]+'</sub> '+cc[1]).appendTo(dv);
                }
        this.setCurrRates()
        this.priceScanConvert()
    },
    setCurrency:function(ob){
        var cid = $(ob).data('crr')
        $.cookie('gh_curr', cid, { expires: 365, path: '/' });
        this.selected_currency = cid
        this.setCurrRates()
        this.priceScanConvert()
        this.makeAvailabilityTab(1)
        this.calculateTotalPrice()
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
      c = "<span class='gcrc'>"+cc[2]+"</span>"
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
    init_index:function () {

        var self = this;
        this.akGorunur = 0
        this.sks = {}
        $('#arabg').fadeTo('fast', .5)
        this.doRePlacements();
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
        $('.slidiv').mouseenter(
            function () {
                sld = $(this)
//            console.log(sld.index()+1)
//            sld.parents('.tabborder').smoothDivScroll("moveToElement", "number", sld.index()+1);
                sld.find('.sbaner').animate({height:'50px'});
            }).mouseleave(function () {
                $(this).find('.sbaner').animate({height:'28px'})
            });
        this.makeScroller('GVS1');
        this.makeScroller('GVS2', 0, 1);
        this.makeScroller('GVS3');
    },
    makeScroller:function (container_id, hidden, lft) {
        if (typeof(hidden) == 'undefined') hidden = false;
        if (typeof(lft) == 'undefined') lft = false;
        var sk = $('#' + container_id);
        this.sks[container_id] = sk
        direction =  lft ? 'endlessloopright' : 'endlessloopleft';
        sk.smoothDivScroll({
            hiddenOnStart:hidden,
            autoScroll:"onstart", //"onstart" ,
            autoScrollDirection:direction,
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
//        this.rePlace('#araf', '#mhtabela', 720, -65, 1);
        this.rePlace('#araf', '#arabg_cont', -27, 20);
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
        var self = this;
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
        $("#" + id).autocomplete({minLength: 1, source:availableTags, appendTo:'#araoneri'
//            ,focus: function(event, ui) {$('#araoneri').scrollTo('ul li:eq('+ $("#araoneri li:contains("+ui.item.value+")'").index() +')');}
        });

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
    _circleMaps:function(){
        this.gmapsLoad('gh.drawCircle')
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
        var myOptions = { zoom: this.gZoom, center: this.glatlng, mapTypeId: google.maps.MapTypeId.ROADMAP }
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
        var tprice = this.convertPrice(this.total.price)
        $('#totalPriceValue').html(tprice)
        $('#displayed_price').val(tprice)
        $('#ndays').val(this.total.ndays)
        $('#currencyid').val(this.selected_currency)
    },
    checkReservationDates:function(dates){
        var loopDate = new Date();
        loopDate.setTime(dates[0]);
        $('#id_checkin').val($.datepick.formatDate('yyyy-mm-dd', dates[0]))
        $('#id_checkout').val($.datepick.formatDate('yyyy-mm-dd', dates[1]))
        this.total = {ndays:0, price:0.0}
        try{
            var days=0 ,price=0.0;
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
            if(er=='unv_dates'){alert(trns('Those dates are not available') )}
        }
        this.total.ndays = days
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
        $('#pcalendar').datepick({monthsToShow:12,multiSelect: 999, minDate:0,  rangeSelect: true,
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
        $(e.target).parents('form').submit()
    },
    init_places:function(){
        var self = this;
        x={}
        var s=0;
        $('#amenul .mhelp').easyTooltip()


        $('#toptabs').tabs();



        $('#uygtab').click(function(){
//            console.log('hmmhs')
//            $('#calendar').DatePickerShow()

        })
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
            })



            $('.vDateField').datepicker({dateFormat: 'yy-mm-dd', minDate: '0', changeMonth: true ,
                beforeShowDay: function(date) { return self.isUnAvailable(date) ? [false,'datepick-reserved','']:[true,'',''] },
                onSelect: function(dateText, inst) {
                    self.selected_dates[$(this).attr('id')] = $(this).datepicker("getDate")
                    if(self.selected_dates.id_checkin && self.selected_dates.id_checkout){
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
//    init_login: function(){
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
        self.loadTemplate('dashboard_place_listing.tpl',function(){self.hashCall()})

            //FIXME: tpl olayindan kurtulsak iyi olur
//        this.editPrices(2)
//        this.editAvailability(2)
    },
    hashCall:function(){
        if(document.location.hash){
            var hs = document.location.hash.replace('#','').split(',') //a paramter can be added with a comma
            console.log(hs[0])
            this[hs[0]](this)
//            if (typeof(hs[1])!='undefined')this[hs[0]](this,hs[1])
//            else this[hs[0]](this)
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
        for(i in data){
        var prc = this.convertPrice(parseFloat(data[i].prc),data[i].cid)
        cc = this.getCurrentCurrency()
//        prc = " <span class='gprc'>"+prc+"</span> "
        currency = "<span class='gcrc'>"+cc[2]+"</span>"
        cprc = prc.split(',')
        prc = cprc[0].length<6 ? cprc[0] + " <span class='decimal'>,"+cprc[1]+"</span>" : cprc[0]
        prc = "<span class='gprc'>"+prc+"</span>"

        data[i].price = cc[3]==1 ? currency + prc : prc + currency


        }
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
        });

    },
    markReqFields:function(container_id, label_fors){
        if(typeof(label_fors)=='undefined'){
            $("#"+container_id+" label").append('<span class="redstar">*</span>')
        }
        else{
            for(l in label_fors){
                $("#"+container_id+" label[for=id_"+label_fors[l]+"]").each(function(){
                    $(this).append('<span class="redstar">*</span>')
                })
            }
        }

    },
    init_add_place:function(place_id){
        var self = this;
        $( "#paccordion").accordion({ autoHeight: false, collapsible: true });
        $('#id_address').keydown(function(event){if(event.keyCode == '13')self.geocodeAddress()});
        $('#addrFindBut').click(function(){self.geocodeAddress()});
        $('#gotodetails').click(function(){ self.changeForm(3); });
        $('#gotomap').click(function(){
            self.changeForm(2);
            self.markerMaps();
            return false
        });
        $('#id_currency').val(this.selected_currency)
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
        });
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
    do_listPlaces:function(self, typ){
        typ = (typeof(typ)!='undefined')? '?type='+typ : ''
        var tpl = self.loadTemplate('dashboard_place_listing.tpl')
        $.get('/'+self.LANGUAGE_CODE+'/dashboard/list_places/'+typ, function(data){
            $('#placelistic').html($.jqote(tpl, data))
            self.showFrame('placelist')
        });

    },
    show_message:function(m){
        md = $('#message')
        md.find('span').html(m)
        md.fadeTo(300,0.0).fadeTo(800,1).fadeTo(300,0.3).fadeTo(300,1)
    },
    do_editProfile:function(self){
        this.genericEdit('/dashboard/edit_profile/',function(){
            $('#id_brithdate').datepicker({dateFormat: 'yy-mm-dd', maxDate: '0',
                            changeMonth: true  ,changeYear: true , yearRange: '1910:2012' });
        })
    },
    do_editPayment:function(self){
        this.genericEdit('/dashboard/edit_payment/',function(){
            $('#generic input:radio').click(function(){
                $('.ptforms').hide()
                $('#form_'+this.id).show()
            })
            $('#pt'+current_payment_selection).trigger('click')
        })
    },
    do_showMessages:function(self){
        this.genericEdit('/dashboard/show_messages/')
    },
    do_changePassword:function(self){
        this.genericEdit('/dashboard/change_password/')
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
            dayNames: this.cal.lang.dayNamesShort
        });
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
        this.genericEdit('/dashboard/edit_prices/'+id,function(){
            $('.datef input').datepicker({dateFormat: 'yy-mm-dd', minDate: '0',
                            changeMonth: true  ,changeYear: true  });
            $('#litetabs').tabs()
            $('.helptext:empty').remove()
            $('#id_currency').change(function(){
                cr = gh_crc[$(this).val()]
//                    console.log(cr)
                $('.current_curr').html(cr[1])
            }).trigger('change')
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
        form.submit(function(){
            $.post(url, form.serialize(),function(data){
                frame.html(data)
                self.form_submit_handler(frame, url, fn)
            });
            return false;
        });

    },



};

MSGS={
    'Those dates are not available':'Seçtiğiniz tarihler uygun değil.'
}

function trns (msg){
     return  MSGS[msg] || msg;
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


