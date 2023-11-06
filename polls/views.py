# 必要なモジュールをインポートしています。
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

# IndexViewはListViewを継承しており、質問のリストを表示するためのビューです。
class IndexView(generic.ListView):
    # 使用するテンプレートを指定しています。
    template_name = "polls/index.html"
    # コンテキストに渡す変数名を指定しています。
    context_object_name = "latest_question_list"

    # get_querysetメソッドをオーバーライドして、
    # 未来の日付に設定された質問を除外し、最新の5件の質問を返します。
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

# DetailViewはDetailViewを継承しており、単一の質問の詳細を表示するためのビューです。
class DetailView(generic.DetailView):
    model = Question  # このビューで使用するモデルを指定しています。
    template_name = "polls/detail.html"  # 使用するテンプレートを指定しています。

    # 未来の日付に設定された質問を除外するためにget_querysetをオーバーライドします。
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

# ResultsViewもDetailViewを継承しており、投票結果を表示するためのビューです。
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

# vote関数は投票処理を行います。
def vote(request, question_id):
    # 指定されたIDの質問が存在しない場合は404エラーを発生させます。
    question = get_object_or_404(Question, pk=question_id)
    try:
        # POSTデータから選択された選択肢を取得します。
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # POSTデータに選択肢がなければ、エラーメッセージとともに投票フォームを再表示します。
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice.",
        })
    else:
        # 選択肢の投票数を増やし、データベースに保存します。
        selected_choice.votes += 1
        selected_choice.save()
        # POSTリクエストを処理した後は、リダイレクトを使用してGETリクエストにリダイレクトします。
        # これはPOSTデータの二重送信を防ぐためです。
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
