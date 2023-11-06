# 必要なDjangoモジュールをインポートしています。
from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin

# Questionモデルを定義しています。
# これはDjangoのModelクラスを継承しており、データベースのテーブルに相当します。
class Question(models.Model):
    # テキストフィールドを定義しています。質問のテキストを保存するためのフィールドです。
    question_text = models.CharField(max_length=200)
    # 日付と時刻のフィールドを定義しています。質問が公開された日時を保存します。
    pub_date = models.DateTimeField("date published")
    
    # オブジェクトを文字列として表す方法を定義しています。
    # このメソッドがあることで、管理サイトなどでオブジェクトを表示する際に、
    # question_textの内容が表示されるようになります。
    def __str__(self):
        return self.question_text

    # 管理サイトで表示するためのメソッドに追加の情報を提供するデコレータです。
    # このメソッドは、質問が最近公開されたかどうかを判定するためのものです。
    @admin.display(
        boolean=True,          # 結果をブール値として表示する
        ordering="pub_date",   # "pub_date"に基づいてオブジェクトを並べ替える
        description="Published recently?",  # 管理サイトでの表示名
    )
    def was_published_recently(self):
        now = timezone.now()
        # 現在時刻と質問の公開時刻を比較し、
        # 公開から1日以内であればTrue、それ以外はFalseを返します。
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
# Choiceモデルを定義しています。
class Choice(models.Model):
    # ForeignKeyを使って、ChoiceがQuestionに関連付けられるようにしています。
    # on_delete=models.CASCADEは、関連するQuestionが削除されたらChoiceも削除されることを意味します。
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # 選択肢のテキストを保存するためのフィールドです。
    choice_text = models.CharField(max_length=200)
    # 投票数を整数で保存するフィールドです。デフォルトは0です。
    votes = models.IntegerField(default=0)

    # Choiceオブジェクトを文字列として表す方法を定義しています。
    def __str__(self):
        return self.choice_text
