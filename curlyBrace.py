# -*- coding: utf-8 -*- 

'''
Module Name : curbrac

Author : 高斯羽 博士 (Dr. GAO, Siyu)

Version : 1.0.1

Last Modified : 2019-04-22

This module is basically an Python implementation of the function written Pål Næverlid Sævik
for Matlab (link in Reference).

The function "curlyBrace" allows you to plot an optionally annotated curly bracket between 
two points when using matplotlib.

The usual settings for line and fonts in matplotlib also applies.

The function takes the axes scales into account automatically. But when the axes aspect is 
set to "equal", the auto switch should be turned off.

Change Log
----------------------
* **Notable changes:**
    + Version : Added considerations for different scaled axes and log scale
    + Version : 1.0.1
        - First version.

Reference
----------------------
https://uk.mathworks.com/matlabcentral/fileexchange/38716-curly-brace-annotation

Definitions
----------------------

'''

import matplotlib.pyplot as plt
import numpy as np

def getAxSize(fig, ax):
    '''
    .. _getAxSize :

    Get the axes size in pixels.

    Parameters
    ----------
    fig : matplotlib figure object
        The of the target axes.

    ax : matplotlib axes object
        The target axes.

    Returns
    -------
    ax_width : float
        The axes width in pixels.

    ax_height : float
        The axes height in pixels.

    Reference
    --------
    https://stackoverflow.com/questions/19306510/determine-matplotlib-axis-size-in-pixels
    '''

    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    ax_width, ax_height = bbox.width, bbox.height
    ax_width *= fig.dpi
    ax_height *= fig.dpi

    return ax_width, ax_height

