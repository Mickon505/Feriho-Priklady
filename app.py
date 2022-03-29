from xml.etree.ElementTree import C14NWriterTarget
from flask import Flask, render_template, request
import math

app = Flask(__name__)


def calculate(_Uce, _Ic): # V, A
    # Poznáme:
    _h11e = 2700
    _h12e = 0.00015
    _h21e = 250 
    _h22e = 0.000018
    _Rg = 600
    _Ube = 0.55
    _Ib = 0.000004
    _Icb0 = 0.000008
    _f = 50
    _Rv = 2500
    s_E12 = []
    with open("resistors.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if "M" in line:
                continue

            if "K" in line:
                _int = float(line[:-1])
                if "." in line:
                    _int = int(float(line[:-1]) * 10)

                _int = int(_int * 1000)
                s_E12.append(_int)
                #print(_int)
                continue

            if "." in line:
                _int = float(line)
                s_E12.append(_int)
                #print(_int)
                continue

            _int = int(line)
            s_E12.append(_int)
            #print(_int)

    s_E12.sort()
    #print(s_E12)
    #s_E12 = [1000, 1200, 1500, 1800, 2200, 2700, 3300, 3900, 4700, 5600, 6800, 8200, 10000, 12000, 15000, 18000, 22000, 27000, 33000, 39000, 47000, 56000, 68000, 82000]

    # Vypočítaj napätie
    _U = 2*_Uce
    if _U <= 9:
        _U = 9
    elif _U > 9:
        _U = 12
    ## Hodnoty: _U
    print("U:",_U)

    # Vypočítaj Rc
    _Rc = _U - _Uce - (0.1 * _U)
    _Rc = round(_Rc / _Ic)
    for R in s_E12:
        if _Rc <= R:
            _Rc = R # Hodnota Rc
            break
    
    _PRc = _Rc * (_Ic ** 2)
    if _PRc <= 0.125:
        _PRc = 0.125
    elif _PRc > 0.126:
        _PRc = 0.250 # Hodnota PRc
    print("Rc:",_Rc, "/", _PRc)


    # Vypočítaj Re
    _Re = _U - (_Rc * _Ic) - _Uce
    _Re = round(_Re / _Ic)
    for R in s_E12:
        if _Re <= R:
            _Re = R # Hodnota Re
            break

    _PRe = _Re * (_Ic ** 2)
    if _PRe <= 0.125:
        _PRe = 0.125
    elif _PRe > 0.126:
        _PRe = 0.250 # Hodnota PRe
    print("Re:",_Re, "/", _PRe)

    
    # Vypočítaj R2
    _I2 = 6 * _Ib

    _R2 = _Ube + (_Re * _Ic)
    _R2 = round(_R2 / _I2)
    for R in s_E12:
        if _R2 <= R:
            _R2 = R # R2
            break

    _PR2 = _R2 * (_I2 ** 2)
    if _PR2 <= 0.125:
        _PR2 = 0.125
    elif _PR2 > 0.126:
        _PR2 = 0.250 # Hodnota PR2
    print("R2:",_R2, "/", _PR2)

    
    # Vypočítaj R1
    _I1 = _I2 + _Ib
    #ur1 = _U - _R2 * _I2
    #u = ur1 + (_R2 * _I2)

    _R1 = _U - (_R2 * _I2)
    _R1 = round(_R1 / _I1)

    for R in s_E12:
        if _R1 <= R:
            _R1 = R # R2
            break

    _PR1 = _R1 * (_I1 ** 2)
    if _PR1 <= 0.125:
        _PR1 = 0.125
    elif _PR1 > 0.126:
        _PR1 = 0.250 # Hodnota PR2
    print("R1:",_R1, "/", _PR1)


    # Vypočítaj CE
    _h11E = _h11e * 0.98 * 3
    _h21E = _h21e * 0.98 * 3
    _CE = (2 * math.pi) * (_f *(_h11E + _Rg))
    _CE = _h21E / _CE
    _CE = round(_CE * (10 ** 6))

    for C in [100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820]:
        if _CE <= C:
            _CE = C # Hodnota CE
            break

    _Uce = _U * 0.5
    for U in [3, 6, 12]:
        if _Uce <= U:
            _Uce = U # V k CE
            break
    print("CE:",_CE, "/", _Uce)
    print("-------------------------")


    # Vypočítaj C1
    _h11E_Re = _h11E + _Re
    _Rvst = (1/_R1) + (1/_R2) + (1/_h11E_Re)
    _Rvst = 1 / _Rvst

    _C1 = (2 * math.pi) * _f *(_Rg + _Rvst)
    _C1 = 1 / _C1
    _C1 = _C1 * (10 ** 6)
    for C in [1, 1.5, 3]:
        if _C1 <= C:
            _C1 = C
            break

    _Uc1 = 6
    if _U > 6:
        _Uc1 = 12
    print("C1:",_C1, "/", _Uc1)
    print("-------------------------")


    # Výpočet C2
    _h22E = _h22e * 0.98 * 3
    _Rvyst = (1/_Rc) + (1/((_Re + 1) / _h22E))
    _Rvyst = 1/_Rvyst

    _C2 = 1 / (2 * math.pi) * (25 *(_Rv + _Rvyst))
    for C in [1, 1.5, 3]:
        if _C2 <= C:
            _C2 = C
            break
    
    _Uc2 = 6
    if _U > 6:
        _Uc2 = 12
    print("C2:",_C2, "/", _Uc2)

Uce = 4
Ic = 0.005
calculate(Uce, Ic)

""" @app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/gw", methods=["POST"])
def generate_word():
    _Uce = request.form.get("uce") # napätie vo V
    _Ic = request.form.get("ic")   # prúd v mA
    _Ic = _Ic / 1000 # premena mA na A
    calculate(_Uce, _Ic)
    #print(values) """