// Based on http://openwall.info/wiki/people/solar/software/public-domain-source-code/md5

#pragma once

#include <stdint.h>

/* Any 32-bit or wider unsigned integer data type will do */
typedef uint32_t MD5_u32plus;

typedef struct {
	MD5_u32plus lo, hi;
	MD5_u32plus a, b, c, d;
	unsigned char buffer[64];
	MD5_u32plus block[16];
} MD5_CTX;


extern void MD5_Init(MD5_CTX *ctx);
extern void MD5_Update(MD5_CTX *ctx, const void *data, unsigned long size);
extern void MD5_Final(MD5_CTX *ctx);
