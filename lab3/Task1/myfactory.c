#include "myfactory.h"
#include <dlfcn.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void* myfactory(char const* libname, char const* ctorarg, char const* mem_all_type) {
    
    if (strcmp(mem_all_type, "heap") != 0 && strcmp(mem_all_type, "stack")) {
        printf("Za odabir cuvanja memorije mora biti unešeno ili \"heap\" ili \"stack\"");
        exit(1);
    }

    // stvaranje putanje za biblioteku na temelju imena:
    size_t path_len = strlen("./") + strlen(libname) + strlen(".so") + 1;
    char* libpath = malloc(path_len);
    if (!libpath) {
        fprintf(stderr, "Greška pri alokaciji memorije za putanju.\n");
        return NULL;
    }
    snprintf(libpath, path_len, "./%s.so", libname);

    //otvaranje dinamicke biblioteke:
    void *handle = dlopen(libpath, RTLD_LAZY);
    free(libpath);
    if (!handle) {
        fprintf(stderr, "%s\n", dlerror());
        exit(1);
    }
    dlerror();   

    typedef void* (*constructFun)(void*, char const*);
    typedef int (*sizeFun)();

    constructFun construct = (constructFun) dlsym(handle, "construct");
    sizeFun size = (sizeFun) dlsym(handle, "size");

    const char* error = dlerror();
    if (error != NULL) {
        fprintf(stderr, "Greška pri dlsym: %s\n", error);
        dlclose(handle);
        return NULL;
    }

    int object_size = size();
    void* obj = strcmp(mem_all_type, "heap") == 0 ? malloc(object_size) : alloca(object_size);
    return construct(obj, ctorarg);
}