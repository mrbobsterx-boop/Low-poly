"""Одеть тело с ригом: одежда Tripo (без рига) подгоняется к телу, получает веса костей тела,
всё пишется в один GLB с общим скелетом и анимациями тела.

  python3 tools/char_dress.py <тело_с_ригом.glb> <выход.glb> <одежда1.glb> [одежда2.glb ...]

Одежда — в той же T-позе, что тело. Место и размер ищутся сами (по близости к телу), потом одежда
раздувается до свободы LOOSE (средний зазор до кожи, см при росте 1,8 м: верх 3, низ 2, обувь 0,5),
точки под кожей выталкиваются наружу. Тип по имени файла: top_ / bottom_ / shoes_.
"""
import json,struct,sys
import numpy as np
def load(p):
    b=open(p,'rb').read(); n=struct.unpack('<I',b[12:16])[0]; j=json.loads(b[20:20+n]); bin_=b[20+n+8:]
    return j,bin_
def acc(j,bin_,i):
    a=j['accessors'][i]; bv=j['bufferViews'][a['bufferView']]
    ct={5126:np.float32,5123:np.uint16,5125:np.uint32,5121:np.uint8}[a['componentType']]
    k={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']]
    off=bv.get('byteOffset',0)+a.get('byteOffset',0); st=bv.get('byteStride',0)
    if st and st!=k*np.dtype(ct).itemsize:
        raw=np.frombuffer(bin_,np.uint8,a['count']*st,off).reshape(-1,st)[:,:k*np.dtype(ct).itemsize]
        return raw.copy().view(ct).reshape(-1,k)
    return np.frombuffer(bin_,ct,a['count']*k,off).reshape(-1,k)
# fit clothes onto rigged body, transfer skin weights, write merged GLB
import numpy as np
GAP=0.004
LOOSE={'top_':3.0,'bottom_':2.0,'shoes_':0.5}   # median gap cloth-skin, cm at 1.8 m
from scipy.spatial import cKDTree

def rot_y(v, deg):
    r=np.radians(deg); c,s=np.cos(r),np.sin(r)
    return v@np.array([[c,0,-s],[0,1,0],[s,0,c]]).T

def fit(cv, tree, bv, kind):
    best=None
    lo,hi = bv.min(0), bv.max(0)
    for ang in (90,-90):
        v=rot_y(cv,ang)
        for s in np.linspace(0.15,1.3,47):
            w=v*s
            # x,z centered; y by search
            w=w-np.array([(w[:,0].min()+w[:,0].max())/2,0,(w[:,2].min()+w[:,2].max())/2])
            for ty in np.linspace(-0.05,1.0,43):
                p=w+[0,ty,0]
                if p[:,1].max()>hi[1]+0.06: continue
                d,_=tree.query(p[::7])
                e=np.mean(d)+0.5*np.percentile(d,95)
                if best is None or e<best[0]: best=(e,ang,s,ty)
    e,ang,s,ty=best
    v=rot_y(cv,ang)*s
    v=v-np.array([(v[:,0].min()+v[:,0].max())/2,0,(v[:,2].min()+v[:,2].max())/2])+[0,ty,0]
    # ICP refine: scale+translation
    for _ in range(30):
        d,i=tree.query(v); q=bv[i]
        mv,mq=v.mean(0),q.mean(0)
        k=np.sum((q-mq)*(v-mv))/np.sum((v-mv)**2)
        k=np.clip(k,0.97,1.03)
        v=(v-mv)*k+mq
    c=v.mean(0); k=1.0
    def med(w):
        d,i=tree.query(w[::3]); return float(np.median(np.einsum('ij,ij->i',w[::3]-bv[i],BN[i])))
    want=next((g for p,g in LOOSE.items() if kind.startswith(p)),2.0)/180.0
    while med((v-c)*k+c)<want and k<1.3: k+=0.005
    v=(v-c)*k+c
    d,i=tree.query(v)
    off=np.einsum('ij,ij->i',v-bv[i],BN[i])
    need=np.clip(GAP-off,0,None)
    v=v+BN[i]*need[:,None]
    print('inflate',round(k,2),'pushed',int((need>0).sum()),'of',len(v),'gap cm median',round(float(np.median(off))*180,1),'p90',round(float(np.percentile(off,90))*180,1))
    d,_=tree.query(v)
    print(kind,'ang',ang,'s',round(s,3),'ty',round(ty,3),'mean dist',round(float(d.mean()),4),'p95',round(float(np.percentile(d,95)),4))
    return v

def main(body, out, clothes):
    j,b=load(body); b=bytearray(b)
    pr=j['meshes'][0]['primitives'][0]
    bv=acc(j,b,pr['attributes']['POSITION']).astype(np.float64)
    bj=acc(j,b,pr['attributes']['JOINTS_0']).astype(np.int64)
    bw=acc(j,b,pr['attributes']['WEIGHTS_0']).astype(np.float64)
    if j['accessors'][pr['attributes']['WEIGHTS_0']].get('normalized') and bw.max()>1: bw/=bw.max()
    tree=cKDTree(bv)
    global BN
    bi=acc(j,b,pr['indices']).astype(np.int64).reshape(-1,3)
    fn=np.cross(bv[bi[:,1]]-bv[bi[:,0]],bv[bi[:,2]]-bv[bi[:,0]]); BN=np.zeros_like(bv)
    for c in range(3): np.add.at(BN,bi[:,c],fn)
    BN/=np.linalg.norm(BN,axis=1,keepdims=True)+1e-12
    nj=len(j['skins'][0]['joints'])
    skin_node=[n for n in j['nodes'] if 'mesh' in n][0]
    for cp in clothes:
        cj,cb=load(cp); cpr=cj['meshes'][0]['primitives'][0]
        cv=acc(cj,cb,cpr['attributes']['POSITION']).astype(np.float64)
        uv=acc(cj,cb,cpr['attributes']['TEXCOORD_0']).astype(np.float32)
        nrm=acc(cj,cb,cpr['attributes']['NORMAL']).astype(np.float64) if 'NORMAL' in cpr['attributes'] else None
        idx=acc(cj,cb,cpr['indices']).astype(np.uint32).ravel()
        kind=cp.rsplit('/',1)[-1][:-4]
        v=fit(cv,tree,bv,kind)
        # rotation for normals
        ang=None
        # weights: 6 nearest, inverse distance
        d,ii=tree.query(v,k=6); wd=1/(d+1e-4)
        acc_w=np.zeros((len(v),nj))
        for c in range(6):
            for t in range(4):
                np.add.at(acc_w,(np.arange(len(v)),bj[ii[:,c],t]),wd[:,c]*bw[ii[:,c],t])
        top=np.argsort(-acc_w,1)[:,:4]
        tw=np.take_along_axis(acc_w,top,1); tw/=tw.sum(1,keepdims=True)
        # normals: recompute from geometry
        tri=idx.reshape(-1,3); fn=np.cross(v[tri[:,1]]-v[tri[:,0]],v[tri[:,2]]-v[tri[:,0]])
        n=np.zeros_like(v)
        for c in range(3): np.add.at(n,tri[:,c],fn)
        n/=np.linalg.norm(n,axis=1,keepdims=True)+1e-12
        def add(arr,ctype,typ,target=None,mm=False):
            arr=np.ascontiguousarray(arr)
            while len(b)%4: b.append(0)
            off=len(b); b.extend(arr.tobytes())
            bvd={'buffer':0,'byteOffset':off,'byteLength':arr.nbytes}
            if target: bvd['target']=target
            j['bufferViews'].append(bvd)
            a={'bufferView':len(j['bufferViews'])-1,'componentType':ctype,'count':len(arr),'type':typ}
            if mm: a['min']=arr.min(0).tolist(); a['max']=arr.max(0).tolist()
            j['accessors'].append(a); return len(j['accessors'])-1
        attrs={'POSITION':add(v.astype(np.float32),5126,'VEC3',34962,True),
               'NORMAL':add(n.astype(np.float32),5126,'VEC3',34962),
               'TEXCOORD_0':add(uv,5126,'VEC2',34962),
               'JOINTS_0':add(top.astype(np.uint16),5123,'VEC4',34962),
               'WEIGHTS_0':add(tw.astype(np.float32),5126,'VEC4',34962)}
        ind=add(idx,5125,'SCALAR',34963)
        # material + texture
        cm=cj['materials'][cpr['material']]; mat=json.loads(json.dumps(cm)); mat['name']=kind
        pbr=mat.get('pbrMetallicRoughness',{})
        for key,holder in (('baseColorTexture',pbr),('metallicRoughnessTexture',pbr),('normalTexture',mat),('emissiveTexture',mat),('occlusionTexture',mat)):
            if key not in holder: continue
            tex=cj['textures'][holder[key]['index']]; img=cj['images'][tex['source']]
            ibv=cj['bufferViews'][img['bufferView']]; data=bytes(cb[ibv.get('byteOffset',0):ibv.get('byteOffset',0)+ibv['byteLength']])
            while len(b)%4: b.append(0)
            off=len(b); b.extend(data)
            j['bufferViews'].append({'buffer':0,'byteOffset':off,'byteLength':len(data)})
            j.setdefault('images',[]).append({'bufferView':len(j['bufferViews'])-1,'mimeType':img.get('mimeType','image/jpeg')})
            j.setdefault('textures',[]).append({'source':len(j['images'])-1})
            holder[key]={'index':len(j['textures'])-1}
        mat['pbrMetallicRoughness']=pbr
        j['materials'].append(mat)
        j['meshes'].append({'name':kind,'primitives':[{'attributes':attrs,'indices':ind,'material':len(j['materials'])-1}]})
        node={'name':kind,'mesh':len(j['meshes'])-1,'skin':skin_node['skin']}
        j['nodes'].append(node)
        # put next to body mesh node
        par=[n for n in j['nodes'] if j['nodes'].index(skin_node) in n.get('children',[])]
        if par: par[0]['children'].append(len(j['nodes'])-1)
        else: j['scenes'][j.get('scene',0)]['nodes'].append(len(j['nodes'])-1)
    while len(b)%4: b.append(0)
    j['buffers']=[{'byteLength':len(b)}]
    js=json.dumps(j,separators=(',',':')).encode()
    while len(js)%4: js+=b' '
    out_b=b'glTF'+struct.pack('<II',2,12+8+len(js)+8+len(b))+struct.pack('<I',len(js))+b'JSON'+js+struct.pack('<I',len(b))+b'BIN\x00'+bytes(b)
    open(out,'wb').write(out_b); print('wrote',out,len(out_b))

main(sys.argv[1],sys.argv[2],sys.argv[3:])
