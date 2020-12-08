import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


# Create your tests here.
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() はpub_dateが将来の質問に対してFalseを返却する
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() はpub_dateが24時間以内の質問に対してTrueを返す
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)

def create_question(question_text, days):
    """
    Questionモデルインタスタンスを作成し保存します。
    質問内容は引数question_textを、pub_dateはシステム日付に引数daysを加減算し設定します。
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_question(self): # テストメソッド実行時、リセットされた
        """
        質問が存在しない場合、適切なメッセージが表示されること
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.") # responseに存在しない旨のメッセージが含まれることを確認
        self.assertQuerysetEqual(response.context['last_question_list'], []) # responseのコンテキスト辞書に設定されたQuerySetが空であることを確認

    def test_past_question(self):
        """
        pub_dateが過去の質問は、indexページに表示されること
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        ) # responseのコンテキスト辞書に設定されたQuerySetに、モデル登録したインスタンスが設定されていることを確認

    def test_future_question(self):
        """
        pub_dateが将来の質問は、indexページに表示されないこと
        :return:
        """
        create_question(question_text="Future question.", days=30) # pub_dateが30日後のQuestionモデルを登録
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.") # responseに文字列"No polls are available"が含まれていることを確認
        self.assertQuerysetEqual(response.context['latest_question_list'], []) # responseのコンテキスト辞書に設定されたQuerySetが空であることを確認

    def test_future_question_and_past_question(self):
        """
        pub_dateが過去と将来の質問が存在する場合、過去の質問のみがindexページに表示されること
        :return:
        """
        create_question(question_text="Past question.", days=30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question. >']
        )

    def test_two_past_questions(self):
        """
        pub_dateが過去の質問が複数存在する場合、該当する質問が全てindexページに表示されること
        :return:
        """
        create_question(question_text="Page question 1.", days=-30) # pub_dateが30日前のQuestionモデルを登録
        create_question(question_text="Past question 2.", days=-5) # pub_dateが5日前のQuestionモデルを登録
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        ) # responseのコンテキスト辞書に設定されたQuerySetに、モデル登録したインスタンスが全て設定されていることを確認

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        pub_dateが将来の質問の場合は、404 Not Foundエラーが表示されること
        :return:
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        pub_dateが過去の質問は、質問のテキストが表示されること
        :return:
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text) # モデルに登録した質問のテキストと同じ文字列がresopnseに含まれていることを確認