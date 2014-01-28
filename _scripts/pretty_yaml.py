import sys
import yaml
import pyaml

in_file = sys.argv[1]
out_file = sys.argv[2]

i = open(in_file, "r")
p = yaml.load(open(in_file))
i.close()

o = open(out_file, "w+")
pyaml.dump(p, o, vspacing=[2, 0])
o.close()

