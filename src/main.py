import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
from sympy import false, true
import convexhull
from os import path

## 1. INPUT NAMA DATASET
print("\n       _   _   _   _   _   _     _   _   _   _  ")
print("      / \ / \ / \ / \ / \ / \   / \ / \ / \ / \ ")
print("     ( C | o | n | v | e | x ) ( H | u | l | l )")
print("      \_/ \_/ \_/ \_/ \_/ \_/   \_/ \_/ \_/ \_/ \n")
print("===========================================================")
print("Terdapat beberapa dataset yang dapat diakses, antara lain =")
print("1 Iris")
print("2 Wine")
print("3 Cancer")
print("4 File CSV (Pastikan sudah ada di folder test)")
print("===========================================================")
namadata = int(input("Pilihan (dalam angka) = "))

## 2. LOAD DATASET & MEMBUAT DATAFRAME
if (namadata == 1) :
    data = datasets.load_iris()
    punyatarget = true
elif (namadata == 2) :
    data = datasets.load_wine()
    punyatarget = true
elif (namadata == 3) :
    data = datasets.load_breast_cancer()
    punyatarget = true
elif (namadata == 4) :
    data = input("Nama file csv (c/: heart.csv) = ")
    file = ".\\test\\" + data
    while not path.exists(file) :
        print("File tidak dapat ditemukan")
        data = input("Nama file csv (c/: heart.csv) = ")
        file = ".\\test\\" + data
    df = pd.read_csv(file)
    punyatarget = false
    if ('target') in df :
        punyatarget = true
    if (punyatarget == false) :
        print("File tidak dapat diproses karena tidak memiliki target")

# Hanya dapat mengakses file apabila memiliki column target
if (punyatarget) :
    ## 3. INISIALISASI PYPLOT
    plt.figure(figsize = (10, 6))
    colors = ['b','r','g']
    plt.title(label='Convex Hull', fontsize=20)

    # Kasus apabila load dari database, simpan df terlebih dahulu
    if (namadata == 1 or namadata == 2 or namadata == 3) :
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df['Target'] = pd.DataFrame(data.target)

    ## 4. MEMINTA INPUT KOLOM ACUAN
    column = df.columns.values.tolist()
    col = len(df.columns) - 1
    print("===========================================================")
    print("Dataset ini terdiri atas ", col, "kolom, yaitu = ")
    for i in range(col): 
        if (namadata == 1 or namadata == 2 or namadata == 3) :
            print(i+1, data.feature_names[i])
        elif (namadata == 4) :
            if (column[i] == "target") :
                continue
            print(i + 1, column[i])
    print("===========================================================")
    print("Silahkan pilih kolom acuan (dalam angka)!")
    while (True) :
        col1 = int(input("Acuan X = "))
        if (col1 > 0 and col1 <= col) :
            break
    while (True) :
        col2 = int(input("Acuan Y = "))
        if (col2 > 0 and col2 <= col) :
            break

    ## 5. MENGOLAH DATA
    # Menggunakan dataset dari sklearn
    if (namadata == 1 or namadata == 2 or namadata == 3) :
        ## 5.1 INISIALISASI LABEL
        plt.xlabel(data.feature_names[col1-1])
        plt.ylabel(data.feature_names[col2-1])

        ## 5.2 MEMBUAT CONVEXHULL
        for i in range(len(data.target_names)) :
            convexhull.convexIndex.clear()
            bucket = df[df['Target'] == i]
            bucket = bucket.iloc[:,[col1-1,col2-1]].values
            hull = convexhull.myConvexHull(bucket)
            plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i])
            for simplex in hull:
                plt.plot(bucket[simplex, 0], bucket[simplex, 1], colors[i%3])

    # Menggunakan dataset csv
    elif (namadata == 4):
        ## 5.1 INISIALISASI LABEL
        plt.xlabel(column[col1-1])
        plt.ylabel(column[col2-1])
        target = df.target.unique()

        ## 5.2 MEMBUAT CONVEXHULL
        for i in range(len(target)) :
            convexhull.convexIndex.clear()
            bucket = df[df['target'] == target[i]]
            bucket = bucket.iloc[:,[col1-1,col2-1]].values
            hull = convexhull.myConvexHull(bucket)
            plt.scatter(bucket[:, 0], bucket[:, 1], label=target[i])
            for simplex in hull:
                plt.plot(bucket[simplex, 0], bucket[simplex, 1], colors[i%3])

    ## 6. MENAMPILKAN VISUALISASI HASIL
    plt.legend()
    plt.show()