def curlyBrace(fig, ax, p1, p2, k_r=0.1, bool_auto=True, str_text='', int_line_num=2, fontdict={}, **kwargs):
# def curlyBrace(fig, ax, p1, p2, k_r=0.1, bool_auto=True, str_text='', int_line_num=2, fontdict={}, **kwargs):
    '''
    .. _curlyBrace :

    Plot an optionally annotated curly bracket on the given axes of the given figure.

    Note that the brackets are anti-clockwise by default. To reverse the text position, swap
    "p1" and "p2".

    Note that, when the axes aspect is not set to "equal", the axes coordinates need to be
    transformed to screen coordinates, otherwise the arcs may not be seeable. 

    Parameters
    ----------
    fig : matplotlib figure object
        The of the target axes.

    ax : matplotlib axes object
        The target axes.

    p1 : two element numeric list
        The coordinates of the starting point.

    p2 : two element numeric list
        The coordinates of the end point.

    k_r : float
        This is the gain controlling how "curvy" and "pointy" the bracket is.

        Note that, if this gain is too big, the bracket would be very strange.

    bool_auto : boolean
        This is a switch controlling wether to use the auto calculation of axes
        scales.

        When the two axes do not have the same aspects, i.e., not "equal" scales,
        this should be turned on, i.e., True.

        When "equal" aspect is used, this should be turned off, i.e., False.

        If you do not set this to False when setting the axes aspect to "equal",
        the bracket will be in funny shape.

        Default = True

    str_text : string
        The annotation text of the bracket. It would displayed at the mid point
        of bracket with the same rotation as the bracket.

        By default, it follows the anti-clockwise convention. To flip it, swap 
        the end point and the starting point.

        The appearance of this string can be set by using "fontdict", which follows
        the same syntax as the normal matplotlib syntax for font dictionary.

        Default = empty string (no annotation)

    int_line_num : int
        This argument determines how many lines the string annotation is from the summit
        of the bracket.

        The distance would be affected by the font size, since it basically just a number
        lines to the given string.

        Default = 2

    fontdict : dictionary
        This is font dictionary setting the string annotation. It is the same as normal
        matplotlib font dictionary.

        Default = empty dict

    **kwargs : matplotlib line setting arguments
        This allows the user to set the line arguments using named arguments that are
        the same as in matplotlib.

    Returns
    -------
    theta : float
        The bracket angle in radians.

    summit : list
        The positions of the bracket summit.

    arc1 : list of lists
        arc1 positions.

    arc2 : list of lists
        arc2 positions.

    arc3 : list of lists
        arc3 positions.

    arc4 : list of lists
        arc4 positions.


    Reference
    --------
    https://uk.mathworks.com/matlabcentral/fileexchange/38716-curly-brace-annotation
    '''

    pt1 = [None, None]
    pt2 = [None, None]

    ax_width, ax_height = getAxSize(fig, ax)

    ax_xlim = ax.get_xlim()
    ax_ylim = ax.get_ylim()

    # log scale consideration
    if 'log' in ax.get_xaxis().get_scale():

        pt1[0] = np.log(p1[0])

        pt2[0] = np.log(p2[0])

        ax_xlim = np.log(ax_xlim)

    else:

        pt1[0] = p1[0]
        pt2[0] = p2[0]

    if 'log' in ax.get_yaxis().get_scale():

        pt1[1] = np.log(p1[1])

        pt2[1] = np.log(p2[1])

        ax_ylim = np.log(ax_ylim)

    else:

        pt1[1] = p1[1]
        pt2[1] = p2[1]

    # get the ratio of pixels/length
    xscale = ax_width / (ax_xlim[1] - ax_xlim[0])
    yscale = ax_height / (ax_ylim[1] - ax_ylim[0])

    # this is to deal with 'equal' axes aspects
    if bool_auto:

        pass

    else:

        xscale = 1.0
        yscale = 1.0

    # convert length to pixels, 
    # need to minus the lower limit to move the points back to the origin. Then add the limits back on end.
    pt1[0] = (pt1[0] - ax_xlim[0]) * xscale
    pt1[1] = (pt1[1] - ax_ylim[0]) * yscale
    pt2[0] = (pt2[0] - ax_xlim[0]) * xscale
    pt2[1] = (pt2[1] - ax_ylim[0]) * yscale

    # calculate the angle
    theta = np.arctan2(pt2[1] - pt1[1], pt2[0] - pt1[0])

    # calculate the radius of the arcs
    r = np.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1]) * k_r

    # arc1 centre
    x11 = pt1[0] + r * np.cos(theta)
    y11 = pt1[1] + r * np.sin(theta)

    # arc2 centre
    x22 = (pt2[0] + pt1[0]) / 2.0 - 2.0 * r * np.sin(theta) - r * np.cos(theta)
    y22 = (pt2[1] + pt1[1]) / 2.0 + 2.0 * r * np.cos(theta) - r * np.sin(theta)

    # arc3 centre
    x33 = (pt2[0] + pt1[0]) / 2.0 - 2.0 * r * np.sin(theta) + r * np.cos(theta)
    y33 = (pt2[1] + pt1[1]) / 2.0 + 2.0 * r * np.cos(theta) + r * np.sin(theta)

    # arc4 centre
    x44 = pt2[0] - r * np.cos(theta)
    y44 = pt2[1] - r * np.sin(theta)

    # prepare the rotated
    q = np.linspace(theta, theta + np.pi/2.0, 50)

    # reverse q
    # t = np.flip(q) # this command is not supported by lower version of numpy
    t = q[::-1]

    # arc coordinates
    arc1x = r * np.cos(t + np.pi/2.0) + x11
    arc1y = r * np.sin(t + np.pi/2.0) + y11

    arc2x = r * np.cos(q - np.pi/2.0) + x22
    arc2y = r * np.sin(q - np.pi/2.0) + y22

    arc3x = r * np.cos(q + np.pi) + x33
    arc3y = r * np.sin(q + np.pi) + y33

    arc4x = r * np.cos(t) + x44
    arc4y = r * np.sin(t) + y44

    # convert back to the axis coordinates
    arc1x = arc1x / xscale + ax_xlim[0]
    arc2x = arc2x / xscale + ax_xlim[0]
    arc3x = arc3x / xscale + ax_xlim[0]
    arc4x = arc4x / xscale + ax_xlim[0]

    arc1y = arc1y / yscale + ax_ylim[0]
    arc2y = arc2y / yscale + ax_ylim[0]
    arc3y = arc3y / yscale + ax_ylim[0]
    arc4y = arc4y / yscale + ax_ylim[0]

    # log scale consideration
    if 'log' in ax.get_xaxis().get_scale():

        arc1x = np.exp(arc1x)
        arc2x = np.exp(arc2x)
        arc3x = np.exp(arc3x)
        arc4x = np.exp(arc4x)

    else:

        pass

    if 'log' in ax.get_yaxis().get_scale():

        arc1y = np.exp(arc1y)
        arc2y = np.exp(arc2y)
        arc3y = np.exp(arc3y)
        arc4y = np.exp(arc4y)

    else:

        pass

    # plot arcs
    ax.plot(arc1x, arc1y, **kwargs)
    ax.plot(arc2x, arc2y, **kwargs)
    ax.plot(arc3x, arc3y, **kwargs)
    ax.plot(arc4x, arc4y, **kwargs)

    # plot lines
    ax.plot([arc1x[-1], arc2x[1]], [arc1y[-1], arc2y[1]], **kwargs)
    ax.plot([arc3x[-1], arc4x[1]], [arc3y[-1], arc4y[1]], **kwargs)

    summit = [arc2x[-1], arc2y[-1]]

    if str_text:

        int_line_num = int(int_line_num)

        str_temp = '\n' * int_line_num
        
        # convert radians to degree and within 0 to 360
        ang = np.degrees(theta) % 360.0

        if (ang >= 0.0) and (ang <= 90.0):

            rotation = ang

            str_text = str_text + str_temp

        if (ang > 90.0) and (ang < 270.0):

            rotation = ang + 180.0

            str_text = str_temp + str_text

        elif (ang >= 270.0) and (ang <= 360.0):

            rotation = ang

            str_text = str_text + str_temp

        ax.axes.text(arc2x[-1], arc2y[-1], str_text, ha='center', va='center', rotation=rotation, fontdict=fontdict)

    else:

        pass

    arc1 = [arc1x, arc1y]
    arc2 = [arc2x, arc2y]
    arc3 = [arc3x, arc3y]
    arc4 = [arc4x, arc4y]

    return theta, summit, arc1, arc2, arc3, arc4