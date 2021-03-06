/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tderwedu <tderwedu@student.s19.be>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/01/20 11:08:26 by tderwedu          #+#    #+#             */
/*   Updated: 2021/03/16 11:43:28 by tderwedu         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"
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
			lines++;
			free(str);
		}
		if (ret == 0)
		{
			printf("%s", str);
			if (*str)
				lines++;
			free(str);
		}
		fprintf(stderr, "%d", lines);
	}
}
