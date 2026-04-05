# Subnetting Trainer

An interactive subnetting trainer for IT apprentices and anyone learning networking fundamentals.
Available in **German and English**.

## Features

- **3 practice modes:**
  - Subnetting — calculate subnet mask, network address, broadcast, first/last host, host count
  - Binary ↔ Decimal — convert between binary and decimal with value table
  - CIDR from hosts — find the smallest fitting prefix for a given host count
- **Difficulty levels:** Easy (/8 /16 /24), Medium (any CIDR), Hard (/17–/30)
- **Detailed error feedback** — octet-by-octet comparison, field-specific tips
- **Binary representation** shown after every subnetting task
- **Explanations menu** — theory on IP addresses, subnetting, subnet masks, CIDR, binary
- **German / English** language selection
- Navigate with `m` (menu) and `q` (quit) at any prompt

## Versions

| File | Requirements |
|------|--------------|
| `trainer.py` | Python 3.6+ (duh) — Linux, macOS, Windows |
| `subnetting-trainer.html` | Any browser, any system — no installation needed |

Windows doesn't come with Python by default, so if you don't have it installed or don't know how to, just use the HTML version — that's the recommended way on Windows anyway.

## Usage

**Terminal:**
```bash
python3 trainer.py
```

**Browser:**
Just open `subnetting-trainer.html` — works on any system, no installation needed.

## Screenshots

```
  Round 1  |  0✓  0✗  |  0%

  Given: 192.168.10.0/26
  Calculate all values for this network:

  ▶ Subnet Mask (m=menu, q=quit): 255.255.255.192
  ✓ Correct!
  ▶ Network Addr (m=menu, q=quit): 192.168.10.0
  ✓ Correct!
  ...

  Binary representation:
  Network Addr   11000000.10101000.00001010.00000000
  Subnet Mask    11111111.11111111.11111111.11000000
  Broadcast      11000000.10101000.00001010.00111111
```

## Who is this for?

- IT apprentices preparing for their exams
- Anyone learning subnetting from scratch
- Network engineers who want to practice quickly

## License

MIT
