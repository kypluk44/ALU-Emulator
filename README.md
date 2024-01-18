# ALU Emulator Documentation

## Project Overview

This project is an emulator for an Arithmetic Logic Unit (ALU) designed for a processor. Throughout the project, you will create a model capable of performing comparison, addition, and bitwise logical operations on two 8-bit integers. The project is developed to understand the fundamental principles of computer operation.

## Project Structure

The project consists of several files:

1. **test.py:** File containing program tests. Tests are automatically executed using Gitlab CI for automated solution verification.

2. **lib/core.py:** File containing abstractions at the lowest level, such as contacts and conductors.

3. **lib/utils.py:** File containing auxiliary constructions.

4. **lib/circuit.py:** Main project file containing the models of basic elements such as NOT, AND, OR, and their compositions for various operations.

## Logical Elements

The logical elements implemented in the project include:

1. **NAND:** Performs the NAND operation.
2. **XOR:** Performs the XOR operation.
3. **AND3:** Three-input AND gate.
4. **OR3:** Three-input OR gate.
5. **XNOR:** Performs the XNOR operation.

## Additional Logical Circuits

The project includes the implementation of additional logical circuits:

1. **ODD:** Outputs 1 if an odd number of input signals are 1; otherwise, outputs 0.
2. **MT1:** Outputs 1 if signals 1 are present on 2, 3, or all inputs; otherwise, outputs 0.
3. **SC:** A circuit with 3 inputs and 4 outputs, counting the number of 1s on the inputs and providing the count on the corresponding outputs.
4. **HADD:** Implements the addition of two bits (a and b) and returns the sum (S) and carry (C).
5. **ADD:** Implements the addition of two bits (a and b) with a carry (c) and returns the sum (S) and carry (C).

## How to Run the Emulator

To run the emulator, follow these steps:

1. Open the terminal and navigate to the project directory.

2. Run the `test.py` file using the following command:
   ```bash
   python test.py
