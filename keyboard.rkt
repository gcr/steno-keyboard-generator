#lang racket

(require racket/gui
         racket/draw
         slideshow/pict
         "key.rkt")
(provide keyboard)

(define tint-map
  (hash
   "control" (make-object color% 170 180 190)
   "*" (make-object color% 255 128 64)
   "A" (make-object color% 157 243 72)
   "C" (make-object color% 176 52 50)
   "B" (make-object color% 128 0 0)
   "E" (make-object color% 238 167 51)
   "D" (make-object color% 127 129 0)
   "G" (make-object color% 0 128 131)
   "F" (make-object color% 0 128 1)
   "I" (make-object color% 88 89 21)
   "H" (make-object color% 197 89 211)
   "K" (make-object color% 129 0 127)
   "J" (make-object color% 1 0 128)
   "M" (make-object color% 132 63 0)
   "L" (make-object color% 127 255 254)
   "O" (make-object color% 87 100 129)
   "N" (make-object color% 255 0 134)
   "Q" (make-object color% 82 15 82)
   "P" (make-object color% 0 127 255)
   "S" (make-object color% 0 255 0)
   "R" (make-object color% 0 254 129)
   "U" (make-object color% 188 243 237)
   "T" (make-object color% 127 0 253)
   "W" (make-object color% 242 106 191)
   "V" (make-object color% 255 255 128)
   "Y" (make-object color% 115 44 174)
   "X" (make-object color% 255 255 0)
   "Z" (make-object color% 255 0 0)))
(define color-groups
  (list
   (list (set "S-" "T-" "P-" "K" "W") "Z")
   (list (set "T-" "P-" "K" "W") "G")
   (list (set "-P" "L" "B" "G") "J")
   (list (set "-P" "L" "B" "G") "J")
   (list (set "-S" "-R" "B" "G") "control")
   (list (set "F" "-P" "L" "-T") "control")
   (list (set "T-" "P-" "H") "N")
   (list (set "K" "W" "R-") "Y")
   (list (set "B" "G" "-S") "X")
   (list (set "K" "P-") "X")
   (list (set "S-" "R-") "V")
   (list (set "K" "W") "Q")
   (list (set "E" "U") "I")
   (list (set "K" "R-") "C")
   (list (set "-P" "B") "N")
   (list (set "-P" "L") "M")
   (list (set "P-" "H") "M")
   (list (set "H" "R-") "L")
   (list (set "T-" "K") "D")
   (list (set "P-" "W") "B")
   (list (set "T-" "P-") "F")
   (list (set "B" "G") "K")
   (list (set "W") "W")
   (list (set "U") "U")
   (list (set "O") "O")
   (list (set "H") "H")
   (list (set "E") "E")
   (list (set "A") "A")
   (list (set "Z") "Z")
   (list (set "F") "V")
   (list (set "L") "L")
   (list (set "K") "K")
   (list (set "G") "G")
   (list (set "F") "F")
   (list (set "B") "B")
   (list (set "R-") "R")
   (list (set "D") "D")
   (list (set "-R") "R")
   (list (set "P-") "P")
   (list (set "-P") "P")
   (list (set "T-") "T")
   (list (set "-T") "T")
   (list (set "S-") "S")
   (list (set "-S") "S")
   (list (set "*") "*")))

(define (pick-color ltr pressed-keys)
  (define base-color (make-object color% 16 16 16)) ;128 118 100))
  (if (member ltr pressed-keys)
      ;; Fold out the remaining ones.
      (let loop ([groups-to-go color-groups]
                 [keyset (list->set pressed-keys)])
        (match-define (list group-set result-letter) (first groups-to-go))
        (cond
         [(empty? groups-to-go)
          (error 'pick-color "Color not found! ~s for key ~s"
                 keyset ltr)]
         [(subset? group-set keyset)
          ;; Found a group
          (if (set-member? group-set ltr)
              (hash-ref tint-map result-letter)
              (loop (rest groups-to-go)
                    (set-subtract keyset group-set)))]
         [else
          (loop (rest groups-to-go) keyset)]))
      base-color))

(define (pick-style ltr pressed-keys)
  (if (member ltr pressed-keys)
      'bold
      'normal))

(define (pick-text-color ltr pressed-keys)
  (if (or (empty? pressed-keys) (member ltr pressed-keys))
      (make-object color% 255 255 255)
      (make-object color% 128 128 128)))

(define (sanitize-ltr ltr)
  (regexp-replace* "-" ltr ""))

(define (keyboard pressed-keys)
  (define-syntax-rule (b ltr arg ...)
    (bkey (pick-color ltr pressed-keys)
          (pick-text-color ltr pressed-keys)
          (sanitize-ltr ltr)
          (pick-style ltr pressed-keys) arg ...))
  (define-syntax-rule (t ltr arg ...)
    (tkey (pick-color ltr pressed-keys)
          (pick-text-color ltr pressed-keys)
          (sanitize-ltr ltr)
          (pick-style ltr pressed-keys) arg ...))
  (inset
   (ht-append 20
    ; S key
    (b "S-" #:height 210)

    ; Rest of keyboard, which is:
    (vl-append 10
     (ht-append 20
      ; Left side: TPH, KWR
      (vl-append 10
       (ht-append 20 (t "T-") (t "P-") (t "H"))
       (ht-append 20 (b "K") (b "W") (b "R-")))
      (b "*" #:height 210 #:width 80)
      ; Right side: FPLTD, RBGSZ
      (vl-append 10
       (hc-append 20 (t "F") (t "-P") (t "L") (t "-T") (t "D"))
       (hc-append 20 (b "-R") (b "B") (b "G") (b "-S") (b "Z")))
      )
     ; Vowels
     (ht-append (blank 80)
                (blank 30)
                (b "A")
                (blank 10)
                (b "O")
                (blank 80)
                (b "E")
                (blank 10)
                (b "U"))))
   4))

(define (save-pict pict file [kind 'png])
  (define width (inexact->exact (ceiling (pict-width pict))))
  (define height (inexact->exact (ceiling (pict-height pict))))
  (define bm (make-object bitmap% width height #f #t))
  (define dc (new bitmap-dc% [bitmap bm]))
  (send dc set-smoothing 'aligned)
  (draw-pict pict dc 0 0)
  (send bm save-file file 'png))

;; (keyboard '("H" "E" "L"))