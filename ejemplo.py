gato = "sotogatear"

#gato[5] = "o"  # No
gato = gato[:5] + "0" + gato[6:] # Si

print(gato)