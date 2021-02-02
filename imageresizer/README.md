# Image Resizer

A micro-service to resize images. It provides an http end-point that takes the original image url, desired height, width & output image format as parameters and returns the resized image in response.

#### Usage:

```
docker pull shahedk/image-resizer:latest

docker run  -p 8080:80 shahedk/image-resizer:latest
```
The above script will start the container at http://localhost:8080

#### Resize images from url
Specify the image url and desired settings in the parameters. The response will contain the output image:

```
http://localhost:8080/resize?url={imageurl}&h={height}&w={width}&f={format}
```

#### Available parameters
* `url` `(string: required)`
* `h` or `height` `(int: required)`
* `w` or `width` `(int: required)`
* `f` or `format` `(possible values: png | jpg | tiff | webp)`
* `fit` `(possible values: cover | contain)`

For example, the http request to resize an image from "http://cdn.shahed.ca/default.jpg" into 100x100 pixel image of PNG format would look like this:

```
http://localhost:8080/resize?w=100&h=100&url=http%3A//cdn.shahed.ca/default.jpg&f=png
```

The service uses the sharp image resizer libarary and supported output image formats are: PNG, JPEG, TIFF and WebP
