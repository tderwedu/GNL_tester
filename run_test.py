import subprocess
import filecmp
import math as m
import os

gnl_path	=	"../getNextLine"

sizes		= [1, 2, 3, 10, 11, 16, 32, 100, 9999, 1000000]
files		= ["file_00.txt", "file_01.txt", "file_02.txt", "file_03.txt", "file_04.txt"]
files_b		= ["bonus_0_0.txt", "bonus_0_1.txt", "bonus_0_2.txt"]
expl		= ["A simple line", "A simple file", "Multiple newlines", "EOF without EOL", "Open() man page"]
lines		= [1, 3, 8, 1, 653]

norme		= "~/.norminette/norminette.rb"
name		= "gnl"

src			= ["get_next_line.c", "get_next_line_utils.c"]
src_b		= ["get_next_line_bonus.c", "get_next_line_utils_bonus.c"]



cflags		= "-Wall -Wextra -Werror -fsanitize=address"
cc			= "gcc"
main		= "main.c"
bonus		= "bonus.c"
result		= "result.txt"
output		= "STD"

BOLD		=	"\033[1m"
BLU			=	"\033[96m"
YLW			=	"\033[33m"
PUR			=	"\033[35m"
GRN			=	"\033[32m"
RED			=	"\033[31m"
NC			=	"\033[0m"

src 		= [os.path.join(gnl_path, file) for file in src]
src_b 		= [os.path.join(gnl_path, file) for file in src_b]
files		= [os.path.join("Test_Files", file) for file in files]
files_b		= [os.path.join("Test_Files", file) for file in files_b]

################################################################################
#                                   Functions                                  #
################################################################################

def ft_checkOuput(process, file, lines):
	if process.returncode:
		ft_writeIfError(1, process, file)
		if "Sanitizer" in process.stderr:
			return BOLD + "|" + NC + PUR + "{:^12}".format("[LEAKS]") + NC
		else:
			return BOLD + "|" + NC + RED + "{:^12}".format("[CRASH]") + NC
	else:
		if filecmp.cmp(result, file):
			ret = BOLD + "|" + NC + GRN + "{:^6}".format("[OK]") + NC
		else:
			ft_writeIfError(2, process, file)
			ret = BOLD + "|" + NC + YLW + "{:^6}".format("[FAIL]") + NC
		if lines == int(process.stderr):
			ret = ret  + GRN + "{:^6}".format("[OK]") + NC
		else:
			ret = ret  + YLW + "{:^6}".format("[FAIL]") + NC
		return ret

def ft_writeIfError(nb, process, file):
	if not os.path.isdir(output):
		os.mkdir(output)
	if nb == 1:
		path = os.path.join(output, "STDERR_" + os.path.basename(file))
		log = open(path, "w", 1)
		log.write(process.stderr)
		log.close
	elif nb == 2:
		path = os.path.join(output, "STDOUT_" + os.path.basename(file))
		log = open(path, "w", 1)
		log.write(process.stdout)
		log.close

def ft_reshape(vec):
	i_max = (os.get_terminal_size().columns - 20) // 13
	j_max = m.ceil(len(vec) / i_max)
	tab		= list()
	i_s	= 0
	for j in range(j_max - 1):
		tab.append([v for v in vec[i_s:(i_s + i_max)]])
		i_s		+= i_max
	i_e = len(vec) % i_max
	tab.append([v for v in vec[i_s:i_s + i_e]])
	return [tab, j_max]

def ft_mandatoryPart(name, files, sizes):
	# Creating executables
	exe_names = list()
	print(BOLD + "Genereating executables" + NC)
	for size in sizes:
		exe_names.append(name + "_" + str(size))
		bflags	= "-D BUFFER_SIZE=" + str(size)
		exe		=	cc + " " + cflags + " " + bflags + " -I " + gnl_path + " -o " +\
					exe_names[-1] + " " + " ".join(src) + " " + main
		process = subprocess.run(exe.split(), stderr=subprocess.DEVNULL)
		if  not process.returncode:
			print(BOLD + "{:<12}: ".format(exe_names[-1]) + NC + GRN + "[OK]" + NC)
		else:
			print(BOLD + "{:<12}: ".format(exe_names[-1]) + NC + RED + "[FAIL]" + NC)
	print("\n")
	# Reshaping to adapt to terminal size
	[sizes, j_max] = ft_reshape(sizes)
	[exe_names, j_max] = ft_reshape(exe_names)
	for j in range(j_max):
		# Printing header
		print(BOLD + "{:^20}".format("BUFFER_SIZE") + NC, end = "")
		for size in sizes[j]:
			print(BOLD + "|{:^12}".format(size) + NC, end = "")
		print("\n{:20}".format(" "), end = "")
		for size in sizes[j]:
			print(BOLD + "|{:^6}{:^6}".format("Ouput", "Lines") + NC, end = "")
		print()
		# Testing and printing result
		for i in range(len(files)):
			print(BOLD + "{:<20}".format(expl[i]) + NC, end="")
			for n in exe_names[j]:
				if not os.path.isfile(n):
					print( BOLD + "|" + NC + RED + "{:^12}".format("[CRASH]") + NC)
				log = open(result, "w", 1)
				process =	subprocess.run(["./" + n, files[i]], \
							text=True, stdout=log, stderr=subprocess.PIPE)
				log.close
				print(ft_checkOuput(process, files[i], lines[i]), end = "")
				os.remove(result)
			print()
		print("\n")
		# Removing executable files
		for name in exe_names[j]:
			os.remove(name)

################################################################################
#                                    Script                                    #
################################################################################

bflags	= "-D BUFFER_SIZE=" + str(32)
exe		=	cc + " " + cflags + " " + bflags + " -I " + gnl_path + " -o " + \
			name + " " + " ".join(src_b) + " " + bonus
process = subprocess.run(exe.split(), stderr=subprocess.DEVNULL)

log = open(result, "w", 1)
process =	subprocess.run(["./" + name] + files_b, text=True, stdout=log, stderr=subprocess.PIPE)
log.close
print(process)
