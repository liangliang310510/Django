from django.shortcuts import redirect


class UserLoginMiddleWare:
    def process_request(self, request):
        # 登录验证
        urls = ['/user/','/user/login_out/'] # 容器内容需要后续不断完善

        if request.path in urls:
            if not request.session.has_key('uid'):
                return redirect('/user/login/')

