<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.9" tiledversion="1.9.2" name="01_tiles_fg" tilewidth="177" tileheight="226" tilecount="7" columns="0">
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="0">
  <image width="171" height="94" source="../../graphics/01_excavation_site/tilesets/objects/01_object_cables.png"/>
 </tile>
 <tile id="1">
  <image width="88" height="226" source="../../graphics/01_excavation_site/tilesets/objects/01_object_stalactite_1.png"/>
 </tile>
 <tile id="2">
  <image width="177" height="82" source="../../graphics/01_excavation_site/tilesets/objects/01_object_stalactite_2.png"/>
 </tile>
 <tile id="3">
  <image width="112" height="105" source="../../graphics/01_excavation_site/tilesets/objects/01_object_stalactite_3.png"/>
 </tile>
 <tile id="4" class="lamp">
  <image width="46" height="107" source="../../graphics/01_excavation_site/tilesets/objects/lamp/01_object_lamp_f1.png"/>
 </tile>
 <tile id="5" class="lamp">
  <image width="46" height="107" source="../../graphics/01_excavation_site/tilesets/objects/lamp/01_object_lamp_f2.png"/>
 </tile>
 <tile id="6" class="lamp">
  <image width="46" height="107" source="../../graphics/01_excavation_site/tilesets/objects/lamp/01_object_lamp_f3.png"/>
  <animation>
   <frame tileid="4" duration="300"/>
   <frame tileid="5" duration="300"/>
   <frame tileid="6" duration="300"/>
  </animation>
 </tile>
</tileset>
