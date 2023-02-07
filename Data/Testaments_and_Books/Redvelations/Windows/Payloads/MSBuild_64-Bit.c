<!--
# -------------------------------------------------------------------------------
# Copyright: (c) BLS OPS LLC.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------------
-->
#include <stdio.h>																											  
#include <stdlib.h>

int
main(int argc, char *argv[])
{
	FILE *kf;
	size_t ks, n, i;
	long pos;
	unsigned char *key, *buf;

	if (argc != 2) {
		fprintf (stderr, "Usage: %s <key>\a\n", argv[0]);
		exit(1);
	}
	if ((kf = fopen(argv[1], "rb")) == NULL) {
		perror("fopen");
		exit(1);
	}

	if (fseek(kf, 0L, SEEK_END)) {
		perror("fseek");
		exit(1);
	}
	if ((pos = ftell(kf)) < 0) {
		perror("ftell");
		exit(1);
	}
	ks = (size_t) pos;
	if (fseek(kf, 0L, SEEK_SET)) {
		perror("fseek");
		exit(1);
	}
	if ((key = (unsigned char *) malloc(ks)) == NULL) {
		fputs("out of memory", stderr);
		exit(1);
	}
	if ((buf = (unsigned char *) malloc(ks)) == NULL) {
		fputs("out of memory", stderr);
		exit(1);
	}

	if (fread(key, 1, ks, kf) != ks) {
		perror("fread");
		exit(1);
	}

	if (fclose(kf)) {
		perror("fclose");
		exit(1);
	}

	freopen(NULL, "rb", stdin);
	freopen(NULL, "wb", stdout);

	while ((n = fread(buf, 1, ks, stdin)) != 0L) {
		for (i = 0; i < n; i++)
			buf[i] ^= key[i];
		if (fwrite(buf, 1, n, stdout) != n) {
			perror("fwrite");
			exit(1);
		}
	}

	free(buf);
	free(key);

	exit(0);
}