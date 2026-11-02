import sys, json, csv, math; sys.path.insert(0,'stage4'); from common import *
F=json.load(open('stage4/frame.json')); FX0,FY0=F['FX0'],F['FY0']
rooms=json.load(open('stage4/rooms_final.json'))
area3=json.load(open('stage3/area_check.json'))
R={r['id']:r for r in rooms}
R['R6h']['name']='Living room - east side (open, TV wall)'
R['R6e']['name']='Entry closet / nook (walled in drawing)'
R['R6e'].setdefault('notes',[]).append('drawing shows walls on all four sides; its door and use could not be identified')
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
# ---- living room is one L-shaped room: merge the open east strip (TV wall) into it ----
L6,T6=R['R6'],R['R6h']
L6['poly']=[(L6['x0'],L6['y0']),(L6['x1'],L6['y0']),(L6['x1'],T6['y0']),(T6['x1'],T6['y0']),(T6['x1'],L6['y1']),(L6['x0'],L6['y1'])]
L6['name']='Living / dining'
L6.setdefault('notes',[]).append(f"L-shaped: {L6['x1']-L6['x0']:.1f} in wide beside the closet at the north end, {T6['x1']-L6['x0']:.1f} in wide (to the TV wall) for the rest")
L6['x1']=T6['x1']; L6['w']=L6['x1']-L6['x0']
rooms=[r for r in rooms if r['id']!='R6h']
def polyarea(P): return abs(sum(P[i][0]*P[(i+1)%len(P)][1]-P[(i+1)%len(P)][0]*P[i][1] for i in range(len(P))))/2
room_out=[]
for r in rooms:
    c='high' if r['id'] in HIGH else ('low' if r['id']=='P' else 'medium')
    sq=(polyarea(r['poly']) if 'poly' in r else r['w']*r['d'])/144; pe,_=ERR[c]
    ro=dict(id=r['id'],name=r['name'],x0=r['x0'],x1=r['x1'],y0=r['y0'],y1=r['y1'],w_in=round(r['w'],1),d_in=round(r['d'],1),
        w_ft=ftin(r['w']),d_ft=ftin(r['d']),sqft=round(sq,1),sqft_err=round(sq*2*pe+ (r['w']+r['d'])*ERR[c][1]/144,1),confidence=c,notes=r.get('notes',[]))
    if 'poly' in r: ro['poly']=[[round(x,2),round(y,2)] for x,y in r['poly']]
    room_out.append(ro)
    if 'poly' in r:
        P=r['poly']; names=['N','E (beside closet)','N (step at closet)','E (TV wall)','S','W']
        sides={names[i]:(P[i],P[(i+1)%len(P)]) for i in range(len(P))}
    else:
        sides={'N':((r['x0'],r['y0']),(r['x1'],r['y0'])),'S':((r['x0'],r['y1']),(r['x1'],r['y1'])),
           'W':((r['x0'],r['y0']),(r['x0'],r['y1'])),'E':((r['x1'],r['y0']),(r['x1'],r['y1']))}
    for s,(a,b) in sides.items():
        L=math.dist(a,b)
        add(id=f"{r['id']}-{s.split()[0]}{list(sides).index(s)}",room=r['id'],type='wall',label=f"{r['name']} - {s} wall (inside face)",value_in=L,confidence=c,
            geom=dict(kind='line',a=a,b=b),verify=False)
# ---- primary bedroom reach-in closet (inside R1's wall-to-wall box) ----
add(id='R1-closet',room='R1',type='fixture',label='Primary bedroom reach-in closet depth (included in room depth above)',value_in=30.0,confidence='low',err_in=7.0,
    geom=None,note='drawn zone is 37 in including the leaning door faces; typical reach-in is 24-30 in')
add(id='R1-sleep',room='R1',type='wall',label='Primary bedroom depth excluding reach-in closet',value_in=R['R1']['d']-30.0,confidence='medium',err_in=7.0,geom=None)
# ---- measured openings (real gaps in wall bands) ----
PEN_W=235.4  # peninsula west end corrected for 3D lean (drawn 241, 36 in tall)
OP=[('O2','R5','Kitchen walkway, left of peninsula (peninsula meets right counter, so no walkway on the right)',(R['R5']['x0'],R['R5']['y0']),(PEN_W,R['R5']['y0']),'low'),
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
       ('D10','R3b','Linen closet door (leaf drawn swinging into kitchen)',(R['R5']['x0'],R['R3b']['y0']+1),'v',+1,+1,24)]
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
     ('F7','R5','White appliance, back-left (range or fridge - drawing unclear)',(194,366),(218,384)),
     ('F8','R8','Bath 2 tub (visible part; top hidden by wall face)',(484,194),(R['R8']['x1'],R['R8']['y1'])),
     ('F9','G','Water heater (round)',(341,410),(362,433)),
     ('F10','R1','Primary bedroom reach-in closet zone (louvered doors)',(25,R['R1']['y0']),(120,142))]
