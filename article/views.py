from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Max
from django.db.models import Q
from django.views.generic.list import MultipleObjectMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.http import JsonResponse
from django.core.paginator import Paginator
import logging

from .forms import InquiryForm, AccountSettingForm, MyPasswordChangeForm, ProfileSettingForm, ArticleCreateForm, CommentCreateForm, CommentReplyForm
from accounts.models import CustomUser
from .models import Article, Comment, SubComment, LikeForArticle
# Create your views here.

logger = logging.getLogger(__name__)

class IndexView(generic.ListView):
    template_name = 'index.html'
    model = Article

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            article_list = Article.objects.filter(Q(title__icontains=query)|Q(content__icontains=query)).order_by('-created_at')
        else:
            article_list = Article.objects.all().order_by('-created_at')

        return article_list

class InquiryView(generic.FormView):
    template_name = 'inquiry.html'
    form_class = InquiryForm
    success_url = reverse_lazy('article:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'You successfully sent message !')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

#マイページ関連
class MyPageView(LoginRequiredMixin, MultipleObjectMixin, generic.DetailView):
    template_name = 'mypage.html'
    model = CustomUser
    slug_field = 'username' #モデルのフィールド名
    slug_url_kwarg = 'username' #urls.pyでのキーワード名
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        object_list = Article.objects.filter(post_user=self.get_object())
        context = super(MyPageView, self).get_context_data(object_list=object_list, **kwargs)

        return context
    
class ProfileSettingView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'profile_setting.html'
    model = CustomUser
    form_class = ProfileSettingForm
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_success_url(self):
        return reverse_lazy('article:mypage', kwargs={'username': self.object.username})
    
    def form_valid(self, form):
        messages.success(self.request, 'Successfully changed your profile')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to change your profile')
        return super().form_invalid(form)
        
#ユーザーページ関連
class UserPageView(MultipleObjectMixin ,generic.DetailView):
    template_name = 'user.html'
    model = CustomUser
    slug_field = 'username' #モデルのフィールド名
    slug_url_kwarg = 'username' #urls.pyでのキーワード名
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        object_list = Article.objects.filter(post_user=self.get_object())
        context = super(UserPageView, self).get_context_data(object_list=object_list, **kwargs)

        return context

#記事関連
class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'article_detail.html'

    def get(self, request, *args, **kwargs): #閲覧数のカウント処理
        self.object = self.get_object()
        self.object.view_count += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #コメント作成フォーム
        context['form'] = CommentCreateForm()

        like_for_article_count = self.object.likeforarticle_set.count()
        #記事に対するイイね数
        context['like_for_article_count'] = like_for_article_count

        #非ログインユーザーの場合
        if self.request.user.id is None:
            context['is_user_liked_for_article'] = False
        #ログインユーザがイイねしているかどうか
        elif self.object.likeforarticle_set.filter(user=self.request.user).exists():
            context['is_user_liked_for_article'] = True
        else:
            context['is_user_liked_for_article'] = False

        #コメント返し
        context['comment_list'] = Comment.objects.select_related('target').filter(target=self.kwargs['pk'])

        return context

#記事に対するイイねの非同期処理
@login_required
def like_for_article(request):
    article_pk = request.POST.get('article_pk')
    context = {
        'user': request.user,
    }
    article = get_object_or_404(Article, pk=article_pk)
    like = LikeForArticle.objects.filter(target=article, user=request.user)

    #既にイイねしていたら削除、していなかったらイイね
    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(target=article, user=request.user)
        context['method'] = 'create'

    context['like_for_article_count'] = article.likeforarticle_set.count()

    return JsonResponse(context)


#記事作成
class ArticleCreateView(LoginRequiredMixin ,generic.CreateView):
    model = Article
    template_name = "article_create.html"
    form_class = ArticleCreateForm
    slug_field = 'username' #モデルのフィールド名
    slug_url_kwarg = 'username' #urls.pyでのキーワード名

    def get_success_url(self):
        return reverse_lazy('article:mypage', kwargs={'username': self.object.post_user})

    def form_valid(self, form):
        article = form.save(commit=False)
        article.post_user = self.request.user
        article.save()
        messages.success(self.request, 'You created an article!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'You failed in creating an article')
        return super().form_invalid(form)

#記事更新
class ArticleUpdateView(LoginRequiredMixin ,generic.UpdateView):
    model = Article
    template_name = 'article_update.html'
    form_class = ArticleCreateForm

    def get_success_url(self):
        return reverse_lazy('article:article_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, 'The article has been successfully updated.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to update the article.')
        return super().form_invalid(form)

#記事削除
class ArticleDeleteView(LoginRequiredMixin ,generic.DeleteView):
    model = Article
    template_name = 'article_delete.html'
    slug_field = 'username' #モデルのフィールド名
    slug_url_kwarg = 'username' #urls.pyでのキーワード名

    def get_success_url(self):
        return reverse_lazy('article:mypage', kwargs={'username': self.object.post_user})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Article has been Deleted")
        return super().delete(request, *args, **kwargs)

#コメント関連
class CommentCreateView(LoginRequiredMixin ,generic.CreateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = 'article_detail.html'

    def form_valid(self, form):
        comment = form.save(commit=False)

        post_pk = self.kwargs['pk']
        post = get_object_or_404(Article, pk=post_pk)

        comment.writer = self.request.user
        comment.target = post 
        comment.save()
        messages.success(self.request, 'You added a comment!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article:article_detail', kwargs={'pk': self.kwargs['pk']})

class CommentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = 'comment_update.html'

    def get_success_url(self):
        article = Article.objects.get(comment__pk=self.kwargs['pk'])
        return reverse_lazy('article:article_detail', kwargs={'pk': article.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Your comment has been successfully updated.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to edit comment.')
        return super().form_invalid(form)

class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = 'article_detail.html'

    def get_success_url(self):
        article = Article.objects.get(comment__pk=self.kwargs['pk'])
        return reverse_lazy('article:article_detail', kwargs={'pk': article.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Comment has been Deleted")
        return super().delete(request, *args, **kwargs)

#コメントのリプライ関係
class ReplyCreateView(LoginRequiredMixin, generic.CreateView):
    model = SubComment
    form_class = CommentReplyForm
    template_name = 'reply_create.html'

    def form_valid(self, form):
        reply = form.save(commit=False)

        comment_pk = self.kwargs['pk'] #返信するコメントのpk
        comment = get_object_or_404(Comment, pk=comment_pk)
                                    
        reply.writer = self.request.user
        reply.target = comment
        reply.save()
        messages.success(self.request, 'You replied to the comment!')
        return redirect('article:article_detail', pk=comment.target.pk)

    def get_context_data(self, **kwargs): #リプライキャンセルした場合のリダイレクト先指定用
        context = super().get_context_data(**kwargs)

        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_pk)
        context['post'] = comment.target #リダイレクト先(article_detail)のArticleモデルのpk指定用
        return context

class ReplyUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = SubComment
    form_class = CommentReplyForm
    template_name = 'reply_update.html'

    def get_success_url(self):
        reply_pk = self.kwargs['pk']
        reply = get_object_or_404(SubComment, pk=reply_pk)
        article = Article.objects.get(comment__pk=reply.target.pk)
        return reverse_lazy('article:article_detail', kwargs={'pk': article.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Your reply has been successfully updated.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to edit your reply.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs): #キャンセルした場合のリダイレクト先指定用
        context = super().get_context_data(**kwargs)

        reply_pk = self.kwargs['pk']
        reply = get_object_or_404(SubComment, pk=reply_pk)
        comment = reply.target
        context['post'] = comment.target #リダイレクト先(article_detail)のArticleモデルのpk指定用
        return context



class ReplyDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = SubComment
    template_name = 'article_detail.html'

    def get_success_url(self):
        reply_pk = self.kwargs['pk']
        reply = get_object_or_404(SubComment, pk=reply_pk)
        article = Article.objects.get(comment__pk=reply.target.pk)
        return reverse_lazy('article:article_detail', kwargs={'pk': article.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Your reply has been Deleted")
        return super().delete(request, *args, **kwargs)

#アカウント設定関係
class AccountSettingView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'account_setting.html'
    model = CustomUser
    form_class = AccountSettingForm
    slug_field = 'username' #モデルのフィールド名
    slug_url_kwarg = 'username' #urls.pyでのキーワード名

    def get_success_url(self):
        return reverse_lazy('article:mypage', kwargs={'username': self.object.username})
    
    def form_valid(self, form):
        messages.success(self.request, 'Successfully changed your account settings')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to change your account settings')
        return super().form_invalid(form)


class MyPasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('article:password_change_done')
    template_name = 'password_change.html'

    def form_valid(self, form):
        messages.success(self.request, 'You successfully changed password !')
        return super().form_valid(form)

class PasswordChengeDone(LoginRequiredMixin, PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'password_change_done.html'