from django.shortcuts import render, HttpResponse, redirect, reverse
from molmass import Formula
from home.final import main_script
from home.CP import inp
from home.predict import cal



def index(request):
    return render(request, 'index.html')

def periodic(request):
    return render(request, 'periodic.html')

def contact(request):
    return render(request, "contact.html")

def mass(request):
    a1 = request.POST.get('name1')
    if a1 == "" or a1 == None:
        a1 = "H2O"
    f = Formula(a1)
    print(type(f.mass))
    context = {
        'var': round(f.mass, 2),
        'var1': a1
    }
    return render(request, "mass.html", context)

def equation(request):
    a7 = ""
    print(a7)
    try:
        a7 = request.POST.get('name7')
    except:
        output = "UNABLE TO GET INPUT"
    if (a7 == None or a7 == ""):    
        output = "INPUT IS BLANK"
    elif("=" not in a7 and '+' not in a7):
        output = "PLEASE ENTER VALID EQUATION"
    else:
            try:
                output = main_script(a7)
            except:
                try:
                    a7 = inp(a7)
                    output = main_script(a7)               
                except:
                    try:
                        a7 = cal(a7)
                        output = main_script(a7)  
                    except: 
                        output = "ERROR"
    if "0" in output and "10" not in output or "-" in output.replace("-->", ""):
            output = "ERROR"
    output = output.replace("1 " , "  ")    
    context = {
        "var": output,
    }
    return render(request, 'equation.html', context)


def numericals(request):
    return render(request, 'numericals.html')


def gcv(request):
    gcv, si, ncv = 0.0, 0.0, 0.0
    if 'btnform1' in request.POST:
        m, W, w, t1, t2, tf, ta, tc, h = request.POST.get('name1'), request.POST.get('name2'), request.POST.get('name3'), request.POST.get(
            'name4'), request.POST.get('name5'), request.POST.get('name6'), request.POST.get('name7'), request.POST.get('name8'), request.POST.get('name9')
        if m == "" or m == None:
            m, W, w, t1, t2 = 1, 1, 1, 1, 1
        if tf == None or tf == "":
            tf = 0.0
        if ta == None or ta == "":
            ta = 0.0
        if tc == None or tc == "":
            tc = 0.0
        if h == None or h == "":
            h = 0.0
        print(m, W, w, t1, t2, tf, ta, tc)
        Tw, Td, Tc = float(W) + float(w), float(t2) - float(t1)+float(tc), float(tf) + float(ta)
        gcv = ((Tw*Td)-(Tc))/(float(m))
        si = gcv * 4.187
        if h != 0.0:
            ncv = gcv - (float(h) * 0.09 * 587)
        else:
            ncv = "Cannot Calculate Without % H"
        print(Tw, Td, Tc, gcv, ncv)
        if type(ncv) == float:
            ncv = round(ncv, 2)
        print(type(ncv))
    gcv1, ncv1 = 0.0, 0.0
    if request.method == 'POST' and 'btnform2' in request.POST:
        V, W1, t11, t21, m = request.POST.get('name10'), request.POST.get('name11'), request.POST.get(
            'name12'), request.POST.get('name13'), request.POST.get('name14')

        if V == "" or V == None:
            V, W1, t11, t21 = 1.0, 1.0, 1.0, 1.0

        if m == "" or m == None:
            m = "NO"

        gcv1 = (float(W1) * (float(t21) - float(t11)))/float(V)

        if m != "NO":
            ncv1 = gcv1 - ((float(m)*587)/float(V))

        if t11 == 1:
            ncv1 = "0.0"

    context = {
        "var": round(gcv, 2), "var1": round(si, 2), "var2": ncv, "var3": round(gcv1, 2), "var4": round(ncv1, 2)
    }
    return render(request, 'gcv.html', context)


def hardness(request):
    a1 = request.POST.get('name1')
    a2 = request.POST.get('name2')

    if a1 == "" or a1 == None:
        a1 = "H2O"

    if a2 == "" or a2 == None:
        a2 = 0.0

    f = Formula(a1)

    print(f.mass)

    HOW = float(a2)*100/(f.mass)

    A = {'Li':1,'Be':2,'Na':1,'Mg':2,'K':1,'Ca':2,'Sc':3,'Ni':2,'Zn':2,'Rb':1,'Sr':2,'Cs':1,'Ba':2,'Ra':2,'Al':3,'Ga':3, 'NH4' : 1}

    for i in A:
        if i in a1:
            eq = A[i]
            HOW = float(a2)*50/(f.mass/eq)
    context = {
        "var": round(HOW, 2)  
    }

    return render(request, "hardness.html", context)


def coal(request):

    C = 0.0
    if 'btnform1' in request.POST:
        a, W = request.POST.get('name10'), request.POST.get('name11')

        if a == "" or a == None:
            a, W = 0.0, 1

        C = (1200*float(a))/(44*float(W))

    H = 0.0
    if request.method == 'POST' and 'btnform2' in request.POST:
        b, W2 = request.POST.get('name1'), request.POST.get('name2')

        if b == "" or b == None:
            b, W2 = 0.0, 1

        H = 200*float(b)/(18*float(W2))

    N = 0.0

    if request.method=='POST' and 'btnform3' in request.POST:
        N1,V1, V2, W  =  request.POST.get('name3'), request.POST.get('name5'), request.POST.get('name6'), request.POST.get('name7'),

        if W == 0 or W == None:
            N1,V1, V2, W = 0,0,0,1

        N=((float(V2)-float(V1))*float(N1)*1400)/(1000*float(W))
        print(N)

    S = 0.0
    if request.method == 'POST' and 'btnform4' in request.POST:
        m, W3 = request.POST.get('name8'), request.POST.get('name9')

        if m == "" or m == None:
            b, W3 = 0.0, 1

        S = float(m)*3200/(233*float(W3))

    context = {
        "var": round(C, 2),
        "var1": round(H, 2),
        "var2": round(N, 2),
        "var3": round(S, 2)

    }
    return render(request, "coal.html", context)
