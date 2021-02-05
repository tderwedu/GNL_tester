import subprocess
import filecmp
import os

gnl_path	=	"../getNextLine"
buffer_size	= 32

sizes		= [1, 2, 3, 10, 11, 16, 32, 100, 9999, 100000]
files		= ["file_00.txt", "file_01.txt", "file_02.txt", "file_03.txt", "file_04.txt"]
expl		= ["A simple line", "A simple file", "Multiple newlines", "EOF without EOL", "Open() man page"]
lines		= [1, 3, 8, 1, 653]

norme		= "~/.norminette/norminette.rb"
bflags		= "-D BUFFER_SIZE=" + str(buffer_size)
name		= "gnl"

src			= ["get_next_line.c", "get_next_line_utils.c"]
src_b		= ["get_next_line_bonus.c", "get_next_line_utils_bonus.c"]



cflags		= "-Wall -Wextra -Werror -fsanitize=address"
cc			= "gcc"
main		= "main.c"
result		= "result.txt"

BOLD		=	"\033[1m"
BLU			=	"\033[96m"
GRN			=	"\033[32m"
RED			=	"\033[31m"
NC			=	"\033[0m"

src 		= [os.path.join(gnl_path, file) for file in src]
src_b 		= [os.path.join(gnl_path, file) for file in src_b]
files		= [os.path.join(gnl_path, file) for file in files]

generate	= cc + " " + cflags + " " + bflags + " -I " + gnl_path + " -o " + name + " " + \
			  " ".join(src) + " " + main

def ft_checkfile(file):
	if not os.path.getsize(result):
		return RED + "{:^8}".format("[CRASH]") + NC
	else:
		if filecmp.cmp(result, file):
			return GRN + "{:^8}".format("[OK]") + NC
		else:
			return RED + "{:^8}".format("[FAIL]") + NC
def ft_checklines(val, lines):
	# if not os.path.getsize(result):
	# 	return RED + "{:^8}".format(" ") + NC
	# else:
	# 	if val == str(lines):
	# 		return GRN + "{:^8}".format("[OK]") + NC
	# 	else:
	# 		return RED + "{:^8}".format("[FAIL]") + NC
	return RED + "{:^8}".format(" ") + NC

subprocess.run(generate.split(), stderr=subprocess.DEVNULL)
print(BOLD + "{:^30}".format("BUFFER_SIZE = " + str(buffer_size)) + "{:^8} {:^8}".format("Output", "Lines") + NC )
for i in range(len(files)):
	log = open(result, "w", 1)
	subprocess.run(["./" + name, files[i]], stdout=log, stderr=subprocess.DEVNULL)
	log.close
	# ret = subprocess.run(["./" + name , files[i], " 1"], text=True, stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
	# print(ret)
	print(BOLD + "{:<30}: ".format(expl[i]) + NC + ft_checkfile(files[i]) + " " + ft_checklines(0, lines[i]))
	# os.remove(result)

