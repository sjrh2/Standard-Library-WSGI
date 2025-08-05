# Simple WSGI Web Application

A minimal WSGI web application demonstrating the core concepts you need to understand.

## 📁 Files

- `simple_wsgi_app.py` - The WSGI web application with routing
- `wsgi_server.py` - Server to run the application  
- `requirements.txt` - Dependencies (none needed - uses Python standard library)

## 🚀 How to Run

1. **Start the server:**
   ```bash
   python wsgi_server.py
   ```

2. **Open your browser:**
   - Go to `http://localhost:8000`

3. **Try the routes:**
   - `/` - Home page (shows request info)
   - `/about` - About page  
   - `/contact` - Contact page
   - `/anything-else` - 404 error page

## 🎯 Core WSGI Concepts Explained

### 1. **The `environ` Dictionary** 📋

The `environ` is a **dictionary containing ALL request information**. It's the first parameter your WSGI app receives.

**Key environ variables:**
```python
environ['REQUEST_METHOD']    # 'GET', 'POST', 'PUT', 'DELETE'
environ['PATH_INFO']         # '/about', '/contact', '/'
environ['QUERY_STRING']      # 'name=john&age=25'
environ['CONTENT_LENGTH']    # Size of request body
environ['CONTENT_TYPE']      # 'application/json', 'text/html'
environ['HTTP_USER_AGENT']   # Browser information
environ['HTTP_HOST']         # 'localhost:8000'
environ['REMOTE_ADDR']       # Client IP address '127.0.0.1'
```

**In your code:**
```python
def application(environ, start_response):
    method = environ['REQUEST_METHOD']      # GET, POST, etc.
    path = environ['PATH_INFO']             # URL path like '/about'
    query = environ.get('QUERY_STRING', '') # URL parameters
```

### 2. **HTTP Status Codes** 🔢

Status codes tell the client what happened with their request.

**What you use in the code:**
```python
status = '200 OK'        # Success - everything worked
status = '404 Not Found' # Error - page doesn't exist
```

**Common status codes:**
- **2xx Success:**
  - `200 OK` - Request successful
  - `201 Created` - Resource created
  - `204 No Content` - Success, no content to return

- **3xx Redirection:**
  - `301 Moved Permanently` - Page moved forever
  - `302 Found` - Page temporarily moved

- **4xx Client Error:**
  - `400 Bad Request` - Malformed request
  - `401 Unauthorized` - Authentication required
  - `403 Forbidden` - Access denied
  - `404 Not Found` - Page doesn't exist
  - `405 Method Not Allowed` - Wrong HTTP method

- **5xx Server Error:**
  - `500 Internal Server Error` - Something broke on server
  - `502 Bad Gateway` - Upstream server error
  - `503 Service Unavailable` - Server overloaded

### 3. **Headers** 📦

Headers provide **metadata about the response** - they tell the browser how to handle the content.

**What you set in the code:**
```python
headers = [
    ('Content-Type', 'text/html; charset=utf-8'),  # What type of content
    ('Content-Length', '1234')                     # How many bytes to expect
]
```

**Common headers explained:**
- **`Content-Type`**: Tells browser what you're sending
  - `text/html` - HTML page
  - `application/json` - JSON data
  - `text/plain` - Plain text
  - `image/png` - PNG image

- **`Content-Length`**: Exact size in bytes
  - Browser knows when response is complete
  - Helps with download progress

- **`Location`**: Used for redirects
  - `Location: /login` - Redirect to login page

- **`Set-Cookie`**: Sets cookies in browser
  - `Set-Cookie: session_id=abc123`

- **`Cache-Control`**: Controls caching
  - `Cache-Control: no-cache` - Don't cache
  - `Cache-Control: max-age=3600` - Cache for 1 hour

### 4. **The `start_response()` Function** ⚡

This is **how your app tells the server what status and headers to send**.

**Purpose:**
- Sets the HTTP status line
- Sets all response headers  
- Must be called BEFORE returning content

**How it works:**
```python
def application(environ, start_response):
    # 1. Prepare your response
    status = '200 OK'
    headers = [('Content-Type', 'text/html')]
    
    # 2. Tell the server: "Send this status and these headers"
    start_response(status, headers)
    
    # 3. Return the actual content
    return [b'<html><body>Hello!</body></html>']
```

**What happens when called:**
1. Server prepares HTTP response line: `HTTP/1.1 200 OK`
2. Server adds your headers:
   ```
   Content-Type: text/html
   Content-Length: 123
   ```
3. Server sends headers to browser
4. Server waits for your app to return content
5. Server sends your content as response body

**Complete HTTP response created:**
```http
HTTP/1.1 200 OK                    ← From status parameter
Content-Type: text/html            ← From headers parameter
Content-Length: 123                ← From headers parameter
                                   ← Empty line separates headers from body
<html><body>Hello!</body></html>   ← From what you return
```

## 🔍 How It All Works Together

### **The WSGI Flow:**

1. **Browser sends request:**
   ```
   GET /about HTTP/1.1
   Host: localhost:8000
   ```

2. **Server creates `environ` dictionary:**
   ```python
   environ = {
       'REQUEST_METHOD': 'GET',
       'PATH_INFO': '/about',
       'HTTP_HOST': 'localhost:8000',
       # ... more request info
   }
   ```

3. **Server calls your WSGI app:**
   ```python
   response = application(environ, start_response)
   ```

4. **Your app processes request:**
   ```python
   def application(environ, start_response):
       path = environ['PATH_INFO']  # '/about'
       
       if path == '/about':
           status = '200 OK'
           headers = [('Content-Type', 'text/html')]
           start_response(status, headers)  # Tell server what to send
           return [b'<html>About page</html>']  # Return content
   ```

5. **Server sends complete HTTP response:**
   ```http
   HTTP/1.1 200 OK
   Content-Type: text/html
   Content-Length: 25
   
   <html>About page</html>
   ```

6. **Browser displays the page**

## 🧪 Understanding the Log Line

When you see:
```
127.0.0.1 - - [05/Aug/2025 20:38:45] "GET / HTTP/1.1" 200 840
```

This means:
- **`127.0.0.1`** - Client IP (localhost)
- **`GET /`** - HTTP method and path from `environ`
- **`200`** - Status code you set in `start_response()`
- **`840`** - Content-Length header you set

## 💡 Key Takeaways

1. **`environ`** = All request information (method, path, headers, etc.)
2. **Status codes** = Tell client what happened (200=success, 404=not found)
3. **Headers** = Metadata about your response (content type, size, etc.)
4. **`start_response()`** = Your way to set status and headers
5. **Return value** = The actual content to send

**The WSGI contract:** Your app gets request info (`environ`), sets response info (`start_response`), and returns content. That's it!

This simple interface allows any WSGI server to run any WSGI application - that's the power of WSGI!
