#!/usr/bin/env python3
# Subnetting Trainer für FiSis
# github.com/blamevlan

import random
import ipaddress
import os

GRN = "\033[92m"; RED = "\033[91m"; YLW = "\033[93m"
BLU = "\033[94m"; CYN = "\033[96m"; MGN = "\033[95m"
BLD = "\033[1m";  DIM = "\033[2m";  RST = "\033[0m"

# ── Sprachen ───────────────────────────────────────────────────────────────────
LANG = {
    "de": {
        "subtitle":    "Subnetting Trainer für FiSis  github.com/blamevlan",
        "lang_prompt": "Sprache / Language (de/en)",
        "menu_title":  "Was möchtest du üben?",
        "mode1":       "Subnetting     — IP/CIDR → Maske, Netz, Broadcast, Hosts",
        "mode2":       "Binär          — Dezimal ↔ Binär Umrechnung",
        "mode3":       "CIDR aus Hosts — Hostanzahl → kleinster Prefix",
        "mode_prompt": "Auswahl (1/2/3/4)",
        "diff_title":  "Schwierigkeit:",
        "diff1":       "Einfach  — /8, /16, /24",
        "diff2":       "Mittel   — beliebige CIDR",
        "diff3":       "Schwer   — ungewöhnliche Prefixe (/17-/30)",
        "given":       "Gegeben",
        "calc_hint":   "Berechne alle Werte für dieses Netz:",
        "correct":     "✓ Richtig!",
        "wrong":       "✗ Falsch. Richtig:",
        "solution":    "Vollständige Lösung",
        "binary":      "Binärdarstellung:",
        "formula":     "Formel Hosts",
        "net_part":    "Netzanteil",
        "host_part":   "Hostanteil",
        "continue":    "Weiter? (Enter = ja, m = Menü, q = Beenden)",
        "result":      "Ergebnis:",
        "right_count": "Richtig",
        "wrong_count": "Falsch",
        "total":       "Gesamt",
        "score_good":  "Gut gemacht! Du bist bereit für die Prüfung!",
        "score_mid":   "Nicht schlecht — weiter üben!",
        "score_bad":   "Nochmal von vorne — du schaffst das!",
        "back_hint":   "m = zurück zum Menü",
        "input_hint":  "m=Menü, q=Beenden",
        "round":       "Runde",
        "mode4":       "Erklärungen  — Was ist Subnetting, CIDR, Binär?",
        "expl": [
            ("Was ist eine IP-Adresse?",
             "Eine IPv4-Adresse besteht aus 32 Bit, aufgeteilt in 4 Oktette (je 8 Bit).\n"
             "  Beispiel: 192.168.1.10\n"
             "  Binär:    11000000.10101000.00000001.00001010\n"
             "  Jedes Oktett hat einen Wert von 0–255."),
            ("Was ist Subnetting?",
             "Subnetting teilt ein großes Netzwerk in kleinere Teilnetze (Subnetze) auf.\n"
             "  Warum? → Weniger Broadcast-Traffic, bessere Sicherheit, effizientere Adressvergabe.\n"
             "  Beispiel: 192.168.1.0/24 kann in zwei /25 aufgeteilt werden:\n"
             "    192.168.1.0/25  → 126 Hosts\n"
             "    192.168.1.128/25 → 126 Hosts"),
            ("Was ist die Subnetzmaske?",
             "Die Maske trennt Netz- von Hostanteil.\n"
             "  Einser-Bits = Netzanteil | Nullen-Bits = Hostanteil\n"
             "  /24 → 255.255.255.0  → 11111111.11111111.11111111.00000000\n"
             "  /26 → 255.255.255.192 → 11111111.11111111.11111111.11000000\n"
             "  Gültige Werte pro Oktett: 0, 128, 192, 224, 240, 248, 252, 254, 255"),
            ("Was ist CIDR?",
             "CIDR = Classless Inter-Domain Routing\n"
             "  Schreibweise: IP/Prefix  →  z.B. 192.168.1.0/26\n"
             "  Der Prefix gibt an wie viele Bits die Netzmaske hat.\n"
             "  /26 = 26 Einser-Bits in der Maske = 255.255.255.192\n"
             "  Ersetzt die alten Klassen A/B/C → flexibler."),
            ("Wie berechnet man Netzadresse & Broadcast?",
             "Netzadresse: IP AND Maske (alle Host-Bits auf 0)\n"
             "  192.168.1.100/26\n"
             "  IP:   11000000.10101000.00000001.01100100\n"
             "  AND:  11111111.11111111.11111111.11000000\n"
             "  Netz: 11000000.10101000.00000001.01000000 = 192.168.1.64\n\n"
             "  Broadcast: Netzadresse + alle Host-Bits auf 1\n"
             "  192.168.1.64 + 63 = 192.168.1.127"),
            ("Wie viele Hosts passen in ein Subnetz?",
             "Formel: 2^(32 - Prefix) - 2\n"
             "  -2 weil: Netzadresse und Broadcast nicht nutzbar sind.\n"
             "  /24 → 2^8 - 2 = 254 Hosts\n"
             "  /26 → 2^6 - 2 = 62 Hosts\n"
             "  /30 → 2^2 - 2 = 2 Hosts (typisch für WAN-Links)\n"
             "  /32 → 1 Adresse (einzelner Host, kein Netz)"),
            ("Binär — Wertetabelle",
             "Jedes Bit in einem Oktett hat einen festen Wert:\n"
             "  Stelle: 128 | 64 | 32 | 16 |  8 |  4 |  2 |  1\n"
             "  Bit:      1     0    1    0    0    0    0    0  = 160\n\n"
             "  Dezimal → Binär: Passt 128 rein? Ja=1, Rest weiter.\n"
             "  Binär → Dezimal: Alle Stellen mit 1 addieren.\n"
             "  192 = 128+64     = 11000000\n"
             "  255 = alle Bits  = 11111111\n"
             "    0 = kein Bit   = 00000000"),
        ],
        "expl_title":  "Erklärungen",
        "expl_prompt": "Nächste (Enter), Menü (m)",
        "fields": {
            "Subnetzmaske": ("Subnetzmaske",  "Die Maske: {p} Einser-Bits, dann Nullen. Gültige Werte: 0,128,192,224,240,248,252,254,255"),
            "Netzadresse":  ("Netzadresse",   "Netzadresse = IP AND Maske → alle Host-Bits auf 0"),
            "Broadcast":    ("Broadcast",     "Broadcast = Netzadresse + alle Host-Bits auf 1"),
            "Erster Host":  ("Erster Host",   "Erster Host = Netzadresse + 1"),
            "Letzter Host": ("Letzter Host",  "Letzter Host = Broadcast - 1"),
            "Anzahl Hosts": ("Anzahl Hosts",  "Anzahl = 2^(32 - Prefix) - 2"),
        },
        "dez2bin":     "Dezimal → Binär",
        "bin2dez":     "Binär → Dezimal",
        "werte":       "Wertetabelle: 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1",
        "bin_q_d2b":   "Binär (8 Bit, z.B. 11000000)",
        "bin_q_b2d":   "Dezimal",
        "bin_tip_d2b": "Von links: Passt 128 in die Zahl? Ja=1, Nein=0. Weiter mit Rest.",
        "bin_tip_b2d": "Addiere alle Stellen wo eine 1 steht.",
        "cidr_title":  "CIDR aus Hostanzahl",
        "cidr_need":   "Du brauchst ein Subnetz für mindestens",
        "cidr_hosts":  "Hosts.",
        "cidr_hint":   "Kleinsten passenden CIDR-Prefix angeben (nur Zahl, z.B. 25 für /25)",
        "cidr_q":      "CIDR Prefix",
        "cidr_table":  "Übersicht:",
        "cidr_best":   "← kleinster passender",
        "cidr_ok":     "Richtig! /{b} bietet {h} Hosts.",
        "cidr_close":  "Fast! /{u} reicht, aber /{b} ist das kleinste Subnetz. Immer kleinstes nehmen → spart Adressen.",
        "cidr_small":  "✗ /{u} bietet nur {h} Hosts — zu wenig! Richtig: /{b}",
        "cidr_tip":    "Tipp: 2^(32−Prefix) − 2 muss >= {n} sein.",
        "sol_notes": {
            "Subnetzmaske": "({p} Einser-Bits)",
            "Netzadresse":  "(Host-Bits alle 0)",
            "Broadcast":    "(Host-Bits alle 1)",
            "Erster Host":  "(Netzadresse + 1)",
            "Letzter Host": "(Broadcast - 1)",
            "Anzahl Hosts": "(2^{e} - 2)",
        },
    },
    "en": {
        "subtitle":    "Subnetting Trainer for FiSis  github.com/blamevlan",
        "lang_prompt": "Sprache / Language (de/en)",
        "menu_title":  "What do you want to practice?",
        "mode1":       "Subnetting     — IP/CIDR → Mask, Network, Broadcast, Hosts",
        "mode2":       "Binary         — Decimal ↔ Binary Conversion",
        "mode3":       "CIDR from Hosts — Host count → smallest prefix",
        "mode_prompt": "Select (1/2/3/4)",
        "diff_title":  "Difficulty:",
        "diff1":       "Easy    — /8, /16, /24",
        "diff2":       "Medium  — any CIDR",
        "diff3":       "Hard    — unusual prefixes (/17-/30)",
        "given":       "Given",
        "calc_hint":   "Calculate all values for this network:",
        "correct":     "✓ Correct!",
        "wrong":       "✗ Wrong. Correct answer:",
        "solution":    "Full Solution",
        "binary":      "Binary representation:",
        "formula":     "Formula hosts",
        "net_part":    "Net part",
        "host_part":   "Host part",
        "continue":    "Continue? (Enter = yes, m = menu, q = quit)",
        "result":      "Result:",
        "right_count": "Correct",
        "wrong_count": "Wrong",
        "total":       "Total",
        "score_good":  "Well done! You are ready for the exam!",
        "score_mid":   "Not bad — keep practicing!",
        "score_bad":   "Try again — you can do it!",
        "back_hint":   "m = back to menu",
        "input_hint":  "m=menu, q=quit",
        "round":       "Round",
        "mode4":       "Explanations — What is subnetting, CIDR, binary?",
        "expl": [
            ("What is an IP address?",
             "An IPv4 address consists of 32 bits, split into 4 octets (8 bits each).\n"
             "  Example: 192.168.1.10\n"
             "  Binary:  11000000.10101000.00000001.00001010\n"
             "  Each octet has a value from 0 to 255."),
            ("What is subnetting?",
             "Subnetting divides a large network into smaller sub-networks (subnets).\n"
             "  Why? → Less broadcast traffic, better security, efficient address usage.\n"
             "  Example: 192.168.1.0/24 can be split into two /25:\n"
             "    192.168.1.0/25   → 126 hosts\n"
             "    192.168.1.128/25 → 126 hosts"),
            ("What is a subnet mask?",
             "The mask separates the network part from the host part.\n"
             "  One-bits = network | Zero-bits = host\n"
             "  /24 → 255.255.255.0   → 11111111.11111111.11111111.00000000\n"
             "  /26 → 255.255.255.192 → 11111111.11111111.11111111.11000000\n"
             "  Valid values per octet: 0, 128, 192, 224, 240, 248, 252, 254, 255"),
            ("What is CIDR?",
             "CIDR = Classless Inter-Domain Routing\n"
             "  Notation: IP/Prefix  →  e.g. 192.168.1.0/26\n"
             "  The prefix tells how many bits are in the subnet mask.\n"
             "  /26 = 26 one-bits in the mask = 255.255.255.192\n"
             "  Replaces old Class A/B/C notation → more flexible."),
            ("How to calculate network address & broadcast?",
             "Network address: IP AND Mask (all host bits set to 0)\n"
             "  192.168.1.100/26\n"
             "  IP:   11000000.10101000.00000001.01100100\n"
             "  AND:  11111111.11111111.11111111.11000000\n"
             "  Net:  11000000.10101000.00000001.01000000 = 192.168.1.64\n\n"
             "  Broadcast: network address + all host bits set to 1\n"
             "  192.168.1.64 + 63 = 192.168.1.127"),
            ("How many hosts fit in a subnet?",
             "Formula: 2^(32 - Prefix) - 2\n"
             "  -2 because: network address and broadcast are not usable.\n"
             "  /24 → 2^8 - 2 = 254 hosts\n"
             "  /26 → 2^6 - 2 = 62 hosts\n"
             "  /30 → 2^2 - 2 = 2 hosts (typical for WAN links)\n"
             "  /32 → 1 address (single host, no network)"),
            ("Binary — value table",
             "Each bit in an octet has a fixed value:\n"
             "  Place: 128 | 64 | 32 | 16 |  8 |  4 |  2 |  1\n"
             "  Bit:     1    0    1    0    0    0    0    0  = 160\n\n"
             "  Decimal → Binary: Does 128 fit? Yes=1, subtract, continue.\n"
             "  Binary → Decimal: Add all positions where bit is 1.\n"
             "  192 = 128+64    = 11000000\n"
             "  255 = all bits  = 11111111\n"
             "    0 = no bits   = 00000000"),
        ],
        "expl_title":  "Explanations",
        "expl_prompt": "Next (Enter), Menu (m)",
        "fields": {
            "Subnetzmaske": ("Subnet Mask",   "Mask: {p} one-bits, then zeros. Valid values: 0,128,192,224,240,248,252,254,255"),
            "Netzadresse":  ("Network Addr",  "Network address = IP AND Mask → all host bits set to 0"),
            "Broadcast":    ("Broadcast",     "Broadcast = Network address + all host bits set to 1"),
            "Erster Host":  ("First Host",    "First host = Network address + 1"),
            "Letzter Host": ("Last Host",     "Last host = Broadcast - 1"),
            "Anzahl Hosts": ("# of Hosts",    "Count = 2^(32 - Prefix) - 2"),
        },
        "dez2bin":     "Decimal → Binary",
        "bin2dez":     "Binary → Decimal",
        "werte":       "Value table: 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1",
        "bin_q_d2b":   "Binary (8 bit, e.g. 11000000)",
        "bin_q_b2d":   "Decimal",
        "bin_tip_d2b": "Left to right: Does 128 fit? Yes=1, No=0. Continue with remainder.",
        "bin_tip_b2d": "Add all positions where a 1 is set.",
        "cidr_title":  "CIDR from host count",
        "cidr_need":   "You need a subnet for at least",
        "cidr_hosts":  "hosts.",
        "cidr_hint":   "Enter the smallest fitting CIDR prefix (number only, e.g. 25 for /25)",
        "cidr_q":      "CIDR Prefix",
        "cidr_table":  "Overview:",
        "cidr_best":   "← smallest fitting",
        "cidr_ok":     "Correct! /{b} provides {h} hosts.",
        "cidr_close":  "Close! /{u} would work, but /{b} is the smallest subnet. Always use smallest → saves addresses.",
        "cidr_small":  "✗ /{u} only provides {h} hosts — not enough! Correct: /{b}",
        "cidr_tip":    "Tip: 2^(32−Prefix) − 2 must be >= {n}.",
        "sol_notes": {
            "Subnetzmaske": "({p} one-bits)",
            "Netzadresse":  "(all host bits = 0)",
            "Broadcast":    "(all host bits = 1)",
            "Erster Host":  "(network address + 1)",
            "Letzter Host": "(broadcast - 1)",
            "Anzahl Hosts": "(2^{e} - 2)",
        },
    }
}

