from django.shortcuts import redirect


def user_login(fun_target):
    def fun(request, *args, **kwargs):
        # 校验用户是否登录
        if request.session.has_key('uid'):
            return fun_target(request, *args, **kwargs)
        else:
            return redirect('/user/login/')
    return fun