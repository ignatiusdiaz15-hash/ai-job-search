from PIL import Image, ImageDraw, ImageFont
S=6; X0,Y0,X1,Y1=30,265,215,440
im=Image.open('source/bancoora_original.png').convert('RGB').crop((X0,Y0,X1,Y1))
im=im.resize((im.width*S,im.height*S),Image.LANCZOS)
d=ImageDraw.Draw(im)
try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26); fs=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',20)
except: f=fs=ImageFont.load_default()
P=lambda x,y:((x-X0)*S,(y-Y0)*S)
def seg(a,b,col,label,off,font=f):
    d.line([P(*a),P(*b)],fill=col,width=7)
    for q in (a,b): x,y=P(*q); d.ellipse([x-8,y-8,x+8,y+8],fill=col)
    mx,my=P((a[0]+b[0])/2,(a[1]+b[1])/2); tx,ty=mx+off[0],my+off[1]
    bb=d.textbbox((tx,ty),label,font=font); d.rectangle([bb[0]-5,bb[1]-4,bb[2]+5,bb[3]+4],fill='white',outline=col,width=3)
    d.text((tx,ty),label,fill=col,font=font)
seg((53,418),(136,418),'#d62728','A  66 in back wall (to shower)',(-170,-55))
seg((136,418),(181,418),'#1f77b4','B  36 in shower',(-60,22))
seg((181,345),(181,418),'#2ca02c','C  69.5 in shower depth',(-330,-60))
seg((137,288),(137,341),'#ff7f0e','D  49.5 in',(12,-15))
seg((55,288),(52,418),'#9467bd','E  "60 in + T / 24 in W" ?',(18,-200),fs)
x,y=P(118,282); d.text((x-40,y-30),'DOOR (from primary bedroom)',fill='black',font=fs)
d.text((15,15),'Primary bathroom - proposed wall matches (plan A, 6x zoom)',fill='black',font=fs)
im.save('stage1/primary_bath_matches.png'); print(im.size)
