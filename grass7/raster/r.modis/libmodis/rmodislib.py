#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################################################################
#
# MODULE:	r.modis
# AUTHOR(S):	Luca Delucchi
# PURPOSE:	Here there are some important class to run r.modis modules
#
#
# COPYRIGHT:	(C) 2011 by Luca Delucchi
#
#		This program is free software under the GNU General Public
#		License (>=v2). Read the file COPYING that comes with GRASS
#		for details.
#
#############################################################################
import grass.script as grass
# interface to g.proj -p


def get_proj(flag='p'):
    """!Returns the output from running "g.proj -p" plus towgs84 parameter
    (g.proj -d), as a dictionary. Example:

    \code
    >>> proj = grass.get_proj()
    >>> (proj['name'], proj['ellps'], proj['datum'])
    (Lat/Lon, wgs84, wgs84)
    \endcode

    @return dictionary of projection values
    """
    gproj = grass.read_command('g.proj', flags=flag)
    if flag == 'p':
        listproj = gproj.split('\n')
        listproj.remove('-PROJ_INFO-------------------------------------------------')
        listproj.remove('-PROJ_UNITS------------------------------------------------')
        listproj.remove('-PROJ_EPSG-------------------------------------------------')
        listproj.remove('')
        proj = {}
        for i in listproj:
            try:
                ilist = i.split(':')
                proj[ilist[0].strip()] = ilist[1].strip()
            except IndexError:
                continue
        proj.update(grass.parse_command('g.proj', flags='j'))
        return proj
    elif flag == 'w':
        return gproj.replace('\n', '').replace('    ', '')


