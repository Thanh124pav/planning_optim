import math 


def binary_present(a):
    if a == 0:
        return [], ""
    n = int(math.log2(a))
    results = [n]
    a1 = a - 2**n 
    results1, _ = binary_present(a1)
    results.extend(results1)
    ans_list = [ f"2^{i}" for i in results]
    present = " + ".join(ans_list)
    ans = f"{a} = " + present
    return results, ans

def compute_modulo(m, n, k):
    if k == 0:
        return 1 
    binary_arr, _ = binary_present(k)
    M = m
    res = 1
    for i in range(binary_arr[0] + 1): # 2^0 to 2^T
        r = M%n # m^{2^i} % n
        if i in binary_arr:
            res = res*r % n
        M = r*r % n # M \eqiuv m^{2^{i+1}} mod n
    return res % n 

if __name__ == "__main__":
    m = 2
    n = 3
    k = 2004
    print(f"m = {m}, n = {n}, k = {k}")
    _, ans = binary_present(k)
    print(ans)
    print(compute_modulo(m, n, k))