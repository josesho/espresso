#!/usr/bin/python
# -*-coding: utf-8 -*-
# Author: Joses Ho
# Email : joseshowh@gmail.com

"""
timecourse plot functions for espresso objects.
"""

 #      # #####  #####    ##   #####  #   #    # #    # #####   ####  #####  #####
 #      # #    # #    #  #  #  #    #  # #     # ##  ## #    # #    # #    #   #
 #      # #####  #    # #    # #    #   #      # # ## # #    # #    # #    #   #
 #      # #    # #####  ###### #####    #      # #    # #####  #    # #####    #
 #      # #    # #   #  #    # #   #    #      # #    # #      #    # #   #    #
 ###### # #####  #    # #    # #    #   #      # #    # #       ####  #    #   #

import sys as _sys
_sys.path.append("..") # so we can import espresso from the directory above.

import os as _os

import numpy as _np
import scipy as _sp
import pandas as _pd

import matplotlib as _mpl
import matplotlib.pyplot as _plt
import matplotlib.ticker as _tk

import seaborn as _sns
import bootstrap_contrast as _bsc

from . import plot_helpers as _plot_helpers
from _munger import munger as _munger

class timecourse_plotter():
    """
    timecourse plotting class for espresso object.
    """

    #    #    #    #    #####
    #    ##   #    #      #
    #    # #  #    #      #
    #    #  # #    #      #
    #    #   ##    #      #
    #    #    #    #      #

    def __init__(self,plotter): # pass along an espresso_plotter instance.
        self.__feeds=plotter._experiment.feeds.copy()

    def __pivot_for_plot(self,resampdf,group_by,color_by):
        return _pd.DataFrame( resampdf.groupby([group_by,
                                                color_by,
                                                'feed_time_s']).sum().to_records() )

    def feed_volume(self,
                    group_by=None,
                    color_by=None,
                    resample_by='10min',
                    fig_size=None,
                    gridlines_major=True,
                    gridlines_minor=True,
                    ax=None):
        """
        Produces a timecourse area plot depicting the feed volume for the entire assay.
        The plot will be tiled horizontally according to the category "group_by", and
        will be stacked and colored according to the category "color_by".
        feed volumes will be binned by the duration in `resample_by`.

        keywords
        --------
        TBA

        Returns
        -------
        A matplotlib Figure.
        """
        # Handle the group_by and color_by keywords.
        if group_by is None:
            group_by="Genotype"
        else:
            _munger.check_column(group_by, self.__feeds)
        if color_by is None:
            color_by='FoodChoice'
        else:
            _munger.check_column(color_by, self.__feeds)

        resampdf=_munger.groupby_resamp(self.__feeds, group_by, color_by, resample_by)
        plotdf=self.__pivot_for_plot(resampdf,group_by,color_by)

        groupby_grps=_np.sort( plotdf[group_by].unique() )
        num_plots=int( len(groupby_grps) )

        # Initialise figure.
        _sns.set(style='ticks',context='poster')
        if fig_size is None:
            x_inches=10*num_plots
            y_inches=7
        else:
            if isinstance(fig_size, tuple) or isinstance(fig_size, list):
                x_inches=fig_size[0]
                y_inches=fig_size[1]
            else:
                raise ValueError('Please make sure figsize is a tuple of the form (w,h) in inches.')

        groupby_grps=_np.sort( plotdf[group_by].unique() )
        num_plots=int( len(groupby_grps) )

        if ax is None:
            fig,axx=_plt.subplots(nrows=1,
                                  ncols=num_plots,
                                  figsize=(x_inches,y_inches),
                                  gridspec_kw={'wspace':0.2} )
        else:
            axx=ax

        # Loop through each panel.
        for c, grp in enumerate( groupby_grps ):
            if len(groupby_grps)>1:
                plotax=axx[c]
            else:
                plotax=axx

            ## Plot the raster plots.
            ### Plot vertical grid lines if desired.
            if gridlines_major:
                plotax.xaxis.grid(True,linestyle='dotted',which='major',alpha=1)
            if gridlines_minor:
                plotax.xaxis.grid(True,linestyle='dotted',which='minor',alpha=0.5)
                ## Filter plotdf according to group_by.
                temp_plotdf=plotdf[plotdf[group_by]==grp]
                temp_plotdf_pivot=temp_plotdf.pivot(index='feed_time_s',
                                                     columns=color_by,
                                                     values='AverageFeedVolumePerFly_µl')

                ### and make area plot.
                temp_plotdf_pivot.plot.area(ax=plotax,lw=1)
            ## Format x-axis.
            _plot_helpers.format_timecourse_xaxis(plotax)

        # Normalize all the y-axis limits.
        if len(groupby_grps)>1:
            _plot_helpers.normalize_ylims(axx)

        _sns.despine(ax=ax,left=True,bottom=True,trim=True)
        # End and return the figure.
        if ax is None:
            return fig


    # def feed_count(self,
    #                 group_by=None,
    #                 color_by=None,
    #                 resample_by='10min',
    #                 fig_size=None):
    #     """
    #     Produces a timecourse area plot depicting the feed volume for the entire assay.
    #     The plot will be tiled horizontally according to the category "group_by", and
    #     will be stacked and colored according to the category "color_by".
    #     feed volumes will be binned by the duration in `resample_by`.
    #
    #     keywords
    #     --------
    #     TBA
    #
    #     Returns
    #     -------
    #     A matplotlib Figure.
    #     """
    #
    #     resampdf=_munger.groupby_resamp(self.__feeds, group_by, color_by, resample_by)
    #     plotdf=self.__pivot_for_plot()
