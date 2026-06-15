import pyvisa


class SignalGenerator:
    def __init__(self):
        self.rm = pyvisa.ResourceManager("@py")
        self.gen = None

    def connect(self):
        resources = self.rm.list_resources()

        for resource in resources:
            if "USB0::1024::2500" in resource:
                print("Benutze Signalgenerator:")
                print(repr(resource))

                self.gen = self.rm.open_resource(resource)
                self.gen.write_termination = "\n"
                self.gen.read_termination = "\n"
                self.gen.timeout = 800
                return True

        print("Kein Signalgenerator gefunden.")
        return False

    def close(self):
        if self.gen is not None:
            self.gen.close()
        self.rm.close()

    def send(self, command):
        print("Sende:", command)
        self.gen.write(command)

    def suffix(self, channel):
        if channel == 1:
            return ""
        return ":CH2"

    def set_signal(self, channel, waveform, frequency, amplitude, offset):
        suffix = self.suffix(channel)

        if waveform == "DC":
            command = f"APPL:DC{suffix} DEF,DEF,{offset}"
        elif waveform == "NOIS":
            command = f"APPL:NOIS{suffix} DEF,{amplitude},{offset}"
        else:
            command = f"APPL:{waveform}{suffix} {frequency},{amplitude},{offset}"

        self.send(command)

    def output_on(self, channel):
        self.send(f"OUTP{self.suffix(channel)} ON")

    def output_off(self, channel):
        self.send(f"OUTP{self.suffix(channel)} OFF")

    def show_idn(self):
        old_timeout = self.gen.timeout
        self.gen.timeout = 1500

        try:
            print(self.gen.query("*IDN?").strip())
        except Exception as error:
            print("IDN nicht möglich:", error)

        self.gen.timeout = old_timeout


def choose_channel():
    while True:
        print()
        print("--- Channel auswählen ---")
        print("1 - Channel 1")
        print("2 - Channel 2")
        print("0 - Zurück")

        choice = input("Auswahl: ")

        if choice == "1":
            return 1
        elif choice == "2":
            return 2
        elif choice == "0":
            return None
        else:
            print("Ungültige Auswahl.")


def choose_waveform():
    while True:
        print()
        print("--- Signalform auswählen ---")
        print("1 - Sinus")
        print("2 - Rechteck")
        print("3 - Rampe")
        print("4 - Puls")
        print("5 - Rauschen")
        print("6 - DC")
        print("0 - Zurück")

        choice = input("Auswahl: ")

        match choice:
            case "1":
                return "SIN"
            case "2":
                return "SQU"
            case "3":
                return "RAMP"
            case "4":
                return "PULS"
            case "5":
                return "NOIS"
            case "6":
                return "DC"
            case "0":
                return None
            case _:
                print("Ungültige Auswahl.")


def set_channel_signal(gen, channel):
    waveform = choose_waveform()

    if waveform is None:
        return

    if waveform == "DC":
        offset = input("DC-Spannung in V: ")
        gen.set_signal(channel, waveform, "DEF", "DEF", offset)
        gen.output_on(channel)
        print(f"CH{channel}: DC {offset} V gesetzt.")
        return

    if waveform == "NOIS":
        amplitude = input("Amplitude in Vpp: ")
        offset = input("Offset in V: ")
        gen.set_signal(channel, waveform, "DEF", amplitude, offset)
        gen.output_on(channel)
        print(f"CH{channel}: Rauschen, {amplitude} Vpp, Offset {offset} V gesetzt.")
        return

    frequency = input("Frequenz in Hz: ")
    amplitude = input("Amplitude in Vpp: ")
    offset = input("Offset in V: ")

    gen.set_signal(channel, waveform, frequency, amplitude, offset)
    gen.output_on(channel)

    print(f"CH{channel}: {waveform}, {frequency} Hz, {amplitude} Vpp, Offset {offset} V gesetzt.")


def quick_signal(gen, channel, waveform):
    gen.set_signal(channel, waveform, 1000, 2, 0)
    gen.output_on(channel)
    print(f"CH{channel}: {waveform} 1 kHz / 2 Vpp / 0 V gesetzt.")


def channel_menu(gen, channel):
    while True:
        print()
        print(f"--- Channel {channel} Menü ---")
        print("1 - Eigenes Signal setzen")
        print("2 - Schnell: Sinus 1 kHz / 2 Vpp")
        print("3 - Schnell: Rechteck 1 kHz / 2 Vpp")
        print("4 - Schnell: Rampe 1 kHz / 2 Vpp")
        print("5 - Schnell: Puls 1 kHz / 2 Vpp")
        print("6 - Output EIN")
        print("7 - Output AUS")
        print("0 - Zurück")

        choice = input("Auswahl: ")

        match choice:
            case "1":
                set_channel_signal(gen, channel)
            case "2":
                quick_signal(gen, channel, "SIN")
            case "3":
                quick_signal(gen, channel, "SQU")
            case "4":
                quick_signal(gen, channel, "RAMP")
            case "5":
                quick_signal(gen, channel, "PULS")
            case "6":
                gen.output_on(channel)
                print(f"Output CH{channel} EIN")
            case "7":
                gen.output_off(channel)
                print(f"Output CH{channel} AUS")
            case "0":
                break
            case _:
                print("Ungültige Auswahl.")


def main_menu(gen):
    while True:
        print()
        print("--- DG1022 Hauptmenü ---")
        print("1 - Channel auswählen")
        print("2 - Geräteinfo (*IDN?)")
        print("3 - Beide Outputs AUS")
        print("0 - Beenden")

        choice = input("Auswahl: ")

        match choice:
            case "1":
                channel = choose_channel()
                if channel is not None:
                    channel_menu(gen, channel)

            case "2":
                gen.show_idn()

            case "3":
                gen.output_off(1)
                gen.output_off(2)
                print("Beide Outputs AUS")

            case "0":
                print("Programm beendet.")
                break

            case _:
                print("Ungültige Auswahl.")


def main():
    gen = SignalGenerator()

    if not gen.connect():
        return

    try:
        main_menu(gen)

    except KeyboardInterrupt:
        print("\nProgramm abgebrochen.")

    except Exception as error:
        print("Fehler:", error)

    finally:
        gen.close()


if __name__ == "__main__":
    main()