fixtures=[]
for i,rm,lab,a,b in FXS:
    w=b[0]-a[0]; d=b[1]-a[1]
    fixtures.append(dict(id=i,room=rm,label=lab,x0=a[0],y0=a[1],x1=b[0],y1=b[1],w_in=round(w,1),d_in=round(d,1),confidence='low'))
    add(id=i+'-W',room=rm,type='fixture',label=lab+' - width (E-W), as drawn',value_in=w,confidence='low',geom=dict(kind='rect',a=a,b=b))
    add(id=i+'-D',room=rm,type='fixture',label=lab+' - depth (N-S), as drawn',value_in=d,confidence='low',geom=dict(kind='rect',a=a,b=b))
FX={f['id']:f for f in fixtures}
# ---- clearances ----
# The drawing is a tilted 3D render: anything shorter than the walls is drawn shifted toward the camera
# (south-east here) and its front faces make it look deeper. Drawn clearances are therefore biased.
# Estimates below anchor on your tape (66 in side wall -> shower glass) and standard fixture depths.
CL=[('C1','R2','Toilet front to shower glass',20.0,36.0,'66 in (tape) minus a ~30 in toilet; drawing shows 20 in because the toilet symbol is drawn shifted ~14 in east'),
    ('C2','R2','Vanity front to shower glass (walkway)',25.0,44.0,'66 in minus a standard 22 in vanity; drawn vanity includes its leaning front face'),
    ('C3','R2','Toilet centerline to back wall (side clearance)',10.8,18.0,'drawing shifts the toilet ~7 in toward the back wall; code minimum is 15 in'),
    ('C4','R2','Toilet centerline to end of vanity',21.5,21.5,'toilet and vanity shift by about the same amount, so the drawn value stands'),
    ('C5','R4','Washer/dryer front to opposite wall',42.2,48.0,'77.8 in laundry width minus ~30 in full-size machines (the drawn symbols are only 16 in deep)'),
    ('C6','R5','Kitchen aisle, peninsula to back counter',65.0,53.5,'back counter front edge is hidden in the drawing; assumes a standard 25.5 in counter')]
for i,rm,lab,drawn,est,why in CL:
    add(id=i,room=rm,type='clearance',label=f"{lab} - estimate (drawing shows {drawn} in)",value_in=est,confidence='low',err_in=6.0,
        geom=None,drawn_in=drawn,note=why)
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
# ---- tape measurements taken at home (override the drawing) ----
# drawn_w / drawn_d are the drawing's values for exactly what was taped
TAPE={'R6':dict(w=181.0,d=250.0,drawn_w=T6['x0']-L6['x0'],drawn_d=L6['y1']-L6['y0'],
                wlab='side to side, not counting the TV nook',dlab='front windows to the corner by the kitchen arch'),
      'R1':dict(w=167.0,d=167.0,drawn_w=R['R1']['w'],drawn_d=R['R1']['d'],
                wlab='side to side (door wall to opposite wall)',dlab='back to front, wall to wall including the closet')}
BATH_WING={'R2','R2s'}          # anchored by the original bathroom tape: no correction
zones=[]; tapefx=[]; tapefy=[]
for rid,t in TAPE.items():
    fx=t['w']/t['drawn_w']; fy=t['d']/t['drawn_d']; tapefx.append(fx); tapefy.append(fy)
    zones.append(dict(room=rid,fx=round(fx,4),fy=round(fy,4),kind='tape'))
