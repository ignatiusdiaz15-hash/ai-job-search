import sys, json, csv, math; sys.path.insert(0,'stage4'); from common import *
F=json.load(open('stage4/frame.json')); FX0,FY0=F['FX0'],F['FY0']
rooms=json.load(open('stage4/rooms_final.json'))
area3=json.load(open('stage3/area_check.json'))
R={r['id']:r for r in rooms}
R['R6h']['name']='Living room - TV wall strip (open)'
def ftin(x):
    s='-' if x<0 else ''; x=abs(x); f=int(x//12); i=round(x-12*f,1)
    if i>=12: f+=1; i-=12
    return f"{s}{f} ft {i:g} in"
# confidence model (linear): high = tape-validated primary wing; medium = elsewhere; low = fixtures/doors/railings
ERR={'high':(0.015,0.5),'medium':(0.04,1.0),'low':(0.05,3.0)}
def err(v,c): p,a=ERR[c]; return round(abs(v)*p+a,1)
HIGH={'R1','R2','R2s','R3','R3b','R4'}
items=[]
def add(**k):
    k['value_in']=round(k['value_in'],1); k['ft_in']=ftin(k['value_in']); k['err_in']=k.get('err_in',err(k['value_in'],k['confidence']))
    k.setdefault('verify',k['confidence']=='low'); items.append(k)
# ---- rooms & their walls ----
room_out=[]
for r in rooms:
    c='high' if r['id'] in HIGH else ('low' if r['id']=='P' else 'medium')
    sq=r['w']*r['d']/144; pe,_=ERR[c]
    room_out.append(dict(id=r['id'],name=r['name'],x0=r['x0'],x1=r['x1'],y0=r['y0'],y1=r['y1'],w_in=round(r['w'],1),d_in=round(r['d'],1),
        w_ft=ftin(r['w']),d_ft=ftin(r['d']),sqft=round(sq,1),sqft_err=round(sq*2*pe+ (r['w']+r['d'])*ERR[c][1]/144,1),confidence=c,notes=r.get('notes',[])))
    sides={'N':((r['x0'],r['y0']),(r['x1'],r['y0'])),'S':((r['x0'],r['y1']),(r['x1'],r['y1'])),
           'W':((r['x0'],r['y0']),(r['x0'],r['y1'])),'E':((r['x1'],r['y0']),(r['x1'],r['y1']))}
    for s,(a,b) in sides.items():
        L=math.dist(a,b)
        add(id=f"{r['id']}-{s}",room=r['id'],type='wall',label=f"{r['name']} - {s} wall (inside face)",value_in=L,confidence=c,
            geom=dict(kind='line',a=a,b=b),verify=False)
# ---- measured openings (real gaps in wall bands) ----
OP=[('O1','R6e','Entry/foyer to living room opening',(165.0,30.0),(165.0,80.0),'medium'),
    ('O2','R5','Kitchen to living opening (left of peninsula)',(192.5,R['R5']['y0']),(251.8,R['R5']['y0']),'medium'),
    ('O3','R5','Kitchen to living opening (right of peninsula)',(282.0,R['R5']['y0']),(322.2,R['R5']['y0']),'medium'),
    ('O4','R8v','Hall opening to bedroom vestibule',(R['R6h']['x1'],168.0),(R['R6h']['x1'],204.0),'medium'),
    ('O5','R10','Storage hall to lower storage closet',(R['R10']['x1'],353.8),(R['R10']['x1'],394.2),'medium'),
    ('O6','G','Garage overhead door opening',(180.8,R['G']['y1']),(354.8,R['G']['y1']),'medium'),
    ('O7','G','Garage side opening to entry landing',(R['G']['x0'],403.2),(R['G']['x0'],439.8),'medium')]
for i,rm,lab,a,b,c in OP:
    add(id=i,room=rm,type='opening',label=lab,value_in=math.dist(a,b),confidence=c,geom=dict(kind='line',a=a,b=b),verify=(i=='O6'))
# ---- doors: location only; width NOT measurable (header drawn over doors, 3D-leaning leaves) ----
# hinge (x,y), wall axis 'h' (door in horizontal wall) or 'v', opening direction sign along wall, swing side (+1 = +y/+x side)
DOORS=[('D2','R1','Primary bedroom door',(166.0,107.0),'v',+1,-1,32),
       ('D3','R2','Primary bathroom door',(R['R2']['x1'],276.5),'h',-1,+1,30),
       ('D4','R3','Primary walk-in closet door',(R['R3']['x0'],276.5),'h',+1,+1,28),
       ('D5','R4','Laundry door (kitchen side)',(R['R4']['x1'],338.0),'v',+1,-1,30),
       ('D6','R4','Laundry to garage door',(176.0,R['R4']['y1']),'h',-1,-1,32),
       ('D7','R7','Bedroom 2 door',(R['R7']['x0'],R['R7']['y1']),'h',+1,-1,30),
       ('D8','R8','Bathroom 2 door',(R['R8']['x0'],196.0),'v',+1,+1,28),
       ('D9','R9','Bedroom 3 door',(R['R9']['x0'],R['R9']['y0']),'h',+1,+1,30),
       ('D1','R6e','Front entry door (position approximate)',(R['R6e']['x0'],R['R6e']['y0']),'h',+1,+1,36)]
doors=[]
for i,rm,lab,h,ax,dirn,sw,assumed in DOORS:
    doors.append(dict(id=i,room=rm,label=lab,hinge=h,axis=ax,dir=dirn,swing=sw,assumed_width_in=assumed,
        swing_clear_in=assumed,confidence='low',
        note='Width not measurable: the render draws a solid header over doorways and door leaves lean in 3D. Width shown is a standard size ASSUMED for the swing arc - verify.'))
    add(id=i,room=rm,type='door',label=lab+' - ASSUMED standard width (not measured)',value_in=assumed,confidence='low',
        err_in=4.0,geom=dict(kind='door',hinge=h,axis=ax,dir=dirn,swing=sw,w=assumed))
# ---- fixtures (stock 3D symbols; read from rectified, inch-gridded image) ----
FXS=[('F1','R2','Primary bath double vanity (top incl. visible front face)',(12,292),(45,362)),
     ('F2','R2','Primary bath toilet',(15,372),(50,395)),
     ('F3a','R4','Washer (stock symbol)',(130,345),(146,367)),
     ('F3b','R4','Dryer (stock symbol)',(130,369),(146,392)),
     ('F4','R5','Kitchen peninsula (dark top, sink + dishwasher)',(241,278),(309,316)),
     ('F5','R5','Kitchen counter run - right wall',(305,285),(R['R5']['x1'],384)),
     ('F6','R5','Kitchen counter run - back wall (front edge partly hidden)',(R['R5']['x0'],381),(R['R5']['x1'],R['R5']['y1'])),
     ('F7','R5','Refrigerator / tall unit (white box, back-left)',(194,366),(218,384)),
     ('F8','R8','Bath 2 tub (visible part; top hidden by wall face)',(484,194),(R['R8']['x1'],R['R8']['y1'])),
     ('F9','G','Water heater (round)',(341,410),(362,433)),
     ('F10','R1','Primary bedroom reach-in closet zone (louvered doors)',(25,R['R1']['y0']),(120,142))]
fixtures=[]
for i,rm,lab,a,b in FXS:
    w=b[0]-a[0]; d=b[1]-a[1]
    fixtures.append(dict(id=i,room=rm,label=lab,x0=a[0],y0=a[1],x1=b[0],y1=b[1],w_in=round(w,1),d_in=round(d,1),confidence='low'))
    add(id=i+'-W',room=rm,type='fixture',label=lab+' - width (E-W)',value_in=w,confidence='low',geom=dict(kind='rect',a=a,b=b))
    add(id=i+'-D',room=rm,type='fixture',label=lab+' - depth (N-S)',value_in=d,confidence='low',geom=dict(kind='rect',a=a,b=b))
FX={f['id']:f for f in fixtures}
# ---- clearances ----
glass=R['R2s']['x0']
CL=[('C1','R2','Toilet front to shower glass',(FX['F2']['x1'],383.5),(glass,383.5)),
    ('C2','R2','Vanity front to shower glass (walkway)',(FX['F1']['x1'],330),(glass,330)),
    ('C3','R2','Toilet centerline to back wall',(32,(FX['F2']['y0']+FX['F2']['y1'])/2),(32,R['R2']['y1'])),
    ('C4','R2','Toilet centerline to vanity edge',(32,(FX['F2']['y0']+FX['F2']['y1'])/2),(32,FX['F1']['y1'])),
    ('C5','R4','Washer/dryer front to opposite wall',(FX['F3a']['x1'],360),(R['R4']['x1'],360)),
    ('C6','R5','Peninsula to back counter (kitchen aisle)',(275,FX['F4']['y1']),(275,FX['F6']['y0'])),
    ('C7','R5','Peninsula end to right counter run',(FX['F4']['x1'],300),(FX['F5']['x0'],300)),
    ('C8','G','Water heater to garage right wall',(FX['F9']['x1'],421),(R['G']['x1'],421))]
for i,rm,lab,a,b in CL:
    add(id=i,room=rm,type='clearance',label=lab,value_in=math.dist(a,b),confidence='low',geom=dict(kind='line',a=a,b=b))
# ---- totals ----
liv=[r for r in room_out if r['id'] not in ('G','P','R2s')]
tot_int=sum(r['sqft'] for r in liv)+R['R2s']['w']*R['R2s']['d']/144
totals=dict(interior_rooms_sqft=round(tot_int,1),footprint_living_sqft=round(area3['living_sqft'],1),
            footprint_err_sqft=round(area3['living_sqft']*area3['area_rel_err'],1),garage_sqft=round(R['G']['w']*R['G']['d']/144,1),
            garage_footprint_sqft=round(area3['garage_sqft'],1),listed_sqft='1,400-1,401',patio_sqft=round(R['P']['w']*R['P']['d']/144,1))
# frame inches -> original image px homography
Hm=np.array([[-(Sv/Sh),U0,U0*FY0-(Sv/Sh)*FX0],[0,VV,VV*FY0-Sv],[0,1,FY0]],float)
chk=Hm@np.array([R['R2']['x0'],R['R2']['y1'],1.0]); 
meta=dict(scale=dict(note='Tilted-perspective render; scale varies by image row.',
     primary_bath_h_in_per_px=0.814,primary_bath_v_in_per_px=0.909,range_in_per_px='0.76-1.00',err_pct=1.5),
     H_frame_to_img=Hm.tolist(),frame_origin_note='x: inches east of unit\'s west outer wall face; y: inches south of north outer face',
     confidence_model={k:f'+/-({int(v[0]*1000)/10}% + {v[1]} in)' for k,v in ERR.items()})
data=dict(meta=meta,rooms=room_out,doors=doors,fixtures=fixtures,items=items,totals=totals)
json.dump(data,open('stage4/measurements.json','w'),indent=1)
print('img check', chk[:2]/chk[2], 'n items',len(items))
for r in room_out: print(f"{r['id']:4s} {r['name']:36s} {r['w_ft']:>12s} x {r['d_ft']:>12s} {r['sqft']:7.1f} ±{r['sqft_err']} {r['confidence']}")
print(totals)
for it in items:
    if it['type'] in ('clearance','opening'): print(it['id'],it['label'],it['value_in'],it['ft_in'],'±',it['err_in'])
