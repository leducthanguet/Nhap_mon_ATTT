import time
dump = False
def findModularInverse(a, mod):
    while (a<0):
        a = a + mod
    # a = a % mod
    x1 = 1;
    x2 = 0;
    x3 = mod
    y1 = 0;
    y2 = 1;
    y3 = a

    q = int(x3 / y3)
    t1 = x1 - q * y1
    t2 = x2 - q * y2
    t3 = x3 - (q * y3)

    if dump == True:
        print("q\tx1\tx2\tx3\ty1\ty2\ty3\tt1\tt2\tt3")
        print("----------------------------------------------------------------------------")
        print(q, "\t", x1, "\t", x2, "\t", x3, "\t", y1, "\t", y2, "\t", y3, "\t", t1, "\t", t2, "\t", t3)

    while (y3 != 1):
        x1 = y1;
        x2 = y2;
        x3 = y3

        y1 = t1;
        y2 = t2;
        y3 = t3

        q = int(x3 / y3)
        t1 = x1 - q * y1
        t2 = x2 - q * y2
        t3 = x3 - (q * y3)

        if dump == True:
            print(q, "\t", x1, "\t", x2, "\t", x3, "\t", y1, "\t", y2, "\t", y3, "\t", t1, "\t", t2, "\t", t3)
            print("----------------------------------------------------------------------------")
            print("")

    while (y2 < 0):
        y2 = y2 + mod

    return y2


def pointAddition(x1, y1, x2, y2, a, b, mod):
    if x1 == x2 and y1 == y2:
        # doubling
        beta = (3 * x1 * x1 + a) * (findModularInverse(2 * y1, mod))

    else:
        # point addition
        beta = (y2 - y1) * (findModularInverse((x2 - x1), mod))

    x3 = beta * beta - x1 - x2
    y3 = beta * (x1 - x3) - y1

    x3 = x3 % mod
    y3 = y3 % mod

    while (x3 < 0):
        x3 = x3 + mod

    while (y3 < 0):
        y3 = y3 + mod

    return x3, y3


def applyDoubleAndAddMethod(x0, y0, k, a, b, mod):
    x_temp = x0
    y_temp = y0

    kAsBinary = bin(k)  # 0b1111111001
    kAsBinary = kAsBinary[2:len(kAsBinary)]  # 1111111001
    # print(kAsBinary)

    for i in range(1, len(kAsBinary)):
        currentBit = kAsBinary[i: i + 1]
        # always apply doubling
        x_temp, y_temp = pointAddition(x_temp, y_temp, x_temp, y_temp, a, b, mod)

        if currentBit == '1':
            # add base point
            x_temp, y_temp = pointAddition(x_temp, y_temp, x0, y0, a, b, mod)

    return x_temp, y_temp


def textToInt(text):
    encoded_text = text.encode('utf-8')
    hex_text = encoded_text.hex()
    int_text = int(hex_text, 16)
    return int_text
def intToText(int_text):
    import codecs
    hex_text = hex(int_text)
    hex_text = hex_text[2:]  # remove 0x
    return codecs.decode(codecs.decode(hex_text, 'hex'), 'ascii')
# ------------------------------------
# curve configuration
mod = pow(2, 256) - pow(2, 32) - pow(2, 9) - pow(2, 8) - pow(2, 7) - pow(2, 6) - pow(2, 4) - pow(2, 0)
order = 115792089237316195423570985008687907852837564279074904382605163141518161494337
# curve configuration
# y^2 = x^3 + a*x + b = y^2 = x^3 + 7
a = 0
b = 7

# base point on the curve
base_point = [55066263022277343669578718895168534326250603453777594175500187360389116729240,
              32670510020758816978083085130507043184471273380659243275938904335757337482424]

print("---------------------")
print("initial configuration")
print("---------------------")
print("Curve: y^2 = x^3 + ", a, "*x + ", b, " mod ", mod, " , #F(", mod, ") = ", order)
print("Base point: (", base_point[0], ", ", base_point[1], ")")

print()


encryption_begins = time.time()

print("--------------------------------------------------------------")
print("Tạo khóa công khai.")

message = 'hi'
plaintext = textToInt(message)
print("Thông báo gửi đi : ", message, ". số tương ứng là : ", plaintext)

plain_coordinates = applyDoubleAndAddMethod(base_point[0], base_point[1], plaintext, a, b, mod)

print("Thông báo được biểu diễn dưới dạng tọa độ điểm sau")
print("plain coordinates: ", plain_coordinates)

secretKey = 75263518707598184987916378021939673586055614731957507592904438851787542395619

publicKey = applyDoubleAndAddMethod(base_point[0], base_point[1], secretKey, a, b, mod)

print("\npublic key: ", publicKey)

print("--------------------------------------------------------------")
print("encryption")

randomKey = 28695618543805844332113829720373285210420739438570883203839696518176414791234


c1 = applyDoubleAndAddMethod(base_point[0], base_point[1], randomKey, a, b, mod)

c2 = applyDoubleAndAddMethod(publicKey[0], publicKey[1], randomKey, a, b, mod)
c2 = pointAddition(c2[0], c2[1], plain_coordinates[0], plain_coordinates[1], a, b, mod)

print("\nciphertext")
print("c1: ", c1)
print("c2: ", c2)

encryption_ends = time.time()

print("encryption lasts ", encryption_ends - encryption_begins, " seconds")
print("--------------------------------------------------------------")
# plaintext = c2 - secretKey * c1

decryption_begins = time.time()

# secret key times c1
dx, dy = applyDoubleAndAddMethod(c1[0], c1[1], secretKey, a, b, mod)
# -secret key times c1
dy = dy * -1  # curve is symmetric about x-axis. in this way, inverse point found

# c2 + secret key * (-c1)
decrypted = pointAddition(c2[0], c2[1], dx, dy, a, b, mod)
print("decrypted coordinates: ", decrypted)

# -----------------------------------

decrytion_begin = time.time()
new_point = pointAddition(base_point[0], base_point[1], base_point[0], base_point[1], a, b, mod)  # 2P

# brute force method
for i in range(3, order):
    new_point = pointAddition(new_point[0], new_point[1], base_point[0], base_point[1], a, b, mod)
    if new_point[0] == decrypted[0] and new_point[1] == decrypted[1]:
        print("decrypted message as numeric: ", i)
        print("decrypted message: ", intToText(i))
        break
print("Đối chiếu với thông báo được gửi ban đầu. Trùng với thông báo ban đầu => thuật toán đúng")