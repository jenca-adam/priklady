import termcolor
import random
import tqdm
import uuid
import termutils
from fpdf import FPDF
import sys
import numpy as np
import os
random.random=np.random.normal
lastgened=-892829892
def onedm(dm=0):
    return (10**dm)**-1
def mkr(i,dm):
    if dm==0:
        return round(i)
    return round(i,dm)
def nahodne(mn,mx,dm=0):
    global lastgened
    np.random.seed()
   
    z=mkr(random.choice(np.arange(mn,mx,onedm(dm))),dm)
    if z==lastgened:
        np.random.seed()
        z=nahodne(mn,mx,dm=0)
    lastgened=z
    return z
def make_id(lenght=10):
    return uuid.uuid4().hex.upper()[:lenght]
def make_pdf(lenght=10):
    x=make_id(lenght)
    return x,x+'.pdf',os.path.join('upls',x+'.pdf')
def make_str(c,parentheses=4):
    if c<0:
        return f'({repr(c)})'
    if random.randrange(parentheses)==0:
        return f'(+{repr(c)})'
    return repr(c)
def gener(c,mn=0,mx=100):
    r=[]
    for q in range(c):
        r.append(random.randint(mn,mx))
    return r
def priklad(cleny=3,operacie=['+','-','*','/'],mn=0,mx=100,dm=0,mocniny=[1,2,3]):
        mocniny=[int(i) for i in mocniny]
        pr=''
        cislo=99999999999
        opka=''
        for i in range(cleny):
            cislo=nahodne(mn,mx,dm)

            if opka in ['/','//']:
                while cislo == 0:
                    cislo=nahodne(mn,mx,dm)
            elif opka=='**':
                cislo=random.choice(mocniny)
            else:
                cislo=nahodne(mn,mx,dm)
            
            opka=random.choice(operacie)
            
            pr+=make_str(cislo)
            if i<cleny-1:
                pr+=' '+opka+' '
        try:
            rs=eval(pr)
        except SyntaxError:
            print()
            termcolor.cprint(f'Zlé operácie: {",".join(operacie)}','red')
            return None
        except ZeroDivisionError:
            pr,rs=priklad(cleny,operacie,mn,mx)
        except RecursionError:

            rs=None

        return pr,rs
def make_argv(lst):
    res=[]
    for q in lst:
        try:
            res.append(int(q))
        except ValueError:
            if q in ['True','False']:
                res.append(eval(q))
            else:
                z=list(q.split(','))
                if len(z)>1:
                    res.append(z)

                else:
                    res.append(z[0])
    print(res)
    return res
def priklady(pocet=10,cleny=3,operacie=['+','-','*','/'],mn=0,mx=100,dm=0,mocniny=[1,2,3],titulok='Test systému "Exampy"',pisomka=True):
    pid,pfn,vysp=make_pdf()
    print(f'Titulok: {titulok!r}')
    print(f'ID: {pid!r}')
    print('Generujem príklady...')
    rq=[]
    m=False
    for c in tqdm.tqdm(range(pocet)):
        n=priklad(cleny,operacie,mn,mx,dm,mocniny)
        if not n:
            termutils.clear()
            termcolor.cprint('Generovanie zlyhalo...','red')
            while True:pass
        rq.append(n)
    else:
        m=True
    if not m:
        exit()
    termcolor.cprint('OK :-)','green')
    print(f'Otváram {pfn!r}')
    print(f'Vytváram FPDF s príkladmi ...')
    fp=FPDF(orientation='P',unit='mm',format='A4')
    fp.add_page()
    pdf_w=210
    pdf_h=297
    print('Zapisujem titulky...')
    if pisomka:
        fp.set_xy(0,0)

        fp.set_font('Arial','B',12)
        fp.set_text_color(0,0,0)
        fp.cell(w=0,h=10, align='L', txt='Meno: ......................' , border=0)
        fp.image('placeholder.png',50,3.5,10)

    fp.set_xy(0,0)
    fp.set_font('Arial','B',16)
    fp.set_text_color(220, 50, 50)
    fp.cell(w=0,h=40.0, align='C', txt=titulok, border=0)
    fp.set_font('Arial','I',12)
    fp.set_text_color(0,0,0)
    fp.set_xy(0,0)
    fp.cell(w=0, h=60.0, align='R', txt=f'ID: {pid}', border=0)
    x=70
    index=1
    fp.set_font('Arial','',12)
    fp.set_text_color(0,0,0)
    page=1
    for r in tqdm.tqdm(rq):
        pnum=21 if page==1 else page*21
        t=r[0]
        text=f'{index}. {t} = '
        fp.set_xy(20,x)

        fp.cell(w=0, h=0, align='L', txt=text, border=0)
        x+=10
        if index==pnum:
            x=10
            fp.add_page()
            page+=1
        index+=1

    fp.output(vysp,'F')
    print(f'Zapísané {pfn!r} do {vysp!r}') 
if __name__=='__main__':
    priklady(*make_argv(sys.argv[1:]))

