<![CDATA[
    <li class=plist>
        <div class="detail">
            <span class="title"><%= this.tt %></span>
            <img align=left class="pimg" src="<%= gh.STATIC_URL %>/yuklemeler/place_photos/<%= this.id %>_plxs.jpg">
            <br><%= this.ci %> - <%= this.di %>, <%= COUNTRIES[this.co] %><br>
            <%= SPACE_TYPES[this.typ] %> / <%= PLACE_TYPES[this.spc] %>
            <br><br>
            <button onclick="gh.publishPlace(<%= this.id %>)"><%=JSTRANS.edit_prices%></button><br>
        </div>
        <div class="buttons">
            <button onclick="gh.editPrices(<%= this.id %>)"><%=JSTRANS.edit_prices%></button><br>
            <button onclick="gh.editPlaceWizzard(<%= this.id %>)"><%=JSTRANS.edit_place_details%></button><br>
            <button onclick="gh.editAvailability(<%= this.id %>)" ><%=JSTRANS.set_availability%></button>
            <!--br><button class="photos"><%=JSTRANS.manage_photos%></button-->
            <!--a href="/<%= gh.LANGUAGE_CODE %>/places/<%= this.id %>"></a-->
        </div>
    </li>
]]>

