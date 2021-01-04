#coldtype -wt -wp mdx,mdy -hkb

from coldtype.test import *

@renderable((1200, 500), rstate=1)
def stub(r, rs):
    kb = rs.cmd or "".join(rs.keybuffer)
    
    rt = (RichText(r,
        ("This is a\n" + (kb + "\n" if kb else "") + "program").upper(),
        dict(default=Style(mutator, 100, wght=0.5, wdth=0.15)),
        fit=r.w - 100 if rs.cmd else None)
        .xa()
        .align(r)
        .f(0))
    
    return DATPenSet([
        DATPen().rect(r.inset(20)).f(0, 0.5).s(0).sw(5),
        rt.pen().f(0).translate(5, -5),
        rt.f(1)])