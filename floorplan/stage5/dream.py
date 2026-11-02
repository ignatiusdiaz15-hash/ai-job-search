import json
M=json.load(open('stage4/measurements.json'))
R={r['id']:r for r in M['rooms']}
def ftin(x):
    f=int(x//12); i=round(x-12*f,1)
    if i>=12: f+=1; i-=12
    return f"{f} ft {i:g} in"
rows=[]
def row(group,item,measured,best,lo,hi,basis,conf,changed):
    rows.append(dict(group=group,item=item,measured=measured,best=best,best_ft=ftin(best) if isinstance(best,(int,float)) else '',
                     range=f"{lo:g} - {hi:g} in" if lo is not None else '',lo=lo,hi=hi,basis=basis,confidence=conf,changed=changed))
# ---- primary bathroom: tape-anchored ----
row('Primary bathroom','Back wall, side wall to shower glass','65.6 (plan)',66.0,64.5,67.5,'Your tape (A). Plan agrees within 0.4 in.','high',False)
row('Primary bathroom','Shower width, glass to far wall','36.4 (plan)',36.0,34.5,37.5,'Your tape (B).','high',False)
row('Primary bathroom','Shower length, back wall to end wall (above shelf)','65.7 (plan)',69.5,68.0,71.0,'Your tape (C). Plan draws the end wall ~3.8 in short.','high',True)
row('Primary bathroom','Shower floor length (in front of 4 in shelf)','-',65.5,63.5,67.5,'69.5 minus the 4 in built-in shelf at the back end (shelf ~4 ft tall, not tape-measured).','medium',True)
row('Primary bathroom','Wall from door wall to shower corner','53.3 (plan)',49.5,48.0,51.0,'Your tape (D). Plan puts the corner ~3.8 in further from the door.','high',True)
row('Primary bathroom','Room depth, back wall to door wall','119.0 (plan)',119.0,117.5,120.5,'Tape C + D; plan agrees exactly.','high',False)
row('Primary bathroom','Main floor width, side wall to wall beside shower','61.0 (plan)',61.0,59.6,62.4,'Plan, inside faces. Not taped.','high',False)
# ---- the same wall line as the shower end wall ----
row('Primary walk-in closet','Depth (door wall to shower/laundry wall)',f"{R['R3']['drawn']['d_in']} (drawing)",round(R['R3']['drawn']['d_in']-3.8,1),round(R['R3']['drawn']['d_in']-5.5,1),round(R['R3']['drawn']['d_in']+0.5,1),
    'If the shower end wall is 3.8 in off in the drawing and runs straight across (as drawn), the closet is that much shallower. Verify.','medium',True)
row('Laundry','Depth (closet wall to back wall)',f"{R['R4']['drawn']['d_in']} (drawing)",round(R['R4']['drawn']['d_in']+3.8,1),round(R['R4']['drawn']['d_in']-0.5,1),round(R['R4']['drawn']['d_in']+5.5,1),
    'Same wall as above: laundry gains what the closet loses. Verify.','medium',True)
# ---- other rooms: measured value; upper bound covers the unexplained 8% area gap (~4% linear) ----
row('Living / dining','Depth, front windows to corner by kitchen arch','245.2 (drawing)',250.0,248.5,251.5,'Your tape. Drawing is 2.0% short here.','high',True)
row('Living / dining','Width, side to side without the TV nook','172.8 (drawing)',181.0,179.5,182.5,'Your tape. Drawing is 4.7% narrow here.','high',True)
row('Living / dining','Width to the TV wall','196.5 (drawing)',R['R6']['w_in'],R['R6']['w_in']-3,R['R6']['w_in']+3,'Drawn width scaled by your tape (not taped directly).','medium',True)
row('Primary bedroom','Side to side (door wall to opposite wall)','160.8 (drawing)',167.0,165.5,168.5,'Your tape. Drawing is 3.9% narrow here.','high',True)
row('Primary bedroom','Back to front, wall to wall including closet','166.2 (drawing)',167.0,165.5,168.5,'Your tape. Drawing is within 1 in.','high',False)
for rid in ['R5','R6e','R7','R8','R9','R10','R10b','G']:
    r=R[rid]
    for dim,key in (('width (E-W)','w_in'),('depth (N-S)','d_in')):
        v=r[key]; dr=r['drawn'][key]
        row(r['name'],dim,f"{dr} (drawing)",v,round(min(dr,v)-1,1),round(v*1.02+1,1),
            'Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet.','medium',abs(v-dr)>=1)
# ---- primary bedroom split ----
row(R['R1']['name'],'Depth excluding the reach-in closet',f"{R['R1']['d_in']} (your tape, wall to wall)",round(R['R1']['d_in']-30,1),round(R['R1']['d_in']-37,1),round(R['R1']['d_in']-24,1),
    'Your 167 in minus a typical 24-30 in reach-in closet; the drawn closet zone (37 in) includes the leaning door faces.','medium',True)
# ---- clearances (estimates) ----
for it in M['items']:
    if it['type']=='clearance':
        row('Clearances (estimated)',it['label'].split(' - estimate')[0],f"{it['drawn_in']} (drawn)",it['value_in'],it['value_in']-6,it['value_in']+6,it['note'],'low',it['drawn_in']!=it['value_in'])
# ---- doors: assumptions (not measurable) ----
for d in M['doors']:
    row('Doors',d['label'],'not measurable',d['assumed_width_in'],d['assumed_width_in']-4,d['assumed_width_in']+4,
        'Standard size ASSUMED. The render draws a solid header over every doorway, so widths cannot be measured.','low',True)
row('Doors','Garage overhead door opening','174.0 (gap in wall)',174.0,166.0,182.0,'Measured gap in the garage front wall. A 16 ft (192 in) door would not fit the 17 ft garage as drawn, so 14 ft 6 in is plausible. Verify.','medium',False)
# ---- fixtures: typical sizes vs stock symbols ----
FX=[('Primary bath double vanity','~33 x 70 (top + leaning front face)','60 or 72 long x 21-22 deep','Stock symbol drawn with its front face, so it looks deeper than a real vanity.',66.0,60,72),
    ('Primary bath toilet','35 x 23 footprint','~20 wide x 28-30 deep','Stock symbol. Drawn centerline is only 10.8 in from the back wall; code minimum is 15 in, so the real toilet sits further out.',29.0,27,31),
    ('Washer and dryer (each)','16 x 22 (each)','27 wide x 30-32 deep','Listing says full-size; the symbols are far too small.',27.0,27,29),
    ('Bath 2 tub','visible part only','60 long x 30 wide (alcove tub)','Bathroom 2 is 63.5 in deep, which fits a standard 60 in tub.',60.0,59,61),
    ('Refrigerator (position not identifiable in the drawing)','not identified','33-36 wide x 30-34 deep','Listing says side-by-side; those are 33-36 in wide.',36.0,33,36),
    ('Kitchen base counters','14 deep visible (back run)','25.5 deep','Standard counter depth; the back run\'s front edge is hidden by the 3D wall face.',25.5,24,26),
    ('Kitchen aisle, peninsula to back counter','65.0 (to visible edge)','~53.5','If the back counter is the standard 25.5 in deep.',53.5,48,58),
    ('Water heater','20.8 x 22.2','20-22 diameter','Typical 40-50 gallon tank; measured size agrees.',21.5,20,22)]
for name,meas,typ,why,best,lo,hi in FX:
    row('Fixtures (typical sizes, not measured)',name+f' - typical {typ}',meas,best,lo,hi,why,'low',True)
corrections=[
 dict(title='Removed things the drawing does not show',detail='A 50 in "foyer to living room" opening and a front-door swing were artifacts: the drawing has a solid wall there, and the small walled space is now listed as an entry closet or nook. Two kitchen "openings" were split by the dark peninsula; it is one 43 in walkway on the left.'),
 dict(title='Fixtures are drawn shifted by the 3D view',detail='Anything shorter than the walls appears pushed toward the camera (south-east) and looks deeper because its front faces show. Drawn clearances around the toilet, vanity, washer/dryer and kitchen were biased; the estimates use your tape plus standard fixture depths.'),
 dict(title='Shower end wall moved 3.8 in toward the door',detail='Your tape (69.5 in + 49.5 in) adds to the room depth exactly, and the plan draws that wall where the 4 in shelf face would be. Best estimate uses your tape.'),
 dict(title='Closet and laundry share that wall',detail='If the wall really is 3.8 in further from the back wall, the walk-in closet is about 45 in deep and the laundry about 69 in. Tape these two before buying shelving or appliances.'),
 dict(title='Door widths are standard-size assumptions',detail='The render covers every doorway with a header and draws 3D leaning door leaves, so no door width could be measured. Swing arcs use typical sizes.'),
 dict(title='Fixtures use typical sizes',detail='Toilets, washer/dryer, tub, fridge and vanity are stock 3D symbols. Real appliances listed for this plan (full-size laundry, side-by-side fridge) are larger than drawn.'),
 dict(title='Living room tape explains most of the area gap',detail='Your living room is 4.7% wider and 2.0% deeper than drawn and your primary bedroom 3.9% wider and 0.5% deeper, while the primary bathroom matched the drawing. If the rest of the house is off the same way, the living area is about 1,354 sq ft against 1,400 listed, instead of 1,287. Bedroom 2 and 3 will confirm it.')]
json.dump(dict(rows=rows,corrections=corrections),open('stage5/dream.json','w'),indent=1)
print(len(rows),'dream rows')
