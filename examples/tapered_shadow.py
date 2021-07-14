from coldtype import *
from coldtype.fx.skia import phototype, rasterized, skia, luma
from coldtype.warping import warp_fn

fnt = Font.Cacheable("assets/ColdtypeObviously-VF.ttf")

rs = random_series(0, 1000)
shake = 0

@animation(bg=0, timeline=Timeline(90, 23.976))
def taper(f):
    return ((StSt("COLD\nTYPE", fnt, 330,
        rotate=10,
        wdth=f.e(1),
        leading=f.e(1, rng=(65, 45)),
        tu=70+f.e(1, rng=(80, 0)))
        .align(f.a.r))
        .layer(
            lambda p: (p.pen().layer(
                    lambda p: p.f(1).t(o:=15+f.e("seio", 1, rng=(0, 10)), -o)
                        .cond(shake, lambda p: p
                            .flatten(5)
                            .nlt(warp_fn(rs[f.i//4], mult=3))),
                    lambda p: p.fssw(0, 0, f.e(1, rng=(7, 11))))
                .ch(phototype(f.a.r, blur=5, cut=183, cutw=8,
                    fill=hsl(0.75, 0.94, 0.68)
                    #fill=rgb(0, 0, 1)
                    ))),
            lambda p: p.pen().f(1)
                .cond(shake, lambda p: p
                    .flatten(5)
                    .nlt(warp_fn(rs[f.i//4+10], xs=100, mult=3)))
                .ch(phototype(f.a.r, blur=3,
                    cut=230+f.e(1, rng=(-30, 5)),
                    cutw=15,
                    fill=hsl(0.2, 0.86, 0.63)
                    #fill=rgb(1, 0, 0)
                    ))))