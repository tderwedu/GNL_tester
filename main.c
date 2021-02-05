/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tderwedu <tderwedu@student.s19.be>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/01/20 11:08:26 by tderwedu          #+#    #+#             */
/*   Updated: 2021/02/05 19:03:41 by tderwedu         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../getNextLine/get_next_line.h"
#include <fcntl.h>
#include <stdio.h>
#include <string.h>

int	main(int argc, char **argv)
{
	int		fd;
	int		ret;
	int		lines;
	char	*str;

	lines = 0;
	fd = open(argv[1], O_RDONLY);
	if (argc == 2)
	{
		while ((ret = get_next_line(fd, &str)) > 0)
		{
			printf("%s\n", str);
			free(str);
		}
		if (ret == 0)
		{
			printf("%s", str);
			free(str);
		}
	}
	else if (argc == 3 && strcmp(argv[2],"1") == 0)
	{
		while ((ret = get_next_line(fd, &str)) > 0)
		{
			lines++;
			free(str);
		}
		if (ret == 0 && *str)
			lines++;
		free(str);
		printf("OK");
		printf("%d\n", lines);
	}
}
