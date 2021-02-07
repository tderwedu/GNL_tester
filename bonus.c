/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bonus.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tderwedu <tderwedu@student.s19.be>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/01/20 11:08:26 by tderwedu          #+#    #+#             */
/*   Updated: 2021/02/07 16:04:52 by tderwedu         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../getNextLine/get_next_line.h"
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int	main(int argc, char **argv)
{
	int		i;
	int		ret;
	int		ret_tot;
	int		*fd;
	char	*str;

	i		= -1;
	ret 	= 1;
	ret_tot	= 1;
	argc--;
	fd 		= malloc(sizeof(int) * argc);
	while (++i < argc)
		fd[i] = open(argv[i + 1], O_RDONLY);
	while ( ret_tot > 0)
	{
		i		= -1;
		ret_tot	= 0;
		while (++i < argc)
		{
			if (fd[i])
			{
				ret = get_next_line(fd[i], &str);
				if (ret > 0)
				{
					printf("%s\n", str);
					free(str);
				}
				else if (ret == 0)
				{
					printf("%s", str);
					free(str);
					fd[i] = 0;
				}
				else
					return (1);
				ret_tot += ret;
			}
		}
	}
	free(fd);
}
