#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_DICT 4096

typedef struct {
    unsigned char *data;
    int length;
} DictEntry;

DictEntry dict[MAX_DICT];
int dictSize;

void initDict() {
    dictSize = 256;
    for (int i = 0; i < 256; i++) {
        dict[i].data = malloc(1);
        dict[i].data[0] = (unsigned char)i;
        dict[i].length = 1;
    }
}

int findInDict(unsigned char *data, int len) {
    for (int i = 0; i < dictSize; i++) {
        if (dict[i].length == len &&
            memcmp(dict[i].data, data, len) == 0)
            return i;
    }
    return -1;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: ./compress <input_file> <compressed.bin>\n");
        return 1;
    }

    FILE *in = fopen(argv[1], "rb");
    FILE *out = fopen(argv[2], "wb");

    if (!in || !out) {
        printf("File error\n");
        return 1;
    }

    initDict();

    unsigned char w[4096];
    int wlen = 0;
    unsigned char c;

    if (fread(&c, 1, 1, in) != 1) return 0;
    w[0] = c;
    wlen = 1;

    while (fread(&c, 1, 1, in) == 1) {
        unsigned char wc[4096];
        memcpy(wc, w, wlen);
        wc[wlen] = c;

        int index = findInDict(wc, wlen + 1);

        if (index != -1) {
            memcpy(w, wc, wlen + 1);
            wlen++;
        } else {
            int code = findInDict(w, wlen);
            fwrite(&code, sizeof(int), 1, out);

            if (dictSize < MAX_DICT) {
                dict[dictSize].data = malloc(wlen + 1);
                memcpy(dict[dictSize].data, wc, wlen + 1);
                dict[dictSize].length = wlen + 1;
                dictSize++;
            }

            w[0] = c;
            wlen = 1;
        }
    }

    int lastCode = findInDict(w, wlen);
    fwrite(&lastCode, sizeof(int), 1, out);

    fclose(in);
    fclose(out);

    printf("Compression completed successfully\n");
    return 0;
}
