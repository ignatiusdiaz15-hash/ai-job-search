import numpy as np
from PIL import Image
IMG='source/bancoora_original.png'
rgb=np.asarray(Image.open(IMG).convert('RGB')).astype(float)
L=rgb.mean(2)
sat=rgb.max(2)-rgb.min(2)
def is_band(v,s): return (v>85)&(v<130)&(s<20)

def band_edges_1d(prof, satp, guess, win=6):
    """Find wall-top band near index guess in 1D profile; return sub-pixel (lo_edge, hi_edge, centre).
    Edges at 50% crossing between band level and neighbouring light level."""
    lo=max(0,int(guess)-win); hi=min(len(prof)-1,int(guess)+win)
    m=is_band(prof[lo:hi+1],satp[lo:hi+1])
    idx=np.where(m)[0]
    if len(idx)<2: return None
    # take the run containing/closest to guess
    runs=np.split(idx, np.where(np.diff(idx)>1)[0]+1)
    run=min(runs,key=lambda r: abs((r[0]+r[-1])/2+lo-guess))
    a,b=run[0]+lo, run[-1]+lo
    if b-a<2: return None
    band=np.median(prof[a:b+1])
    def cross(i_in,i_out):
        out=prof[i_out]; thr=(band+out)/2
        # linear interpolate between i_in (band side) and i_out
        p_in=prof[i_in]
        if abs(out-p_in)<1e-6: return (i_in+i_out)/2
        t=(thr-p_in)/(out-p_in)
        return i_in+t*(i_out-i_in)
    # step outward 2 px to reach light level for threshold, crossing between edge px
    e_lo=cross(a, a-1) if a-1>=0 else a-0.5
    e_hi=cross(b, b+1) if b+1<len(prof) else b+0.5
    # use outer light level 2px away for threshold robustness
    def cross2(i_in,step):
        out=prof[i_in+2*step]; thr=(band+out)/2
        for k in (0,1):
            p0=prof[i_in+k*step]; p1=prof[i_in+(k+1)*step]
            if (p0-thr)*(p1-thr)<=0 and p0!=p1:
                return i_in+k*step+step*(thr-p0)/(p1-p0)
        return i_in+step*0.5
    e_lo=cross2(a,-1); e_hi=cross2(b,1)
    return e_lo,e_hi,(e_lo+e_hi)/2

def track_vertical(x0, y0, y1, win=5):
    pts=[];x=x0
    for y in range(y0,y1+1):
        r=band_edges_1d(L[y],sat[y],x,win)
        if r and 3<=r[1]-r[0]<=7.5:
            pts.append((y,)+r); x=r[2]
    return np.array(pts)
def track_horizontal(y0,x0,x1,win=5):
    pts=[];y=y0
    for x in range(x0,x1+1):
        r=band_edges_1d(L[:,x],sat[:,x],y,win)
        if r and 3<=r[1]-r[0]<=7.5:
            pts.append((x,)+r); y=r[2]
    return np.array(pts)
