# Djangoのadminモジュールをインポートしています。
# これにより、Djangoの管理サイトの機能を利用できるようになります。
from django.contrib import admin

# 同じディレクトリ内のmodels.pyファイルからChoiceモデルとQuestionモデルをインポートしています。
from .models import Choice, Question

# Choiceモデルをインライン表示するためのクラスです。
# TabularInlineを継承しているため、表形式で表示されます。
class ChoiceInline(admin.TabularInline):
    model = Choice  # Choiceモデルを指定
    extra = 3  # デフォルトで3つの選択肢フィールドを表示

# Questionモデルの管理ページをカスタマイズするためのクラスです。
class QuestionAdmin(admin.ModelAdmin):
    # 管理ページで表示するフィールドセットを定義します。
    fieldsets = [
        (None, {"fields": ["question_text"]}),  # 「question_text」フィールドのみのセクション
        # 「pub_date」フィールドのセクションで、「collapse」クラスを使ってデフォルトで折り畳み可能にします。
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    # Questionモデルを作成または編集する際にChoiceモデルも一緒に編集できるようにします。
    inlines = [ChoiceInline]
    # 管理ページのリストに表示するフィールドを定義します。
    list_display = ["question_text", "pub_date", "was_published_recently"]
    # リストページでフィルタリングできるフィールドを指定します。
    list_filter = ["pub_date"]  # 「pub_date」フィールドでフィルタリング

# 最後に、カスタマイズした管理クラスとQuestionモデルをDjangoのadminサイトに登録しています。
# これにより、管理サイトからQuestionモデルを操作する際に、上記のカスタマイズが適用されます。
admin.site.register(Question, QuestionAdmin)
