import json, numpy as np, cv2
C=json.load(open('stage3/scale_totals.json'))
Sh,Sv,U0,VV=C['Sh'],C['Sv'],C['u0'],C['v_vp']
SRC='source/bancoora_original.png'
def img2plan(u,v):
    w=np.asarray(v,float)-VV; return Sh*(np.asarray(u,float)-U0)/w, -Sv/w
def plan2img(X,Y):
    w=-Sv/np.asarray(Y,float); return U0+np.asarray(X,float)*w/Sh, w+VV
# plan frame: origin at top-left of unit footprint (computed once), inches
_corn=np.array([[0,0],[750,0],[750,750],[0,750]],float)
def frame():
    img=cv2.imread(SRC); h,w=img.shape[:2]
    # footprint bbox from stage3 at 2ppi => recompute origin directly from band mask extent
    return img
PPI=4.0
def H_rect(ox,oy,ppi=PPI):
    H=np.array([[Sh,0,-Sh*U0],[0,0,-Sv],[0,1,-VV]],float)
    T=np.array([[ppi,0,-ox*ppi],[0,ppi,-oy*ppi],[0,0,1]],float); return T@H

def build_rect():
    img=cv2.imread(SRC)
    cx,cy=img2plan(np.array([0,750,750,0]),np.array([0,0,750,750]))
    ox,oy=cx.min()-5,cy.min()-5
    W=int((cx.max()-ox+5)*PPI); Hh=int((cy.max()-oy+5)*PPI)
    H=H_rect(ox,oy)
    rect=cv2.warpPerspective(img,H,(W,Hh),flags=cv2.INTER_CUBIC,borderValue=(255,255,255))
    rgb=img[:,:,::-1].astype(int); L=rgb.mean(2); s=rgb.max(2)-rgb.min(2)
    band=((L>85)&(L<130)&(s<20)).astype(np.uint8)*255
    bm=cv2.warpPerspective(band,H,(W,Hh),flags=cv2.INTER_LINEAR)
    return rect,bm,ox,oy
