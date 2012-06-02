#!/usr/bin/env python2
# -*- coding: utf-8

import cairo

def blend(a, scale, b):
    """
    Returns a color 'scale' of the way between 'a' and 'b'.
    """
    ar,ag,ab = a
    br,bg,bb = b
    return (min(255, max(0, br- (br-ar)*(1-scale))),
            min(255, max(0, bg- (bg-ag)*(1-scale))),
            min(255, max(0, bb- (bb-ab)*(1-scale))))

def rect_shape(ctx, inset, width,height):
    ctx.rectangle(inset,inset,  width-inset-inset, height-inset-inset)
    ctx.fill()

def round_shape(ctx, inset, width,height):
    """
    Draws a key at 0,0 with the given inset
    and fill.
    """
    right = width-inset
    bottom_edge = height - 20 - inset*0.7
    ctl_point_length = 20 - inset/2
    ctx.move_to(inset, bottom_edge)
    ctx.line_to(inset,inset)
    ctx.line_to(right,inset)
    ctx.line_to(right,bottom_edge)
    ctx.curve_to(right-ctl_point_length, bottom_edge+ctl_point_length,
                 inset+ctl_point_length, bottom_edge+ctl_point_length,
                 inset, bottom_edge)
    ctx.close_path()
    ctx.fill()

def draw_key_base(ctx, shape, base_color, width=60, height=100):
    """
    Draw a key shape at 0,0 with the given base color, width, and
    height.
    """
    # Dark border on outside
    ctx.set_source_rgb(*blend((0,0,0), 0.7, base_color))
    shape(ctx, 0, width, height)
    hilight = cairo.RadialGradient(0,height,0,  0,height,height)
    hilight.add_color_stop_rgb(1, *base_color)
    hilight.add_color_stop_rgb(0, *blend((1,1,1), 0.7,base_color))
    ctx.set_source(hilight)
    shape(ctx, 4, width,height)
    bg = cairo.LinearGradient(0,0, width,0)
    bg.add_color_stop_rgb(0, *base_color)
    bg.add_color_stop_rgb(1, *blend((1,1,1), 0.85, base_color))
    ctx.set_source(bg)
    shape(ctx, 4+4, width,height)

def draw_key(ctx, shape, base_color, letter, lettercolor, bold, width=60, height=100):
    """
    Draw a key with the given letter.
    """
    draw_key_base(ctx,shape,base_color,width,height)
    ctx.set_font_size(50)
    xb, yb, w, h, _, _, = ctx.text_extents(letter)
    ctx.move_to((width-w)/2 - xb, (height-h)/2-yb-7)
    ctx.set_line_width(8)
    ctx.set_source_rgb(*base_color)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.select_font_face("", 0, cairo.FONT_WEIGHT_BOLD if bold else 0)
    ctx.text_path(letter)
    ctx.stroke()
    ctx.move_to((width-w)/2 - xb, (height-h)/2-yb-8)
    ctx.text_path(letter)
    ctx.set_source_rgb(*lettercolor)
    ctx.fill()
    #ctx.stroke()

if __name__ == "__main__":
    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, 400, 300)
    ctx = cairo.Context (surface)
    ctx.set_source_rgb(1,1,1)
    ctx.paint()

    ctx.translate(10,10)
    draw_key(ctx, round_shape, (.1,.2,.3), "B", (1,1,1), False, width=60, height=100)


    surface.write_to_png("test.png")
