#include "local_proto.h"
	
int open_maps(void) {
	
	int i;
	char* mapset;
	struct Cell_head cellhd;
	
	for (i=0;i<nmaps;++i) {
		
			if (s_maps[i].output) {
		s_maps[i].in_buf=NULL;
		continue;
			}
		
		mapset = G_find_cell2(s_maps[i].name, "");
	
	    if (mapset == NULL)
		G_fatal_error(_("Raster map <%s> not found"), s_maps[i].name);
	
	    if ((s_maps[i].cfd = G_open_cell_old(s_maps[i].name, mapset)) < 0)
		G_fatal_error(_("Unable to open raster map <%s>"), s_maps[i].name);
	
	    if (G_get_cellhd(s_maps[i].name, mapset, &cellhd) < 0)
		G_fatal_error(_("Unable to read file header of <%s>"), s_maps[i].name);
	
		s_maps[i].raster_type = G_get_raster_map_type(s_maps[i].cfd);
		s_maps[i].in_buf = G_allocate_raster_buf(s_maps[i].raster_type);
		
	}

return 0;
}


int get_rows (int row) {
	
	int i;
	for (i=0;i<nmaps;++i) {

			if (s_maps[i].output)
		continue;

		if (G_get_raster_row(s_maps[i].cfd, s_maps[i].in_buf, row, s_maps[i].raster_type)<0) {
			G_close_cell(s_maps[i].cfd);
			G_fatal_error(_("Cannot to read <%s> at row <%d>"), s_maps[i].name,row);
		}
	}

return 0;
}

int get_cells (int col) {
	int i;
	CELL c;
	FCELL f;
	DCELL d;
	
		for (i=0;i<nmaps;++i) {

			if (s_maps[i].output)
		continue;
	
			switch (s_maps[i].raster_type) {

				case CELL_TYPE:
				c = ((CELL *) s_maps[i].in_buf)[col];
					if (G_is_null_value(&c,CELL_TYPE)) 
				return 1;
					else
				s_maps[i].cell = (FCELL) c;
					break;

				case FCELL_TYPE:
				f = ((FCELL *) s_maps[i].in_buf)[col];
					if (G_is_null_value(&f,FCELL_TYPE))  
				return 1;
					else
				s_maps[i].cell =  (FCELL) f;
			break;

				case DCELL_TYPE:
			d = ((DCELL *) s_maps[i].in_buf)[col];
					if (G_is_null_value(&d,DCELL_TYPE)) 
				return 1;
					else
				s_maps[i].cell =  (FCELL) d;		
			break;
			}
		} /* end for */

return 0;
}

int create_output_maps(void) {
		
	STRING connector="_";
	int i;
	m_outputs = (OUTPUTS* )G_malloc(nrules * sizeof (OUTPUTS));

	for (i=0;i<nrules;++i) {
		strcpy(m_outputs[i].output_name,output);
		strcat(m_outputs[i].output_name,connector);
		strcat(m_outputs[i].output_name,s_rules[i].outname);
		
			if ((m_outputs[i].ofd = G_open_raster_new(m_outputs[i].output_name, FCELL_TYPE)) < 0)
		G_fatal_error(_("Unable to create raster map <%s>"), m_outputs[i].output_name);
	
		m_outputs[i].out_buf = G_allocate_f_raster_buf();

	}

}

int process_coors (char *answer) {

	struct Cell_head window;
	double x, y;
	int i, j;
	int r,c;
	int num_points;
	float result;
	
	G_get_window(&window);
	num_points=sscanf(answer,"%lf,%lf", &x, &y);

  r= (int) G_easting_to_col	(	x, &window); 
  c= (int) G_northing_to_row	(	y, &window); 
	
	get_rows(r);
	get_cells(c);
	result=implicate();
	
				for (i=0;i<nrules;++i)
		
		fprintf(stdout,"ANTECEDENT %s: %5.3f\n",s_rules[i].outname,antecedents[i]);
		fprintf(stdout,"RESULT (deffuzified):  %5.3f\n",result);
	
	
	fprintf(stdout,"UNIVERSE,");
			for (i=0;i<nrules;++i)
		fprintf(stdout,"%s,",s_rules[i].outname);
	fprintf(stdout,"AGREGATE \n");	
	
				for (i=0;i<resolution;++i) 
		for (j=0;j<nrules+2;++j) {
			fprintf(stdout,"%5.3f",visual_output[i][j]);
				if (j<nrules+1)
			fprintf(stdout,",");
				else
			fprintf(stdout,"\n");	
		}
	
	exit(EXIT_SUCCESS);
}

