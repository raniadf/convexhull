## IMPORT FUNGSI BAWAAN
import numpy as np
import math

## INISIALISASI INDEX GLOBAL
global convexIndex
convexIndex = []

## PEMBENTUKAN FUNGSI GLOBAL 
"""
1. Fungsi Menghitung Determinan

Parameter input : Titik pembentuk garis (a dan b), Titik yang ingin ditinjau
Return : Nilai determinan
"""
def determinant(a, b, c) :
    value = (a[0] * b[1]) + (c[0] * a[1]) + (b[0] * c[1]) - (c[0] * b[1]) - (b[0] * a[1]) - (a[0] * c[1])
    return value

"""
2. Fungsi Mencari Sudut

Parameter input : P1, Pn, titik yang ingin ditinjau
Return : Besar sudut pada P1
"""
def findAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

"""
3. Fungsi Menghitung Jarak Titik Ke Garis

Parameter input : Titik pembentuk garis (a dan b), Titik yang ingin ditinjau
Return : Jarak 
"""
def distLToP(a, b, c) :
    # Garis p1 dan p2
    p1 = np.array([(a[0]), (a[1])])
    p2 = np.array([(b[0]), (b[1])])
    # Titik p3
    p3 = np.array([(c[0]), (c[1])])
    # Mencari jarak
    dist = np.cross(p2-p1, p1-p3)/np.linalg.norm(p2-p1)
    return abs(dist)

"""
4. Fungsi Mencari P1 dan Pn

Parameter input : Kumpulan point yang ingin ditinjau
Return : indeks P1 dan Pn
"""
def extremePoints(arrList):
    # 1. Cari P1 sementara dengan x terkecil
    P1 = 0
    for i in range (len(arrList)) :
        if (arrList[i, 0] < arrList[P1, 0]) :
            P1 = i
            P3 = i

    # 2. Cari titik dengan jarak terjauh dari min
    Pn = 0
    distance = 0
    x1 = arrList[P1, 0]
    y1 = arrList[P1, 1]
    for i in range (len(arrList)) :
        x2 = arrList[i, 0]
        y2 = arrList[i, 1]
        newdist = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
        if (newdist > distance) :
            distance = newdist
            Pn = i
    
    # 3. Mengembalikan P1 dan Pn
    return P1, Pn

"""
5. Fungsi Mencari Pasangan Titik Hull Untuk S1

Parameter input : Kumpulan point yang ingin ditinjau, Kumpulan index yang ingin dicek, P1, dan Pn
Return : -
"""
def findHull1(arrList, S, P1, Pn) :
    # 1. Kasus S belum kosong
    if (len(S) != 0) :
        # 1.1 Mencari titik terjauh
        dist = 0
        titikterjauh = S[0]
        for i in range (len(S)) :
            temp = S[i]
            newdist = distLToP(arrList[P1], arrList[Pn], arrList[temp])
            if (dist < newdist) :
                titikterjauh = S[i]
                dist = newdist
            elif (dist == newdist) :
                if (findAngle(arrList[temp], arrList[P1], arrList[Pn]) > findAngle(arrList[titikterjauh], arrList[P1], arrList[Pn])) :
                    titikterjauh = S[i]
                    dist = newdist

        # 1.2 Membuat array S1 dan S2
        S1 = []
        S2 = []
        for i in range (len(S)) :
            temp = S[i]
            if (arrList[temp, 0] < arrList[titikterjauh, 0]) :
                if (determinant(arrList[P1], arrList[titikterjauh], arrList[temp]) > 0) :
                    S1.append(temp)
                    continue
                elif (determinant(arrList[titikterjauh], arrList[Pn], arrList[temp]) > 0) :
                    S2.append(temp)
                    continue
            elif (arrList[temp, 0] > arrList[titikterjauh, 0]) :
                if (determinant(arrList[titikterjauh], arrList[Pn], arrList[temp]) > 0) :
                    S2.append(temp)
                    continue
                elif (determinant(arrList[P1], arrList[titikterjauh], arrList[temp]) > 0) :
                    S1.append(temp)
                    continue
            else :
                if (arrList[temp, 1] > arrList[titikterjauh, 1]) :
                    if (determinant(arrList[P1], arrList[titikterjauh], arrList[temp]) > 0) :
                        S1.append(temp)
                        continue
                else :
                    if (determinant(arrList[titikterjauh], arrList[Pn], arrList[temp]) > 0) :
                        S2.append(temp)
                        continue
        
        # 1.3 Melakukan iterasi
        findHull1(arrList, S1, P1, titikterjauh)
        findHull1(arrList, S2, titikterjauh, Pn)

    # 2. Kasus S kosong
    else :
        convexIndex.append([P1, Pn])

