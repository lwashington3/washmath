from ..tools import superscript
from ..stats.statlist import StatList
from ..stats.lsr import Least_Squares_Regression as LSR
from colors import Color, Colors, convert_color
from io import StringIO
from re import sub
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


colors = Colors()


def format_file(file:str, text_columns:tuple[int]=None) -> StringIO:
	with open(file, 'r') as f:
		data = f.readlines()
	for i in range(1, len(data)):
		if text_columns is None:
			data[i] = sub("[^\\dE,.-]", "", data[i]) + "\n"  # I'm having it keep e because a number may be 0.##E-9
		else:
			row = data[i].split(",")
			for j in range(len(row)):
				contains = text_columns == j if isinstance(text_columns, int) else j in text_columns
				if not contains:
					row[j] = sub("[^\\dE,.-]", "", row[j])  # [^0-9,.-]
			data[i] = ",".join(row) + "\n"
	return StringIO("".join(data))


def map_sheet_colors(groups:list, start=0, rgb_format=True) -> dict:
	dct = {}
	i = start
	for group in groups:
		dct[group] = Colors.GOOGLE_SHEETS[i]
		if rgb_format:
			dct[group] = dct[group].get_rgba()
		i += 1
	return dct


def read_csv(file:str, remove_formatting=True, index="Trial #", text_columns=None) -> pd.DataFrame:
	"""

	:param str file: The file that contains the raw data.
	:param bool remove_formatting: Whether the number formatting should be removed.
	:param str index: The column name that should be set as the index
	:param tuple[int] text_columns: The columns that contain strings and should not be converted to numbers. The first column is 0, second column 1, etc.
	"""
	if remove_formatting:
		file = format_file(file, text_columns)
	df = pd.read_csv(file).set_index(index)
	del file
	return df


