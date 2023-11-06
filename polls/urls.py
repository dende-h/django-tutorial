# Djangoのurlsモジュールからpath関数をインポートしています。
# path関数はURLパターンをビューにマッピングする際に使用します。
from django.urls import path

# 現在のディレクトリからviewsモジュール（views.pyファイル）をインポートしています。
from . import views

# このURLconfモジュール（urls.pyファイル）に名前空間を設定しています。
# 'polls'という名前空間を使うことで、他のアプリケーションとビューの名前が衝突することを防ぎます。
app_name = "polls"

# urlpatternsリストにURLパターンを定義しています。
urlpatterns = [
    # トップレベルのURL（例：/polls/）にアクセスがあったときに、
    # views.py内のIndexViewクラスベースビューを呼び出します。
    path("", views.IndexView.as_view(), name="index"),
    
    # 詳細ページのURL（例：/polls/3/）にアクセスがあったときに、
    # views.py内のDetailViewクラスベースビューを呼び出します。
    # <int:pk>はURLからキャプチャされた整数値を「pk」というパラメータでビューに渡します。
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    
    # 結果ページのURL（例：/polls/3/results/）にアクセスがあったときに、
    # views.py内のResultsViewクラスベースビューを呼び出します。
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    
    # 投票アクションを処理するURL（例：/polls/3/vote/）にアクセスがあったときに、
    # views.py内のvote関数ベースビューを呼び出します。
    # <int:question_id>はURLからキャプチャされた整数値を「question_id」というパラメータでビューに渡します。
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
