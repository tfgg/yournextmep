import sys
import yaml
import pyaml

in_file = sys.argv[1]

if len(sys.argv) > 2:
  out_file = sys.argv[2]
else:
  out_file = in_file

i = open(in_file, "r")
p = yaml.load(open(in_file))
i.close()

o = open(out_file, "w+")
pyaml.dump(p, o, vspacing=[2, 0])
o.close()

