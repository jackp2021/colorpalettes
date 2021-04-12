# Harvard Art Museums Color Palettes

This app uses Python and [Matplotlib](https://matplotlib.org/) to create color palettes of works in the [Harvard Art Museums](https://harvardartmuseums.org/collections?q=)' collections.

Charts are first rendered in the browser using the [MPLD3](https://mpld3.github.io/) library. The  script was then adapted for Flask through [this example](https://github.com/nipunbatra/mpld3-flask) and deployed in Heroku: https://colorpalettes-harvardart.herokuapp.com/

To run this code locally on your machine, request a new API key from HAM and place it in the apikey.json file.