T = LANG["de"]  # aktive Sprache

# ── Hilfsfunktionen ────────────────────────────────────────────────────────────
class BackToMenu(Exception): pass

def clear(): os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(f"{BLU}{BLD}")
    print("  ███████╗██╗   ██╗██████╗ ███╗   ██╗███████╗████████╗")
    print("  ██╔════╝██║   ██║██╔══██╗████╗  ██║██╔════╝╚══██╔══╝")
    print("  ███████╗██║   ██║██████╔╝██╔██╗ ██║█████╗     ██║   ")
    print("  ╚════██║██║   ██║██╔══██╗██║╚██╗██║██╔══╝     ██║   ")
    print("  ███████║╚██████╔╝██████╔╝██║ ╚████║███████╗   ██║   ")
    print("  ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ")
    print(f"  {YLW}{T['subtitle']}{RST}")
    print()

def eingabe(frage):
    val = input(f"  {CYN}▶ {frage}{DIM} ({T['input_hint']}){RST}{CYN}: {RST}").strip()
    if val.lower() == "m":
        raise BackToMenu()
    return val

# ── IP-Rechnen ─────────────────────────────────────────────────────────────────
def ip_zu_binaer_okt(ip_str):
    return [int(x) for x in str(ip_str).split(".")]

def vergleiche_ip(richtig_str, falsch_str):
    try:
        r = ip_zu_binaer_okt(richtig_str)
        f = ip_zu_binaer_okt(falsch_str)
    except: return
    print(f"  {DIM}Vergleich:")
    zr = "  " + (" " * 14)
    zf = "  " + (" " * 14)
    for i in range(4):
        if i < len(r) and i < len(f):
            if r[i] == f[i]:
                zr += f"{GRN}{r[i]:<4}{RST}."
                zf += f"{GRN}{f[i]:<4}{RST}."
            else:
                zr += f"{GRN}{BLD}{r[i]:<4}{RST}."
                zf += f"{RED}{BLD}{f[i]:<4}{RST}."
    print(zr.rstrip(".")); print(zf.rstrip("."))

