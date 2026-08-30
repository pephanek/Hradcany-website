# -*- coding: utf-8 -*-
import io

PATH = "assets/cancel_map.html"
with io.open(PATH, encoding="utf-8") as f:
    s = f.read()

def rep(s, old, new, expect=1):
    n = s.count(old)
    assert n == expect, f"expected {expect}, got {n}: {old[:200]!r}"
    return s.replace(old, new, expect)

old = """var groups={B:L.layerGroup(),C:L.layerGroup(),E:L.layerGroup(),G:L.layerGroup(),H:L.layerGroup(),TD3:L.layerGroup(),TD4:L.layerGroup(),IMP:L.layerGroup(),TD7:L.layerGroup(),multi:L.layerGroup()};

function rowsHtml(g,grp){
  if(!g.rows||!g.rows.length) return '';
  var h='';
  g.rows.forEach(function(r){
    if(Array.isArray(r)){ h+='<tr><td>'+r.join('</td><td>')+'</td></tr>'; }
    else {
      var mid=(r.tr?T.train+' '+r.tr+' · ':'')+r.n+' '+T.pcs;
      var tdl=LANG==='en'?String(r.td).replace('TD','plate '):r.td;
      h+='<tr><td>'+tdl+'</td><td>'+mid+'</td><td>'+(r.per||'')+'</td></tr>';
    }
  });
  return '<table>'+h+'</table>';
}

PLACES.forEach(function(p){
  var present=PORD.filter(function(q){return p.g[q];});
  var total=0; present.forEach(function(q){total+=p.g[q].n;});
  var sz=Math.max(18,Math.min(40,14+total*2.2));
  var style,grp;
  if(present.length>1){
    var seg=100/present.length,stops=[];
    present.forEach(function(q,k){stops.push(PCOL[q]+' '+Math.round(k*seg)+'% '+Math.round((k+1)*seg)+'%');});
    style='background:conic-gradient('+stops.join(',')+');'; grp=groups.multi;
  } else {
    style='background:'+PCOL[present[0]]+';'; grp=groups[present[0]];
  }
  var icon=L.divIcon({className:'',html:'<div class="pmark" style="'+style+'width:'+sz+'px;height:'+sz+
    'px;font-size:'+Math.round(sz*0.48)+'px">'+total+'</div>',iconSize:[sz,sz],iconAnchor:[sz/2,sz/2]});
  var pop='<div class="pop"><b>'+p.name+'</b>';
  present.forEach(function(q){
    pop+='<div><span class="grp" style="color:'+PCOL[q]+'">'+PLBL[q]+'</span> — '+p.g[q].n+' '+T.pcs+rowsHtml(p.g[q],q)+'</div>';
  });
  pop+='</div>';
  L.marker([p.lat,p.lon],{icon:icon,title:p.name}).bindPopup(pop,{maxWidth:460}).addTo(grp);
});

LINES.forEach(function(l){
  var pts=l.pts||[l.pa,l.pb];
  var col=PCOL[l.g]||'#555';
  var pop='<div class="pop"><b>'+T.tpo+' '+l.a+' – '+l.b+'</b>'+(l.n?' ('+T.train+' '+l.n+')':'')+
    '<br><span class="grp" style="color:'+col+'">'+(PLBL[l.g]||l.g)+'</span></div>';
  L.polyline(pts,{color:col,weight:3,dashArray:'8 6',opacity:.85}).bindPopup(pop,{maxWidth:420})
    .addTo(groups[l.g]||groups.multi);
});

var overlays={};
overlays[PLBL.B]=groups.B; overlays[PLBL.C]=groups.C; overlays[PLBL.E]=groups.E; overlays[PLBL.G]=groups.G; overlays[PLBL.H]=groups.H;
overlays[PLBL.TD3]=groups.TD3; overlays[PLBL.TD4]=groups.TD4; overlays[PLBL.IMP]=groups.IMP;
overlays[PLBL.TD7]=groups.TD7; overlays[T.multi]=groups.multi;
Object.keys(groups).forEach(function(k){groups[k].addTo(map);});
L.control.layers(null,overlays,{collapsed:false}).addTo(map);"""

