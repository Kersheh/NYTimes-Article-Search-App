# NYTimes Article Search App w/ Flask Server
An elegant, minimalistic web app to search the New York Times.
## Server
Install python module Flask:
```sh
pip install Flask
```
Before running the server, you will need your own [NYTimes API key](http://developer.nytimes.com/docs); more specifically, "The Article Search API". Modify line 65 of server.py with your key:
```python
article_key = "API_KEY_HERE"
```
Either uncomment line 94 and set the IP and port within server.py:
```python
app.run(host="127.0.0.1", port=5000)
```
Or run the server at localhost with default app.run().

---

Run the server:
```sh
python server.py
```