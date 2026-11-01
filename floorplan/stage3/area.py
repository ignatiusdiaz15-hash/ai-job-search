import json, numpy as np, cv2
cfg=json.load(open('stage3/scale_totals.json')); ppo=cfg['out_ppi']
bw=cv2.imread('stage3/band_mask_rect.png',0)
rect=cv2.imread('stage3/rectified_2ppi.png')
# keep thin wall-like structures: open with small kernels removes noise; close gaps (doors) generously
m=(bw>0).astype(np.uint8)
m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
# fill: everything not reachable from the border through non-wall pixels = inside
inv=(1-m).astype(np.uint8)
n,lab=cv2.connectedComponents(inv,connectivity=4)
border=set(np.unique(np.r_[lab[0],lab[-1],lab[:,0],lab[:,-1]]))
inside=np.isin(lab,[k for k in range(n) if k not in border]).astype(np.uint8)|m
# largest connected blob
n2,lab2,st,_=cv2.connectedComponentsWithStats(inside,connectivity=4)
k=1+np.argmax(st[1:,cv2.CC_STAT_AREA]); fp=(lab2==k).astype(np.uint8)
cv2.imwrite('stage3/footprint_raw.png',fp*255)
ys,xs=np.where(fp>0); print('footprint bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max(),'area sqft',fp.sum()/ppo**2/144)
# row profile of footprint width to locate house/garage split
for y in range(ys.min(),ys.max(),40): r=np.where(fp[y])[0]; print(y, r.min() if len(r) else '-', r.max() if len(r) else '-', len(r))

# ---- split living / patio / garage ----
Y,X=np.mgrid[0:fp.shape[0],0:fp.shape[1]]
SPLIT=825   # outer (south) face of house's south wall / centre of house-garage wall, rect px
patio=fp.astype(bool)&(Y<231)&(X<388)
living=fp.astype(bool)&(Y<=SPLIT)&~patio
garage=fp.astype(bool)&(Y>SPLIT)
sq=lambda m: m.sum()/ppo**2/144
res={'living_sqft':sq(living),'patio_sqft':sq(patio),'garage_sqft':sq(garage)}
res['living_plus_garage']=res['living_sqft']+res['garage_sqft']
res['living_plus_patio']=res['living_sqft']+res['patio_sqft']
# scale-uncertainty: tape +/-1.5 in on 102 in and 119 in totals
eh,ev=1.5/102,1.5/119; res['area_rel_err']=float(np.hypot(eh,ev))
for k,v in res.items(): print(f'{k:20s} {v:9.1f}' if 'err' not in k else f'{k:20s} {v*100:.1f}%')
json.dump(res,open('stage3/area_check.json','w'),indent=1)
vis=rect.copy()
for msk,col in ((living,(80,180,80)),(patio,(60,160,230)),(garage,(200,120,200))):
    ov=vis.copy(); ov[msk]=col; vis=cv2.addWeighted(ov,0.35,vis,0.65,0)
cv2.imwrite('stage3/area_check.png',vis)
