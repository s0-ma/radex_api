radex_api
====
Call RADEX on-line version from python.

Overview
----

Call RADEX on-line version from python.  
DO NOT HEAVILY USE THIS SCRIPT.  
This script simply calls the RADEX on-line page.  
Please do not apply heavy load on the RADEX server.  
If needed, please use official off-line version.

How to use
----
syntax:

    $ ./radex.py molecule fmin[GHz] fmax[GHz] T_bg[K] T_k[K] n(H_2) N(molecule) dv[km/s]

example:

    $ ./radex.py 13co 50 500 2.73 30 1e4 1e14 1.0


If a key for the molecule is needed, please check the HTML source of the RADEX on-line page,  
or type:

    $ ./radex.py list

