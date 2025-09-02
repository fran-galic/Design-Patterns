

import random

# racunanje percentila;
def percentile_moja_ideja(data, perc):
    if not data:
        raise ValueError("Nije moguće odrediti percentile od praznih nizova.")
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * (perc / 100)
    f = int(k)
    c = min(f + 1, len(sorted_data) - 1)
    if f == c:
        return sorted_data[int(k)]
    d0 = sorted_data[f] * (c - k)
    d1 = sorted_data[c] * (k - f)
    return d0 + d1

def percentil_klasicno(data, perc):
    if not data:
        raise ValueError("Nije moguće odrediti percentile od praznih nizova.")
    sorted_data = sorted(data)
    N = len(sorted_data)
    n_p = perc * N / 100 + 0.5
    idx = round(n_p) - 1
    idx = min(max(idx, 0), N - 1) 
    return sorted_data[idx]

def percentil_interpolirano(data, p):
    if not data:
        raise ValueError("Nije moguće odrediti percentile od praznih nizova.")
    soreted_data = sorted(data)
    N = len(soreted_data)

    p_min = 100 * (0.5) / N
    p_max = 100 * (N - 0.5) / N

    if p <= p_min:
        return soreted_data[0]
    if p >= p_max:
        return soreted_data[-1]

    for i in range(N - 1):
        p_i = 100 * (i + 0.5) / N
        p_next = 100 * (i + 1.5) / N

        if p_i <= p < p_next:
            v_i = soreted_data[i]
            v_next = soreted_data[i + 1]
            omjer = (p - p_i) / (p_next - p_i)
            return v_i + omjer * (v_next - v_i)

def gen_slijedno(first, stop, step):
    arr = []
    for i in range(first, stop, step):
        arr.append(i)
    return arr

def gen_gauss(e, std, n):
    return [ int(random.gauss(e, std)) for _ in range(n)]

def gen_fibonacci(n):
    arr= []
    a, b = 0, 1
    for _ in range(n):
        arr.append(a)
        a, b = b, a + b
    return arr

class DistributionTester:
    def __init__(self, generator=None, find_percentile=None):
        self.generator = generator
        self.find_percentile = find_percentile
    
    # dodatna mogucnost - omogucava nam dinamicko mnijenjanje strategije generiranja kada je objekt vec stvoren
    def set_generator(self, generator):
        self.generator = generator

    def set_find_percentile(self, find_percentile):
        self.find_percentile = find_percentile
    
    def generate_array(self, *args, **kwargs):
        if self.generator is None:
            raise ValueError("Strategija za generiranje nizova nije postavljanja")
        self.array = self.generator(*args, **kwargs)
        print(f"Generirani array: \n{self.array}")

    def print_percenitles(self):
        if self.array is None:
            raise AttributeError("Array jos nije generiran. Pozovite generate_array() i provjerite dali ste" \
            "postavili strategiju za generiranje brojeva")
        if self.find_percentile is None:
            raise AttributeError("Funkcija za traženje percentila još nije postavljena")
        print("10-ti percentili:")
        percentili= [self.find_percentile(self.array, i) for i in range(10, 100, 10)]
        print(percentili)
        return percentili
    
    def print_single_percentile(self, perc):
        if self.array is None:
            raise AttributeError("Array jos nije generiran. Pozovite generate_array() i provjerite dali ste" \
            "postavili strategiju za generiranje brojeva")
        if self.find_percentile is None:
            raise AttributeError("Funkcija za traženje percentila još nije postavljena")
        print(self.find_percentile(self.array, perc) )
    

def main():
    # testiranje generirajucih funkcija:
    print(gen_slijedno(1,6,1))
    print(gen_gauss(50, 10, 5))
    print(gen_fibonacci(5))

    # glavni dio koda:
    print()
    print("Glavni dio programa:")
    dis_test = DistributionTester(generator= gen_slijedno, find_percentile= percentil_interpolirano)
    dis_test.generate_array(0, 10, 1)
    dis_test.print_percenitles()
    dis_test.set_find_percentile(find_percentile= percentil_klasicno)
    dis_test.print_percenitles()

    dis_test.set_generator(generator= gen_gauss)
    dis_test.set_find_percentile(find_percentile= percentile_moja_ideja)
    dis_test.generate_array(0, 10, 10)
    dis_test.print_percenitles()

    dis_test.set_generator(generator= gen_fibonacci)
    dis_test.set_find_percentile(find_percentile= percentil_interpolirano)
    dis_test.generate_array(10)
    dis_test.print_percenitles()


if __name__ == "__main__":
    main()