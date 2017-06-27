import os


''' SERVER SETTINGS '''


class Config(object):
    '''
    SECRET_KEY is the secret value used to creation sessions and sign strings. This should be set to a random string. In the
    interest of ease, CTFd will automatically create a secret key file for you. If you wish to add this secret key to
    your instance you should hard code this value to a random static value.

    You can also remove .ctfd_secret_key from the .gitignore file and commit this file into whatever repository
    you are using.

    http://flask.pocoo.org/docs/0.11/quickstart/#sessions
    '''
    SECRET_KEY = os.getenv('CTFD_SECRET_KEY', str(os.urandom(64)))

    '''
    SQLALCHEMY_DATABASE_URI is the URI that specifies the username, password, hostname, port, and database of the server
    used to hold the CTFd database.

    http://flask-sqlalchemy.pocoo.org/2.1/config/#configuration-keys
    '''
    SQLALCHEMY_DATABASE_URI = os.getenv('CTFD_DATABASE_URL', 'sqlite:///{}/ctfd.db'.format(os.path.dirname(os.path.abspath(__file__))))

    '''
    SQLALCHEMY_TRACK_MODIFICATIONS is automatically disabled to suppress warnings and save memory. You should only enable
    this if you need it.
    '''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    '''
    SESSION_TYPE is a configuration value used for Flask-Session. It is currently unused in CTFd.
    http://pythonhosted.org/Flask-Session/#configuration
    '''
    SESSION_TYPE = os.getenv('CTFD_SESSION_TYPE', 'filesystem')
    if SESSION_TYPE == 'redis':
        from redis import StrictRedis
        SESSION_REDIS = StrictRedis(host=os.getenv('CTFD_CACHE_HOST'),
                                    port=os.getenv('CTFD_CACHE_PORT'),
                                    password=os.getenv('CTFD_CACHE_PASSWORD'),
                                    db=os.getenv('CTFD_CACHE_DB'))

    '''
    SESSION_FILE_DIR is a configuration value used for Flask-Session. It is currently unused in CTFd.
    http://pythonhosted.org/Flask-Session/#configuration
    '''
    SESSION_FILE_DIR = "/tmp/flask_session"

    '''
    SESSION_COOKIE_HTTPONLY controls if cookies should be set with the HttpOnly flag.
    '''
    SESSION_COOKIE_HTTPONLY = True

    '''
    PERMANENT_SESSION_LIFETIME is the lifetime of a session.
    '''
    PERMANENT_SESSION_LIFETIME = 604800  # 7 days in seconds

    '''
    HOST specifies the hostname where the CTFd instance will exist. It is currently unused.
    '''
    HOST = os.getenv('CTFD_HOST', '')

    '''
    MAILFROM_ADDR is the email address that emails are sent from if not overridden in the configuration panel.
    '''
    MAILFROM_ADDR = os.getenv('CTFD_MAILFROM_ADDR', '')

    '''
    UPLOAD_FOLDER is the location where files are uploaded.
    The default destination is the CTFd/uploads folder. If you need Amazon S3 files
    you can use the CTFd S3 plugin: https://github.com/ColdHeat/CTFd-S3-plugin
    '''
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

    '''
    Configuration for S3 for attachments

    S3_ATTACHMENTS_ACCESS_KEY_ID is your AWS Access Key. If you do not provide this, it will try to use an IAM role or credentials file.

    S3_ATTACHMENTS_SECRET_ACCESS_KEY is your AWS Secret Key. If you do not provide this, it will try to use an IAM role or credentials file.

    S3_ATTACHMENTS_BUCKET is the name of your Amazon S3 bucket.

    Adapted from CTFd-S3-plugin https://github.com/CTFd/CTFd-S3-plugin
    '''
    S3_ATTACHMENTS_ACCESS_KEY_ID = os.getenv('CTFD_S3_ATTACHMENTS_ACCESS_KEY_ID', None)
    S3_ATTACHMENTS_SECRET_ACCESS_KEY = os.getenv('CTFD_S3_ATTACHMENTS_SECRET_ACCESS_KEY', None)
    S3_ATTACHMENTS_BUCKET = os.getenv('CTFD_S3_ATTACHMENTS_BUCKET', None)

    '''
    TEMPLATES_AUTO_RELOAD specifies whether Flask should check for modifications to templates and
    reload them automatically
    '''
    TEMPLATES_AUTO_RELOAD = True

    '''
    TRUSTED_PROXIES defines a set of regular expressions used for finding a user's IP address if the CTFd instance
    is behind a proxy. If you are running a CTF and users are on the same network as you, you may choose to remove
    some proxies from the list.

    CTFd only uses IP addresses for cursory tracking purposes. It is ill-advised to do anything complicated based
    solely on IP addresses.
    '''
    TRUSTED_PROXIES = [
        '^127\.0\.0\.1$',
        # Remove the following proxies if you do not trust the local network
        # For example if you are running a CTF on your laptop and the teams are all on the same network
        '^::1$',
        '^fc00:',
        '^10\.',
        '^172\.(1[6-9]|2[0-9]|3[0-1])\.',
        '^192\.168\.'
    ]

    '''
    CACHE_TYPE specifies how CTFd should cache configuration values. If CACHE_TYPE is set to 'redis', CTFd will make use
    of the REDIS_URL specified in environment variables. You can also choose to hardcode the REDIS_URL here.

    CACHE_REDIS_URL is the URL to connect to Redis server.
    Example: redis://user:password@localhost:6379/2.

    http://pythonhosted.org/Flask-Caching/#configuring-flask-caching
    '''
    CACHE_TYPE = os.getenv('CTFD_CACHE_TYPE', 'simple')
    if CACHE_TYPE == 'redis':
        CACHE_KEY_PREFIX = 'cache-'
        CACHE_REDIS_URL = os.getenv('CTFD_CACHE_URL')
        CACHE_REDIS_USER = os.getenv('CTFD_CACHE_USER'),
        CACHE_REDIS_PASSWORD = os.getenv('CTFD_CACHE_PASSWORD'),
        CACHE_REDIS_HOST = os.getenv('CTFD_CACHE_HOST'),
        CACHE_REDIS_PORT = os.getenv('CTFD_CACHE_PORT'),
        CACHE_REDIS_DB = os.getenv('CTFD_CACHE_DB')


class TestingConfig(Config):
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