def zeige_binaer_tabelle(netz):
    def fmt(ip_str):
        okt = [int(x) for x in str(ip_str).split(".")]
        return ".".join(f"{o:08b}" for o in okt)
    p = netz.prefixlen
    print(f"\n  {MGN}{BLD}{T['binary']}{RST}")
    print(f"  {DIM}{'─'*60}{RST}")
    print(f"  {BLD}{T['fields']['Netzadresse'][0]:<14}{RST} {fmt(netz.network_address)}")
    print(f"  {BLD}{T['fields']['Subnetzmaske'][0]:<14}{RST} {fmt(netz.netmask)}")
    print(f"  {BLD}{'Broadcast':<14}{RST} {fmt(netz.broadcast_address)}")
    print(f"  {DIM}{'─'*60}{RST}")
    print(f"  {GRN}{T['net_part']} ({p} Bit){RST} / {YLW}{T['host_part']} ({32-p} Bit){RST}")
    print(f"  {GRN}{'N'*p}{RST}{YLW}{'H'*(32-p)}{RST}")
    print(f"  {T['formula']}: 2^(32-{p}) - 2 = {BLD}{GRN}{max(0,2**(32-p)-2)}{RST}")

def erklaere_ip_fehler(feld_key, richtig, nutzer_eingabe, netz):
    label, tipp = T['fields'][feld_key]
    tipp = tipp.replace("{p}", str(netz.prefixlen))
    print(f"  {RED}✗ {T['wrong']} {BLD}{richtig}{RST}")
    print(f"  {YLW}{tipp}{RST}")
    if feld_key != "Anzahl Hosts":
        try:
            ipaddress.IPv4Address(nutzer_eingabe)
            vergleiche_ip(richtig, nutzer_eingabe)
        except:
            print(f"  {DIM}'{nutzer_eingabe}' ist keine gültige IP (Format: xxx.xxx.xxx.xxx){RST}")

