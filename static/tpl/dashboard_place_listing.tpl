    <![CDATA[
    <li>
<div class="pimg">
<img src="<%= gh.STATIC_URL %>/yuklemeler/place_photos/<%= this.id %>_s.jpg">
</div>
<div class="detail">
<h4><a href="/<%= gh.LANGUAGE_CODE %>/places/<%= this.id %>"><%= this.tt %></a></h4>
<%= this.ci %> - <%= this.di %>, <%= COUNTRIES[this.co] %><br>
<%= SPACE_TYPES[this.typ] %> / <%= PLACE_TYPES[this.spc] %>
</div>
        <div class="buttons">

            <button class="manage-photos">Manage Photos</button><br>
            <button class="edit-details">Edit Place Details</button><br>
            <button class="edit-prices">Edit Prices</button><br>
            <button class="edit-availability">Set Availability</button>



        </div>
</li>


    ]]>

