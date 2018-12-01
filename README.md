# emojiCoding
An implementation of Brainfuck using emoji

To start, simply run `start.py`.
 
 
| KEY | BRAINFUCK | EMOJI                               | DESCRIPTION |
|-----|-----------|------------------                   |-------------|
| a   | <         | :skull:                             | Decrement the data pointer            |
| s   | >         | :tropical_drink:                    | Increment the data pointer            |
| d   | +         | :fire:                              | Increment the byte at the data pointer            |
| f   | -         | :knife:                             | Decrement the byte at the data pointer            |
| j   | [         | :rainbow:                           | If the byte at the data pointer is 0, jump to matching `]`            |
| k   | ]         | &#129501; &#8205; &#9792; &#65039;  | If the byte at the data pointer is nonzero, jump to matching `[`            |
| l   | .         | :sparkles:                          | Output the byte at the data pointer            |
| ;   | ,         | &#129430;                           | Store one byte of input at the data pointer            |
