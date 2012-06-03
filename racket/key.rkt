#lang racket

(require racket/gui
         racket/draw
         slideshow/pict
         unstable/gui/pict)
(provide tkey bkey)

(define *border* 4)

(define (clip-color x)
  (min 255 (max 0 x)))
(define (blend a scale b)
  (cond
   [(list? a)
    (blend (apply make-object color% a) scale b)]
   [(list? b)
    (blend a scale (apply make-object color% b))]
   [else
    (define (alpha a1 b1)
      (clip-color (- b1 (inexact->exact (round (* (- b1 a1)
                                                  (- 1 scale)))))))
    (make-object color%
                 (alpha (send a red) (send b red))
                 (alpha (send a green) (send b green))
                 (alpha (send a blue) (send b blue)))]))

(define (rect-shape inset width height)
  (define path (new dc-path%))
  (send path rectangle inset inset
        (- width inset inset)
        (- height inset inset))
  path)

(define (round-key-shape inset width height)
  (define path (new dc-path%))
  (define right (- width inset))
  (define bottom-edge (- height 20 (* 0.7 inset)))
  (define ctl-pt-len (- 20 (* 0.5 inset)))
  (send path move-to inset bottom-edge)
  (send path lines (list (cons inset inset)
                         (cons right inset)
                         (cons right bottom-edge)))
  (send path curve-to (- right ctl-pt-len) (+ bottom-edge ctl-pt-len)
                      (+ inset ctl-pt-len) (+ bottom-edge ctl-pt-len)
                      inset        bottom-edge)
  (send path close)
  path)

(define (draw-key/base key-shape base-color [width 60] [height 100])
  (dc
   (λ(dc x y)
     (define tr (send dc get-transformation))
     (send dc translate x y)

     (define dark-border (blend '(0 0 0) 0.7 base-color))
     (define bg
       (new brush%
            [gradient
             (new linear-gradient% [x0 0] [y0 0] [x1 width] [y1 0]
                  [stops (list (list 0 base-color)
                               (list 1 (blend '(255 255 255)
                                              0.85 base-color)))])]))
     (define hilight
       (new brush%
            [gradient
             (new radial-gradient%
                  [x0 0] [y0 height] [r0 0]
                  [x1 0] [y1 height] [r1 height]
                  [stops (list (list 1 base-color)
                               (list 0 (blend '(255 255 255)
                                              0.7 base-color)))])]))

     (send dc set-pen "white" 0 'transparent)
     (send dc set-brush dark-border 'solid)
     (send dc draw-path (key-shape 0 width height))
     (send dc set-brush hilight)
     (send dc draw-path (key-shape *border* width height))
     (send dc set-brush bg)
     (send dc draw-path (key-shape (+ *border* *border*) width height))

     (send dc set-transformation tr))
   width
   height))

(define (draw-text letter border-color text-color style)
  (define font (make-object font% 30 'default 'normal style))
  (define-values (w h bl vl)
    (send (dc-for-text-size) get-text-extent letter font))
  (dc
   (λ(dc x y)
     (define tr (send dc get-transformation))
     (send dc translate x y)
     (send dc translate *border* *border*)
     (send dc set-font font)
     (send dc set-text-foreground border-color)
     (for* ([x (in-range 0 (* 2 pi) (/ pi 4))])
       (send dc draw-text letter
             (* *border* (cos x))
             (* *border* (sin x))))
     (send dc set-text-foreground text-color)
     (send dc draw-text letter 0 0)
     (send dc set-transformation tr))
   (+ *border* *border* w)
   (+ *border* *border* *border* *border* h)))

(define (draw-shadow key-shape width height)
  (blur
   (cellophane
      (dc
       (λ(dc x y)
         (define tr (send dc get-transformation))
         (send dc translate x y)
         (send dc set-brush "black" 'solid)
         (send dc draw-path (key-shape 0 width height))
         (send dc set-transformation tr))
       width height)
     0.5)
    5))

(define ((key shape)
         base-color
         text-color
         letter
         style
         #:width [width 60]
         #:height [height 100])
  (pin-under
   (cc-superimpose
    (draw-key/base shape base-color width height)
    (draw-text letter (blend '(0 0 0) 0.7 base-color) text-color style))
   3 5
   (draw-shadow shape width height)))

(define tkey (key rect-shape))
(define bkey (key round-key-shape))

(define blk (make-object color% 0 0 0))