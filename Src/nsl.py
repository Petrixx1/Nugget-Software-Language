import sys
import os
import random
import time

print("===================================================")
print("Nugget Software Language by Petar Reljic(Petrixx1).")
print("All right reserved.\n")
print("===================================================")

# Provjeri da je korisnik unio ime datoteke
if len(sys.argv) < 2:
    print("Usage: nsl.exe program.nsl")
    sys.exit(1)

datoteka = sys.argv[1]

# Sigurne varijable
varijable = {}

# Spremnik funkcija
funkcije = {}

# Učitaj kod iz datoteke
try:
    with open(datoteka, "r", encoding="utf-8") as f:
        kod = f.readlines()
except FileNotFoundError:
    print(f"File '{datoteka}' isn't exist.")
    sys.exit(1)

# Stack za FOR i WHILE
stack_for = []
stack_while = []
izvodi_blok = True

# Trenutni indeks
i = 0

# Funkcija koja izvršava jednu liniju koda
def exec_line(linija):
    global izvodi_blok, varijable, stack_for, stack_while, i
    linija = linija.strip()
    if not linija or linija.startswith("#"):
        return
    tokens = linija.split(maxsplit=1)

    # IF/ELSE/ENDIF
    if tokens[0] == "IF":
        uvjet_tekst = tokens[1].split("THEN")[0].strip()
        for var, val in varijable.items():
            if val.isdigit():
                uvjet_tekst = uvjet_tekst.replace(f"v%{var}", val)
            else:
                uvjet_tekst = uvjet_tekst.replace(f"v%{var}", f'"{val.lower()}"')
        try:
            rezultat = eval(uvjet_tekst.lower())
        except:
            rezultat = False
        izvodi_blok = rezultat
    elif tokens[0] == "ELSE":
        izvodi_blok = not izvodi_blok
    elif tokens[0] == "ENDIF":
        izvodi_blok = True

    # FOR/NEXT
    elif tokens[0] == "FOR" and izvodi_blok:
        dijelovi = tokens[1].split()
        var_name = dijelovi[0]
        start = int(dijelovi[2])
        end = int(dijelovi[4])
        varijable[var_name] = str(start)
        stack_for.append({"var": var_name, "start": start, "end": end, "line": i})
    elif tokens[0] == "NEXT" and izvodi_blok:
        if stack_for:
            loop = stack_for[-1]
            varijable[loop["var"]] = str(int(varijable[loop["var"]]) + 1)
            if int(varijable[loop["var"]]) <= loop["end"]:
                i = loop["line"]
            else:
                stack_for.pop()

    # WHILE/ENDWHILE
    elif tokens[0] == "WHILE" and izvodi_blok:
        stack_while.append({"uvjet": tokens[1], "line": i})
    elif tokens[0] == "ENDWHILE" and izvodi_blok:
        if stack_while:
            loop = stack_while[-1]
            uvjet = loop["uvjet"]
            for var, val in varijable.items():
                uvjet = uvjet.replace(f"v%{var}", val)
            try:
                if eval(uvjet):
                    i = loop["line"]
                else:
                    stack_while.pop()
            except:
                stack_while.pop()

    # VAR
    elif tokens[0] == "VAR" and izvodi_blok:
        if len(tokens) > 1:
            args = tokens[1].split()
            izraz = args[1]
            for var, val in varijable.items():
                izraz = izraz.replace(f"v%{var}", val)
            try:
                vrijednost = str(int(eval(izraz)))
            except:
                vrijednost = izraz
            varijable[args[0]] = vrijednost

    # READ
    elif tokens[0] == "READ" and izvodi_blok:
        if len(tokens) > 1:
            args = tokens[1].split('"')
            pitanje = args[1]
            var_name = args[2].strip()
            vrijednost = input(pitanje + " ").strip()
            varijable[var_name] = vrijednost

    # ECHO
    elif tokens[0] == "ECHO" and izvodi_blok:
        if len(tokens) > 1:
            text = tokens[1]
            for var, val in varijable.items():
                text = text.replace(f"v%{var}", val)
            print(text)
        else:
            print()

    # RANDOM
    elif tokens[0] == "RANDOM" and izvodi_blok:
        dijelovi = tokens[1].split()
        var_name = dijelovi[0]
        start = int(dijelovi[1])
        end = int(dijelovi[3])
        varijable[var_name] = str(random.randint(start, end))

    # SLEEP
    elif tokens[0] == "SLEEP" and izvodi_blok:
        if len(tokens) > 1:
            sekunde = float(tokens[1])
            time.sleep(sekunde)

    # CLEAR
    elif tokens[0] == "CLEAR" and izvodi_blok:
        os.system('cls' if os.name == 'nt' else 'clear')

    # BREAK
    elif tokens[0] == "BREAK":
        sys.exit(0)
    else:
        print("Unkown command:", tokens[0])
        print("Stop.")
        exit()

i = 0
while i < len(kod):
    linija = kod[i].strip()
    if not linija or linija.startswith("#"):
        i += 1
        continue
    tokens = linija.split(maxsplit=1)

    # PROC
    if tokens[0] == "PROC":
        trenutna_funkcija = tokens[1].split()[0]      # ime funkcije
        parametri = tokens[1].split()[1:]             # lista parametara
        kod_funkcije = []
        i += 1
        while i < len(kod):
            linija_func = kod[i].strip()
            if linija_func == "END":
                break
            kod_funkcije.append(linija_func)
            i += 1
        funkcije[trenutna_funkcija] = {"kod": kod_funkcije, "parametri": parametri}
        i += 1
        continue

    # CALL
    elif tokens[0] == "CALL":
        ime = tokens[1].split()[0]
        args = tokens[1].split()[1:]
        if ime in funkcije:
            saved_i = i
            saved_kod = kod

            funkcija = funkcije[ime]
            parametri = funkcija["parametri"]
            kod_func = funkcija["kod"]
            temp_vars = {}
            for p, a in zip(parametri, args):
                if a.startswith('"') and a.endswith('"'):
                    a = a[1:-1]
                temp_vars[p] = a

            stari_vars = varijable.copy()
            varijable.update(temp_vars)

            i = 0
            kod = kod_func
            while i < len(kod):
                exec_line(kod[i])
                i += 1

            varijable = stari_vars
            kod = saved_kod
            i = saved_i + 1
            continue  # funkcija završila, ide dalje

    # Sve ostalo su obične naredbe jezika
    exec_line(linija)
    i += 1

