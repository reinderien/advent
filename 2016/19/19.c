#include <assert.h>
#include <stdio.h>
#include <stdlib.h>


struct Elf_tag
{
    unsigned id;
    unsigned presents;
    struct Elf_tag *next;
};
typedef struct Elf_tag Elf;

unsigned run(unsigned n_elves)
{
    Elf *all_elves = malloc(n_elves * sizeof(Elf));

    unsigned i;
    for (i = 0; i < n_elves; i++)
    {
        all_elves[i].id = i+1;
        all_elves[i].next = all_elves + (i+1)%n_elves;
        all_elves[i].presents = 1;
    }

    Elf *e;
    for (e = all_elves; e != e->next; e = e->next)
    {
        e->presents += e->next->presents;
        e->next = e->next->next;
    }

    return e->id;
}

int main()
{
    assert(run(5) == 3);

    printf("Part 1: %u\n", run(3001330));
    return 0;
}