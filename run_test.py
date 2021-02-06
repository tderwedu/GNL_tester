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
files		= [os.path.join("Files", file) for file in files]


def ft_checkOuput(process, file, lines):
	if process.returncode:
		ft_writeError(1, process, file)
		if "Sanitizer" in process.stderr:
			return PUR + "{:^13}".format("[LEAKS]") + NC
		else:
			return RED + "{:^13}".format("[CRASH]") + NC
	else:
		if filecmp.cmp(result, file):
			ret = GRN + "{:^6}".format("[OK]") + NC
		else:
			ft_writeError(2, process, file)
			ret =  YLW + "{:^6}".format("[FAIL]") + NC
		if lines == int(process.stderr):
			ret = ret + " " + GRN + "{:^6}".format("[OK]") + NC
		else:
			ret = ret + " " + YLW + "{:^6}".format("[FAIL]") + NC
		return ret

def ft_writeError(nb, process, file):
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

for i in range(len(4)):
	print(BOLD + "{:>20}  {:^7} {:^7}".format("BUFFER_SIZE  " + str(sizes[i]), "Output", "Lines") + NC )

# for size in sizes:
# 	# Generating executable file
# 	bflags	= "-D BUFFER_SIZE=" + str(size)
# 	exe		=	cc + " " + cflags + " " + bflags + " -I " + gnl_path + " -o " + \
# 		 		name + " " + " ".join(src) + " " + main
# 	subprocess.run(exe.split(), stderr=subprocess.DEVNULL)
	
# 	print(BOLD + "{:>30}  {:^7} {:^7}".format("BUFFER_SIZE  " + str(buffer_size), "Output", "Lines") + NC )
# 	for i in range(len(files)):
# 		log = open(result, "w", 1)
# 		process = subprocess.run(["./" + name, files[i]], text=True, stdout=log, stderr=subprocess.PIPE)
# 		log.close
# 		print(BOLD + "{:<30}: ".format(expl[i]) + NC + ft_checkOuput(process, files[i], lines[i]))
# 		# os.remove(result)


