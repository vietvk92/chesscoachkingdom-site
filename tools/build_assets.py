import os, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os as _o
O=_o.environ.get('CHESS_APP_REPO','/Users/viet.vk/Projects/VietVk/ChessCoach/iOS/'); A=O+'.orchestra/'  # source art lives in the app repo (override with CHESS_APP_REPO)
S=_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'..','assets')+'/'
for d in ('','art','fx','shots','residents','rivals','firefly'): os.makedirs(S+d,exist_ok=True)
def save(im,path,w=None,q=80,png=False,alpha=False):
    im=im.convert('RGBA' if alpha else 'RGB')
    if w and im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    base=S+path
    im.save(base+'.webp',quality=q,method=6)
    if png:
        (im if alpha else im).save(base+'.png',optimize=True) if not alpha else im.quantize(256,method=Image.FASTOCTREE).save(base+'.png',optimize=True) if False else im.save(base+'.png',optimize=True)
    return im
def jpgfb(im,path,w,q=78):
    im=im.convert('RGB')
    if im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    im.save(S+path+'.jpg',quality=q,optimize=True,progressive=True)
op=Image.open
# icon
ic=op(A+'appstore/icon-src.png'); save(ic,'icon-512',512,png=True)
ic.resize((180,180),Image.LANCZOS).save(S+'apple-touch-icon.png',optimize=True)
ic.resize((32,32),Image.LANCZOS).save(S+'favicon-32.png',optimize=True)
ic.resize((192,192),Image.LANCZOS).save(S+'icon-192.png',optimize=True)
save(ic,'icon-128',128)
# panorama + hero (jpg fallbacks)
pano=op(A+'art/final/art.home.panorama/panorama@3x.png'); save(pano,'art/panorama',2400,q=74); jpgfb(pano,'art/panorama',2400,72)
hero=op(A+'art/final/art.onboarding.hero/hero@3x.png'); save(hero,'art/hero',1083,q=78); jpgfb(hero,'art/hero',1083)
for n,f in (('village','lang-tot_1'),('citadel','thanh-quan-co_1'),('fortress','phao-dai-luat-le_1'),('forest','rung-chien-thuat_1')):
    im=op(A+f'art/kingdom/{f}.png'); save(im,'art/'+n,640,q=76); jpgfb(im,'art/'+n,640,74)
# firefly
for n in ('happy','proud','nervous','sleepy','worried','giggle'):
    im=op(A+f'art/firefly/firefly_{n}.png').convert('RGBA'); bb=im.getbbox(); im=im.crop(bb)
    save(im,'firefly/'+n,560,q=82,png=True,alpha=True)
# residents
R=O+'App/Resources/Assets.xcassets/Kingdom/Residents/'
for n in ('cave.fortress','cave.minor','city.bishop','city.king','city.knight','city.queen','sea.captain','temple.theory','pass.general','village.postie','port.frenchie','sea.lighthouse'):
    p=glob.glob(R+f'res.{n}.s.imageset/*@3x.png')
    if not p: continue
    im=op(p[0]).convert('RGBA'); im=im.crop(im.getbbox()); save(im,'residents/'+n.replace('.','-'),264,q=84,png=True,alpha=True)
# rivals
for n in ('kai','luna','milo','nova','orion'):
    im=op(A+f'art/final/ai.{n}/ai.{n}@3x.png'); save(im,'rivals/'+n,360,q=80); jpgfb(im,'rivals/'+n,360)
    if n=='orion': save(im,'rivals/orion-lg',360,q=80); jpgfb(im,'rivals/orion-lg',360)
# screenshots
def shots(src,dst,names,w):
    for n in names:
        p=glob.glob(A+f'appstore/screenshots/{src}/{n}_*.png')[0]
        im=op(p); save(im,f'shots/{dst}-{n}',w,q=78); jpgfb(im,f'shots/{dst}-{n}',w,76)
names=['home','learn','coach','review','scan','family','festival','resident','training','game']
shots('iphone','iphone',names,420); shots('iphone_vi','iphone-vi',names,420)
inames=['home','learn','coach','review','training','family']
shots('ipad','ipad',inames,1000); shots('ipad_vi','ipad-vi',inames,1000)
# OG image 1200x630
W,H=1200,630
bg=pano.convert('RGB'); bg=bg.resize((int(H*bg.width/bg.height),H),Image.LANCZOS); bg=bg.crop((bg.width//2-W//2+250,0,bg.width//2+W//2+250,H))
ov=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(ov)
for x in range(W):
    a=int(235*max(0,1-x/ (W*0.85))**0.8)
    d.line([(x,0),(x,H)],fill=(26,17,28,a))
bg=Image.alpha_composite(bg.convert('RGBA'),ov)
ff=op(A+'art/firefly/firefly_proud.png').convert('RGBA'); ff=ff.crop(ff.getbbox()); ff.thumbnail((380,480))
glow=Image.new('RGBA',(W,H),(0,0,0,0)); g=ImageDraw.Draw(glow); g.ellipse((740,150,1140,560),fill=(255,190,90,95)); glow=glow.filter(ImageFilter.GaussianBlur(70))
bg=Image.alpha_composite(bg,glow); bg.alpha_composite(ff,(790,110))
ic2=ic.convert('RGBA').resize((120,120),Image.LANCZOS); m=Image.new('L',(120,120),0); ImageDraw.Draw(m).rounded_rectangle((0,0,119,119),27,fill=255); bg.paste(ic2,(70,100),m)
d=ImageDraw.Draw(bg)
fb='/System/Library/Fonts/Supplemental/Georgia Bold.ttf'; fr='/System/Library/Fonts/Supplemental/Georgia.ttf'
d.text((70,260),'Chess Coach',font=ImageFont.truetype(fb,92),fill=(250,238,214))
d.text((70,365),'Kingdom',font=ImageFont.truetype(fb,92),fill=(240,185,85))
d.text((72,500),'Learn chess as an adventure',font=ImageFont.truetype(fr,38),fill=(222,205,176))
bg.convert('RGB').save(S+'og.jpg',quality=84,optimize=True,progressive=True)