"""
6. Fungsi Mencari Pasangan Titik Hull Untuk S2

Parameter input : Kumpulan point yang ingin ditinjau, Kumpulan index yang ingin dicek, P1, dan Pn
Return : -
"""
def findHull2(arrList, S, Pn, P1) :
    # 1. Kasus S belum kosong
    if (len(S) != 0) :
        # 1.1 Mencari titik terjauh
        dist = 0
        titikterjauh = S[0]
        for i in range (len(S)) :
            temp = S[i]
            newdist = distLToP(arrList[P1], arrList[Pn], arrList[temp])
            if (dist < newdist) :
                titikterjauh = S[i]
                dist = newdist
                continue
            elif (dist == newdist) :
                if (findAngle(arrList[temp], arrList[Pn], arrList[P1]) > findAngle(arrList[titikterjauh], arrList[Pn], arrList[P1])) :
                    titikterjauh = S[i]
                    dist = newdist
                    continue

        # 1.2 Membuat array S1 dan S2
        S1 = []
        S2 = []
        for i in range (len(S)) :
            temp = S[i]
            if (arrList[temp, 0] > arrList[titikterjauh, 0]) :
                if (determinant(arrList[Pn], arrList[titikterjauh], arrList[temp]) > 0) :
                    S1.append(temp)
                    continue
                elif (determinant(arrList[titikterjauh], arrList[P1], arrList[temp]) > 0) :
                    S2.append(temp)
                    continue
            elif (arrList[temp, 0] < arrList[titikterjauh, 0]) :
                if (determinant(arrList[titikterjauh], arrList[P1], arrList[temp]) > 0) :
                    S2.append(temp)
                    continue
                elif (determinant(arrList[Pn], arrList[titikterjauh], arrList[temp]) > 0) :
                    S1.append(temp)
                    continue
            else :
                if (arrList[temp, 1] > arrList[titikterjauh, 1]) :
                    if (determinant(arrList[Pn], arrList[titikterjauh], arrList[temp]) > 0) :
                        S1.append(temp)
                        continue
                else :
                    if (determinant(arrList[titikterjauh], arrList[P1], arrList[temp]) > 0) :
                        S2.append(temp)
                        continue

        # 1.3 Melakukan iterasi
        findHull2(arrList, S1, Pn, titikterjauh)
        findHull2(arrList, S2, titikterjauh, P1)

    # 2. Kasus S kosong
    else :
        convexIndex.append([P1, Pn])

## FUNGSI UTAMA
def myConvexHull(arrList) :
    # 1. Mencari P1 dan Pn
    P1, Pn = extremePoints(arrList)

    # 2. Membagi titik menjadi 2 bagian, S1 dan S2
    S1 = []
    S2 = []
    for i in range (len(arrList)) :
        if ((arrList[i, 0] == arrList[P1, 0] and arrList[i, 1] == arrList[P1, 1]) or (arrList[i, 0] == arrList[Pn, 0] and arrList[i, 1] == arrList[Pn, 1])) :
            continue
        if (determinant(arrList[P1], arrList[Pn], arrList[i]) > 0) :
            S1.append(i)
        elif (determinant(arrList[P1], arrList[Pn], arrList[i]) < 0) :
            S2.append(i)
    
    # 3. Mencari Hull
    findHull1(arrList, S1, P1, Pn)
    findHull2(arrList, S2, Pn, P1)

    return convexIndex