class product:
    """Definition of MODIS product with url and path in the ftp server
    """

    def __init__(self, value=None):
        # url to download products
        urlbase = 'http://e4ftl01.cr.usgs.gov'
        usrsnow = 'ftp://n5eil01u.ecs.nsidc.org'
        # values of lst product:
        lst_spec = '( 1 0 0 0 1 0 0 0 0 0 0 0 )'
        lst_specqa = '( 1 1 0 0 1 1 0 0 0 0 0 0 )'
        # suffix for the lst product (key is the lst map, value the QA)
        lst1km_suff = {'.LST_Day_1km': '.QC_Day',
                       '.LST_Night_1km': '.QC_Night'}
        lst6km_suff = {'.LST_Day_6km': '.QC_Day',
                       '.LST_Night_6km': '.QC_Night'}
        # color for lst product
        lst_color = ['celsius']
        # values of vi product:
        vi_spec = '( 1 1 0 0 0 0 0 0 0 0 0 0 )'
        vi_specqa = '( 1 1 1 0 0 0 0 0 0 0 0 1 )'
        vi_color = ['ndvi', 'evi']
        vi250m_suff = {'.250m_16_days_NDVI': '.250m_16_days_VI_Quality',
                       '.250m_16_days_EVI': '.250m_16_days_VI_Quality'}
        vi500m_suff = {'.500m_16_days_NDVI': '.500m_16_days_VI_Quality',
                       '.500m_16_days_EVI': '.500m_16_days_VI_Quality'}
        vi1km_suff = {'.1_km_16_days_NDVI': '.1_km_16_days_VI_Quality',
                      '.1_km_16_days_EVI': '.1_km_16_days_VI_Quality'}
        # values of snow product:
        snow1_spec = ('( 1 )')
        snow1_specqa = ('( 1 1 )')
        snow1_suff = {'.Snow_Cover_Daily_Tile': '.Snow_Spatial_QA'}
        snow8_spec = ('( 1 1 )')
        snow_color = ['gyr']  # TODO CREATE THE COLOR TABLE FOR MODIS_SNOW
        snow8_suff = {'.Maximum_Snow_Extent': None,
                      '.Eight_Day_Snow_Cover': None}
        lstL2_spec = 'LST; QC; Error_LST; Emis_31; Emis_32; View_angle; View_time'
        # values of surface reflectance product:
        surf_spec = '( 1 1 1 1 1 1 1 0 0 0 0 0 0 )'
        surf_specqa = '( 1 1 1 1 1 1 1 1 0 0 0 0 0 )'
        surf_suff = {'.sur_refl_b01': '.sur_refl_qc_500m', '.sur_refl_b02':
                     '.sur_refl_qc_500m', '.sur_refl_b03': '.sur_refl_qc_500m',
                     '.sur_refl_b04': '.sur_refl_qc_500m', '.sur_refl_b05':
                     '.sur_refl_qc_500m', '.sur_refl_b06': '.sur_refl_qc_500m',
                     '.sur_refl_b07': '.sur_refl_qc_500m'}
        # granularity
        daily = 1
        eight = 8
        sixteen = 16
        self.prod = value
        lst = {'lst_aqua_daily_1000': {'url': urlbase, 'folder': 'MOLA/',
                                       'prod': 'MYD11A1.005', 'days': daily,
                                       'spec': lst_spec, 'spec_qa': lst_specqa,
                                       'suff': lst1km_suff, 'res': 1000,
                                       'color': lst_color},
               'lst_terra_daily_1000': {'url': urlbase, 'folder': 'MOLT/',
                                        'prod': 'MOD11A1.005', 'days': daily,
                                        'spec': lst_spec, 'spec_qa': lst_specqa,
                                        'suff': lst1km_suff, 'res': 1000,
                                        'color': lst_color},
               'lst_terra_eight_1000': {'url': urlbase, 'folder': 'MOLT/',
                                        'prod': 'MOD11A2.005', 'days': eight,
                                        'spec': lst_spec, 'spec_qa': lst_specqa,
                                        'suff': lst1km_suff, 'res': 1000,
                                        'color': lst_color},
               'lst_aqua_eight_1000': {'url': urlbase, 'folder': 'MOLA/',
                                       'prod': 'MYD11A2.005', 'days': eight,
                                       'spec': lst_spec, 'spec_qa': lst_specqa,
                                       'suff': lst1km_suff, 'res': 1000,
                                       'color': lst_color},
               'lst_terra_daily_6000': {'url': urlbase, 'folder': 'MOLT/',
                                        'prod': 'MOD11B1.005', 'days': daily,
                                        'spec': lst_spec, 'spec_qa': lst_specqa,
                                        'suff': lst6km_suff, 'res': 6000,
                                        'color': lst_color},
               'lst_aqua_daily_6000': {'url': urlbase, 'folder': 'MOLA/',
                                       'prod': 'MYD11B1.005', 'days': daily,
                                       'spec': lst_spec, 'spec_qa': lst_specqa,
                                       'suff': lst6km_suff, 'res': 6000,
                                       'color': lst_color}
               }
        vi = {'ndvi_terra_sixteen_250': {'url': urlbase, 'folder': 'MOLT/',
                                         'prod': 'MOD13Q1.005',
                                         'spec': vi_spec, 'spec_qa': vi_specqa,
                                         'suff': vi250m_suff, 'res': 250,
                                         'color': vi_color, 'days': sixteen},
              'ndvi_aqua_sixteen_250': {'url': urlbase, 'folder': 'MOLA/',
                                        'prod': 'MYD13Q1.005',
                                        'spec': vi_spec, 'spec_qa': vi_specqa,
                                        'suff': vi250m_suff, 'res': 250,
                                        'color': vi_color, 'days': sixteen},
              'ndvi_terra_sixteen_500': {'url': urlbase, 'folder': 'MOLT/',
                                         'prod': 'MOD13A1.005',
                                         'spec': vi_spec, 'spec_qa': vi_specqa,
                                         'suff': vi1km_suff, 'res': 500,
                                         'color': vi_color, 'days': sixteen},
              'ndvi_aqua_sixteen_500': {'url': urlbase, 'folder': 'MOLA/',
                                        'prod': 'MYD13A1.005',
                                        'spec': vi_spec, 'spec_qa': vi_specqa,
                                        'suff': vi500m_suff, 'res': 500,
                                        'color': vi_color, 'days': sixteen},
              'ndvi_terra_sixteen_1000': {'url': urlbase, 'folder': 'MOLT/',
                                          'prod': 'MOD13A2.005',
                                          'spec': vi_spec, 'spec_qa': vi_specqa,
                                          'suff': vi500m_suff, 'res': 1000,
                                          'color': vi_color, 'days': sixteen},
              'ndvi_aqua_sixteen_1000': {'url': urlbase, 'folder': 'MOLA/',
                                         'prod': 'MYD13A2.005',
                                         'spec': vi_spec, 'spec_qa': vi_specqa,
                                         'suff': vi1km_suff, 'res': 1000,
                                         'color': vi_color, 'days': sixteen}
              }
        surf_refl = {'surfreflec_terra_eight_500': {'url': urlbase,
                                                    'folder': 'MOLT/',
                                                    'prod': 'MOD09A1.005',
                                                    'spec': surf_spec,
                                                    'spec_qa': surf_specqa,
                                                    'res': 500, 'days': eight,
                                                    'color': snow_color,
                                                    'suff': surf_suff},
                     'surfreflec_aqua_eight_500': {'url': urlbase,
                                                   'folder': 'MOLA/',
                                                   'prod': 'MYD09A1.005',
                                                   'spec': surf_spec,
                                                   'spec_qa': surf_specqa,
                                                   'res': 500, 'days': eight,
                                                   'color': snow_color,
                                                   'suff': surf_suff}
                     }
        snow = {'snow_terra_daily_500': {'url': usrsnow, 'folder': 'SAN/MOST/',
                                         'prod': 'MOD10A1.005',
                                         'spec': snow1_spec, 'days': daily,
                                         'spec_qa': snow1_specqa,
                                         'color': snow_color,
                                         'suff': snow1_suff, 'res': 500},
                'snow_aqua_daily_500': {'url': usrsnow,
                                        'folder': 'SAN/MOSA/',
                                        'prod': 'MYD10A1.005',
                                        'spec': snow1_spec, 'days': daily,
                                        'spec_qa': snow1_specqa,
                                        'color': snow_color,
                                        'suff': snow1_suff, 'res': 500},
                'snow_terra_eight_500': {'url': usrsnow,
                                         'folder': 'SAN/MOST/',
                                         'prod': 'MOD10A2.005',
                                         'spec': snow8_spec,
                                         'spec_qa': None, 'days': eight,
                                         'color': snow_color,
                                         'suff': snow8_suff, 'res': 500},
                'snow_aqua_eight_500': {'url': usrsnow,
                                        'folder': 'SAN/MOSA/',
                                        'prod': 'MYD10A2.005',
                                        'spec': snow8_spec,
                                        'spec_qa': None, 'days': eight,
                                        'color': snow_color,
                                        'suff': snow8_suff, 'res': 500}
                }
        self.products = {}
        self.products.update(lst)
        self.products.update(vi)
        self.products.update(snow)
        self.products.update(surf_refl)
        self.products_swath = {'lst_terra_daily': {'url': urlbase,
                                                   'folder': 'MOLT/',
                                                   'prod': 'MOD11_L2.005',
                                                   'spec': lstL2_spec},
                               'lst_aqua_daily': {'url': urlbase,
                                                  'folder': 'MOLA/',
                                                  'prod': 'MYD11_L2.005',
                                                  'spec': lstL2_spec}
                               }

    def returned(self):
        if self.products.keys().count(self.prod) == 1:
            return self.products[self.prod]
        elif self.products_swath.keys().count(self.prod) == 1:
            return self.products_swath[self.prod]
        else:
            grass.fatal(_("The code insert is not supported yet. Consider "
                          "to ask on the grass-dev mailing list for future "
                          "support"))

    def fromcode(self, code):
        import string
        for k, v in self.products.iteritems():
            if string.find(v['prod'], code) != -1:
                return self.products[k]
        for k, v in self.products_swath.iteritems():
            if string.find(v['prod'], code) != -1:
                return self.products_swath[k]
        grass.fatal(_("The code insert is not supported yet. Consider to "
                      "ask on the grass-dev mailing list for future support"))

    def color(self, code=None):
        if code:
            return self.fromcode(code)['color']
        else:
            return self.returned()['color']

    def suffix(self, code=None):
        if code:
            return self.fromcode(code)['suff']
        else:
            return self.returned()['suff']

    def __str__(self):
        prod = self.returned()
        string = "url: " + prod['url'] + ", folder: " + prod['folder']
        if prod.keys().count('spec') == 1:
            string += ", spectral subset: " + prod['spec']
        if prod.keys().count('spec_qa') == 1:
            string += ", spectral subset qa:" + prod['spec_qa']
        return string


