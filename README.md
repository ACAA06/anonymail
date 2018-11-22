# anonymail

> an anonymous feedback platform built using flask and sqlite3 database.

#### Requirements
```
pip install Werkzeug itsdangerous click Flask
```
#### Run on local server

``` 
$ git clone https://github.com/rajkumaar23/anonymail.git
```
>The app uses Gmail's SMTP server to send _reset password_ links to an user and hence make sure to create a **secrets.py** and store your gmail credentials as **EMAIL** and **PASSWORD**. 
```
$ FLASK_APP = anonymail FLASK_ENV = development 
$ flask init-db
$ flask run
````
 and you're good to go. 
 server will be live at `http://localhost:5000`
 
> To provide anonymous feedback for any registered user, follow this route   
`http://localhost:5000/registered-username/send`
 
#### Open Source License

Unless explicitly stated otherwise all files in this repository are licensed under the [MIT License](https://opensource.org/licenses/MIT). All projects **must** properly attribute [The Original Source](https://github.com/rajkumaar23/anonymail).
        
    MIT License
    
    Copyright (c) 2018 RAJKUMAR S
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    
An unmodified copy of the above license text must be included in all forks.

