from django.test import TestCase

import datetime
from django.utils import timezone
from django.urls import reverse
from .models import Question

# Questionモデルに関するテストケースを定義するクラス
class QuestionModelTests(TestCase):
    # 未来の日付で公開される質問は最近公開されたものとして判定されないことをテスト
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    # 1日以上前に公開された質問は最近公開されたものとして判定されないことをテスト
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    # 最近（1日以内）に公開された質問が最近公開されたと判定されることをテスト
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

# 質問を作成するヘルパー関数
def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

# インデックスビューに関するテストケースを定義するクラス
class QuestionIndexViewTests(TestCase):
    # 質問が存在しない場合に適切なメッセージが表示されるかをテスト
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    # 過去の日付で公開された質問がインデックスページに表示されるかをテスト
    def test_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    # 未来の日付で公開された質問がインデックスページに表示されないことをテスト
    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    # 過去と未来の質問が存在する場合でも、過去の質問のみが表示されることをテスト
    def test_future_question_and_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    # 複数の過去の質問がインデックスページに表示されることをテスト
    def test_two_past_questions(self):
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question2, question1])

# 詳細ビューに関するテストケースを定義するクラス
class QuestionDetailViewTests(TestCase):
    # 未来の日付で公開された質問の詳細ビューが404エラーを返すことをテスト
    def test_future_question(self):
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # 過去の日付で公開された質問の詳細ビューに質問のテキストが表示されることをテスト
    def test_past_question(self):
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
