import subprocess
import filecmp
import math as m
import os

################################################################################
#                                  Input Data                                  #
################################################################################

gnl_path	=	"../getNextLine"

src			=	["get_next_line.c", "get_next_line_utils.c"]
src_b		=	["get_next_line_bonus.c", "get_next_line_utils_bonus.c"]

buffSizes	=	[1, 2, 3, 10, 11, 16, 32, 100, 9999, 1000000]
files		=	["file_00.txt", "file_01.txt", "file_02.txt", "file_03.txt", "file_04.txt",\
				 "file_05.txt", "file_06.txt"]
files_b0	= 	["bonus_0_0.txt", "bonus_0_1.txt", "bonus_0_2.txt"]
files_b1	= 	["bonus_1_0.txt", "bonus_1_1.txt", "bonus_1_2.txt", "bonus_1_3.txt"]
expl		= 	["A simple line", "A simple file", "Multiple newlines", "EOF without EOL", "Open() man page", \
				 "Long line with EOL", "Long line w/o EOL"]
expl_b		=	["Open() 3 files", "Long line w/o EOL"]
nbLines		=	[1, 3, 8, 1, 653, 1, 1]

norme		=	os.environ["HOME"] + "/.norminette/norminette.rb"
execName	=	"gnl"

cflags		=	"-Wall -Wextra -Werror -fsanitize=address"
cc			=	"gcc"
main		=	"main.c"
bonus		=	"bonus.c"
result		=	"result.txt"
outputDir	=	"Errors"

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
files_b0	= [os.path.join("Test_Files", file) for file in files_b0]
files_b1	= [os.path.join("Test_Files", file) for file in files_b1]

################################################################################
#                                   Functions                                  #
################################################################################

def ft_reshape(vec, length):
	i_max = (os.get_terminal_size().columns - 21) // length
	j_max = m.ceil(len(vec) / i_max)
	tab		= list()
	i_s	= 0
	for j in range(j_max - 1):
		tab.append([v for v in vec[i_s:(i_s + i_max)]])
		i_s		+= i_max
	i_e = len(vec) % i_max
	tab.append([v for v in vec[i_s:i_s + i_e]])
	return [tab, j_max]

def ft_createExec(execName, mainName, sizes):
	execNames = list()
	# Reshaping to adapt to terminal size
	[sizes, j_max] = ft_reshape(sizes, 10)
	print(BOLD + BLU + "\nCreating executables" + NC)
	for j in range(j_max):
		print(BOLD + "{:^20}".format("BUFFER_SIZE") + NC, end = "")
		for size in sizes[j]:
				print(BOLD + "|{:^9}".format(size) + NC, end = "")
		print(BOLD + "|" + NC + "\n{:20}".format(" "), end = "")
		for size in sizes[j]:
			execNames.append(execName + "_" + str(size))
			bflags	= "-D BUFFER_SIZE=" + str(size)
			exe		=	cc + " " + cflags + " " + bflags + " -I " + gnl_path + " -o " +\
						execNames[-1] + " " + " ".join(src) + " " + mainName
			process = subprocess.run(exe.split(), stderr=subprocess.DEVNULL)
			if  not process.returncode:
				print(BOLD + "|" + NC + GRN + "{:^9}".format("[OK]") + NC, end = "", flush = True)
			else:
				print(BOLD + "|" + NC + RED + "{:^9}".format("[FAIL]") + NC, end = "", flush = True)
		print(BOLD + "|" + NC +"\n")
	return execNames

def ft_printBuffSizes(sizes, j):
	print(BOLD + "{:^20}".format("BUFFER_SIZE") + NC, end = "")
	for size in sizes[j]:
		print(BOLD + "|{:^12}".format(size) + NC, end = "")
	print(BOLD + "|" + NC + "\n{:20}".format(" "), end = "")
	for size in sizes[j]:
		print(BOLD + "|{:^6}{:^6}".format("Ouput", "Lines") + NC, end = "")
	print(BOLD + "|" + NC )

def ft_checkOuput(process, file, lines, size):
	if process.returncode:
		ft_writeIfError(1, process, file, size)
		if "Sanitizer" in process.stderr:
			return BOLD + "|" + NC + PUR + "{:^12}".format("[LEAKS]") + NC
		else:
			return BOLD + "|" + NC + RED + "{:^12}".format("[CRASH]") + NC
	else:
		if filecmp.cmp(result, file):
			ret = BOLD + "|" + NC + GRN + "{:^6}".format("[OK]") + NC
		else:
			ft_writeIfError(2, process, file, size)
			ret = BOLD + "|" + NC + YLW + "{:^6}".format("[FAIL]") + NC
		if lines:
			if lines == int(process.stderr):
				ret += GRN + "{:^6}".format("[OK]") + NC
			else:
				ret += YLW + "{:^6}".format("[FAIL]") + NC
		else:
			ret += "{:^6}".format(" ")
		return ret