class resampling:
    """Return the resampling value from the code used in the modules
    """
    def __init__(self, value):
        self.code = value
        self.resampling = {'nearest': 'NEAREST_NEIGHBOR',
                           'bilinear': 'BILINEAR',
                           'cubic': 'CUBIC CONVOLUTION'}

    def returned(self):
        return self.resampling[self.code]


class projection:
    """Definition of projection for converting from sinusoidal projection to
    another one. Not all projection systems are supported"""
    def __init__(self):
        self.proj = get_proj()
        self.val = self.proj['proj']
        if self.proj['datum']:
            self.dat = self.proj['datum']
        else:
            self.dat = 'none'
        self.projections = {'laea': 'LA', 'll': 'GEO', 'lcc': 'LCC',
                            'merc': 'MERCAT', 'polar': 'PS', 'utm': 'UTM',
                            'tmerc': 'TM'}
        self.datumlist = {'none': 'NONE', 'nad27': 'NAD27', 'nad83': 'NAD83',
                          'wgs66': 'WGS66', 'wgs72': 'WGS72', 'wgs84': 'WGS84',
                          'etrs89': 'WGS84'}
        self.datumlist_swath = {'Clarke 1866': 0, 'Clarke 1880': 1,
                                'bessel': 2, 'International 1967': 3,
                                'International 1909': 4, 'wgs72': 5,
                                'Everest': 6, 'wgs66': 7, 'wgs84': 8,
                                'Airy': 9, 'Modified Everest': 10,
                                'Modified Airy': 11, 'Walbeck': 12,
                                'Southeast Asia': 13, 'Australian National': 14,
                                'Krassovsky': 15, 'Hough': 16,
                                'Mercury1960': 17, 'Modified Mercury1968': 18,
                                'Sphere 19 (Radius 6370997)': 19,
                                'MODIS Sphere (Radius 6371007.181)': 20
                                }

    def returned(self):
        """Return the projection in the MRT style"""
        if self.val not in self.projections.keys():
            grass.fatal(_("Projection <%s> is not supported") % self.val)
        else:
            return self.projections[self.val]

    def _par(self, key):
        """Function use in return_params"""
        if self.proj[key]:
            Val = self.proj[key]
        else:
            Val = 0.0
        return float(Val)

    def _outpar(self, SMajor, SMinor, Val, Factor, CentMer, TrueScale, FE, FN,
                swath):
        if swath:
            return '%i %i %d %d %d %d %d %d 0.0 0.0 0.0 0.0 0.0 0.0 0.0' % (
                    SMajor, SMinor, Val, Factor, CentMer, TrueScale, FE, FN)
        else:
            return '( %i %i %d %d %d %d %d %d 0.0 0.0 0.0 0.0 0.0 0.0 0.0 )' % (
                    SMajor, SMinor, Val, Factor, CentMer, TrueScale, FE, FN)

    def return_params(self, swath=False):
        """ Return the 13 parameters for MRT parameter file """
        if self.val == 'll' or self.val == 'utm':
            return self._outpar(0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, swath)
        elif self.val == 'laea':
            SMajor = self._par('+a')
            try:
                SMinor = self._par('+b')
            except:
                SMinor = self._par('+rf')
            CentMer = self._par('+lon_0')
            CentLat = self._par('+lat_0')
            FE = self._par('+x_0')
            FN = self._par('+y_0')
            return self._outpar(SMajor, SMinor, 0.0, 0.0, CentMer,
                                CentLat, FE, FN, swath)
        elif self.val == 'lcc':
            SMajor = self._par('+a')
            try:
                SMinor = self._par('+b')
            except:
                SMinor = self._par('+rf')
            STDPR1 = self._par('+lat_1')
            STDPR2 = self._par('+lat_2')
            CentMer = self._par('+lon_0')
            CentLat = self._par('+lat_0')
            FE = self._par('+x_0')
            FN = self._par('+y_0')
            return self._outpar(SMajor, SMinor, STDPR1, STDPR2, CentMer,
                                CentLat, FE, FN, swath)
        elif self.val == 'merc' or self.val == 'polar' or self.val == 'tmerc':
            SMajor = self._par('+a')
            try:
                SMinor = self._par('+b')
            except:
                SMinor = self._par('+rf')
            CentMer = self._par('+lon_0')
            if self.val == 'tmerc':
                Factor = self._par('+k_0')
            else:
                Factor = 0.0
            TrueScale = self._par('+lat_ts')
            FE = self._par('+x_0')
            FN = self._par('+y_0')
            return self._outpar(SMajor, SMinor, 0.0, Factor, CentMer,
                                TrueScale, FE, FN, swath)
        else:
            grass.fatal(_('Projection not supported, please contact the '
                          'GRASS-dev mailing list'))

    def datum(self):
        """Return the datum in the MRT style"""
        if self.dat not in self.datumlist.keys():
            grass.fatal(_("Datum <%s> is not supported") % self.dat)
        elif self.dat == 'etrs89':
            grass.warning(_("Changing datum <%s> to <%s>") % (self.dat,
                                                              'wgs84'))
        return self.datumlist[self.dat]

    def datumswath(self):
        """Return the datum in MRT style"""
        return self.datumlist_swath[self.dat]

    def utmzone(self):
        """Return the utm zone number"""
        return self.proj['zone']
