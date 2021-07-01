import time
from sage.all import mq

def recoverKey(n, r, c, e):
    """     n: number of rounds
    r: number of rows of the state array
    c: number of columns of the state array
    e: word size"""
    print("n:", n, "r:", r, "c:", c, "e:", e)
    vectorp = [0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1]
    vectork = [1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1]

    aes = mq.SR(n, r, c, e, gf2=True, star=True, allow_zero_inversions=True)
    plain = aes.vector(vectorp[0:(r*c*e)])
    print("plain: ", plain._list())
    key = aes.vector(vectork[0:(r*c*e)])
    print("key:   ", key._list())

    # set_verbose(2)
    cipher = aes(plain, key)
    # set_verbose(0)

    print("cipher:", cipher._list())
    t0 = time.time()
    F, s = aes.polynomial_system(P=plain, C=cipher)
       

    print("                 ########## RESULTS ########## ")
    print("number of solutions:", len(F.ideal().variety()))
    print(F.groebner_basis())
    list(F.groebner_basis())
    for V in F.ideal().variety():
        tmp = []
        for key, value in sorted(V.items()):
            if str(key)[0:2] == "k0":
                tmp.append(int(value))
            result = []
            for i in range(len(tmp)):
                result.append(tmp[len(tmp) - 1 - i])
                print(result)
    
    print(time.time() - t0)

if __name__ == "__main__":
    print("*********************** 1 ********************")
    recoverKey(1, 1, 1, 4)

    print("*********************** 2 ********************")
    recoverKey(2, 1, 1, 4)

    print("*********************** 3 ********************")
    recoverKey(2, 2, 1, 4)

    print("*********************** 4 ********************")
    recoverKey(1, 2, 1, 4)

    print("*********************** 5 ********************")
    recoverKey(3, 2, 1, 4)

    print("*********************** 6 ********************")
    recoverKey(3, 1, 1, 4)

    print("*********************** 7 ********************")
    recoverKey(3, 2, 1, 4)

    print("*********************** 8 ********************")
    recoverKey(4, 2, 1, 4)

    print("*********************** 9 ********************")
    recoverKey(1, 2, 2, 4)

    print("*********************** 10 ********************")
    recoverKey(1, 1, 1, 8)

    print("*********************** 11 ********************")
    recoverKey(2, 1, 1, 8)

    print("*********************** 12 ********************")
    recoverKey(3, 1, 1, 8)

    print("*********************** 13 ********************")
    recoverKey(2, 2, 2, 4)

    print("*********************** 14 ********************")
    recoverKey(4, 1, 1, 8)

    print("*********************** 15 ********************")
    recoverKey(1, 2, 1, 8)

    print("*********************** 16 ********************")
    recoverKey(2, 2, 1, 8)

    print("*********************** 17 ********************")
    recoverKey(1, 2, 2, 8)