def zufaellige_ip(schwierigkeit):
    if schwierigkeit == 1:   prefix = random.choice([8, 16, 24])
    elif schwierigkeit == 2: prefix = random.randint(8, 30)
    else:                    prefix = random.randint(17, 30)
    okt = [random.randint(1, 254) for _ in range(4)]
    return ipaddress.IPv4Network(f"{'.'.join(map(str,okt))}/{prefix}", strict=False)

# ── Modi ───────────────────────────────────────────────────────────────────────
def modus_subnetting(schwierigkeit):
    netz  = zufaellige_ip(schwierigkeit)
    hosts = list(netz.hosts())
    print(f"\n  {BLD}{T['given']}: {YLW}{netz.network_address}/{netz.prefixlen}{RST}")
    print(f"  {DIM}{T['calc_hint']}  ({T['back_hint']}){RST}\n")

    felder = [
        ("Subnetzmaske", str(netz.netmask)),
        ("Netzadresse",  str(netz.network_address)),
        ("Broadcast",    str(netz.broadcast_address)),
        ("Erster Host",  str(hosts[0]) if hosts else "keine"),
        ("Letzter Host", str(hosts[-1]) if hosts else "keine"),
        ("Anzahl Hosts", str(len(hosts))),
    ]
    richtig = 0; falsch = 0
    for feld_key, antwort in felder:
        label = T['fields'][feld_key][0]
        nutz  = eingabe(label)
        if nutz.lower() == antwort.lower():
            print(f"  {GRN}{T['correct']}{RST}")
            richtig += 1
        else:
            erklaere_ip_fehler(feld_key, antwort, nutz, netz)
            falsch += 1

    notes = T['sol_notes']
    print(f"\n  {YLW}{BLD}┌─ {T['solution']} ────────────────────────────┐{RST}")
    for feld_key, antwort in felder:
        label = T['fields'][feld_key][0]
        note  = notes[feld_key].replace("{p}", str(netz.prefixlen)).replace("{e}", str(32-netz.prefixlen))
        print(f"  {BLD}│ {label:<14}{RST}{GRN}{antwort:<17}{RST}{DIM}{note}{RST}")
    print(f"  {YLW}{BLD}└──────────────────────────────────────────────┘{RST}")
    zeige_binaer_tabelle(netz)
    return richtig, falsch

