from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from blog.forms import CommentForm
from blog.models import Post, Commentary


class ListView(generic.ListView):
    model = Post
    paginate_by = 5
    context_object_name = "post_list"
    template_name = "blog/index.html"

    def get_queryset(self):
        return (Post.objects.select_related("owner")
                .prefetch_related("comments"))


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_queryset(self):
        return (Post.objects.select_related("owner")
                .prefetch_related("comments__user"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["counted"] = post.comments.count()
        # Dodaj formularz do kontekstu dla żądania GET
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        if form.is_valid():
            # Pobierz aktualny post
            post = self.get_object()
            # Utwórz nowy komentarz i przypisz do posta oraz użytkownika
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.user = request.user
                comment.save()
                return HttpResponseRedirect(reverse("blog:post-detail",
                                                    kwargs={"pk": post.pk}))
            else:
                return HttpResponseRedirect(reverse("login"))


class CommentUpdateView(generic.UpdateView):
    model = Commentary
    form_class = CommentForm
    template_name = "blog/update_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "blog:post-detail",
            kwargs={"pk": self.object.post.pk}
        )


class CommentDeleteView(generic.DeleteView):
    model = Commentary
    template_name = "blog/confirm_delete_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "blog:post-detail",
            kwargs={"pk": self.object.post.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.META.get("HTTP_REFERER")
        return context
