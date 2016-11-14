import gzip
import netCDF4
import numpy
import os
import pickle

class NSIDC0530:

    with gzip.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'latlon.gz'), 'rb') as f:
        __latitude, __longitude = pickle.load(f)

    def __init__(self, yyyy, mm, dd, reqvars=[], bounds=None):

        def subset(var, bbox):
            return '{0}[0:1:0][{1}:1:{2}][{3}:1:{4}]'.format(var, *bbox)

        def url(reqvars, yyyy, mm, dd, bbox):
            mm = '{:02d}'.format(mm)
            dd = '{:02d}'.format(dd)
            return (
                'http://n5eil01u.ecs.nsidc.org/opendap/MEASURES/NSIDC-0530.001/'
                '{0}.{1}.{2}/nhtsd25e2_{0}{1}{2}_v01r01.nc?'.format(yyyy, mm, dd)
            ) + ','.join([subset(var, bbox) for var in reqvars])

        valids = [
            'ims_snow_cover_extent',
            'merged_snow_cover_extent',
            'modis_cloud_gap_filled_snow_cover_extent',
            'passive_microwave_gap_filled_snow_cover_extent',
        ]

        reqvars = reqvars or valids

        for var in reqvars:
            if var not in valids:
                raise RuntimeError("Valid variables are %s (not %s)" % (', '.join(valids), var))

        bbox = [0, 719, 0, 719]

        if bounds:
            row, col = numpy.where(
                (NSIDC0530.__latitude >= bounds['s']) &
                (NSIDC0530.__latitude <= bounds['n']) &
                (NSIDC0530.__longitude >= bounds['w']) &
                (NSIDC0530.__longitude <= bounds['e'])
            )
            bbox = [numpy.min(row), numpy.max(row), numpy.min(col), numpy.max(col)]

        dataset = netCDF4.Dataset(url(reqvars, yyyy, mm, dd, bbox))

        for variable in reqvars:
            setattr(self, variable, numpy.squeeze(dataset.variables[variable])[:, :])

        self.latitude = NSIDC0530.__latitude[bbox[0]:bbox[1]+1, bbox[2]:bbox[3]+1]
        self.longitude = NSIDC0530.__longitude[bbox[0]:bbox[1]+1, bbox[2]:bbox[3]+1]

        self.variables = sorted(reqvars + ['latitude', 'longitude'])