def modus_binaer():
    werte   = [128, 64, 32, 16, 8, 4, 2, 1]
    zahl    = random.randint(0, 255)
    bits    = f"{zahl:08b}"
    richtung = random.choice(["dez2bin", "bin2dez"])

    if richtung == "dez2bin":
        print(f"\n  {BLD}{T['dez2bin']}{RST}  {DIM}({T['back_hint']}){RST}")
        print(f"  Zahl: {YLW}{BLD}{zahl}{RST}")
        print(f"  {DIM}{T['werte']}{RST}\n")
        antwort = bits
        nutz    = eingabe(T['bin_q_d2b']).replace(" ","").replace(".","")
    else:
        print(f"\n  {BLD}{T['bin2dez']}{RST}  {DIM}({T['back_hint']}){RST}")
        print(f"  {YLW}{BLD}{bits}{RST}")
        print(f"  {DIM}{T['werte']}{RST}\n")
        antwort = str(zahl)
        nutz    = eingabe(T['bin_q_b2d'])

    print(f"\n  {MGN}Auflösung:{RST}")
    print(f"  {BLD}{'  '.join(f'{w:>3}' for w in werte)}{RST}")
    zeile = "  "
    for i, b in enumerate(bits):
        farbe = GRN if b == "1" else DIM
        zeile += f"{farbe}{b:>3}{RST}  "
    print(zeile)
    aktiv = [str(werte[i]) for i, b in enumerate(bits) if b == "1"]
    print(f"  {' + '.join(aktiv) if aktiv else '0'} = {GRN}{BLD}{zahl}{RST}  →  {GRN}{BLD}{bits}{RST}")

    if nutz == antwort:
        print(f"\n  {GRN}{T['correct']}{RST}")
        return 1, 0
    else:
        print(f"\n  {RED}✗ {T['wrong']} {BLD}{antwort}{RST}")
        tipp = T['bin_tip_d2b'] if richtung == "dez2bin" else T['bin_tip_b2d']
        print(f"  {YLW}{tipp}{RST}")
        return 0, 1

