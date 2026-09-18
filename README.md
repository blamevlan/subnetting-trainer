# Subnetting Trainer

A small practice tool for subnetting and basic IP math. I built it mainly to drill the things that come up again and again when learning networking.

There are two versions: a Python terminal version and a single-file browser version. Both can be used in German or English.

## Practice modes

- subnetting: subnet mask, network, broadcast, first and last host, host count
- binary and decimal conversion
- finding the smallest CIDR prefix for a required number of hosts
- easy, medium and hard difficulty levels
- hints and detailed feedback after wrong answers

## Run it

Terminal version:

```bash
python3 subnetting-trainer.py
```

Browser version:

Open `subnetting-trainer.html` directly in a browser. It does not need a server or installation.

The Python version needs Python 3.6 or newer. The HTML version is the easier option on systems where Python is not installed.

## Example

```text
Round 1  |  0✓  0✗  |  0%

Given: 192.168.10.0/26

Subnet Mask:  255.255.255.192
Network:      192.168.10.0
Broadcast:    192.168.10.63
```

## License

MIT. See [LICENSE](LICENSE).
