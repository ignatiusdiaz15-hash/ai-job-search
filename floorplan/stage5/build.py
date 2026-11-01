import json, base64, pathlib
T=pathlib.Path('stage5/template.html').read_text()
data=json.load(open('stage4/measurements.json')); dream=json.load(open('stage5/dream.json')); views=json.load(open('stage5/views.json'))
imgo='data:image/png;base64,'+base64.b64encode(open('source/bancoora_original.png','rb').read()).decode()
imgs='data:image/jpeg;base64,'+base64.b64encode(open('stage5/straight.jpg','rb').read()).decode()
def j(o): return json.dumps(o,separators=(',',':')).replace('</','<\\/')
def make(offline):
    s=T.replace('__DATA__',j(data)).replace('__DREAM__',j(dream)).replace('__VIEWS__',j(views))
    s=s.replace('__IMGO__',imgo).replace('__IMGS__',imgs).replace('__OFFLINE__','true' if offline else 'false')
    return s
pathlib.Path('stage5/bancoora_viewer_artifact.html').write_text(make(False))
# offline file: full standalone document
off=make(True)
off='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>body{margin:0}[hidden]{display:none!important}</style></head><body>'+off+'</body></html>'
pathlib.Path('bancoora_viewer.html').write_text(off)
# CSV export copy for the repo
import csv
with open('bancoora_measurements.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['room_id','room','type','id','label','inches','feet_inches','plus_minus_in','confidence','verify_with_tape'])
    R={r['id']:r for r in data['rooms']}
    for r in data['rooms']:
        w.writerow([r['id'],r['name'],'room',r['id'],'Width (E-W)',r['w_in'],r['w_ft'],'',r['confidence'],r['confidence']=='low'])
        w.writerow([r['id'],r['name'],'room',r['id'],'Depth (N-S)',r['d_in'],r['d_ft'],'',r['confidence'],r['confidence']=='low'])
        w.writerow([r['id'],r['name'],'room',r['id'],'Area (sq ft)',r['sqft'],'',r['sqft_err'],r['confidence'],r['confidence']=='low'])
    order={'room':0,'wall':1,'opening':2,'door':3,'fixture':4,'clearance':5}
    for i in sorted(data['items'],key=lambda i:(i['room'],order[i['type']])):
        w.writerow([i['room'],R[i['room']]['name'],i['type'],i['id'],i['label'],i['value_in'],i['ft_in'],i['err_in'],i['confidence'],i['verify']])
import os; print({p:os.path.getsize(p) for p in ['stage5/bancoora_viewer_artifact.html','bancoora_viewer.html','bancoora_measurements.csv']})