def modus_cidr_aus_hosts():
    prefix     = random.randint(20, 30)
    benoetigt  = random.randint(1, max(1, 2**(32-prefix)-2))
    bestes = None
    for p in range(30, 0, -1):
        if 2**(32-p)-2 >= benoetigt:
            bestes = p
            break
    if bestes is None: bestes = 1

    print(f"\n  {BLD}{T['cidr_title']}{RST}  {DIM}({T['back_hint']}){RST}")
    print(f"  {T['cidr_need']} {YLW}{BLD}{benoetigt}{RST} {T['cidr_hosts']}")
    print(f"  {DIM}{T['cidr_hint']}{RST}\n")
    nutz = eingabe(T['cidr_q']).replace("/","").strip()

    print(f"\n  {MGN}{T['cidr_table']}{RST}")
    for p in range(max(1, bestes-3), min(31, bestes+4)):
        h = 2**(32-p)-2
        ok = h >= benoetigt
        marker = f"  {GRN}{T['cidr_best']}{RST}" if p == bestes else ""
        farbe  = GRN if ok else RED
        print(f"  /{p}  →  {farbe}{h:>6} Hosts{RST}{marker}")

    try: p_nutz = int(nutz); h_nutz = 2**(32-p_nutz)-2
    except: p_nutz = -1; h_nutz = -1

    if p_nutz == bestes:
        print(f"\n  {GRN}{T['cidr_ok'].format(b=bestes, h=2**(32-bestes)-2)}{RST}")
        return 1, 0
    elif h_nutz >= benoetigt:
        print(f"\n  {YLW}{T['cidr_close'].format(u=p_nutz, b=bestes)}{RST}")
        return 0, 1
    else:
        print(f"\n  {RED}{T['cidr_small'].format(u=p_nutz, h=h_nutz, b=bestes)}{RST}")
        print(f"  {YLW}{T['cidr_tip'].format(n=benoetigt)}{RST}")
        return 0, 1

