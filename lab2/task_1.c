#include <stddef.h>
#include <string.h>
#include <stdio.h>

const void* mymax(
  const void *base, size_t nmemb, size_t size,
  int (*compar)(const void *, const void *)) {

    const char* p = base;
    const void* max = p;

    for (int i = 1; i < nmemb; i++) { 
        const void* current = p + i * size;
        if (compar(current, max) == 1) {
            max = current;
        }
    }

    return max;
}

int gt_int(const void* a, const void* b) {
    if (*(int*)a > *(int*)b) {
        return 1;
    } else {
        return 0;
    }
}
int gt_char(const void* a, const void* b) {
    if (*(char*)a > *(char*)b) {
        return 1;
    } else {
        return 0;
    }
}
int gt_str(const void* s1, const void* s2) {
    const char* const* str1 = s1;
    const char* const* str2 = s2;

    if (strcmp(*str1, *str2) > 0) {
        return 1;
    } else {
        return 0;
    }
}

int main(void) {
    int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
    char arr_char[] = "Sunca na strana ulice";
    const char* arr_str[] = {
        "Gle", "malu", "vocku", "poslije", "kise",
        "Puna", "je", "kapi", "pa", "ih", "njise"
    };

    printf("Ispisivanje najvecih:\n");

    printf("polje integera: %d\n", *(int*)mymax(arr_int, 9, sizeof(int), gt_int));
    printf("polje char: %c\n", *(char*)mymax(arr_char, sizeof(arr_char) - 1, sizeof(char), gt_char));
    printf("polje stringova: %s\n", *(char**)mymax(arr_str, 11, sizeof(char*), gt_str));

    return 0;
}