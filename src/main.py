import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
from sympy import false, true
import convexhull
import os.path
from os import path

## 1. INPUT NAMA DATASET
print("\n   _   _   _   _   _   _     _   _   _   _  ")
print("  / \ / \ / \ / \ / \ / \   / \ / \ / \ / \ ")
print(" ( C | o | n | v | e | x ) ( H | u | l | l )")
print("  \_/ \_/ \_/ \_/ \_/ \_/   \_/ \_/ \_/ \_/ \n")
print("Terdapat beberapa dataset yang dapat diakses, antara lain =")
print("1 Iris")
print("2 Wine")
print("3 Cancer")
print("4 File CSV (Pastikan sudah ada di folder test)")
print("")
namadata = int(input("Pilihan (dalam angka) = "))

## 2. LOAD DATASET & MEMBUAT DATAFRAME
if (namadata == 1) :
    data = datasets.load_iris()
    punyatarget = true
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['Target'] = pd.DataFrame(data.target)
elif (namadata == 2) :
    data = datasets.load_wine()
    punyatarget = true
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['Target'] = pd.DataFrame(data.target)
elif (namadata == 3) :
    data = datasets.load_breast_cancer()
    punyatarget = true
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['Target'] = pd.DataFrame(data.target)
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
    # Menggunakan dataset sklearn
    if (namadata == 1 or namadata == 2 or namadata == 3) :
        ## 3. MEMBUAT DATAFRAME
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df['Target'] = pd.DataFrame(data.target)
        col = len(df.columns) - 1
        print("Dataset ini terdiri atas ", col, "kolom, yaitu = ")
        for i in range (col) :
            print(i+1, data.feature_names[i])
        print("\nSilahkan pilih kolom acuan (dalam angka)!")
        while (True) :
            col1 = int(input("Acuan X = "))
            if (col1 > 0 and col1 <= col) :
                break
        while (True) :
            col2 = int(input("Acuan Y = "))
            if (col2 > 0 and col2 <= col) :
                break

        ## 4. INISIALISASI PYPLOT
        plt.figure(figsize = (10, 6))
        colors = ['b','r','g']
        plt.title(label='Convex Hull', fontsize=20)
        plt.xlabel(data.feature_names[col1-1])
        plt.ylabel(data.feature_names[col2-1])

        ## 5. MEMBUAT CONVEXHULL
        for i in range(len(data.target_names)) :
            convexhull.convexIndex.clear()
            bucket = df[df['Target'] == i]
            bucket = bucket.iloc[:,[col1-1,col2-1]].values
            hull = convexhull.myConvexHull(bucket)
            plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i])
            for simplex in hull:
                plt.plot(bucket[simplex, 0], bucket[simplex, 1], colors[i%3])

    # Menggunakan dataset csv`
    elif (namadata == 4):
        ## 3. MEMBUAT DATAFRAME
        print("Dataset ini terdiri atas ", len(df.columns) - 1, "kolom, yaitu = ")
        col = df.columns.values.tolist()
        for i in range(len(df.columns)): 
            if (col[i] == "target") :
                continue
            print(i + 1, col[i])
        print("\nSilahkan pilih kolom acuan (dalam angka)!")
        while (True) :
            col1 = int(input("Acuan X = "))
            if (col1 > 0 and col1 <= len(col)) :
                break
        while (True) :
            col2 = int(input("Acuan Y = "))
            if (col2 > 0 and col2 <= len(col)) :
                break

        ## 4. INISIALISASI PYPLOT
        plt.figure(figsize = (10, 6))
        colors = ['b','r','g']
        plt.title(label='Convex Hull', fontsize=20)
        plt.xlabel(col[col1-1])
        plt.ylabel(col[col2-1])
        target = df.target.unique()

        ## 5. MEMBUAT CONVEXHULL
        for i in range(len(target)) :
            convexhull.convexIndex.clear()
            bucket = df[df['target'] == target[i]]
            bucket = bucket.iloc[:,[col1-1,col2-1]].values
            hull = convexhull.myConvexHull(bucket)
            P1, Pn = convexhull.extremePoints(bucket)
            plt.scatter(bucket[:, 0], bucket[:, 1], label=target[i])
            for simplex in hull:
                plt.plot(bucket[simplex, 0], bucket[simplex, 1], colors[i%3])


    ## 6. MENAMPILKAN VISUALISASI HASIL
    plt.legend()
    plt.show()