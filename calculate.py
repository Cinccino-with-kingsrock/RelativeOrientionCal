import numpy as np

file = open(file=('D:\大學用\大三\下學期\攝影測量實習\chp2\新的\data.txt'), mode='r', encoding='utf-8')
rotate = open(file=('D:\大學用\大三\下學期\攝影測量實習\chp2\新的\R.txt'), mode='r', encoding='utf-8')
EOIO_iphone = []
R_iphone = []
EOIO_xi =[]
R_xi = []

for line in file.readlines()[:13]: #4-9 Camera Image Xc Yc	 Zc	  Omega	  Phi   Kappa	
    data = line.split()
    for i in range(len(data))[2:]:
        EOIO_iphone.append(float(data[i]))
file.seek(0)

for line in file.readlines()[13:]: #4-9 Camera Image Xc Yc	 Zc	  Omega	  Phi   Kappa	
    data = line.split()
    for i in range(len(data))[2:]:
        EOIO_xi.append(float(data[i]))

for line in rotate.readlines()[:13]:#10項
    data = line.split()
    for i in range(len(data))[1:]:#只有數字    Image  R11  R12  R13  R21  R22  R23  R31  R32  R33
        R_iphone.append(float(data[i]))
rotate.seek(0)

for line in rotate.readlines()[13:]:#10項
    data = line.split()
    for i in range(len(data))[1:]:#只有數字    Image  R11  R12  R13  R21  R22  R23  R31  R32  R33
        R_xi.append(float(data[i]))

file.close()
rotate.close()

EOIO_iphone = np.array(EOIO_iphone).reshape(13,9)
EOIO_xi = np.array(EOIO_xi).reshape(13,9)
R_iphone = np.array(R_iphone).reshape(13,9)
R_xi = np.array(R_xi).reshape(13,9)
###################讀取數據######################
iphone_reshape = []
for row in R_iphone:
    iphone_reshape.append(np.transpose(row.reshape(3,3)))
iphone_reshape = np.array(iphone_reshape)

xi_reshape = []
for row in R_xi:
    xi_reshape.append(np.transpose(row.reshape(3,3)))
xi_reshape = np.array(xi_reshape)
#######將資料轉換為3*3的矩陣#########
iphone_inv = []
xi_inv = []

for row in iphone_reshape:
    iphone_inv.append(np.linalg.inv(row))

for row in xi_reshape:
    xi_inv.append(np.linalg.inv(row))

iphone_inv = np.array(iphone_inv)
xi_inv = np.array(xi_inv)
########產生逆矩陣############
A2 =[]
for apple,xi in zip(iphone_inv,xi_reshape):
    A2.append(np.dot(apple,xi))
A2 = np.array(A2)
#############################
R13 = []
for matrix in A2:
    R13.append(matrix[0, 2])
results_φ = [np.arcsin(value) for value in R13]

R23 =[]
for matrix in A2:
    R23.append(matrix[1, 2])

R33 =[]
for matrix in A2:
    R33.append(matrix[2, 2])

results_tanω = []
for r23, r33 in zip(R23,R33):
    results_tanω.append(np.arctan(-(r23/r33)))

R12 = []
for matrix in A2:
    R12.append(matrix[0, 1])

R11 = []
for matrix in A2:
    R11.append(matrix[0, 0])

results_tanκ = []
for r12, r11 in zip(R12,R11):
    results_tanκ.append(np.arctan(-(r12/r11)))
############ Omega  Phi  Kappa ###################
data = {
    'ω_values': results_tanω,
    'φ_values': results_φ,
    'κ_values': results_tanκ
}

with open('D:\\大學用\\大三\\下學期\\攝影測量實習\\chp2\\新的\\relative orientation.txt', mode='w') as file:
    for i in range(13):
        file.write(f"{data['ω_values'][i]}\t {data['φ_values'][i]}\t {data['κ_values'][i]}\n")
#############相對方位###############s      
XYZ_iphone = []
for line in EOIO_iphone:
    XYZ_iphone.append(line[:3])
XYZ_iphone= np.array(XYZ_iphone)

XYZ_xi =[]
for line in EOIO_xi:
    XYZ_xi.append(line[:3])
XYZ_xi = np.array(XYZ_xi)

XYZ =XYZ_iphone - XYZ_xi
results =[np.dot(matrix,np.transpose(XYZ[i])) for i, matrix in enumerate(iphone_inv, start=0)]

with open('D:\\大學用\\大三\\下學期\\攝影測量實習\\chp2\\新的\\relative orientation2.txt',mode= "w") as f:
    for i, result in enumerate(results, start=1):
        f.write(f"{result}\n")