new = """var ACTIVE={}; PORD.forEach(function(q){ACTIVE[q]=true;}); ACTIVE.multi=true;

function rowsHtml(g,grp){
  if(!g.rows||!g.rows.length) return '';
  var h='';
  g.rows.forEach(function(r){
    if(Array.isArray(r)){ h+='<tr><td>'+r.join('</td><td>')+'</td></tr>'; }
    else {
      var mid=(r.tr?T.train+' '+r.tr+' · ':'')+r.n+' '+T.pcs;
      var tdl=LANG==='en'?String(r.td).replace('TD','plate '):r.td;
      h+='<tr><td>'+tdl+'</td><td>'+mid+'</td><td>'+(r.per||'')+'</td></tr>';
    }
  });
  return '<table>'+h+'</table>';
}

var placeMarkers=[];
var lineLayers=[];

PLACES.forEach(function(p){
  var present=PORD.filter(function(q){return p.g[q];});
  var total=0; present.forEach(function(q){total+=p.g[q].n;});
  var sz=Math.max(18,Math.min(40,14+total*2.2));
  var style;
  if(present.length>1){
    var seg=100/present.length,stops=[];
    present.forEach(function(q,k){stops.push(PCOL[q]+' '+Math.round(k*seg)+'% '+Math.round((k+1)*seg)+'%');});
    style='background:conic-gradient('+stops.join(',')+');';
  } else {
    style='background:'+PCOL[present[0]]+';';
  }
  var icon=L.divIcon({className:'',html:'<div class="pmark" style="'+style+'width:'+sz+'px;height:'+sz+
    'px;font-size:'+Math.round(sz*0.48)+'px">'+total+'</div>',iconSize:[sz,sz],iconAnchor:[sz/2,sz/2]});
  var pop='<div class="pop"><b>'+p.name+'</b>';
  present.forEach(function(q){
    pop+='<div><span class="grp" style="color:'+PCOL[q]+'">'+PLBL[q]+'</span> — '+p.g[q].n+' '+T.pcs+rowsHtml(p.g[q],q)+'</div>';
  });
  pop+='</div>';
  var marker=L.marker([p.lat,p.lon],{icon:icon,title:p.name}).bindPopup(pop,{maxWidth:460});
  placeMarkers.push({marker:marker, present:present});
});

LINES.forEach(function(l){
  var pts=l.pts||[l.pa,l.pb];
  var col=PCOL[l.g]||'#555';
  var pop='<div class="pop"><b>'+T.tpo+' '+l.a+' – '+l.b+'</b>'+(l.n?' ('+T.train+' '+l.n+')':'')+
    '<br><span class="grp" style="color:'+col+'">'+(PLBL[l.g]||l.g)+'</span></div>';
  var line=L.polyline(pts,{color:col,weight:3,dashArray:'8 6',opacity:.85}).bindPopup(pop,{maxWidth:420});
  lineLayers.push({layer:line, cat:l.g});
});

function placeVisible(present){
  for(var i=0;i<present.length;i++){ if(ACTIVE[present[i]]) return true; }
  if(present.length>1 && ACTIVE.multi) return true;
  return false;
}

function refreshVisibility(){
  placeMarkers.forEach(function(pm){
    var show=placeVisible(pm.present);
    var onMap=map.hasLayer(pm.marker);
    if(show && !onMap) pm.marker.addTo(map);
    if(!show && onMap) map.removeLayer(pm.marker);
  });
  lineLayers.forEach(function(lm){
    var show=!!ACTIVE[lm.cat];
    var onMap=map.hasLayer(lm.layer);
    if(show && !onMap) lm.layer.addTo(map);
    if(!show && onMap) map.removeLayer(lm.layer);
  });
}
refreshVisibility();

var layerCtl=L.control({position:'topright'});
layerCtl.onAdd=function(){
  var d=L.DomUtil.create('div','leaflet-control-layers leaflet-control-layers-expanded');
  var h='<div class="leaflet-control-layers-overlays">';
  PORD.forEach(function(q){
    h+='<label><input type="checkbox" data-cat="'+q+'" checked> <span style="color:'+PCOL[q]+'">●</span> '+PLBL[q]+'</label><br>';
  });
  h+='<label><input type="checkbox" data-cat="multi" checked> '+T.multi+'</label>';
  h+='</div>';
  d.innerHTML=h;
  L.DomEvent.disableClickPropagation(d);
  var boxes=d.querySelectorAll('input[type=checkbox]');
  for(var i=0;i<boxes.length;i++){
    boxes[i].addEventListener('change', function(e){
      ACTIVE[e.target.getAttribute('data-cat')] = e.target.checked;
      refreshVisibility();
    });
  }
  return d;
};
layerCtl.addTo(map);"""

s = rep(s, old, new)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("OK, new size", len(s))