def graph(df:pd.DataFrame, x_column:str, y_column:str, x_unit:str="", y_unit:str="", **kwargs) -> LSR:
	"""
	A function made to quickly graph data from IIT's PHYS 123 and 221 labs
	:param pd.DataFrame df: The dataframe holding the necessary data
	:param str x_column: The column name the independent values are stored in
	:param str y_column: The column name the dependent values are stored in
	:param str x_unit: The unit of the independent variable for labels
	:param str y_unit: The unit of the dependent variable for labels
	:param str slope_unit: The unit of the slope.
	:param str or Color scatter_color: The color of the scatter plot
	:param str or Color text_color: The color for any text and the axes. Legend label colors excluded.
	:param str or Color line_color: The color of the line of best fit for the data.
	:param str save: The location to save the image. Default is None which will not save the graph.
	:param bool transparent: Whether the graph should have no background when it is saved. Default is true.
	:param fancybox:
	:param capsize: The size of the caps for standard deviation caps. Default is 8.
	:param framealpha: The transparency of the box around the legened.
	:param str scatter_marker: The marker format for the scatter plot
	:param str line_format: The marker format for the line of best fit
	:param str error_format: The format for the error bar. Look at the documentation of matplotlib formats for possible values.
	:param str watermark: The file location of the image you want to watermark
	:param tuple figsize: The size in inches of the image. (width, height). Default is (12, 8).
	:param markersize:
	:param str x_deviation: The type of deviation to put parallel to the x-axis. The given variable MUST be the exact attribute in LSR. Recommended values "standard_deviation" or "standard_error"
	:param str y_deviation: The type of deviation to put parallel to the y-axis. The given variable MUST be the exact attribute in LSR. Recommended values "standard_deviation" or "standard_error"
	:param bool barsabove: Whether the error bars should be on top of the data point.
	:param str legend_loc: The location of the legend on the graph. Check matplotlib's documentation for what the possible values are.
	:param str groupby: The column in the dataframe that should be used to group data points by color
	:param dict or list group_colors: The collection of colors each group should use. If not provided, the system will automatically generate them using colors from Google Sheets.
	:param str groupby_unit: The unit of the groups
	:param np.ndarray xticks: The ticks along the x-axis
	:param np.ndarray yticks: The ticks along the y-axis
	:param tuple xlim: The lower and upper limits of the x-axis, even if xticks extends beyond these values, they will be cut off.
	:param tuple ylim: The lower and upper limits of the y-axis, even if yticks extends beyond these values, they will be cut off.
	:param float x_spacing: The spacing between the ticks on the x-axis. Can be None if xticks is defined.
	:param float y_spacing: The spacing between the ticks on the y-axis. Can be None if yticks is defined.
	:param str style:
	:param bool gridlines: Controls if the grid lines are shown or not.
	:param bool auto_superscript: Whether the function should automatically turn strings into exponents if they have a carat. Default is True.
	:return: The line on the graph
	:rtype: LSR
	"""
	auto_superscript = kwargs.get("auto_superscript", False)
	if auto_superscript:
		x = StatList(df[x_column], title=f"{superscript(x_column)} ({superscript(x_unit)})")
		y = StatList(df[y_column], title=f"{superscript(y_column)} ({superscript(y_unit)})")
		slope_unit = " " + superscript(kwargs["slope_unit"]) if "slope_unit" in kwargs else ""
	else:
		x = StatList(df[x_column], title=f"x_column (x_unit)")
		y = StatList(df[y_column], title=f"y_column (y_unit)")
		slope_unit = " " + kwargs["slope_unit"] if "slope_unit" in kwargs else ""

	background_color = convert_color(kwargs.get("background_color", colors.WHITE))
	face_color = convert_color(kwargs.get("face_color", background_color))
	text_color = kwargs.get("text_color", None)
	if text_color is None:
		text_color = colors.WHITE if Color(rgba=background_color).is_dark else colors.BLACK
	text_color = convert_color(text_color)

	scatter_color = convert_color(kwargs.get("scatter_color", colors.GOOGLE_SHEETS[0]))
	line_color = convert_color(kwargs.get("line_color", colors.GOOGLE_SHEETS[1]))

	scatter_marker = kwargs.get("scatter_marker", "o")
	error_format = kwargs.get("error_format", "o")
	capsize = kwargs.get("capsize", 8)
	barsabove = kwargs.get("barsabove", False)
	markersize = kwargs.get("markersize", 0)
	x_spacing = kwargs.get("x_spacing", .03)
	y_spacing = kwargs.get("y_spacing", .03)
	xerr = getattr(x, kwargs["x_deviation"]) if "x_deviation" in kwargs.keys() else None
	yerr = getattr(y, kwargs["y_deviation"]) if "y_deviation" in kwargs.keys() else None

	title_prefix = kwargs.get("title_prefix", "")
	title_suffix = kwargs.get("title_suffix", "")
	point_alpha = kwargs.get("point_alpha", 1)
	line_alpha = kwargs.get("line_alpha", 1)

	xtick_rotation = kwargs.get("xtick_rotation", 0)
	ytick_rotation = kwargs.get("ytick_rotation", 0)

	plt.style.use(kwargs.get("style", "_mpl-gallery"))
	fig = plt.figure(figsize=kwargs.get("figsize", (12,8)), facecolor=background_color)

	ax = fig.add_subplot()
	ax.xaxis.label.set_color(text_color)
	ax.yaxis.label.set_color(text_color)

	for direction in ("x", "y"):
		ax.tick_params(axis=direction, colors=text_color)

	for direction in ("top", "left", "right", "bottom"):
		ax.spines[direction].set_color(text_color)

	if "groupby" in kwargs.keys():
		groupby = kwargs["groupby"]
		if "group_colors" not in kwargs.keys():
			group_colors = map_sheet_colors(df[groupby].unique())
		else:
			group_colors = kwargs["group_colors"]
			for key in group_colors.keys():
				if isinstance(group_colors[key], Color):
					group_colors[key] = group_colors[key].get_rgba()

		scatter_color = df[groupby].map(group_colors)

	if "groupby" not in kwargs.keys():
		ax.scatter(x, y, color=scatter_color, marker=scatter_marker, alpha=point_alpha)
	else:
		data_groups = [df[df[groupby] == key] for key, group in df.groupby(groupby)]
		for group in data_groups:
			key = group[groupby].iloc[0]
			if auto_superscript:
				groupby_unit = f" {superscript(kwargs['groupby_unit'])}" if "groupby_unit" in kwargs.keys() else ""
			else:
				groupby_unit = f" {kwargs['groupby_unit']}" if "groupby_unit" in kwargs.keys() else ""
			ax.scatter(group[x_column], group[y_column], label=f"{groupby} ({key}{groupby_unit})",
					   color=group_colors[key], marker=scatter_marker, alpha=point_alpha)

	if "xticks" in kwargs.keys():
		ax.set_xticks(kwargs["xticks"])
	if "yticks" in kwargs.keys():
		ax.set_yticks(kwargs["yticks"])
	ax.set_facecolor(face_color)

	# TODO: Add minor gridlines/ticks
	# ax.minorticks_on()
	# ax.grid(True, which="minor", alpha=.2)

	if "xlim" in kwargs.keys():
		ax.set_xlim(kwargs["xlim"][0], kwargs["xlim"][1])
	elif "x_deviation" in kwargs.keys():
		ax.set_xlim(np.floor(min(x) - xerr), np.ceil(max(x) + xerr))
	else:
		ax.set_xlim(np.floor(min(x)), np.ceil(max(x)))

	if "ylim" in kwargs.keys():
		ax.set_ylim(kwargs["ylim"][0], kwargs["ylim"][1])
	elif "y_deviation" in kwargs.keys():
		ax.set_ylim(np.floor(min(y) - yerr), np.ceil(max(y) + yerr))
	else:
		ax.set_ylim(np.floor(min(y)), np.ceil(max(y)))

	possible_values = np.arange(ax.get_xlim()[0], ax.get_xlim()[1] + x_spacing, x_spacing)
	line = LSR(x, y)

	if xerr is not None or yerr is not None:
		if "groupby" not in kwargs.keys():
			ax.errorbar(x, y, xerr=xerr, yerr=yerr,
						fmt=error_format, ecolor=scatter_color, capsize=capsize,
						barsabove=barsabove, ms=markersize)
		else:
			for group in data_groups:
				key = group[groupby].iloc[0]
				ax.errorbar(group[x_column], group[y_column], xerr=xerr, yerr=yerr, fmt=error_format,
							ecolor=group_colors[key], capsize=capsize, barsabove=barsabove, ms=markersize)

	ax.plot(possible_values, [line.predict(i) for i in possible_values],
			kwargs.get("line_format", "-"),
			label=f"Slope: {line.slope:.6}{slope_unit}\nY-Intercept: {line.y_intercept:.6} {y_unit}\n$R^{2}$: {line.r_squared:.6}",
			color=line_color, alpha=line_alpha)

	ax.set_xlabel(x.title, color=text_color)
	ax.set_ylabel(y.title, color=text_color)

	title = f"{x.title} vs {y.title}"
	if title_prefix:
		title = title_prefix + " " + title
	if title_suffix:
		title += " " + title_suffix

	fig.suptitle(title, color=text_color)
	if "subtitle" in kwargs.keys():
		ax.set_title(kwargs["subtitle"], color=text_color)

	ax.tick_params(axis="x", rotation=xtick_rotation)
	ax.tick_params(axis="y", rotation=ytick_rotation)

	ax.legend(fancybox=kwargs.get("fancybox", True),
			  framealpha=kwargs.get("framealpha", 0),
			  loc=kwargs.get("legend_loc", "best"),
			  labelcolor=text_color)

	watermark = kwargs.get("watermark", None)
	if watermark is not None:
		from matplotlib import image, cbook
		with cbook.get_sample_data(watermark) as file:
			im = image.imread(file)
		fig.figimage(im,
					 kwargs.get("waterx", 10), kwargs.get("watery", 10), zorder=kwargs.get("zorder", 3),
					 alpha=kwargs.get("watermark_alpha", .5), resize=kwargs.get("watermark_resize", False))

	if not kwargs.get("gridlines", True):
		plt.grid(b=False)
	plt.tight_layout()
	if "save" in kwargs.keys():
		plt.savefig(kwargs["save"], transparent=kwargs.get("transparent", True))
	plt.show()
	return line
