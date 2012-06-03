#!/usr/bin/env python2
# -*- coding: utf-8

from key import *

tint_map = {
    "*": (255,128,64),
    "A": (157,243,72),
    "C": (176,52,50),
    "B": (128,0,0),
    "E": (238,167,51),
    "D": (127,129,0),
    "G": (0,128,131),
    "F": (0,128,1),
    "J": (1,0,128),
    "K": (129,0,127),
    "H": (197,89,211),
    "I": (88,89,21),
    "N": (255,0,134),
    "O": (87,100,129),
    "L": (127,255,254),
    "M": (132,63,0),
    "R": (0,254,129),
    "S": (0,255,0),
    "P": (0,127,255),
    "Q": (82,15,82),
    "V": (255,255,128),
    "W": (242,106,191),
    "T": (127,0,253),
    "U": (188,243,237),
    "Z": (255,0,0),
    "X": (255,255,0),
    "Y": (115,44,174),
    "control": (170,180,190),
    }

color_groups=[
    (set(["K", "W", "S-", "P-", "T-"]), "Z"),
    (set(["K", "W", "P-", "T-"]), "G"),
    (set(["B", "G", "L", "-P"]), "J"),
    (set(["B", "G", "L", "-P"]), "J"),
    (set(["B", "G", "-R", "-S"]), "control"),
    (set(["F", "L", "-P", "-T"]), "control"),
    (set(["H", "P-", "T-"]), "N"),
    (set(["K", "W", "R-"]), "Y"),
    (set(["B", "G", "-S"]), "X"),
    (set(["K", "P-"]), "X"),
    (set(["S-", "R-"]), "V"),
    (set(["K", "W"]), "Q"),
    (set(["E", "U"]), "I"),
    (set(["K", "R-"]), "C"),
    (set(["B", "-P"]), "N"),
    (set(["L", "-P"]), "M"),
    (set(["H", "P-"]), "M"),
    (set(["H", "R-"]), "L"),
    (set(["K", "T-"]), "D"),
    (set(["W", "P-"]), "B"),
    (set(["P-", "T-"]), "F"),
    (set(["B", "G"]), "K"),
    (set(["W"]), "W"),
    (set(["U"]), "U"),
    (set(["O"]), "O"),
    (set(["H"]), "H"),
    (set(["E"]), "E"),
    (set(["A"]), "A"),
    (set(["Z"]), "Z"),
    (set(["F"]), "V"),
    (set(["L"]), "L"),
    (set(["K"]), "K"),
    (set(["G"]), "G"),
    (set(["F"]), "F"),
    (set(["B"]), "B"),
    (set(["R-"]), "R"),
    (set(["D"]), "D"),
    (set(["-R"]), "R"),
    (set(["P-"]), "P"),
    (set(["-P"]), "P"),
    (set(["T-"]), "T"),
    (set(["-T"]), "T"),
    (set(["S-"]), "S"),
    (set(["-S"]), "S"),
    (set(["*"]), "*"),
    ]

def pick_letter(ltr):
    return ltr.replace("-","")
def pick_bold(ltr,keys):
    return ltr in keys
def pick_lettercolor(ltr,keys):
    return (1,1,1) if ltr in keys or len(keys)==0 else (0.5,.5,.5)
def pick_color(base,ltr,keys):
    keys = set(keys)
    for (s, choice) in color_groups:
        if s.issubset(keys):
            if ltr in s:
                r,g,b = tint_map[choice]
                return (r/255., g/255., b/255.)
            keys = keys - s
    return base

def draw_keyboard(ctx, keys):
    base_color = (.06,.06,.06)
    def b(ltr, width=60,height=100):
        return lambda: draw_key(ctx, round_shape,
                                pick_color(base_color,ltr,keys),
                                pick_letter(ltr),
                                pick_lettercolor(ltr,keys),
                                pick_bold(ltr,keys), width, height)
    def t(ltr, width=60,height=100):
        return lambda: draw_key(ctx, rect_shape,
                                pick_color(base_color,ltr,keys),
                                pick_letter(ltr),
                                pick_lettercolor(ltr,keys),
                                pick_bold(ltr,keys), width, height)
    #ugh, i have to manually position it.
    # :( :( :(
    x=60 + 20
    r=4*x + 80 + 20
    l = 100 + 10

    v = l*2
    for pos, key in {
        (0*x,0): b("S-", height=210),
        (1*x,0): t("T-"),
        (2*x,0): t("P-"),
        (3*x,0): t("H"),
        (4*x,0): b("*",width=80,height=210),
        (r+0*x,0): t("F"),
        (r+1*x,0): t("-P"),
        (r+2*x,0): t("L"),
        (r+3*x,0): t("-T"),
        (r+4*x,0): t("D"),

        # Bottom
        (x*1,l): b("K"),
        (x*2,l): b("W"),
        (x*3,l): b("R-"),
        (x*0+r,l): b("-R"),
        (x*1+r,l): b("B"),
        (x*2+r,l): b("G"),
        (x*3+r,l): b("-S"),
        (x*4+r,l): b("Z"),

        # Vowels
        (x*2+30, v): b("A"),
        (x*3+20, v): b("O"),
        (x*5-00, v): b("E"),
        (x*6-10, v): b("U"),

        }.items():
        ctx.save()
        ctx.translate(*pos)
        key()
        ctx.restore()

def draw_keyboard_to_ctx(ctx, keys, scale=1):
    ctx.set_source_rgba(1,1,1,0)
    ctx.paint()
    ctx.scale(scale,scale)
    ctx.translate(10,10)
    draw_keyboard(ctx, keys)

def draw_keyboard_to_png(keys, file, scale=1):
    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32,
                                  int(scale*825),
                                  int(scale*340))
    ctx = cairo.Context (surface)
    ctx.scale(scale,scale)
    draw_keyboard_to_ctx(ctx, keys, scale=1)
    surface.write_to_png(file)

#draw_keyboard_to_png(["K","W","R-"], "test.png")
