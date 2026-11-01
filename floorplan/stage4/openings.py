import sys, json; sys.path.insert(0,'stage4'); from common import *
F=json.load(open('stage4/frame.json')); ox,oy,FX0,FY0=F['ox'],F['oy'],F['FX0'],F['FY0']
bm=cv2.imread('stage4/band4.png',0)>127
def px(xi,yi): return (FX0+xi-ox)*PPI, (FY0+yi-oy)*PPI
rooms=[r for r in json.load(open('stage4/rooms_final.json')) if r['id'] not in ('P',)]
found=[]
for r in rooms:
    for side in 'LRTB':
        if side in 'LR':
            xf=r['x0']-2.2 if side=='L' else r['x1']+2.2      # sample inside wall band
            a,b=r['y0'],r['y1']; samp=[bm[int(px(xf,t)[1]), int(px(xf,t)[0])] for t in np.arange(a,b,0.25)]
        else:
            yf=r['y0']-2.2 if side=='T' else r['y1']+2.2
            a,b=r['x0'],r['x1']; samp=[bm[int(px(t,yf)[1]), int(px(t,yf)[0])] for t in np.arange(a,b,0.25)]
        s=np.array(samp,bool)
        # close tiny gaps (<1.5in) and find gaps (non-band runs)
        k=6; sm=np.convolve(s.astype(float),np.ones(k)/k,'same')>0.2
        idx=np.where(~sm)[0]
        if len(idx)==0: continue
        for g in np.split(idx,np.where(np.diff(idx)>1)[0]+1):
            st=a+g[0]*0.25; en=a+(g[-1]+1)*0.25; wd=en-st
            if wd>=14:
                found.append(dict(room=r['id'],side=side,start=round(st,1),end=round(en,1),width=round(wd,1),
                    full_side=bool(wd>=(b-a)-3)))
for f in found: print(f)
json.dump(found,open('stage4/openings_raw.json','w'),indent=1)
