from .settings_common import *

#デバッグモードを有効にするかどうか(本番は必ずFalse)
DEBUG = False

#許可するホスト名のリスト
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]

#静的ファイルの配置場所
STATIC_ROOT = '/usr/share/nginx/html/static'
MEDIA_ROOT = '/usr/share/nginx/html/media'

#Amazon SES関連設定
AWS_SES_ACCESS_KEY_ID = os.environ.get('AWS_SES_ACCESS_KEY_ID')
AWS_SES_SECRET_ACCESS_KEY = os.environ.get('AWS_SES_SECRET_ACCESS_KEY')
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'

#ロギング
LOGGING = {
    'version':1,
    'disable_existing_loggers':False,

    #ロガーの設定
    'loggers':{
        #Djangoが利用するロガー
        'django':{
            'handlers':['file'],
            'level':'INFO',
        },

        #articleアプリケーションが利用するロガー
        'article':{
            'handlers':['file'],
            'level':'INFO',
        },
    },

    #ハンドラの設定
    'handlers':{
        'file':{
            'level':'INFO',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'prod',
            'when': 'D', #ログローテーション(新しいファイルへの切り替え)間隔の単位(D=日)
            'interval': 1, #ログローテーション間隔(一日単位)
            'backupCount': 7, #保存しておくログファイル数
        },
    },

    #フォーマッタの設定
    'formatters':{
        'prod': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}