def ft_writeIfError(nb, process, file, size):
	if not os.path.isdir(outputDir):
		os.mkdir(outputDir)
	if nb == 1:
		path = os.path.join(outputDir, "BF_" + size + "_" + os.path.basename(file))
		log = open(path, "w", 1)
		log.write(process.stderr)
		log.close
	elif nb == 2:
		path = os.path.join(outputDir, "BF_" + size + "_" + os.path.basename(file))
		os.rename(result, path)

def ft_checkGNL(execName, testfiles, checkFiles, cFile, nbLines, buffSizes, expl):
	# Creating executables
	execNames = ft_createExec(execName, cFile, buffSizes)
	# Reshaping to adapt to terminal size
	[buffSizes, j_max] = ft_reshape(buffSizes, 13)
	[execNames, j_max] = ft_reshape(execNames, 13)
	for j in range(j_max):
		print(BOLD + BLU + "Testing GNL" + NC)
		# Printing BUFFER_SIZES
		ft_printBuffSizes(buffSizes, j)
		# Testing and printing result
		for i in range(len(testfiles)):
			print(BOLD + "{:<20}".format(expl[i]) + NC, end="")
			for name in execNames[j]:
				if not os.path.isfile(name):
					print( BOLD + "|" + NC + RED + "{:^12}".format("[CRASH]") + NC)
				log = open(result, "w", 1)
				process =	subprocess.run(["./" + name] + testfiles[i], text=True,\
							stdout = log, stderr = subprocess.PIPE)
				log.close
				buffSize = name.split("_")[-1]
				print(ft_checkOuput(process, checkFiles[i], nbLines[i], buffSize),\
						end = "", flush = True)
				os.remove(result)
			print(BOLD + "|" + NC)
		print()
		# Removing executable files
		for name in execNames[j]:
			os.remove(name)

def	ft_printHeader(s):
	l = os.get_terminal_size().columns
	print(BOLD + BLU + "{:#^{x}}".format("#", x = l))
	print("#{:^{x}}#".format(s, x = l - 2))
	print("{:#^{x}}".format("#", x = l) + NC)

def ft_isFiles(src, msg):
	b = 1
	for f in src:
		b *= os.path.isfile(f)
	print(BOLD + "{:^20}".format(msg) + "|" + NC, end = "", flush = True)
	if b:
		print(GRN + "{:^6}".format("[OK]") + NC)
	else:
		print(RED + "{:^6}".format("[FAIL]") + NC)
	return b

def ft_norminette(src, msg):
	process = subprocess.run([norme] + src, text=True, stdout = subprocess.PIPE,\
				stderr = subprocess.PIPE, env = os.environ)
	print(BOLD + "{:^20}".format(msg) + "|" + NC, end = "", flush = True)
	if not "Error" in process.stdout:
		print(GRN + "{:^6}".format("[OK]") + NC)
	else:
		print(RED + "{:^6}".format("[FAIL]") + NC)

def ft_nbStaticVar(src):
	print(BOLD + BLU + "Static Variable" + NC)
	msg = "Only One"
	nbStaticVar = 0
	for file in src:
		with open(file, 'r') as f:
			for line in f.readlines():
				if ("static" in line) and (";" in line):
						nbStaticVar += 1
	print(BOLD + "{:^20}".format(msg) + "|" + NC, end = "", flush = True)
	if 	nbStaticVar <= 1:
		print(GRN + "{:^6}".format("[OK]") + NC + "\n")
	else:
		print(RED + "{:^6}".format("[FAIL]") + NC + "\n")
	


################################################################################
#                                    Script                                    #
################################################################################

if __name__ == "__main__":
	ft_printHeader("Test of get_next_line() - 2021")
	print("\n" + BOLD + BLU + "Source Files" + NC)
	f_m = ft_isFiles(src, "Mandatory Part")
	f_b = ft_isFiles(src_b,"Bonus Part")

	print(BOLD + BLU + "Norminette" + NC)
	if f_m:
		ft_norminette(src, "Mandatory Part")
	if f_b:
		ft_norminette(src_b, "Bonus Part")
	print()

	if f_m:
		ft_printHeader("MANDATORY PART")
		testfiles	= [[f] for f in files]
		checkFiles	= files
		ft_checkGNL(execName, testfiles, checkFiles, "main.c", nbLines, buffSizes, expl)
	if f_b:
		ft_printHeader("BONUS PART")
		testfiles	= [files_b0, files_b1]
		checkFiles	= [files[4], files[6]]
		buffSizes	= [buffSizes[i] for i in range(len(buffSizes)) if not i % 2 ]
		nbLines		= [0] * len(testfiles)
		ft_checkGNL(execName, testfiles, checkFiles, "bonus.c", nbLines, buffSizes, expl_b)
		ft_nbStaticVar(src_b)
	ft_printHeader("THE END")

