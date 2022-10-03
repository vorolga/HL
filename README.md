# Static HTTP Python Thread-pool Server

* Respond to `GET` with status code in `{200,404,403}`
* Respond to `HEAD` with status code in `{200,404,403}`
* Respond to all other request methods with status code `405`
* Directory index file name `index.html`
* Respond to requests for `/<file>.html` with the contents of `DOCUMENT_ROOT/<file>.html`
* Requests for `/<directory>/` should be interpreted as requests for `DOCUMENT_ROOT/<directory>/index.html`
* Respond with the following header fields for all requests:
  * `Server`
  * `Date`
  * `Connection`
* Respond with the following additional header fields for all `200` responses to `GET` and `HEAD` requests:
  * `Content-Length`
  * `Content-Type`
* Respond with correct `Content-Type` for `.html, .css, js, jpg, .jpeg, .png, .gif, .swf`
* Respond to percent-encoding URLs
* Correctly serve a 2GB+ files
* No security vulnerabilities

---------------------------
# Build docker containers

```
docker build -t server -f Dockerfile .
docker run -p 80:80 server
```

```
docker build -t nginx -f nginx.Dockerfile .
docker run -p 9090:9090 nginx
```

--------------------------
# Functional testing
### `pyhon3 httptest.py`
<details><summary>Ran 24 tests in 0.271s - OK<br>
(click to see all)</summary>
  <code>

    test_directory_index (__main__.HttpServer)
    directory index file exists ... ok
    test_document_root_escaping (__main__.HttpServer)
    document root escaping forbidden ... ok
    test_empty_request (__main__.HttpServer)
    Send empty line ... ok
    test_file_in_nested_folders (__main__.HttpServer)
    file located in nested folders ... ok
    test_file_not_found (__main__.HttpServer)
    absent file returns 404 ... ok
    test_file_type_css (__main__.HttpServer)
    Content-Type for .css ... ok
    test_file_type_gif (__main__.HttpServer)
    Content-Type for .gif ... ok
    test_file_type_html (__main__.HttpServer)
    Content-Type for .html ... ok
    test_file_type_jpeg (__main__.HttpServer)
    Content-Type for .jpeg ... ok
    test_file_type_jpg (__main__.HttpServer)
    Content-Type for .jpg ... ok
    test_file_type_js (__main__.HttpServer)
    Content-Type for .js ... ok
    test_file_type_png (__main__.HttpServer)
    Content-Type for .png ... ok
    test_file_type_swf (__main__.HttpServer)
    Content-Type for .swf ... ok
    test_file_urlencoded (__main__.HttpServer)
    urlencoded filename ... ok
    test_file_with_dot_in_name (__main__.HttpServer)
    file with two dots in name ... ok
    test_file_with_query_string (__main__.HttpServer)
    query string with get params ... ok
    test_file_with_slash_after_filename (__main__.HttpServer)
    slash after filename ... ok
    test_file_with_spaces (__main__.HttpServer)
    filename with spaces ... ok
    test_head_method (__main__.HttpServer)
    head method support ... ok
    test_index_not_found (__main__.HttpServer)
    directory index file absent ... ok
    test_large_file (__main__.HttpServer)
    large file downloaded correctly ... ok
    test_post_method (__main__.HttpServer)
    post method forbidden ... ok
    test_request_without_two_newlines (__main__.HttpServer)
    Send GET without to newlines ... ok
    test_server_header (__main__.HttpServer)
    Server header exists ... ok

    ----------------------------------------------------------------------
    Ran 24 tests in 0.271s
    
    OK

  </code>
</details>

----------------------
# Highload testing
### Using [Apache Benchmark](https://httpd.apache.org/docs/2.4/programs/ab.html)

## This server:80
Test:
`ab -n 10000 -c 20 127.0.0.1:80/httptest/wikipedia_russia.html`

<details>
<summary>Result: <code>Total: min:56 mean:370 [+/-sd]:121.7 median:342 max:2260</code><br>
(click to see all)</summary>
<code>

    This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/
    
    Benchmarking 127.0.0.1 (be patient)
    Completed 1000 requests
    Completed 2000 requests
    Completed 3000 requests
    Completed 4000 requests
    Completed 5000 requests
    Completed 6000 requests
    Completed 7000 requests
    Completed 8000 requests
    Completed 9000 requests
    Completed 10000 requests
    Finished 10000 requests
    
    
    Server Software:        Python
    Server Hostname:        127.0.0.1
    Server Port:            80
    
    Document Path:          /httptest/wikipedia_russia.html
    Document Length:        954824 bytes
    
    Concurrency Level:      20
    Time taken for tests:   185.101 seconds
    Complete requests:      10000
    Failed requests:        5
       (Connect: 0, Receive: 0, Length: 5, Exceptions: 0)
    Total transferred:      9545931432 bytes
    HTML transferred:       9544371432 bytes
    Requests per second:    54.02 [#/sec] (mean)
    Time per request:       370.201 [ms] (mean)
    Time per request:       18.510 [ms] (mean, across all concurrent requests)
    Transfer rate:          50362.86 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    1   0.4      1      12
    Processing:    55  369 121.6    341    2259
    Waiting:       10   33  18.8     29     362
    Total:         56  370 121.7    342    2260
    
    Percentage of the requests served within a certain time (ms)
      50%    342
      66%    371
      75%    390
      80%    407
      90%    472
      95%    564
      98%    688
      99%    770
     100%   2260 (longest request)

</code>
</details>

## Nginx:90

Test:
`ab -n 10000 -c 20 127.0.0.1:9090/httptest/wikipedia_russia.html`

<details>
<summary>Result: <code>Total: min:55 mean:373 [+/-sd]:139.0 median:78 max:2821</code><br>
(click to see all)</summary>
<code>

    This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/
    
    Benchmarking 127.0.0.1 (be patient)
    Completed 1000 requests
    Completed 2000 requests
    Completed 3000 requests
    Completed 4000 requests
    Completed 5000 requests
    Completed 6000 requests
    Completed 7000 requests
    Completed 8000 requests
    Completed 9000 requests
    Completed 10000 requests
    Finished 10000 requests
    
    
    Server Software:        nginx/1.23.1
    Server Hostname:        127.0.0.1
    Server Port:            9090
    
    Document Path:          /httptest/wikipedia_russia.html
    Document Length:        954824 bytes
    
    Concurrency Level:      20
    Time taken for tests:   186.804 seconds
    Complete requests:      10000
    Failed requests:        4
       (Connect: 0, Receive: 0, Length: 4, Exceptions: 0)
    Total transferred:      9548249928 bytes
    HTML transferred:       9545869928 bytes
    Requests per second:    53.53 [#/sec] (mean)
    Time per request:       373.607 [ms] (mean)
    Time per request:       18.680 [ms] (mean, across all concurrent requests)
    Transfer rate:          49915.85 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    1   0.4      1       7
    Processing:    55  373 138.9    350    2820
    Waiting:       10   33  19.1     29     402
    Total:         55  373 139.0    350    2821
    
    Percentage of the requests served within a certain time (ms)
      50%    350
      66%    378
      75%    399
      80%    413
      90%    466
      95%    526
      98%    623
      99%    768
     100%   2821 (longest request)

</code>
</details>
