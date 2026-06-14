Wie man am Osziloskop IP herausfindet: Lan anstecken -> Utility -> EA Einstellungen -> LAN Einstellungen -> FERTIG VISA ADRESSE ist wichtig für die Connection bei uns „TCPIPO::169.254.7.40::INSTR“

Virtueles Env: -> nutzen wir damit wir unseren PC nicht zumüllen und damit es keine Dependscie Konflikte gibt 

1.Ordner erstellen 
2.in VSC öffnen
3. Schauen ob man im richtigen Ordner ist 
4. Folgende Commands ausführen
	Python -m venv .venv
	source .venv/bin/activate // braucht man nicht wirklich weil windows automatisch macht
	pip install pyvisa-py
	pip freeze > requirements.txt // maybe 



Datenblatt: DS1000Z Series Digital Oscilloscope					
Hauptbibliothek: PyVisa 
