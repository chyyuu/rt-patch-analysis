#include <stdio.h>
#include <stdbool.h>

bool condition() { return false; }

void spin_lock_irqsave() {
    printf("spin_lock_irqsave\n");
}

void spin_unlock_irqrestore() {
    printf("spin_unlock_irqrestore\n");
}

void foo() {
    spin_lock_irqsave();
    while (condition()) {
        spin_lock_irqsave();

        int i = 1, j = 2;
        double k = i + j;

        printf("%f\n", k);

        spin_unlock_irqrestore();
    }

    for (int i = 0; i < 10; i++) {

    }

    spin_unlock_irqrestore();
}

int main(int argc, char const *argv[]) {
    foo();
    return 0;
}