import sys, json, base64; sys.path.insert(0,'stage4'); from common import *
F=json.load(open('stage4/frame.json')); FX0,FY0=F['FX0'],F['FY0']
# straightened image aligned to frame inches: world [-10,560] x [-10,690] at 3 px/in
P=3.0; X0,Y0,X1,Y1=-10,-10,560,690
H=np.array([[Sh,0,-Sh*U0],[0,0,-Sv],[0,1,-VV]],float)              # img -> plan
T=np.array([[P,0,-(X0+FX0)*P],[0,P,-(Y0+FY0)*P],[0,0,1]],float)       # plan -> out px
img=cv2.imread(SRC)
out=cv2.warpPerspective(img,T@H,(int((X1-X0)*P),int((Y1-Y0)*P)),flags=cv2.INTER_CUBIC,borderValue=(255,255,255))
cv2.imwrite('stage5/straight.jpg',out,[cv2.IMWRITE_JPEG_QUALITY,86])
json.dump(dict(straight=dict(x0=X0,y0=Y0,x1=X1,y1=Y1,w=out.shape[1],h=out.shape[0])),open('stage5/views.json','w'))
print(out.shape)
