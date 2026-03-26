import psycopg2
import json
import csv

with open("config.json", "r") as f:
    json_config = json.load(f)

conn = psycopg2.connect(
    host=json_config["host"],
    database=json_config["db_name"],
    user=json_config["user"],
    password=json_config["password"]
)

def create_table_if_not_exists() -> None:
    req = """
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                phone VARCHAR(63)
            )
          """
    with conn.cursor() as cursor:
        cursor.execute(req)
        conn.commit()


def print_contacts(contacts: list[tuple]) -> None:
    print()
    if not contacts:
        print("(no contacts)")
        return
    
    for c in contacts:
        print(f"[{c[0]}]. {c[1]} - {c[2]}")


def get_all_contacts() -> list[tuple]:
    req = """
            SELECT * FROM contacts
          """
    with conn.cursor() as cursor:
        cursor.execute(req)
        data = cursor.fetchall()

    return data


def find_contacts(pattern: str) -> list[tuple]:
    req = """
            SELECT * FROM contacts WHERE (name ILIKE %s OR phone ILIKE %s)
          """
    pattern = f"%{pattern}%"
    with conn.cursor() as cursor:
        cursor.execute(req, (pattern, pattern))
        data = cursor.fetchall()

    return data


def add_from_terminal() -> None:
    req = """
            INSERT INTO contacts(name, phone) VALUES (%s, %s)
          """
    name = input("Name: ")
    phone = input("Phone: ")
    with conn.cursor() as cursor:
        cursor.execute(req, (name, phone))
        conn.commit()


def insert_from_csv(path: str) -> None:
    req = """
            INSERT INTO contacts(name, phone) VALUES (%s, %s)
          """
    with conn.cursor() as cur:
        with open(path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                name, phone = row
                cur.execute(req, (name, phone))
        conn.commit()


def update_phone_by_name(name: str, new_phone: str) -> None:
    req = """
            UPDATE contacts SET phone = %s WHERE name = %s
          """
    with conn.cursor() as cursor:
        cursor.execute(req, (new_phone, name))
        conn.commit()


def update_name_by_phone(name: str, new_phone: str) -> None:
    req = """
            UPDATE contacts SET name = %s WHERE phone = %s
          """
    with conn.cursor() as cursor:
        cursor.execute(req, (name, new_phone))
        conn.commit()


def delete_by_name(name: str) -> None:
    req = """
            DELETE FROM contacts WHERE name = %s
          """
    with conn.cursor() as cursor:
        cursor.execute(req, (name,))
        conn.commit()


def delete_by_phone(phone: str) -> None:
    req = """
            DELETE FROM contacts WHERE phone = %s
          """
    with conn.cursor() as cursor:
        cursor.execute(req, (phone,))
        conn.commit()
    

def main() -> None:
    create_table_if_not_exists()

    while True:
        print()
        print("--- PhoneBook ---")
        print("1(s). Show all contacts")
        print("2(a). Add contact (from terminal)")
        print("3(c). Add from CSV")
        print("4(f). Find by name or phone")
        print("5(pn). Update phone by name")
        print("6(np). Update name by phone")
        print("7(dn). Delete by name")
        print("8(dp). Delete by phone")
        print("0(q). Exit")

        choice = input("\nChoice: ")

        if choice == "1" or choice == "s":
            print_contacts(get_all_contacts())
        elif choice == "2" or choice == "a":
            add_from_terminal()
        elif choice == "3" or choice == "c":
            filename = input("CSV file path: ")
            insert_from_csv(filename)
        elif choice == "4" or choice == "f":
            pattern = input("Find: ")
            print_contacts(find_contacts(pattern))
        elif choice == "5" or choice == "pn":
            name = input("Name: ")
            new_phone = input("New phone: ")
            update_phone_by_name(name, new_phone)
        elif choice == "6" or choice == "np":
            phone = input("Phone: ")
            new_name = input("New name: ")
            update_name_by_phone(phone, new_name)
        elif choice == "7" or choice == "dn":
            name = input("Name: ")
            delete_by_name(name)
        elif choice == "8" or choice == "dp":
            phone = input("Phone: ")
            delete_by_phone(phone)
        elif choice == "0" or choice == "q":
            break
        else:
            print("Please choose valid option")

    conn.close()

if __name__ == "__main__":
    main()
