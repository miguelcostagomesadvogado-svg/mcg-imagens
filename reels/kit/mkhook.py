import sys
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920
NAVY=(14,32,64); GOLD=(201,162,77); WHITE=(255,255,255)
XB='/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
SB='/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
X0,X1=70,920; PAD=40; TW=X1-X0-2*PAD
text,ngold,size,lh,out=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
ws=text.split(); hook=[(w,WHITE) for w in ws[:-ngold]]+[(w,GOLD) for w in ws[-ngold:]]
f=ImageFont.truetype(XB,size); fb=ImageFont.truetype(SB,30)
def lines_of(d):
    lines=[];cur=[]
    for w in hook:
        t=' '.join(x[0] for x in cur+[w])
        if cur and d.textlength(t,font=f)>TW: lines.append(cur);cur=[w]
        else: cur.append(w)
    lines.append(cur); return lines
def draw(d,y):
    L=lines_of(d); gaps=[]
    for i,ln in enumerate(L):
        x=X0+PAD
        if i<len(L)-1 and len(ln)>1:
            tot=sum(d.textlength(t,font=f) for t,_ in ln); gap=(TW-tot)/(len(ln)-1); gaps.append(round(gap))
        else: gap=d.textlength(' ',font=f)
        for t,c in ln: d.text((x,y),t,font=f,fill=c); x+=d.textlength(t,font=f)+gap
        y+=lh
    return y,L,gaps
top=960
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
L=lines_of(d); yend=top+PAD+48+lh*len(L)
d.rounded_rectangle((X0,top,X1,yend+PAD-8),radius=22,fill=NAVY+(215,))
d.rectangle((X0+PAD,top+PAD+34,X0+PAD+90,top+PAD+38),fill=GOLD)
d.text((X0+PAD,top+PAD-6),'MCG ADVOGADO',font=fb,fill=GOLD)
_,L,gaps=draw(d,top+PAD+48)
im.save(out)
print(out,'linhas',len(L),[' '.join(t for t,_ in l) for l in L],'gaps',gaps,'fundo',yend+PAD-8)
