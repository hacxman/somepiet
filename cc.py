#!/usr/bin/python

# something to piet compiler

import os
import sys
import math
import png

RED = 0
YELLOW = 1
GREEN = 2
CYAN = 3
BLUE = 4
MAGENTA = 5
WHITE = 6
BLACK = 7

LIGHT = 0
NORMAL = 1
DARK = 2

COLORS = {RED: [255, 0, 0],
          YELLOW: [255, 255,0],
          GREEN: [0, 255, 0],
           CYAN: [0, 255, 255],
          BLUE: [0, 0, 255],
          MAGENTA: [255, 0, 255],
          WHITE: [255, 255, 255],
          BLACK: [0, 0, 0]}

class Color(object):
    def __init__(self, hue=None, lightness=None):
        if hue is None:
            self.hue = 0
        if lightness is None:
            self.lightness = 0

        if type(hue) is Color:
            self.hue = hue.hue
            self.lightness = hue.lightness
        else:
            self.hue = hue
            self.lightness = lightness

    def darker(self, step = None):
        if step is None:
            step = 1

        if self.hue in [WHITE, BLACK]:
            return

        self.lightness = (self.lightness + step) % 3

    def huer(self, step = None):
        if step is None:
            step = 1

        if self.hue in [WHITE, BLACK]:
            return

        self.hue = (self.hue + step) % 6

    def to_rgb(self):
        rgb = COLORS[self.hue]
        if self.lightness == 1:
            return rgb
        elif self.lightness == 2:
            return map(lambda x: max(x-63, 0), rgb)
        elif self.lightness == 0:
            return map(lambda x: min(x+192, 255), rgb)


class Instruction(object):
    def __init__(self, color=None):
        self.area = 1
        if color is None:
            self.color = Color()
        self.color = color

class Context(object):
    def __init__(self):
        self.instructions = []
        self.last = None

    def add_isn(self, isn):
        self.instructions.append(isn)
        self.last = isn
#        print 'added', isn.color

    def show(self):
        for i in self.instructions:
            print i
            print '{} {} @ {}sq'.format(i.color.hue, i.color.lightness, i.area)

    def make_image(self, name):
        # compute area
        area = 0
        max_isn_area = 0
        toth = 0
        totw = 0

        for i in self.instructions:
            area += i.area
#            max_isn_area = max(max_isn_area, i.area)
            ih = int(math.ceil(math.sqrt(i.area)))
            iw = int(math.ceil(i.area/float(ih)))
            toth = max(toth, ih)
            totw += iw
        h, w = toth, totw
        #int(math.ceil(1+math.sqrt(max_isn_area))), int(math.ceil((1+math.sqrt(max_isn_area))*len(self.instructions)))

        #create image
        rows = [[[0, 0, 0]] * w for _ in range(h)]
        print area, w, h
#        print rows

        last_col = 0
        for i in self.instructions:
            ih = int(math.ceil(math.sqrt(i.area)))
            iw = int(math.ceil(i.area/float(ih)))
            print 'iw {}, ih {}'.format(iw, ih)
            last_col_size = int(ih - (ih*iw - i.area))

            for x in range(iw):
#                print x, iw-1
                for y in range(last_col_size if x == iw - 1 else ih):
#                    print 'y {}, last_col + x {}'.format(y, last_col+x)
                    rows[y][last_col + x] = i.color.to_rgb()
            last_col = x+last_col+1
            #for r in rows: print r
            print
        from operator import add
        img = [reduce(add, r) for r in rows]
        i = png.from_array(img, 'RGB')
        i.save(name)

def emit_isn(context, hue_change, light_change):
    newcolor = Color(context.last.color)
    newcolor.huer(hue_change)
    newcolor.darker(light_change)
    context.add_isn(Instruction(newcolor))


def emit_add(context):
    emit_isn(context, 1, 0)

def emit_div(context):
    emit_isn(context, 2, 0)

def emit_greater(context):
    emit_isn(context, 3, 0)

def emit_dup(context):
    emit_isn(context, 4, 0)

def emit_in_char(context):
    emit_isn(context, 5, 0)

def emit_push(context):
    emit_isn(context, 0, 1)

def emit_sub(context):
    emit_isn(context, 1, 1)

def emit_mod(context):
    emit_isn(context, 2, 1)

def emit_pointer(context):
    emit_isn(context, 3, 1)

def emit_roll(context):
    emit_isn(context, 4, 1)

def emit_out_number(context):
    emit_isn(context, 5, 1)

def emit_pop(context):
    emit_isn(context, 0, 2)

def emit_mul(context):
    emit_isn(context, 1, 2)

def emit_not(context):
    emit_isn(context, 2, 2)

def emit_switch(context):
    emit_isn(context, 3, 2)

def emit_in_number(context):
    emit_isn(context, 4, 2)

def emit_out_char(context):
    emit_isn(context, 5, 2)

def emit_number(context, number):
    isn = context.last
    if isn is None:
        isn = Instruction(Color(RED, NORMAL)) #TODO make this random
        context.add_isn(isn)
    isn.area = number

def test_emit_push_1_number():
    ctx = Context()
    emit_number(ctx, 10)
    emit_push(ctx)
    ctx.show()

def test_emit_push_2_numbers():
    ctx = Context()
    emit_number(ctx, 10)
    emit_push(ctx)
    emit_number(ctx, 20)
    emit_push(ctx)
    ctx.show()
    ctx.make_image('test_push.png')

def test_emit_print_2_numbers():
    ctx = Context()
    emit_number(ctx, 42)
    emit_push(ctx)
    emit_out_number(ctx)
    emit_number(ctx, 88)
    emit_push(ctx)
    emit_out_number(ctx)
    ctx.show()
    ctx.make_image('test_nums.png')
    os.system('convert test_nums.png -scale 1600% test_nums_resize.png')

    ctx = Context()
    emit_number(ctx, 42)
    emit_push(ctx)
    emit_number(ctx, 88)
    emit_push(ctx)
    emit_out_number(ctx)
    emit_out_number(ctx)
    ctx.show()
    ctx.make_image('test_nums_2.png')
    os.system('convert test_nums_2.png -scale 1600% test_nums_2_resize.png')


def test_print_hello_world():
    ctx = Context()
    def emit_push_num(c, n):
        emit_number(c, n)
        emit_push(c)
    string = reversed('Hello, Piet!')
    map(lambda x: emit_push_num(ctx, ord(x)), string)
    string = reversed('Hello, Piet!')
    map(lambda x: emit_out_char(ctx), string)
    ctx.make_image('test_hello_piet.png')
    os.system('convert test_hello_piet.png -scale 1600% test_hello_piet_resize.png')


def test_print_hello_world_ordered():
    ctx = Context()
    def emit_push_num(c, n):
        emit_number(c, n)
        emit_push(c)
        emit_out_char(ctx)
    string = 'Hello, Piet!'
    map(lambda x: emit_push_num(ctx, ord(x)), string)
    ctx.make_image('test_hello_piet_order.png')
    os.system('convert test_hello_piet_order.png -scale 1600% test_hello_piet_order_resize.png')

tests = [('push 1 number', test_emit_push_1_number),
         ('push 2 numbers', test_emit_push_2_numbers),
         ('print 2 numbers', test_emit_print_2_numbers),
         ('print hello piet', test_print_hello_world),
         ('print hello piet in order', test_print_hello_world_ordered)]

def run_tests():
    for (name, test) in tests:
        print 'testing {}'.format(name)
        test()
        print

def main():
    run_tests()

if __name__ == '__main__':
    main()
 
