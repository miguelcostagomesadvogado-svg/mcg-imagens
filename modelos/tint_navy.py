import sys, numpy as np
from PIL import Image
NAVY=np.array([16,32,63],float)
def tint(src,dst):
    a=np.asarray(Image.open(src).convert('RGB')).astype(float)
    L=a.mean(axis=2,keepdims=True); c=(a.max(axis=2,keepdims=True)-a.min(axis=2,keepdims=True))
    w=np.clip((85-L)/60,0,1)*np.clip(1-c/45,0,1)
    base=np.array([13,13,15],float)
    out=a+w*(NAVY-base)
    Image.fromarray(np.clip(out,0,255).astype('uint8')).save(dst,quality=92)
if __name__=='__main__':
    tint(sys.argv[1],sys.argv[2])
