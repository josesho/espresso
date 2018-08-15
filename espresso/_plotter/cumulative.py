#!/usr/bin/python
# -*-coding: utf-8 -*-
# Author: Joses Ho
# Email : joseshowh@gmail.com

"""
cumulative plotting functions for espresso objects.
"""



class cumulative_plotter:
    """
    cumulative plotting class for espresso object.
    """


    def __init__(self, plotter): # pass along an espresso_plotter instance.
        self.__feeds = plotter._experiment.feeds.copy()
        self.__expt_end_time = plotter._experiment.expt_duration_minutes


    def __cumulative_plotter(self, yvar, row, col, time_col,
                             start_hour, end_hour,
                             ylim, color_by, font_scale=1.5,
                             height=10, width=10, palette=None,
                             resample_by='5min', gridlines=True):


        import matplotlib.pyplot as plt
        import seaborn as sns
        from . import plot_helpers as plothelp
        from .._munger import munger as munge

        # Not sure at all why scipy throws up warnings?
        import warnings
        warnings.filterwarnings("ignore")

        # Handle the group_by and color_by keywords.
        munge.check_group_by_color_by(col, row, color_by, self.__feeds)

        # Resample (aka bin by time).
        resamp_feeds = munge.groupby_resamp_sum(self.__feeds, resample_by)

        # Perform cumulative summation.
        plotdf = munge.cumsum_for_cumulative(resamp_feeds)


        # Parse keywords.
        if palette is None:
            palette = 'tab10'

        # Convert hour input to seconds.
        min_time_sec = start_hour * 3600
        max_time_sec = end_hour * 3600

        # Filter the cumsum dataframe for the desired time window.
        df_win = plotdf[(plotdf.time_s >= min_time_sec) &
                        (plotdf.time_s <= max_time_sec)]

        # initialise FacetGrid.
        sns.set(style='ticks', context='poster')

        g = sns.FacetGrid(df_win, row=row, col=col,
                          hue=color_by, legend_out=True,
                          palette=palette,
                          xlim=(min_time_sec, max_time_sec),
                          sharex=False, sharey=True,
                          height=height, aspect=width/height,
                          gridspec_kws={'hspace':0.3, 'wspace':0.3}
                          )

        g.map(sns.lineplot, time_col, yvar, ci=95)

        if row is None:
            g.set_titles("{col_var} = {col_name}")
        elif col is None:
            g.set_titles("{row_var} = {row_name}")
        elif row is not None and col is not None:
            g.set_titles("{row_var} = {row_name}\n{col_var} = {col_name}")

        g.add_legend()

        # Aesthetic tweaks.
        for j, ax in enumerate(g.axes.flat):

            plothelp.format_timecourse_xaxis(ax, min_time_sec, max_time_sec)
            ax.tick_params(which='major', length=12, pad=12)
            ax.tick_params(which='minor', length=6)
            ax.set_ylabel(ax.get_ylabel())

            ax.set_ylim(0, ax.get_ylim()[1])
            ax.yaxis.set_tick_params(labelleft=True)

            if gridlines:
                ax.xaxis.grid(True, which='major',
                              linestyle='dotted',
                              alpha=0.75)


        sns.despine(fig=g.fig, offset={'left':5, 'bottom': 5})
        sns.set() # reset style.

        # End and return the FacetGrid.
        return g


    def consumption(self, row, col, color_by,
                    end_hour, start_hour=0,
                    ylim=None, palette=None,
                    resample_by='5min',
                    height=10, width=10,
                    gridlines=True):
        """
        Produces a cumulative line plot depicting the average total volume
        consumed per fly for the entire assay. The plot will be tiled
        horizontally according to the `col`, horizontally according to the
        category `row`, and will be colored according to the category `color_by`.
        Feed volumes will be binned by the duration in `resample_by`.

        keywords
        --------
        col, row: string
            Accepts a categorical column in the espresso object. Each group in
            this column will be plotted on along the desired axis. If None,
            the plots will be arranged in the other orthogonal dimension.

        color_by: string
            Accepts a categorical column in the espresso object. Each group in
            this column will be colored seperately, and stacked as an area plot.

        end_hour, start_hour: float, default <required>, 0
            Enter the time window (in hours) you want to plot here.

        ylim: tuple, default None
            Enter the desired ylims here.

        palette: matplotlib palette OR a list of named matplotlib colors.
            Full list of matplotlib palettes
            https://matplotlib.org/examples/color/colormaps_reference.html
            Full list of named matplotlib colors
            https://matplotlib.org/gallery/color/named_colors.html

        resample_by: string, default '5min'
            The time frequency used to bin the timecourse data. For the format,
            please see
            http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases

        font_scale: float, default 1.5
            The fontsize will be multiplied by this amount.

        height, width: float, default 10, 10
            The height and width of each panel in inches.

        gridlines boolean, default True
            Whether or not vertical gridlines are displayed at each hour.

        Returns
        -------
        seaborn FacetGrid object
        """

        out = self.__cumulative_plotter(yvar='Cumulative Volume (nl)',
                                        col=col,
                                        row=row,
                                        color_by=color_by,
                                        time_col='time_s',
                                        start_hour=start_hour,
                                        end_hour=end_hour,
                                        palette=palette,
                                        resample_by=resample_by,
                                        ylim=ylim, height=height, width=width,
                                        gridlines=gridlines)
        return out


    def feed_count(self, row, col, color_by,
                    end_hour, start_hour=0,
                    ylim=None, palette=None,
                    resample_by='5min', height=10, width=10,
                    gridlines=True):
        """
        Produces a cumulative line plot depicting the average total feed count
        consumed per fly for the entire assay. The plot will be tiled
        horizontally according to the `col`, horizontally according to the
        category `row`, and will be colored according to the category `color_by`.
        Feed counts will be binned by the duration in `resample_by`.

        keywords
        --------
        col, row: string
            Accepts a categorical column in the espresso object. Each group in
            this column will be plotted on along the desired axis.

        color_by: string
            Accepts a categorical column in the espresso object. Each group in
            this column will be colored seperately, and stacked as an area plot.

        end_hour, start_hour: float, default <required>, 0
            Enter the time window (in hours) you want to plot here.

        ylim: tuple, default None
            Enter the desired ylims here.

        palette: matplotlib palette

        resample_by: string, default '5min'
            The time frequency used to bin the timecourse data. For the format,
            please see
            http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases

        font_scale: float, default 1.5
            The fontsize will be multiplied by this amount.

        height, width: float, default 10, 10
            The height and width of each panel in inches.

        gridlines: boolean, default True
            Whether or not vertical gridlines are displayed at each hour.

        Returns
        -------
        seaborn FacetGrid object
        """

        out = self.__cumulative_plotter(yvar='Cumulative Feed Count',
                                        col=col,
                                        row=row,
                                        color_by=color_by,
                                        time_col='time_s',
                                        start_hour=start_hour,
                                        end_hour=end_hour,
                                        palette=palette,
                                        resample_by=resample_by,
                                        ylim=ylim, height=height, width=width,
                                        gridlines=gridlines)
        return out
