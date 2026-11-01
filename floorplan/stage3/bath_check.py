import json, numpy as np, cv2
c=json.load(open('stage3/scale_totals.json')); f=json.load(open('stage3/scale_fit.json'))
Sh,Sv,u0,vv=c['Sh'],c['Sv'],c['u0'],c['v_vp']; e=f['edges']
def plan(u,v): w=v-vv; return Sh*(u-u0)/w, -Sv/w        # inches (top plane)
# key faces in plan inches
xL,yA=plan(e['xL'],e['yA']); xD,_=plan(e['xD'],e['yA']); xR,_=plan(e['xR'],e['yA'])
_,yClo=plan(0,e['yClo']); _,yTop=plan(0,e['yTop'])
_,yCloN=plan(0,340.48)                        # closet wall north face
# wall D east face at back-wall row
import sys; sys.path.insert(0,'stage3'); from geom import track_vertical
p=track_vertical(138,290,338); mE=np.polyfit(p[:,0],p[:,2],1); xDE,_=plan(np.polyval(mE,e['yA']),e['yA'])
print(f"Totals: side wall->shower far wall = {xR-xL:.2f} in (tape 102 by construction); back wall->door wall = {yA-yTop:.2f} (tape 119)")
print(f"Wall D west face: {xD-xL:.2f} in from side wall ; wall D east face: {xDE-xL:.2f} ; your 66 in mark sits {66-(xD-xL):+.2f} in from west face")
print(f"Shower end (closet wall S face) {yA-yClo:.2f} in from back wall ; closet wall N face {yA-yCloN:.2f} ; your 69.5 mark offset {69.5-(yA-yClo):+.2f}")
print(f"Door wall -> closet S face {yClo-yTop:.2f} in ; your 49.5 offset {49.5-(yClo-yTop):+.2f}")
print(f"Wall thickness: wall D {xDE-xD:.2f} in, closet wall {yClo-yCloN:.2f} in")
# px/in in the original image at bathroom rows, and range over the plan
for v in (110,353,420,735):
    w=v-vv; print(f"row {v}: horizontal {w/Sh:.4f} px/in ({Sh/w:.3f} in/px), vertical {w*w/Sv:.4f} px/in ({Sv/w/w:.3f} in/px)")
json.dump(dict(xL=xL,xD=xD,xDE=xDE,xR=xR,yA=yA,yClo=yClo,yCloN=yCloN,yTop=yTop),open('stage3/bath_faces_in.json','w'),indent=1)

# ---- picture: rectified bathroom at 6 px/in with plan faces vs tape marks ----
P=6.0; x0,y0=xL-12,yTop-14; W=int((xR-xL+30)*P); Hh=int((yA-yTop+30)*P)
H=np.array([[Sh,0,-Sh*u0],[0,0,-Sv],[0,1,-vv]],float)
T=np.array([[P,0,-x0*P],[0,P,-y0*P],[0,0,1]],float)
img=cv2.imread('source/bancoora_original.png')
r=cv2.warpPerspective(img,T@H,(W,Hh),flags=cv2.INTER_CUBIC,borderValue=(255,255,255))
q=lambda x,y:(int(round((x-x0)*P)),int(round((y-y0)*P)))
F=cv2.FONT_HERSHEY_SIMPLEX
def lab(t,pt,col,s=0.55):
    (tw,th),_=cv2.getTextSize(t,F,s,2); x,y=pt
    cv2.rectangle(r,(x-3,y-th-4),(x+tw+3,y+5),(255,255,255),-1); cv2.putText(r,t,(x,y),F,s,col,2,cv2.LINE_AA)
RED,BLU,GRN,ORG,BLK=(40,40,214),(180,119,31),(44,160,44),(14,127,255),(0,0,0)
# plan faces (solid black dashed-ish)
for xx in (xD,xDE): cv2.line(r,q(xx,yClo),q(xx,yA),BLK,1,cv2.LINE_AA)
# tape marks
ya=yA-3
cv2.line(r,q(xL,ya),q(xL+66,ya),RED,3); cv2.line(r,q(xL+66,ya),q(xL+102,ya),BLU,3)
for xx in (xL,xL+66,xL+102): cv2.circle(r,q(xx,ya),5,RED,-1)
lab('A 66 (tape)',q(xL+20,ya-4),RED); lab('B 36',q(xL+72,ya-4),BLU)
xc=xR-3
cv2.line(r,q(xc,yA),q(xc,yA-69.5),GRN,3); cv2.circle(r,q(xc,yA-69.5),5,GRN,-1); lab('C 69.5',q(xc-62,yA-35),GRN)
xd=xD-3
cv2.line(r,q(xd,yTop),q(xd,yTop+49.5),ORG,3); cv2.circle(r,q(xd,yTop+49.5),5,ORG,-1); lab('D 49.5',q(xd-75,yTop+25),ORG)
lab(f'plan: wall D face {xD-xL:.1f} in from side wall',q(xL+2,yClo+12),BLK,0.45)
lab(f'plan: shower end {yA-yClo:.1f} in from back wall',q(xL+2,yClo+24),BLK,0.45)
cv2.imwrite('stage3/bath_tape_vs_plan.png',r); print('img',r.shape)
