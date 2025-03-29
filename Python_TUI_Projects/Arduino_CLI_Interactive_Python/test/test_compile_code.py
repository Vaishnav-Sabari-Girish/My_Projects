from arduino_utils import compile_sketch

filename = "Test/Test.ino"
fqbn = "arduino:avr:uno"

compile_sketch(filename, fqbn)
