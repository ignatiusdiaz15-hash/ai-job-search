import json, numpy as np, cv2
fit=json.load(open('stage3/scale_fit.json'))
u0,v_vp=fit['u0'],fit['v_vp']
tab={r['id']:r for r in fit['table']}
# totals-based scale: A+B = 102 in (side wall -> shower far wall), C+D = 119 in (back wall -> door wall)
Sh=fit['Sh']*102.0/(tab['A']['pred_in']+tab['B']['pred_in'])
Sv=fit['Sv']*119.0/(tab['C']['pred_in']+tab['D']['pred_in'])
def H_img2plan(ppi_out, off):
    H=np.array([[Sh,0,-Sh*u0],[0,0,-Sv],[0,1,-v_vp]],float)
    T=np.array([[ppi_out,0,off[0]],[0,ppi_out,off[1]],[0,0,1]],float)
    return T@H
img=cv2.imread('source/bancoora_original.png')
h,w=img.shape[:2]
corners=np.array([[0,0],[w,0],[w,h],[0,h]],float)
H0=H_img2plan(1,(0,0))
pc=cv2.perspectiveTransform(corners[None],H0)[0]
ppo=2.0  # output px per inch
off=(-pc[:,0].min()*ppo+10, -pc[:,1].min()*ppo+10)
H=H_img2plan(ppo,off)
W=int((pc[:,0].max()-pc[:,0].min())*ppo+20); Hh=int((pc[:,1].max()-pc[:,1].min())*ppo+20)
rect=cv2.warpPerspective(img,H,(W,Hh),flags=cv2.INTER_CUBIC,borderValue=(255,255,255))
cv2.imwrite('stage3/rectified_2ppi.png',rect)
# wall-top band mask in source, then warp
rgb=img[:,:,::-1].astype(int); L=rgb.mean(2); sat=rgb.max(2)-rgb.min(2)
band=((L>85)&(L<130)&(sat<20)).astype(np.uint8)*255
bw=cv2.warpPerspective(band,H,(W,Hh),flags=cv2.INTER_NEAREST)
cv2.imwrite('stage3/band_mask_rect.png',bw)
np.save('stage3/H_img2rect.npy',H)
json.dump({'Sh':Sh,'Sv':Sv,'u0':u0,'v_vp':v_vp,'out_ppi':ppo,'size':[W,Hh]},open('stage3/scale_totals.json','w'),indent=1)
print('rectified size',W,Hh,'Sh',Sh,'Sv',Sv)
