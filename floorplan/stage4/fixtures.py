import sys, json; sys.path.insert(0,'stage4'); from common import *
F=json.load(open('stage4/frame.json')); ox,oy,FX0,FY0=F['ox'],F['oy'],F['FX0'],F['FY0']
rect=cv2.imread('stage4/rect4.png'); g=cv2.cvtColor(rect,cv2.COLOR_BGR2GRAY).astype(int)
hsv=cv2.cvtColor(rect,cv2.COLOR_BGR2HSV)
def px(xi,yi): return int((FX0+xi-ox)*PPI), int((FY0+yi-oy)*PPI)
def inx(p): return p/PPI+ox-FX0
def iny(p): return p/PPI+oy-FY0
# search boxes (frame inches) and color rule for the fixture surface
FX=json.load(open('stage4/fixtures_approx.json'))
out=[]
for f in FX:
    x0,x1,y0,y1=f['box']; a=px(x0,y0); b=px(x1,y1)
    G=g[a[1]:b[1],a[0]:b[0]]; S=hsv[a[1]:b[1],a[0]:b[0],1].astype(int)
    rule=f['rule']
    if rule=='dark': m=G<85
    elif rule=='white': m=(G>238)
    elif rule=='black': m=G<45
    elif rule=='blue': m=(S>80)
    m=cv2.morphologyEx(m.astype(np.uint8),cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(m)
    if n<=1: print(f['id'],'none'); continue
    k=1+np.argmax(st[1:,cv2.CC_STAT_AREA]); xs,ys=st[k,0],st[k,1]; ww,hh=st[k,2],st[k,3]
    X0,X1=inx(a[0]+xs),inx(a[0]+xs+ww); Y0,Y1=iny(a[1]+ys),iny(a[1]+ys+hh)
    fill=st[k,cv2.CC_STAT_AREA]/(ww*hh)
    r=dict(f,x0=round(X0,1),x1=round(X1,1),y0=round(Y0,1),y1=round(Y1,1),w=round(X1-X0,1),d=round(Y1-Y0,1),fill=round(fill,2))
    out.append(r); print(f"{f['id']:5s} {f['name']:34s} {X1-X0:6.1f} x {Y1-Y0:6.1f}  fill={fill:.2f}  at x{X0:.0f}-{X1:.0f} y{Y0:.0f}-{Y1:.0f}")
json.dump(out,open('stage4/fixtures_meas.json','w'),indent=1)
vis=rect.copy()
for r in out:
    cv2.rectangle(vis,px(r['x0'],r['y0']),px(r['x1'],r['y1']),(0,140,255),3)
    cv2.putText(vis,r['id'],(px(r['x0'],r['y0'])[0]+4,px(r['x0'],r['y0'])[1]+30),cv2.FONT_HERSHEY_SIMPLEX,1.1,(0,100,255),3)
cv2.imwrite('stage4/fixtures_check.png',cv2.resize(vis,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_AREA))
