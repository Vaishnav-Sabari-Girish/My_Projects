from arduino_utils import create_new_sketch

file_name = str(input("Enter sketch filename : "))

sketch_path = create_new_sketch(f"{file_name}")

print(sketch_path)
