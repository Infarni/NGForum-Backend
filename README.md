<h1>Description</h1>
This is the server side for the future forum written with python and django, django-rest-framework.
<h1>Deploy</h1>
<ol>
  <li>Copy this repository to your server</li>
  <li>
    <p>Set up dependencies</p>
    <ul>
      <li>Go to the project directory</li>
      <li>Create a virtual environment by running the command <code>python -m venv .venv</code></li>
      <li>
        <p>Activate the virtual environment by running</p>
        On Unix-like systems <code>source .venv/bin/activate</code><br>
        On Windows <code>.venv/Scripts/Activate.bat</code>
      </li>
      <li>Install the necessary packages by running the command <code>pip install -r requirements.txt</code></li>
    </ul>
  </li>
  <li>Create migrations and activate them by running the command <code>python manage.py makemigrations & python manage.py migrate</code></li>
  <li>Configure the project in the NGForum/settings.py file</li>
  <li>Set up your web server</li>
  <li>Start the wsgi server</li>
</ol>
