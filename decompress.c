#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_DICT 4096

typedef struct
{
    unsigned char *data;
    int length;
} DictEntry;

DictEntry dict[MAX_DICT];
int dictSize;

void initDict()
{
    dictSize = 256;
    for (int i = 0; i < 256; i++)
    {
        dict[i].data = malloc(1);
        dict[i].data[0] = (unsigned char)i;
        dict[i].length = 1;
    }
}

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        printf("Usage: ./decompress <compressed.bin> <output_file>\n");
        return 1;
    }

    FILE *in = fopen(argv[1], "rb");
    FILE *out = fopen(argv[2], "wb");

    if (!in || !out)
    {
        printf("File error\n");
        return 1;
    }

    initDict();

    int prevCode;
    fread(&prevCode, sizeof(int), 1, in);
    fwrite(dict[prevCode].data, 1, dict[prevCode].length, out);

    int currCode;
    while (fread(&currCode, sizeof(int), 1, in) == 1)
    {
        if (currCode >= dictSize)
            break;

        fwrite(dict[currCode].data, 1, dict[currCode].length, out);

        if (dictSize < MAX_DICT)
        {
            int newLen = dict[prevCode].length + 1;
            dict[dictSize].data = malloc(newLen);
            memcpy(dict[dictSize].data, dict[prevCode].data, dict[prevCode].length);
            dict[dictSize].data[newLen - 1] = dict[currCode].data[0];
            dict[dictSize].length = newLen;
            dictSize++;
        }

        prevCode = currCode;
    }

    fclose(in);
    fclose(out);

    printf("Decompression completed successfully\n");
    return 0;
}
