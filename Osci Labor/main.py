import pyvisa


OSZI_IP = "169.254.7.40" #169.254.7.40
RESOURCE = f"TCPIP0::{OSZI_IP}::INSTR"


def connect():
    rm = pyvisa.ResourceManager("@py")

    scope = rm.open_resource(RESOURCE)
    scope.write_termination = "\n"
    scope.read_termination = "\n"
    scope.timeout = 5000

    return scope


def check_channel(channel):
    if channel < 1 or channel > 4:
        print("Fehler: Channel muss zwischen 1 und 4 sein.")
        return False

    return True


def show_idn(scope):
    answer = scope.query("*IDN?")
    print("Geräteinfo:")
    print(answer.strip())


def select_channel(scope):
    channel = int(input("Channel 1-4: "))

    if not check_channel(channel):
        return

    for i in range(1, 5):
        scope.write(f":CHANnel{i}:DISPlay OFF")

    scope.write(f":CHANnel{channel}:DISPlay ON")

    print(f"Channel {channel} wurde eingeschaltet.")


def set_y_scale(scope):
    channel = int(input("Channel 1-4: "))
    scale = float(input("Y-Scale in V/div, z.B. 0.5: "))

    if not check_channel(channel):
        return

    scope.write(f":CHANnel{channel}:DISPlay ON")
    scope.write(f":CHANnel{channel}:SCALe {scale}")

    current_scale = scope.query(f":CHANnel{channel}:SCALe?")
    print(f"Y-Scale CH{channel}: {current_scale.strip()} V/div")


def set_x_scale(scope):
    scale = float(input("X-Scale in s/div, z.B. 0.001: "))

    scope.write(f":TIMebase:MAIN:SCALe {scale}")

    current_scale = scope.query(":TIMebase:MAIN:SCALe?")
    print(f"X-Scale: {current_scale.strip()} s/div")


def measure(scope):
    channel = int(input("Channel 1-4: "))

    if not check_channel(channel):
        return

    print("Messwerte:")
    print("1 - VMAX")
    print("2 - VMIN")
    print("3 - VPP")
    print("4 - VRMS")
    print("5 - FREQ")
    print("6 - PERIOD")

    choice = input("Auswahl: ")

    match choice:
        case "1":
            measurement = "VMAX"
        case "2":
            measurement = "VMIN"
        case "3":
            measurement = "VPP"
        case "4":
            measurement = "VRMS"
        case "5":
            measurement = "FREQ"
        case "6":
            measurement = "PER"
        case _:
            print("Ungültige Auswahl.")
            return

    scope.write(f":CHANnel{channel}:DISPlay ON")

    value = scope.query(f":MEASure:ITEM? {measurement},CHANnel{channel}")

    print(f"{measurement} CH{channel}: {value.strip()}")


def print_menu():
    print()
    print("--- Oszilloskop Tool ---")
    print("1 - Geräteinfo anzeigen")
    print("2 - Channel auswählen")
    print("3 - Y-Scale setzen")
    print("4 - X-Scale setzen")
    print("5 - Messwert lesen")
    print("0 - Beenden")


def main():
    scope = None

    try:
        scope = connect()
        print("Verbindung zum Oszilloskop hergestellt.")

        while True:
            print_menu()
            choice = input("Auswahl: ")

            match choice:
                case "1":
                    show_idn(scope)

                case "2":
                    select_channel(scope)

                case "3":
                    set_y_scale(scope)

                case "4":
                    set_x_scale(scope)

                case "5":
                    measure(scope)

                case "0":
                    print("Programm beendet.")
                    break

                case _:
                    print("Ungültige Auswahl.")

    except KeyboardInterrupt:
        print("\nProgramm wurde abgebrochen.")

    except Exception as error:
        print("Fehler:", error)

    finally:
        if scope is not None:
            scope.close()


if __name__ == "__main__":
    main()