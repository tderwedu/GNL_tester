
GNL_PATH	=	../getNextLine

NORME		=	~/.norminette/norminette.rb

SHELL		=	bash

BUFFER_SIZE	=	32

BFLAG		= -D BUFFER_SIZE=

NAME		=	gnl

CFLAGS		=	-Wall -Wextra -Werror -fsanitize=address

CC			=	gcc

SRC			=	${GNL_PATH}/get_next_line_bonus.c \
				${GNL_PATH}/get_next_line_utils_bonus.c

######################
#		Colors		 #
######################

BOLD		=	\e[1m
BLU			=	\e[96m
GRN			=	\e[32m
RED			=	\e[31m
NC			=	\e[0m

######################
#		MACROS		 #
######################

CRASH		=	printf "${RED}[CRASH]${NC}"
FAIL		=	printf "${RED} [FAIL]${NC}"
OK			=	printf "${GRN}  [OK] ${NC}"

TEST		=	"One simple 32 bits line"
FILE		=	file_01.txt
LAUNCH		=	{ ./${NAME} ${FILE} >result.txt ; } 2>/dev/null || :

PRINT		=	printf "${BOLD}%-30s${NC}:" ${TEST}
#OF_BASIC	=	if diff -U 3 result.txt >/dev/null $$file; then ${PRINT}; ${OK}; else ${PRINT}; ${FAIL}; fi
OF_BASIC	=	if diff -U 3 result.txt >/dev/null ${FILE}; then ${PRINT}; ${OK}; else ${PRINT}; ${FAIL}; fi
IFBASIC		=	if [ -s result.txt ]; then ${OF_BASIC}; else ${PRINT}; ${CRASH}; fi

SIZE_LIST	= 	1 2 3 4 5 10 11 15 16 30 50 100 256
FILES		=	file_00.txt  file_01.txt  file_02.txt  file_03.txt  file_04.txt
OF_LOOP		=	if diff -U 3 result.txt >/dev/null ${FILE}; then ${OK}; else ${FAIL}; fi
IFLOOP		=	if [ -s result.txt ]; then ${OF_LOOP}; else ${CRASH}; fi

#SIZES		=	("1" "2" "3" "4" "5" "10" "11" "15" "16" "30" "50" "100" "256")
FILES_AR	=	("file_00.txt" "file_01.txt" "file_02.txt" "file_03.txt" "file_04.txt")
#EXPL_AR		= 	"One simple 32 bits line" "A simple file" "file_02.txt" "file_03.txt" "file_04.txt"


all:		norm basic loop

prog:		clean
			${CC} ${CFLAGS} ${BFLAG}${BUFFER_SIZE} -I ${GNL_PATH} -o ${NAME} ${SRC} main.c

test:
			files_ar="${FILES_AR}}"
			@file="test"
			@printf "%s\n" ${FILE}
			FILE=${shell $${files_ar[0]}}
			@printf "%s\n" ${FILE}


#printf "%s - %s\n" $$nb ${FILE} ;
#${eval FILE=$${files_ar[$$nb]}}

buff:		clean
			@${CC} ${CFLAGS} ${BFLAG}${BUFFER_SIZE}  -I ${GNL_PATH} -o ${NAME} ${SRC} main.c
			@printf "${BOLD}%30s${NC}= 32\n" "BUFFER_SIZE "
			@for file in ${FILES}; do \
				{ ./${NAME} $$file >result.txt ; } 2>/dev/null || :; \
				${IFBASIC}; \
				printf "\n"; \
			done
			@rm -f restult.txt

basic:		clean
			@${CC} ${CFLAGS} ${BFLAG}${BUFFER_SIZE}  -I ${GNL_PATH} -o ${NAME} ${SRC} main.c
			@printf "${BOLD}%30s${NC}= 32\n" "BUFFER_SIZE "
# Test 00
			${eval TEST="One simple 32 bits line"}
			${eval FILE=file_00.txt}
			@${LAUNCH}
			@${IFBASIC}
			@printf "\n"
			@rm -f restult.txt
# Test 01
			${eval TEST="A simple file"}
			${eval FILE=file_01.txt}
			@${LAUNCH}
			@${IFBASIC}
			@printf "\n"
			@rm -f restult.txt
# Test 02
			${eval TEST="Many newlines in one buffer"}
			${eval FILE=file_02.txt}
			@${LAUNCH}
			@${IFBASIC}
			@printf "\n"
			@rm -f restult.txt
# Test 03
			${eval TEST="EOF w/o newline"}
			${eval FILE=file_03.txt}
			@${LAUNCH}
			@${IFBASIC}
			@printf "\n"
			@rm -f restult.txt
# Test 04
			${eval TEST="Open() man page"}
			${eval FILE=file_04.txt}
			@${LAUNCH}
			@${IFBASIC}
			@printf "\n"
			@rm -f ${NAME} result.txt
loop:
			@printf "${BOLD}%30s${NC}= " "BUFFER_SIZE "
			@for number in ${SIZE_LIST}; do printf "   %-3s " $$number ; done
			@printf  "\n"
			@for number in  ${SIZE_LIST} ; do \
				${CC} ${CFLAGS} ${BFLAG}$$number  -I ${GNL_PATH} -o "${NAME}_$$number" ${SRC} main.c; \
			done
# Test 00
			${eval FILE=file_00.txt}
			@printf "${BOLD}%-30s${NC}: " "One simple 32 bits line"
			@for number in  ${SIZE_LIST} ; do \
				{ ./${NAME}_$$number ${FILE} >result.txt ; } 2>/dev/null || :;\
				${IFLOOP}; \
			done
			@printf  "\n"
# Test 01
			${eval FILE=file_01.txt}
			@printf "${BOLD}%-30s${NC}: " "One simple 32 bits line"
			@for number in  ${SIZE_LIST} ; do \
				{ ./${NAME}_$$number ${FILE} >result.txt ; } 2>/dev/null || :;\
				${IFLOOP}; \
			done
			@printf  "\n"
# Test 02
			${eval FILE=file_02.txt}
			@printf "${BOLD}%-30s${NC}: " "One simple 32 bits line"
			@for number in  ${SIZE_LIST} ; do \
				{ ./${NAME}_$$number ${FILE} >result.txt ; } 2>/dev/null || :;\
				${IFLOOP}; \
			done
			@printf  "\n"
# Test 03
			${eval FILE=file_03.txt}
			@printf "${BOLD}%-30s${NC}: " "One simple 32 bits line"
			@for number in  ${SIZE_LIST} ; do \
				{ ./${NAME}_$$number ${FILE} >result.txt ; } 2>/dev/null || :;\
				${IFLOOP}; \
			done
			@printf  "\n"
# Test 04
			${eval FILE=file_04.txt}
			@printf "${BOLD}%-30s${NC}: " "One simple 32 bits line"
			@for number in  ${SIZE_LIST} ; do \
				{ ./${NAME}_$$number ${FILE} >result.txt ; } 2>/dev/null || :;\
				${IFLOOP}; \
			done
			@printf  "\n"
			@rm -f ${NAME}* result.txt
clean:
			@rm -f ${NAME} result.txt

norm:
			@if ${NORME} ${SIZE_LIST}/*.[ch] | grep -qv Norme ;then\
			printf "${BOLD}%-30s${NC}: ${GRN} [OK] ${NC}\n" "norminette";\
			else\
			printf "${BOLD}%-30s${NC}: ${RED}[FAIL]${NC}\n" "norminette";fi

.phony:		all basic loop clean norm

