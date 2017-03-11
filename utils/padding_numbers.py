
# Padding generator, makes a clean padding

def padder(number, pad=3):
	
	counter = len(str(number))    
	addition = pad - counter
	number = str(number)
	
	for each in range(addition):
		padding_zero = '0'
		number = padding_zero + number    

	return number

def rev_padder(number, pad=2):
	
	padding_zero = '0'

	for each in range(pad):
		number = number + padding_zero    

	return number


