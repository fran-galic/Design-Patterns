#include <cstdio>
#include <iterator>
#include <iostream>
#include <cstring>
#include <vector>
#include <set>

using namespace std;

template <typename Iterator, typename Predicate>
Iterator mymax(
  Iterator first, Iterator last, Predicate pred){
    Iterator max = first;
    for(Iterator i = first; i != last; i++) {
        if (pred(*i, *max) == 1) {
            max = i;
        }
    }
    return max;
}

int gt_int(const int a, const int b) {
    if (a > b) {
        return 1;
    } else {
        return 0;
    }
}
int gt_char(const char a, const char b) {
    if (a > b) {
        return 1;
    } else {
        return 0;
    }
}
int gt_cppstr(const string& s1, const string& s2) {
    return s1 > s2;
}

int main(void) {
    int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
    char arr_char[] = "Sunca na strana ulice";
    const char* arr_str[] = {
        "Gle", "malu", "vocku", "poslije", "kise",
        "Puna", "je", "kapi", "pa", "ih", "njise"
    };
    // dodatno:
    vector<int> polje;
    polje.push_back(1);
    polje.push_back(2);
    polje.push_back(3);

    set<string> cars = {"Volvo", "BMW", "Ford", "Mazda"};

    printf("Ispisivanje najvecih:\n");

    const int* max_int = mymax(&arr_int[0], &arr_int[sizeof(arr_int) / sizeof(*arr_int)], gt_int);
    cout << "polje int: " << *max_int << endl;

    const char* max_c = mymax(begin(arr_char), end(arr_char), gt_char);
    cout << "polje char: " << *max_c << endl;

    const char** max_s = mymax(begin(arr_str), end(arr_str), gt_cppstr);
    cout << "polje stringova: " << *max_s << endl;

    cout << "vektor intigera: " << *mymax(polje.begin(), polje.end(), gt_int) << endl;
    cout << "set stringova: " << *mymax(cars.begin(), cars.end(), gt_cppstr) << endl;
    return 0;
}

// ZAVRŠNI KOMENTAR:
//
// Ovo rješenje koristi C++ predloške i iteratore što ga čini puno fleksibilnijim od C verzije.
// Prednost je što može raditi s bilo kojim tipom i kontejnerom (niz, vector, set...)
// bez potrebe za ručnim kastanjem ili void* pokazivačima kao u C-u.
// Nedostatak je nešto veća kompleksnost i "magija" iza kulisa koju kompajler odrađuje,
// pa je kod možda manje jasan početnicima u odnosu na C gdje se sve vidi "crno na bijelo".