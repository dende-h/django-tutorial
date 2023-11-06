# Djangoが生成したマイグレーションファイルです。
# ファイル名は特定のフォーマットに従い、生成された日時が含まれます。
# このファイルは、Django 4.2.6で2023年11月6日01:13に生成されました。

from django.db import migrations, models
import django.db.models.deletion

# Migrationクラスは、このマイグレーションの具体的な内容を定義します。
class Migration(migrations.Migration):

    # このマイグレーションが初期（最初のマイグレーション）であることを示します。
    initial = True

    # このマイグレーションが依存する他のマイグレーションのリストです。
    # 初期マイグレーションの場合、依存関係はありません。
    dependencies = [
    ]

    # このマイグレーションで実行される操作のリストです。
    operations = [
        # Questionモデルを作成する操作です。
        migrations.CreateModel(
            name='Question',
            fields=[
                # IDフィールドは自動的に作成される主キーです。
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # 質問のテキストを格納するためのcharフィールドです（最大200文字）。
                ('question_text', models.CharField(max_length=200)),
                # 質問が公開された日時を格納するためのdatetimeフィールドです。
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        # Choiceモデルを作成する操作です。
        migrations.CreateModel(
            name='Choice',
            fields=[
                # IDフィールドは自動的に作成される主キーです。
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # 選択肢のテキストを格納するためのcharフィールドです（最大200文字）。
                ('choice_text', models.CharField(max_length=200)),
                # この選択肢が獲得した票数を格納するためのintegerフィールドです。デフォルトは0です。
                ('votes', models.IntegerField(default=0)),
                # ForeignKeyを使用して、各Choiceが特定のQuestionに関連づけられるようにします。
                # on_deleteオプションがCASCADEに設定されているため、Questionが削除された場合、
                # 関連するChoiceも自動で削除されます。
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question')),
            ],
        ),
    ]
