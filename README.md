# Django YouTube Downloader

This YouTube downloader website works using two essential libraries: `pytube` and `requests`.

## User Interface

When the user enters the link, an asynchronous request occurs in the background with JavaScript, which then receives a response containing available resolutions, titles, and thumbnails using `pytube`.

## Backend

When the server receives a 'GET' request with both URL and resolution parameters, the server retrieves the same stream object with the help of `pytube`. Each stream object filtered with different resolutions has a different URL. The server then begins fetching the video progressively using the `requests` library. For each chunk that gets downloaded, it is checked for validity. Subsequently, it is redirected to the client. All of this happens using the TCP protocol and is managed by Django.

Finally, you only need to include three headers:

-   `Content-Disposition`: Set this header to 'attachment' so that the file is downloaded instead of played and encode this string so the name will work.
-   `Content-Length`: This header should specify the file size, which you can obtain from the `pytube` stream object.
-   `Content-Type`: This header should be set to 'application/octet-stream'.
