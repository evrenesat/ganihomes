    <li>
            <div class="pimg">
                <img src="<%gh.STATIC_URL%>/yuklemeler/place_photos/<%=this.id%>_s.jpg">
            </div>
            <div class="detail">
                <h4><a href="/<%gh.LANGUAGE_CODE %>/places/<%=this.id%>"><%=this.tt%></a></h4>
                <%=this.ci%> - <%=this.di%>, <%=COUNTRIES[this.co]%><br>
                <%=SPACE_TYPES[this.typ]%> / <%=PLACE_TYPES[this.spc]%><br>
                <img class="ownimg" src="<%gh.STATIC_URL%>/yuklemeler/user_photos/<%=this.oid%>_s.jpg">

            </div>


            <div class="price">
                <div class="gh-prc crc" data-prc="<%=this.prc%>" data-crc="<%=this.cid%>">
                <%=this.price%>
                </div>

            </div>
            <div class="ratingdiv"><div class="rating star<%=this.or%>"></div></div>
        </li>
