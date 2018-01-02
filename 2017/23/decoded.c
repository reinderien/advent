c = 123700;  // set c b
for (b = 106700;; b += 17) {	// sub b -17
    f = 1;	     // set f 1
    d = 2;	     // set d 2
    do {
        e = 2;	 // set e 2

        do {
            if (d*e - b == 0)  // jnz g 2
                f = 0;         // set f 0
            e++;               // sub e -1
        } while (e - b != 0);  // jnz g -8

        d++;    	        // sub d -1
    } while (d - b != 0);	// jnz g -13

    if (f == 0) 	// jnz f 2
        h++;    	// sub h -1
    if (b - c == 0) // jnz g 2
        break;   	// jnz 1 3
} // jnz 1 -23
