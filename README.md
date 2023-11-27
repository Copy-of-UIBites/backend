# Run the App Locally

1. Clone the new Django template repository from your GitHub account to a
   location in the filesystem of your local development environment by using
   Git:

   ```shell
   git clone <URL to your repository on GitHub> <path in local development environment>
   ```

2. Go to the location where the cloned repository is located in the local
   development environment:

   ```shell
   cd <path to the cloned repository>
   ```

3. Create a Python virtual environment named `env` inside the cloned repository
   by using Python's `venv` module:

   ```shell
   python -m venv env
   ```

4. Activate the virtual environment:

   ```shell
   # Windows
   .\env\Scripts\activate
   # Linux/Unix, e.g. Ubuntu, MacOS
   source env/bin/activate
   ```

5. Verify the virtual environment has been activated by looking at the prompt
   of your shell. Make sure there is a `env` prefix in your shell. For example:

   ```shell
   # Windows using `pwsh` shell
   (env) PS C:\Users\RickeyAstley\my-django-app
   # Linux/Unix, e.g. Ubuntu using `bash` shell
   (env) rickeyastley@ubuntu:~/my-django-app
   ```

   > Note: You can use [Visual Studio Code][] (with Python extension) or [PyCharm][]
   > to open the source code directory that has a virtual environment directory.
   > Both will detect the virtual environment and use the correct Python virtual
   > environment. Furthermore, you can also run your shell directly in both text
   > editor/IDE.

6. Install the dependencies needed to build, test, and run the application:

   ```shell
   pip install -r requirements.txt
   ```

7. Run the Django Web application using local development server:

   ```shell
   python manage.py runserver
   ```

8. Open http://localhost:8000 in your favourite Web browser to see if the Web
   application is running.
