import sys, json, itertools
sys.path.insert(0,'stage3'); from geom import *

# ---- 1. vanishing point of plan-vertical lines (pitch-only perspective) ----
VW={'left_ext':(56,272,415),'wall_D':(138,290,338),'shower_R':(182,350,415),
    'garage_L':(240,476,735),'garage_R':(500,460,735),'hall':(287,300,405)}
lines={}
for k,(x0,y0,y1) in VW.items():
    p=track_vertical(x0,y0,y1)
    lines[k]={'n':len(p),
      'lo':np.polyfit(p[:,0],p[:,1],1),'hi':np.polyfit(p[:,0],p[:,2],1),'c':np.polyfit(p[:,0],p[:,3],1)}
# all centrelines x = m*y + b pass through (u0, v_vp): b = u0 - m*v_vp
M=np.array([[1,-lines[k]['c'][0]] for k in lines]); B=np.array([lines[k]['c'][1] for k in lines])
(u0,v_vp),*_=np.linalg.lstsq(M,B,rcond=None)
resid=B-M@np.array([u0,v_vp])
print(f'vanishing point u0={u0:.1f} v_vp={v_vp:.0f}  line-fit residual rms={resid.std():.2f}px')
# bootstrap-ish: leave-one-out spread of v_vp
loo=[]
for i in range(len(B)):
    idx=[j for j in range(len(B)) if j!=i]
    s,*_=np.linalg.lstsq(M[idx],B[idx],rcond=None); loo.append(s[1])
print('v_vp leave-one-out range', np.round(min(loo)), np.round(max(loo)))

# ---- 2. horizontal wall edges (rows) ----
HW={'back':(421,60,175),'top':(285,60,130),'closet':(343,142,178)}
rows={}
for k,(y0,x0,x1) in HW.items():
    p=track_horizontal(y0,x0,x1)
    rows[k]={'lo':np.median(p[:,1]),'hi':np.median(p[:,2]),'w':np.median(p[:,2]-p[:,1]),'sd':p[:,1].std()}
    print(f"row {k:7s} north/top edge={rows[k]['lo']:.2f} south/bottom edge={rows[k]['hi']:.2f} band={rows[k]['w']:.2f}")

def X(line,edge,y): m,b=lines[line][edge]; return m*y+b
yA=rows['back']['lo']          # inside face of back (exterior) wall
xL=X('left_ext','hi',yA)       # inside (east) face of side wall
xD=X('wall_D','lo',yA)         # bathroom-side (west) face of wall D, extended to back wall = shower edge
xR=X('shower_R','lo',yA)       # inside (west) face of shower far wall
yClo=rows['closet']['hi']       # south face of closet wall = end of shower / corner of wall D
yTop=rows['top']['hi']          # south face of bedroom/bath wall (door wall)
w=lambda y: y-v_vp
print(f'\nyA={yA:.2f} xL={xL:.2f} xD={xD:.2f} xR={xR:.2f}  yClo={yClo:.2f} yTop={yTop:.2f}')

# plan inches: horizontal dX = Sh*du/w(y);  vertical dY = Sv*|1/w1-1/w2|
feat={'A':('h',(xD-xL)/w(yA),66.0,'Back wall, side wall to shower edge'),
      'B':('h',(xR-xD)/w(yA),36.0,'Back wall across shower recess'),
      'C':('v',abs(1/w(yClo)-1/w(yA)),69.5,'Shower depth, back wall to closet-wall face'),
      'D':('v',abs(1/w(yTop)-1/w(yClo)),49.5,'Wall D, shower corner to door wall')}
def fit(keys):
    out={}
    for t in 'hv':
        ks=[k for k in keys if feat[k][0]==t]
        f=np.array([feat[k][1] for k in ks]); m=np.array([feat[k][2] for k in ks])
        out[t]=(f@m)/(f@f)   # least squares through origin
    return out
S=fit('ABCD')
# local px-per-inch at bathroom rows for reporting
def ppi_h(y): return w(y)/S['h']
def ppi_v(y): return w(y)**2/S['v']
ym=(yTop+yA)/2
print(f"\nFitted: horizontal {ppi_h(ym):.4f} px/in, vertical {ppi_v(ym):.4f} px/in at bathroom centre row {ym:.1f}")
print(f"  -> 1 px = {1/ppi_h(ym):.3f} in horizontally, {1/ppi_v(ym):.3f} in vertically")
tab=[]
for k,(t,f,m,desc) in feat.items():
    pred=S[t]*f
    px=(f*w(yA)) if t=='h' else None
    tab.append((k,desc,m,pred,pred-m))
    print(f"{k} {desc:45s} tape={m:6.1f}  predicted={pred:6.2f}  diff={pred-m:+5.2f}")
# leave-one-out cross-validation per direction is impossible with 2 per axis; report pair consistency
for t,(k1,k2) in {'h':('A','B'),'v':('C','D')}.items():
    r_img=feat[k1][1]/feat[k2][1]; r_tape=feat[k1][2]/feat[k2][2]
    print(f"{t}: image ratio {k1}/{k2}={r_img:.4f} tape ratio={r_tape:.4f}")
# single-measurement scales
for k,(t,f,m,_) in feat.items():
    s=m/f; print(f"scale from {k} alone: {'h' if t=='h' else 'v'} ppi at centre = {(w(ym)/s if t=='h' else w(ym)**2/s):.4f}")

# ---- 3. wall-thickness check of the h/v ratio ----
# interior walls drawn same thickness both ways -> compare
th_v_walls={k:(np.polyval(lines[k]['hi'],ym)-np.polyval(lines[k]['lo'],ym))/w(ym)*S['h'] for k in ('left_ext','wall_D','shower_R')}
th_h_walls={k:abs(1/w(rows[k]['lo'])-1/w(rows[k]['hi']))*S['v'] for k in rows}
print('\nwall thickness (in) of N-S walls via horizontal scale:',{k:round(v,2) for k,v in th_v_walls.items()})
print('wall thickness (in) of E-W walls via vertical scale  :',{k:round(v,2) for k,v in th_h_walls.items()})
json.dump({'u0':u0,'v_vp':v_vp,'Sh':S['h'],'Sv':S['v'],
  'edges':{'yA':yA,'xL':xL,'xD':xD,'xR':xR,'yClo':yClo,'yTop':yTop},
  'table':[dict(id=a,desc=b,tape_in=c,pred_in=round(d,2),diff_in=round(e,2)) for a,b,c,d,e in tab]},
  open('stage3/scale_fit.json','w'),indent=1)
