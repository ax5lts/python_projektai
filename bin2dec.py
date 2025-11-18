while True:
    binary = input("Įveskite dvejetainį skaičių (arba 'q' baigti): ")

    if binary.lower() == 'q':
        print("Programa baigta.")
        break

    try:
        decimal = int(binary, 2)
        print(f"{binary} -> {decimal}")
    except ValueError:
        print("Klaida: įveskite tik 0 ir 1 simbolius.")