FXA=sum(tapefx)/len(tapefx); FYA=sum(tapefy)/len(tapefy)
for ro in room_out:
    rid=ro['id']
    if rid in BATH_WING or rid=='P': continue
    if rid in TAPE:
        t=TAPE[rid]; fx=t['w']/t['drawn_w']; fy=t['d']/t['drawn_d']
        area_draw=ro['sqft']; ro['drawn']=dict(w_in=ro['w_in'],d_in=ro['d_in'],sqft=area_draw)
        ro.update(w_in=round(ro['w_in']*fx,1),d_in=round(ro['d_in']*fy,1),sqft=round(area_draw*fx*fy,1),confidence='high',tape=True)
        if rid=='R1': ro.update(w_in=t['w'],d_in=t['d'])
        if rid=='R6': ro.update(d_in=t['d'])
        ro['notes']=[f"Tape-measured: {t['w']:g} in {t['wlab']}; {t['d']:g} in {t['dlab']}",
                     f"Drawing showed {t['drawn_w']:.1f} x {t['drawn_d']:.1f} in ({100*(fx-1):+.1f}% / {100*(fy-1):+.1f}%)"]+(
                     [f"Width to the TV wall is the drawn {L6['x1']-L6['x0']:.1f} in scaled by the same factor (not taped)"] if rid=='R6' else [])
        ro['sqft_err']=round(ro['sqft']*0.02,1)
        add(id=f'{rid}-tapeW',room=rid,type='wall',label=f"{ro['name']} - {t['wlab']} - YOUR TAPE",value_in=t['w'],confidence='high',err_in=1.5,geom=None)
        add(id=f'{rid}-tapeD',room=rid,type='wall',label=f"{ro['name']} - {t['dlab']} - YOUR TAPE",value_in=t['d'],confidence='high',err_in=1.5,geom=None)
    else:
        fx,fy=FXA,FYA; area_draw=ro['sqft']; ro['drawn']=dict(w_in=ro['w_in'],d_in=ro['d_in'],sqft=area_draw)
        ro.update(w_in=round(ro['w_in']*fx,1),d_in=round(ro['d_in']*fy,1),sqft=round(area_draw*fx*fy,1),scaled=True)
        ro['notes']=ro.get('notes',[])+[f"Best estimate: drawing ({ro['drawn']['w_in']} x {ro['drawn']['d_in']} in) scaled by the average of your living-room and bedroom tape ({100*(fx-1):+.1f}% side to side, {100*(fy-1):+.1f}% front to back). Not taped yet"]
        zones.append(dict(room=rid,fx=round(fx,4),fy=round(fy,4),kind='estimate'))
    ro['w_ft']=ftin(ro['w_in']); ro['d_ft']=ftin(ro['d_in'])
    for it in items:
        if it['room']==rid and it['type']=='wall' and it.get('geom') and it['geom'].get('kind')=='line':
            g=it['geom']; v=math.hypot(abs(g['a'][0]-g['b'][0])*fx,abs(g['a'][1]-g['b'][1])*fy)
            it.update(value_in=round(v,1),ft_in=ftin(v),err_in=round(v*0.02+1,1),label=it['label']+(' (scaled to your tape)' if rid in TAPE else ' (scaled estimate)'))
# primary bedroom depth without the reach-in closet follows the tape
for it in items:
    if it['id']=='R1-sleep': v=TAPE['R1']['d']-30.0; it.update(value_in=v,ft_in=ftin(v))
bath=sum(r['sqft'] for r in room_out if r['id'] in BATH_WING)
proj=round(area3['living_sqft']+(area3['living_sqft']-bath*1.15)*(FXA*FYA-1),0)
totals.update(projected_living_sqft=proj,interior_rooms_sqft=round(sum(r['sqft'] for r in room_out if r['id'] not in ('G','P')),1),
              garage_sqft=next(r['sqft'] for r in room_out if r['id']=='G'),scale_fx=round(FXA,4),scale_fy=round(FYA,4))
meta['zones']=zones
data=dict(meta=meta,rooms=room_out,doors=doors,fixtures=fixtures,items=items,totals=totals)
json.dump(data,open('stage4/measurements.json','w'),indent=1)
print('img check', chk[:2]/chk[2], 'n items',len(items))
for r in room_out: print(f"{r['id']:4s} {r['name']:36s} {r['w_ft']:>12s} x {r['d_ft']:>12s} {r['sqft']:7.1f} ±{r['sqft_err']} {r['confidence']}")
print(totals)
for it in items:
    if it['type'] in ('clearance','opening'): print(it['id'],it['label'],it['value_in'],it['ft_in'],'±',it['err_in'])
