<![CDATA[
    <li class=plist>
        <div class="pimg">
            <img src="<%= gh.STATIC_URL %>/yuklemeler/place_photos/<%= this.id %>_pls.jpg">
        </div>
        <div class="detail">
            <h4><a href="/<%= gh.LANGUAGE_CODE %>/places/<%= this.id %>"><%= this.tt %></a></h4>
            <%= this.ci %> - <%= this.di %>, <%= COUNTRIES[this.co] %><br>
            <%= SPACE_TYPES[this.typ] %> / <%= PLACE_TYPES[this.spc] %>
        </div>
        <div class="buttons">
            <button><%=JSTRANS.edit_prices%></button><br>
            <button><%=JSTRANS.edit_place_details%></button><br>
            <button><%=JSTRANS.set_availability%></button>
            <button><%=JSTRANS.manage_photos%></button><br>
        </div>
    </li>
]]>

