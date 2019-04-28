
import sys

#list_file = sys.arv[1]
list_file = 'signals.lst'

with open(list_file) as lf:
    signals = [line.strip() for line in lf]
#print(signals)
sig_width = 1

for sig in signals:
    if len(sig) > sig_width:
        sig_width = len(sig)
sig_width += 2

print('{ "signal" : [')
for sig in signals:
    if ':' in sig:
        print("    {name: '" + sig + "'," + " "*(sig_width - len(sig)) + "wave: 'x3',  data: ['']},")
    elif ('clk' or 'clock') in sig:
        print("    {name: '" + sig + "'," + " " * (sig_width - len(sig)) + "wave: 'p.'},")
    else:
        print("    {name: '" + sig + "'," + " " * (sig_width - len(sig)) + "wave: '0.'},")

print("  ],")
print('  "config": { "hscale" : 4.5 }')
print('}')