# ── Menüs ──────────────────────────────────────────────────────────────────────
def hinweis_zeile(extra=""):
    """Zeigt immer sichtbare Steuerhinweise am unteren Rand."""
    h = f"{DIM}  ┌ q = Beenden"
    if extra:
        h += f"  │  {extra}"
    h += f"{RST}"
    print(h)

def sprachauswahl():
    global T
    print(f"  {BLD}Sprache / Language:{RST}")
    print(f"  {GRN}[de]{RST} Deutsch")
    print(f"  {BLU}[en]{RST} English")
    print()
    hinweis_zeile()
    while True:
        wahl = input(f"  {CYN}▶ {LANG['de']['lang_prompt']}: {RST}").strip().lower()
        if wahl in ("de", "en"):
            T = LANG[wahl]
            return
        if wahl == "q":
            raise SystemExit
        print(f"  {RED}Bitte 'de' oder 'en' eingeben.{RST}")

def modus_erklaerungen():
    themen = T['expl']
    for i, (titel, inhalt) in enumerate(themen):
        clear(); banner()
        print(f"  {MGN}{BLD}{T['expl_title']} ({i+1}/{len(themen)}){RST}\n")
        print(f"  {YLW}{BLD}{titel}{RST}\n")
        for zeile in inhalt.split("\n"):
            print(f"  {zeile}")
        print()
        hinweis_zeile("m = Menü  │  Enter = weiter" if T == LANG["de"] else "m = menu  │  Enter = next")
        try:
            wahl = input(f"  {CYN}▶ : {RST}").strip().lower()
        except EOFError:
            return
        if wahl == "m":
            return
        if wahl == "q":
            raise SystemExit

