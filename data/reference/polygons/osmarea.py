import sys, urllib.request, xml.etree.ElementTree as ET, json
from shapely.geometry import LineString, Polygon, MultiPolygon, mapping
from shapely.ops import linemerge, polygonize, unary_union, transform
from pyproj import Geod, Transformer, CRS
UA={'User-Agent':'research-zone-areas/0.1 (academic)'}
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=120).read()
def build(kind, oid):
    x=ET.fromstring(get(f'https://api.openstreetmap.org/api/0.6/{kind}/{oid}/full'))
    nodes={n.get('id'):(float(n.get('lon')),float(n.get('lat'))) for n in x.iter('node')}
    ways={w.get('id'):[nodes[nd.get('ref')] for nd in w.iter('nd')] for w in x.iter('way')}
    tags={}
    if kind=='way':
        el=x.find('way'); tags={t.get('k'):t.get('v') for t in el.iter('tag')}
        return Polygon(ways[str(oid)]), tags
    rel=[r for r in x.iter('relation') if r.get('id')==str(oid)][0]
    tags={t.get('k'):t.get('v') for t in rel.findall('tag')}
    outer=[];inner=[]
    for m in rel.findall('member'):
        if m.get('type')!='way' or m.get('ref') not in ways: continue
        (inner if m.get('role')=='inner' else outer).append(LineString(ways[m.get('ref')]))
    po=unary_union(list(polygonize(linemerge(outer)))) if outer else None
    pi=unary_union(list(polygonize(linemerge(inner)))) if inner else None
    g=po.difference(pi) if pi is not None and not pi.is_empty else po
    return g, tags
def areas(g):
    c=g.centroid
    laea=CRS.from_proj4(f'+proj=laea +lat_0={c.y} +lon_0={c.x} +datum=WGS84 +units=m')
    t=Transformer.from_crs(4326,laea,always_xy=True)
    a1=transform(t.transform,g).area/1e6
    a2=abs(Geod(ellps='WGS84').geometry_area_perimeter(g)[0])/1e6
    return a1,a2
if __name__=='__main__':
    kind,oid,label=sys.argv[1],sys.argv[2],sys.argv[3]
    g,tags=build(kind,oid)
    a1,a2=areas(g)
    open(f'/tmp/poly/{label}.geojson','w').write(json.dumps({'type':'Feature','properties':{'osm':f'{kind}/{oid}',**tags},'geometry':mapping(g)}))
    print(f'{label}\t{kind}/{oid}\tLAEA={a1:.3f} km2\tgeodesic={a2:.3f} km2\tvalid={g.is_valid}\tparts={len(getattr(g,"geoms",[g]))}\tname={tags.get("name")}\tstart={tags.get("start_date")}')
