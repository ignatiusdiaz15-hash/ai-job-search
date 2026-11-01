import sys, json; sys.path.insert(0,'stage4'); from common import *
from rooms import snap, px
F=json.load(open('stage4/frame.json')); FX0,FY0=F['FX0'],F['FY0']
R={r['id']:r for r in json.load(open('stage4/rooms_snapped.json'))}
B=json.load(open('stage3/bath_faces_in.json'))
WT=4.3  # typical interior wall thickness measured in stage 3 (4.2-4.5 in)
def setv(i,k,v,why): R[i][k]=round(float(v),2); R[i].setdefault('notes',[]).append(why)
# living right edge = west face of the wall left of closet R7c (snap on upper span only)
v,_=snap('R',300,341,31,91); setv('R6','x1',v,'right edge = wall face beside closet (open to hall below)')
setv('R6h','x0',R['R6']['x1'],'left edge open to living room (nominal line)')
# kitchen / living boundary is open (peninsula): use south face line of closet walls
setv('R5','y0',R['R3']['y0'],'top edge open to living (nominal, in line with closet wall)')
setv('R6','y1',R['R5']['y0'],'bottom edge open to kitchen (nominal)')
setv('R6e','x1',R['R6']['x0']-WT,'right edge = entry side of living-room wall (wall thickness assumed 4.3 in)')
setv('R6h','y1',R['R10']['y0'],'bottom edge nominal (open to storage hall)')
setv('R8v','x0',R['R6h']['x1'],'left edge open to hallway (nominal)')
setv('R10b','x0',R['R10']['x1'],'continuous with storage hall R10 (L-shape)')
setv('R4','y1',R['R2']['y1'],'bottom = house back wall, same as primary bath')
# shower from stage-3 measurements (glass line to far wall; back wall to end wall)
setv('R2s','x0',B['xDE']-FX0,'left edge = shower glass line (stage 3)')
setv('R2s','x1',B['xR']-FX0,'far wall inside face (stage 3)')
setv('R2s','y0',B['yClo']-FY0,'end wall (wall 2) as drawn; tape says 3.8 in further')
setv('R2s','y1',B['yA']-FY0,'back wall inside face')
for k in ('x0','x1','y0','y1'): R['P'][k]=R['P']['approx'][['x0','x1','y0','y1'].index(k)] if False else R['P'][k]
P=R['P']; P['x0'],P['x1'],P['y0'],P['y1']=32.0,P['x1'],64.0,P['y1']; P.setdefault('notes',[]).append('railing edges, approximate')
for r in R.values():
    r['w']=round(r['x1']-r['x0'],2); r['d']=round(r['y1']-r['y0'],2)
json.dump(list(R.values()),open('stage4/rooms_final.json','w'),indent=1)
for r in R.values(): print(f"{r['id']:4s} {r['name']:30s} {r['w']:6.1f} x {r['d']:6.1f}  = {r['w']*r['d']/144:6.1f} sq ft")
rect=cv2.imread('stage4/rect4.png')
for r in R.values():
    a=tuple(int(v) for v in px(r['x0'],r['y0'])); b=tuple(int(v) for v in px(r['x1'],r['y1']))
    cv2.rectangle(rect,a,b,(0,0,255),3); cv2.putText(rect,r['id'],(a[0]+8,a[1]+40),cv2.FONT_HERSHEY_SIMPLEX,1.4,(0,0,255),3)
cv2.imwrite('stage4/rooms_check.png',cv2.resize(rect,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_AREA))
