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
            <button onclick="gh.editPrices(<%= this.id %>)"><%=JSTRANS.edit_prices%></button><br>
            <button onclick="gh.editPlaceWizzard(<%= this.id %>)"><%=JSTRANS.edit_place_details%></button><br>
            <button onclick="gh.editAvailability(<%= this.id %>)" ><%=JSTRANS.set_availability%></button>
            <!--br><button class="photos"><%=JSTRANS.manage_photos%></button-->
        </div>
    </li>
]]>

