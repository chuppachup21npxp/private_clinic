from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask import request
from flask_admin.contrib.sqla import ModelView
from qlnhathuoc.models import UserRole, User, Medicine, TypeMedicine, MedicalRecord, DateMedical, Prescription, Receipt, Patient
from qlnhathuoc import app, db, dao
from flask_login import logout_user, current_user
from flask import redirect
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()



class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        stats = dao.count_medicine_by_cate()
        return self.render('admin/stats.html', stats=stats)

class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.stats_revenue(kw=request.args.get('kw'),
                                  from_date=request.args.get('from_date'),
                                  to_date=request.args.get('to_date'))
        total = dao.total_revenue_medicine()
        return self.render('admin/index.html', stats=stats, total=total)


admin = Admin(app=app, name='Quản trị phòng mạch',
              template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))