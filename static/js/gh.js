gh = {
    bas:function (m) {
        $('#arabg').prepend(m + '<br>')
    },
    init:function () {
        var usableHeight = $(window).height(), hdr_h = 0, logo_pad = 0, sc_pad = 0;
        if (usableHeight > 800)hdr_h = 110, logo_pad = -6, sc_pad = 20;
        else if (usableHeight > 610)  hdr_h = 90, logo_pad = -6;

//        if (hdr_h)$('#hdr').css({height:hdr_h + 'px'})
//        if (logo_pad)$('.logo div').css({marginTop:logo_pad + 'px'})
//        if (sc_pad)$('.showcase').css({paddingTop:sc_pad + 'px'})
        $('#smekle').click(function(){document.location='/add_place/'})
        $('#smkayit').click(function(){document.location='/register/'})
        $('#smgir').click(function(){document.location='/login/'})
    },
    index_init:function () {

        var self = this;
        this.akGorunur = 0
        this.sks = {}
        $('#arabg').fadeTo('fast', .5)
        this.doRePlacements();
        this.otoTamamla('arainput')
        $(window).resize(function () {
            self.doRePlacements()
        });
        $('#araf input').focus(function () {
            self.akToggle(0)
        });
        $('#aradugme').click(function () {document.location='/search/?place='+$('#arainput').val()});
        $('.logo').mouseover(function () {$('.krm').removeClass('krm').addClass('dekrm')}).mouseleave(function () {$('.dekrm').removeClass('dekrm').addClass('krm')});

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
                $('#pmin').html(values[0]);
                $('#pmax').html(values[1]);
            }
        });
        $('.vDateField').datepicker({dateFormat: 'yy-mm-dd' });
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
        $('#adres_form').toggle();
        $('#adres_harita').toggle();
    },
    //////////////////////////////////////////////////////
    ////////////////////MAPPPS - GEOCODING////////////////
    //////////////////////////////////////////////////////
    gmapsLoad:function(initFunc){
        var self = this
        if(typeof(initFunc)=='undefined')initFunc='gh.gcinit';
//        if (typeof(this.geocoder)=='undefined'){
            $.getScript('http://maps.googleapis.com/maps/api/js?sensor=false&callback='+initFunc)
//        }
    },
    latlng:'',
    glatlng:'',
    gZoom:8,
    setLatLng:function(l){
//        console.log($(l))
        if(l) this.latlng = $(l).val().replace('(','').replace(')','').split(',')
    },
    markerMaps:function(){
        var self = this;
//        console.log(self)
        this.gmapsLoad('gh.gcinit')
    },
    _circleMaps:function(latlng){
        this.setLatLng(latlng);
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
        if (!this.latlng)this.latlng=[38.434, 27.125]
        this.geocoder = new google.maps.Geocoder();
        this.glatlng = new google.maps.LatLng(this.latlng[0],this.latlng[1]);
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
            self.map.setCenter(results[0].geometry.location);
            self.gcResult = results[0];
            self.infoWindow.setContent(results[0].formatted_address+self.popup_html)
            self.marker.setPosition(results[0].geometry.location)
            self.infoWindow.open(self.map, self.marker);

          } else {
            alert("Adres bulunamadı\n\n" + status);
          }
        });
      },
    getGCResult:function(){return this.gcResult;},
    gcAdresTamam:function(){
        acs = this.gcResult.address_components
        $('#id_geocode').val(this.gcResult.geometry.location)
        for (i in acs){
            var ac = acs[i]
            var typ = ac.types[0]
//            console.log(ac.long_name, typ)
            if(typ=='country')$('#id_country').val(ac.short_name)
            if(typ=='route')$('#id_street').val(ac.long_name)
            if(typ=='neighborhood')$('#id_street').val($('#id_street').val() + ' ' + ac.long_name)

            if(typ=='postal_code')$('#id_postcode').val(ac.long_name)
            if(typ=='administrative_area_level_2')$('#id_district').val(ac.long_name)
            if(typ=='administrative_area_level_1')$('#id_city').val(ac.long_name)
        }
        this.gcGosterGizle()
    },
    //////////////////////////////////////////////////////
    ////////////////////ENDO OF MAPPPS - GEOCODING////////
    //////////////////////////////////////////////////////
    showPlaceInit:function(){
        var self = this;
        $('#toptabs').tabs();

        this.currentImg = $('.pthumb').first()
        $('.pthumb').click(function(){return self._gotoNextPhoto(this)})
        $('#phimg').click(function(){self._changePlacePhoto()})
        $('#openmap').click(function(){self._circleMaps('#latlng')})
        $('#photoslider-right').click(function(){self._changePlacePhoto()})
        $('#photoslider-left').click(function(){self._changePlacePhoto('prev')})
        $('.vDateField').datepicker({dateFormat: 'yy-mm-dd' });
        this.rePlace('#titlediv', '.fetiket', 615, -3);

    },
    addPlaceInit:function(){
        var self = this;
//        console.log(self,this)
        $( "#paccordion").accordion({ autoHeight: false, collapsible: true });
        $('#address').keydown(function(event){if(event.keyCode == '13')self.geocodeAddress()});
        $('#addrFindBut').click(function(){self.geocodeAddress()});
        $('#gotodetails').click(function(){ self.changeForm(3); });
        $('#gotomap').click(function(){
            self.changeForm(2);
            self.markerMaps();
        });
        $('#apbutton3').click(function(){
            if(typeof(LGD)=='undefined'){
                self.changeForm(4);
            }
            else $('#addplaceform').submit()
        });
        /*gecici*/
//        self.changeForm(3);
//        $( "#accordion").accordion( "activate" , 4 )
        //**//
        this.upload_init()
    },
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
        if(typeof(place_id)=='undefined')place_id=''
        //console.log($('#fileupload'))
        $('#fileupload').fileupload({
               dataType: 'json',
               url: '/upload_photo/'+place_id,
               done: function (e, data) {
                   $.each(data.result, function (index, file) {
                       $('<img />').attr('src',(file.turl)).attr('id','img_'+file.id).dblclick(function(){
                           $.post('/delete_photo/'+file.id,function(data){$('#img_'+file.id).hide('slow')})
                       }).appendTo('#uploaded');
                   });
               }
           });
    },
    login_init: function(){
        $('html').click(function (data) {
            $('#uyekapsar').addClass('silik');
        });
        $('#uyekapsar').click(function (event) {
            event.stopPropagation();
        })
        $('#uyeol input').focus(function(){
            $('#uyekapsar').removeClass('silik');
        })
        $('#uyeol').mouseenter(function(){
            $('#uyekapsar').removeClass('silik');
        })
    },
    dashboardInit: function(){
        var self = this;
        $( "#menuccordion").accordion({  collapsible: true});
        $('.btn').click(function(data){
            var target_div=''
            $(data.target).parents('.btn').andSelf().each(function(){
            if(typeof($(this).attr('class'))=='string' && $(this).attr('class').indexOf('btn')>=0)target_div=$(this);
            })
            if (target_div){
                $(target_div.attr('class').split(' ')).each(function(){
                    if(this.indexOf('show_')==0)self.showFrame(this.split('show_')[1])
                    if(this.indexOf('do_')==0)self[this](self)
                })
                }
            });
    },
    showFrame:function(target,data){

        if(typeof(target)=='string') target = $('#'+target)
        if(typeof(data)!='undefined' && data!='')target.html(data)
        $('div.dbcontent').hide()
        target.show('normal')

        if (window.PIE) {
            $('.piee').each(function () {
                PIE.attach(this);
            });
        }
    },
    new_place_wizard_html:'',
    add_place_url:'/add_place_ajax/',
    do_dbAddPlaceWizzard:function(self){
        var frm=$('#addplace_wizard')
        var icerik = frm.html()
        if (!icerik||icerik.indexOf('npw-flag')==-1){
            if(!self.new_place_wizard_html){
                self.showFrame('loading')
                $.get(self.add_place_url,function(data){
                    self.new_place_wizard_html = '<!--npw-flag-->'+data
                    self.showFrame(frm,self.new_place_wizard_html)
                    self.init_placeWizzard()
                })
            }else {
                self.showFrame(frm,self.new_place_wizard_html)
                self.init_placeWizzard()
            }

        }else self.showFrame(frm)
    },
    init_placeWizzard:function(place_id){
        if(typeof(place_id)=='undefined')place_id=''
        var self=this
        $( "#paccordion").accordion({ autoHeight: false, collapsible: true });
        $('#gotomap').click(function(){ self.changeForm(2); self.markerMaps();});
        $('#gotodetails').click(function(){ self.changeForm(3); });
        $('#uploaded img').dblclick(function(){
            $.post('/delete_photo/'+$(this).attr('id').replace('img_',''),function(data){$('#img_'+data).hide('slow')})
        })
//        self.gcGosterGizle()
        $('#apbutton3').val('Kaydet').click(function(){
            $.post(self.add_place_url+place_id, $("#addplaceform").serialize(),function(){
                self.showFrame('results','<div class="success">İşlem başarılı</div>')
                $("#addplaceform").html()
            });
        });
        $('#address').keydown(function(event){if(event.keyCode == '13')self.geocodeAddress()});
        $('#addrFindBut').click(function(){self.geocodeAddress()});
        this.upload_init(place_id)
    },
    editPlaceWizzard:function(id){
        var self = this
        this.showFrame('loading')
        $.get(this.add_place_url+id,function(data){
            self.showFrame('addplace_wizard',data)

            self.init_placeWizzard(id)

            self.gcGosterGizle()
            self.setLatLng('#id_geocode')
        })
    },
    showPlace:function(id){
        document.location='/places/'+id
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

//console.log($("#araoneri li").length)
//focitem=$("#araoneri li:contains("+ui.item.value+")'").index();
//console.log(focitem)
//if(focitem < 1)focitem = 1;
////                console.log(focitem)


