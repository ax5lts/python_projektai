
def show_menu():
    print("\n--- ToDo meniu ---")
    print("1. Prideti užduoti")





    
    print("2. Pašalinti užduoti")
    print("3. Peržiureti užduotis")
    print("4. Baigti programa")

tasks = []

while True:
    show_menu()
    choice = input("Pasirinkite veiksma: ")

    if choice == "1":
        task = input("Iveskite nauja užduoti: ")
        tasks.append(task)
        print(f"Užduotis '{task}' prideąčta.")

    elif choice == "2":
        if tasks:
            for i, t in enumerate(tasks, 1):
                print(f"{i}. {t}")
            num = int(input("Iveskite numeri, kuri norite pašalinti: "))
            if 1 <= num <= len(tasks):
                removed = tasks.pop(num - 1)
                print(f"Užduotis '{removed}' pašalinta.")
            else:
                print("Neteisingas numeris.")
        else:
            print("Sarašas tuščias.")

    elif choice == "3":
        if tasks:
            print("\n Užduoči sarašas:")
            for i, t in enumerate(tasks, 1):
                print(f"{i}. {t}")
        else:
            print("Sarašas tuščias.")

    elif choice == "4":
        print("Programa baigta.")
        break

    else:
        print("Neteisingas pasirinkimas, bandykite dar karta.")
