import sys, json; sys.path.insert(0,'stage4'); from common import *
F=json.load(open('stage4/frame.json')); ox,oy,FX0,FY0=F['ox'],F['oy'],F['FX0'],F['FY0']
bm=cv2.imread('stage4/band4.png',0)>127
def px(xi,yi): return (FX0+xi-ox)*PPI, (FY0+yi-oy)*PPI      # frame inches -> rect4 px
def inch_x(p): return p/PPI+ox-FX0
def inch_y(p): return p/PPI+oy-FY0
def snap(side, x0,x1,y0,y1, win=10):
    """Return inner wall-face coordinate (frame inches) for a side of approx interior box."""
    if side in('L','R'):
        ya,yb=[int(px(0,v)[1]) for v in (y0+(y1-y0)*0.15, y1-(y1-y0)*0.15)]
        c=x0 if side=='L' else x1; ca,cb=int(px(c-win,0)[0]),int(px(c+win,0)[0])
        prof=bm[ya:yb, ca:cb].mean(0)
    else:
        xa,xb=[int(px(v,0)[0]) for v in (x0+(x1-x0)*0.15, x1-(x1-x0)*0.15)]
        c=y0 if side=='T' else y1; ca,cb=int(px(0,c-win)[1]),int(px(0,c+win)[1])
        prof=bm[ca:cb, xa:xb].mean(1)
    isb=prof>0.30
    idx=np.where(isb)[0]
    if len(idx)==0: return None,0.0
    runs=np.split(idx,np.where(np.diff(idx)>1)[0]+1)
    mid=(cb-ca)/2
    run=min(runs,key=lambda r: abs((r[0]+r[-1])/2-mid))
    # inner face = edge facing the room interior
    if side in('L','T'): e=run[-1]+1
    else: e=run[0]
    e=ca+e
    val=inch_x(e) if side in('L','R') else inch_y(e)
    return float(val), float(prof[run].mean())
ROOMS=json.load(open('stage4/rooms_approx.json'))
out=[]
for r in ROOMS:
    x0,x1,y0,y1=r['box']; s={}
    for side in 'LRTB':
        v,strength=snap(side,x0,x1,y0,y1)
        s[side]=(v,strength)
    fixed=r.get('fix',{})
    X0=fixed.get('L',s['L'][0] if s['L'][0] is not None else x0)
    X1=fixed.get('R',s['R'][0] if s['R'][0] is not None else x1)
    Y0=fixed.get('T',s['T'][0] if s['T'][0] is not None else y0)
    Y1=fixed.get('B',s['B'][0] if s['B'][0] is not None else y1)
    out.append(dict(id=r['id'],name=r['name'],x0=round(X0,2),x1=round(X1,2),y0=round(Y0,2),y1=round(Y1,2),
        w=round(X1-X0,2),d=round(Y1-Y0,2),snap={k:round(v[1],2) for k,v in s.items()},approx=r['box']))
    print(f"{r['id']:4s} {r['name']:26s} W={X1-X0:6.1f} D={Y1-Y0:6.1f}  snapstr={ {k:round(v[1],2) for k,v in s.items()} }  dx={X0-x0:+.1f},{X1-x1:+.1f} dy={Y0-y0:+.1f},{Y1-y1:+.1f}")
json.dump(out,open('stage4/rooms_snapped.json','w'),indent=1)
# overlay
rect=cv2.imread('stage4/rect4.png')
for r in out:
    a=tuple(int(v) for v in px(r['x0'],r['y0'])); b=tuple(int(v) for v in px(r['x1'],r['y1']))
    cv2.rectangle(rect,a,b,(0,0,255),3); cv2.putText(rect,r['id'],(a[0]+8,a[1]+40),cv2.FONT_HERSHEY_SIMPLEX,1.4,(0,0,255),3)
cv2.imwrite('stage4/rooms_check.png',cv2.resize(rect,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_AREA))
