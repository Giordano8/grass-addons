#ifndef _RLEGEND_H_
#define _RLEGEND_H_

/* Header file: rlegend.h
 *
 *  AUTHOR:    E. Jorge Tizado, Spain 2009
 *
 *  COPYRIGHT: (c) 2009 E. Jorge Tizado, and the GRASS Development Team
 *             This program is free software under the GNU General Public
 *             License (>=v2). Read the file COPYING that comes with GRASS
 *             for details.
 */

#include <stdio.h>
#include "legends.h"

typedef struct
{
    char name[128];
    char mapset[128];
	LEGEND legend;

    /* category rlegend */
    int do_nodata;          /* show no data categoty */
    char cat_order[512];    /* category custom order */

    /* gradient rlegend */
    int do_gradient;        /* forze gradient when no float */
    double height;          /* Next only for float raster */
	int custom_range;
    double min, max;
    int tickbar;
	int whiteframe;
} RLEGEND;

#endif