def hauptmenue():
    print(f"  {BLD}{T['menu_title']}{RST}")
    print(f"  {GRN}[1]{RST} {T['mode1']}")
    print(f"  {YLW}[2]{RST} {T['mode2']}")
    print(f"  {RED}[3]{RST} {T['mode3']}")
    print(f"  {BLU}[4]{RST} {T['mode4']}")
    print(f"  {DIM}[l]{RST} Sprache / Language")
    print()
    hinweis_zeile()
    while True:
        try:
            wahl = input(f"  {CYN}▶ {T['mode_prompt']}: {RST}").strip().lower()
        except EOFError:
            return "q"
        if wahl in ("1","2","3","4","l","q"):
            return wahl
        print(f"  {RED}1, 2, 3, 4, l oder q.{RST}")

def schwierigkeitsmenue():
    print(f"  {BLD}{T['diff_title']}{RST}")
    print(f"  {GRN}[1]{RST} {T['diff1']}")
    print(f"  {YLW}[2]{RST} {T['diff2']}")
    print(f"  {RED}[3]{RST} {T['diff3']}")
    print()
    hinweis_zeile("m = Menü" if T == LANG["de"] else "m = menu")
    while True:
        try:
            wahl = input(f"  {CYN}▶ {T['mode_prompt']}: {RST}").strip().lower()
        except EOFError:
            return 2
        if wahl == "m":
            raise BackToMenu()
        if wahl == "q":
            raise SystemExit
        if wahl in ("1","2","3"):
            return int(wahl)
        print(f"  {RED}1, 2 oder 3.{RST}")

# ── Hauptprogramm ──────────────────────────────────────────────────────────────
def main():
    global T
    clear(); banner()
    sprachauswahl()

    punkte = 0; falsch_gesamt = 0

    while True:
        clear(); banner()
        wahl = hauptmenue()

        if wahl == "q":
            break
        if wahl == "l":
            clear(); banner()
            sprachauswahl()
            continue
        if wahl == "4":
            modus_erklaerungen()
            continue

        modus = int(wahl)
        schwierigkeit = 2
        if modus == 1:
            clear(); banner()
            try:
                schwierigkeit = schwierigkeitsmenue()
            except BackToMenu:
                continue

        runde = 0
        while True:
            clear(); banner()
            runde += 1
            g = punkte + falsch_gesamt
            p = round(punkte/g*100) if g > 0 else 0
            print(f"  {T['round']} {BLD}{runde}{RST}  |  {GRN}{punkte}{RST}✓  {RED}{falsch_gesamt}{RST}✗  |  {YLW}{p}%{RST}\n")

            try:
                if modus == 1: r, f = modus_subnetting(schwierigkeit)
                elif modus == 2: r, f = modus_binaer()
                else:            r, f = modus_cidr_aus_hosts()
            except BackToMenu:
                break

            punkte += r; falsch_gesamt += f
            print()
            try:
                weiter = input(f"  {CYN}▶ {T['continue']}: {RST}").strip().lower()
            except EOFError:
                weiter = "q"
            if weiter == "q":
                # Ergebnis zeigen und beenden
                clear(); banner()
                g = punkte + falsch_gesamt
                p = round(punkte/g*100) if g > 0 else 0
                print(f"  {BLD}{T['result']}{RST}")
                print(f"  {T['right_count']}: {GRN}{punkte}{RST}  |  {T['wrong_count']}: {RED}{falsch_gesamt}{RST}  |  {T['total']}: {g}")
                print(f"  Score: {YLW}{BLD}{p}%{RST}\n")
                if p >= 80:   print(f"  {GRN}{BLD}{T['score_good']}{RST}")
                elif p >= 50: print(f"  {YLW}{T['score_mid']}{RST}")
                else:         print(f"  {RED}{T['score_bad']}{RST}")
                print()
                return
            elif weiter == "m":
                break

if __name__ == "__main__":
    main()
